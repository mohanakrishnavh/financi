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
    if (!API_KEY) {
      throw new Error('FINANCI_API_KEY environment variable is required');
    }

    try {
      // Import fetch for HTTP requests
      const fetch = (await import('node-fetch')).default;
      
      const url = `${FUNCTION_APP_URL}/api/${functionName}`;
      const headers = {
        'Content-Type': 'application/json',
        'x-functions-key': API_KEY
      };

      let body = {};
      if (functionName !== 'hello_financi') {
        body = { arguments: args };
      }

      console.error(`Calling Azure Function: ${url}`);
      console.error(`Request body:`, JSON.stringify(body, null, 2));

      const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error(`Azure Function call failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.text();
      console.error(`Azure Function response:`, result);
      
      return result;
      
    } catch (error) {
      console.error(`Error calling Azure Function ${functionName}:`, error);
      throw error;
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