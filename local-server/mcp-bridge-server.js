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
const FUNCTION_APP_URL = process.env.FINANCI_SERVER_URL || 'https://financi.azurewebsites.net';
const API_KEY = process.env.FINANCI_API_KEY;

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
    try {
      // For now, we'll try to use the real Azure Functions but fallback to mock data
      // if the experimental MCP triggers aren't accessible via HTTP
      
      if (API_KEY) {
        try {
          const fetch = (await import('node-fetch')).default;
          
          // Try the MCP runtime endpoint first
          const mcpUrl = `${FUNCTION_APP_URL}/runtime/webhooks/mcp/invoke/${functionName}`;
          console.error(`Attempting MCP call: ${mcpUrl}`);
          
          const mcpResponse = await fetch(mcpUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'x-functions-key': API_KEY
            },
            body: JSON.stringify({ arguments: args })
          });

          if (mcpResponse.ok) {
            const result = await mcpResponse.text();
            console.error(`Azure MCP Function response:`, result);
            return result;
          }
        } catch (error) {
          console.error(`Azure MCP call failed, using mock data: ${error.message}`);
        }
      }

      // Fallback to mock data while Azure MCP integration is being worked out
      console.error(`Using mock data for ${functionName}`);
      return this.getMockData(functionName, args);
      
    } catch (error) {
      console.error(`Error in callAzureFunction ${functionName}:`, error);
      throw error;
    }
  }

  getMockData(functionName, args) {
    const timestamp = new Date().toISOString();
    
    switch (functionName) {
      case 'hello_financi':
        return "Hello! I am the Financi MCP server - your financial data assistant!";
        
      case 'get_stock_price':
        const symbol = args.symbol || 'UNKNOWN';
        // Mock stock price data
        const mockPrice = Math.round((Math.random() * 200 + 50) * 100) / 100;
        const mockChange = Math.round((Math.random() * 10 - 5) * 100) / 100;
        const changePercent = (mockChange / mockPrice * 100).toFixed(2);
        
        return JSON.stringify({
          symbol: symbol.toUpperCase(),
          price: mockPrice,
          currency: "USD",
          timestamp: timestamp,
          change: `${changePercent > 0 ? '+' : ''}${changePercent}%`,
          previous_close: Math.round((mockPrice - mockChange) * 100) / 100,
          company_name: `${symbol.toUpperCase()} Corporation`,
          status: "success",
          note: "Mock data - Azure MCP integration in progress"
        }, null, 2);
        
      case 'calculate_portfolio_value':
        const portfolioSymbol = args.symbol || 'UNKNOWN';
        const amount = args.amount || 1;
        const pricePerShare = Math.round((Math.random() * 200 + 50) * 100) / 100;
        const totalValue = Math.round(pricePerShare * amount * 100) / 100;
        const mockChangePercent = (Math.random() * 10 - 5).toFixed(2);
        
        return JSON.stringify({
          symbol: portfolioSymbol.toUpperCase(),
          shares: amount,
          price_per_share: pricePerShare,
          total_value: totalValue,
          currency: "USD",
          timestamp: timestamp,
          company_name: `${portfolioSymbol.toUpperCase()} Corporation`,
          current_change: `${mockChangePercent > 0 ? '+' : ''}${mockChangePercent}%`,
          status: "success",
          note: "Mock data - Azure MCP integration in progress"
        }, null, 2);
        
      default:
        throw new Error(`Unknown function: ${functionName}`);
    }
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