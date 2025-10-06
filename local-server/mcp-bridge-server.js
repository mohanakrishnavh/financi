#!/usr/bin/env node

/**
 * MCP Bridge Server for Financi Azure Functions
 * 
 * This server acts as a bridge between VS Code's MCP client and
 * the Azure Functions with experimental MCP triggers.
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');

// Configuration
const FUNCTION_APP_URL = 'https://financi.azurewebsites.net';
const API_KEY = process.env.FINANCI_API_KEY || 'REPLACE_WITH_YOUR_API_KEY';

class FinanciMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'financi-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'hello_financi',
            description: 'Hello world from Financi MCP server.',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'get_stock_price',
            description: 'Get current stock price for a given symbol.',
            inputSchema: {
              type: 'object',
              properties: {
                symbol: {
                  type: 'string',
                  description: 'The stock symbol to get the price for (e.g., AAPL, MSFT).',
                },
              },
              required: ['symbol'],
            },
          },
          {
            name: 'calculate_portfolio_value',
            description: 'Calculate the value of shares for a given stock.',
            inputSchema: {
              type: 'object',
              properties: {
                symbol: {
                  type: 'string',
                  description: 'The stock symbol.',
                },
                amount: {
                  type: 'number',
                  description: 'The number of shares.',
                },
              },
              required: ['symbol', 'amount'],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        let result;
        
        switch (name) {
          case 'hello_financi':
            result = await this.callAzureFunction('hello_financi', {});
            break;
          case 'get_stock_price':
            result = await this.callAzureFunction('get_stock_price', { symbol: args.symbol });
            break;
          case 'calculate_portfolio_value':
            result = await this.callAzureFunction('calculate_portfolio_value', { 
              symbol: args.symbol, 
              amount: args.amount 
            });
            break;
          default:
            throw new Error(`Unknown tool: ${name}`);
        }

        return {
          content: [
            {
              type: 'text',
              text: result,
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async callAzureFunction(functionName, args) {
    // For now, return mock data since the MCP endpoints aren't accessible
    // In a real implementation, you'd call the Azure Function HTTP endpoints
    
    const mockResponses = {
      hello_financi: "Hello! I am the Financi MCP server - your financial data assistant!",
      get_stock_price: JSON.stringify({
        symbol: args.symbol?.toUpperCase() || "UNKNOWN",
        price: 150.25,
        currency: "USD",
        timestamp: new Date().toISOString(),
        change: "+2.5%",
        status: "success (mock data)"
      }, null, 2),
      calculate_portfolio_value: JSON.stringify({
        symbol: args.symbol?.toUpperCase() || "UNKNOWN",
        shares: args.amount || 0,
        price_per_share: 150.25,
        total_value: (args.amount || 0) * 150.25,
        currency: "USD",
        timestamp: new Date().toISOString(),
        status: "success (mock data)"
      }, null, 2)
    };

    return mockResponses[functionName] || "Function not found";
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Financi MCP Bridge Server running...');
  }
}

// Start the server
if (require.main === module) {
  const server = new FinanciMCPServer();
  server.run().catch(console.error);
}

module.exports = { FinanciMCPServer };