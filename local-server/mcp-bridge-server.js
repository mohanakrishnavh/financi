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
          {
            name: 'eight_pillar_stock_analysis',
            description: 'Perform comprehensive Eight Pillar Stock Analysis to evaluate investment quality based on PE ratio, ROIC, shares outstanding, cash flow, net income, revenue growth, liabilities, and price-to-free-cash-flow.',
            inputSchema: {
              type: 'object',
              properties: {
                symbol: {
                  type: 'string',
                  description: 'The stock symbol to analyze (e.g., AAPL, MSFT).',
                },
              },
              required: ['symbol'],
            },
          },
          {
            name: 'compound_interest_calculator',
            description: 'Calculate compound interest for an investment with customizable compounding frequency.',
            inputSchema: {
              type: 'object',
              properties: {
                principal: {
                  type: 'number',
                  description: 'Initial investment amount in dollars.',
                },
                rate: {
                  type: 'number',
                  description: 'Annual interest rate as a percentage (e.g., 5 for 5%).',
                },
                time: {
                  type: 'number',
                  description: 'Investment period in years.',
                },
                frequency: {
                  type: 'string',
                  description: 'Compounding frequency: annually, semi-annually, quarterly, monthly, or daily.',
                  enum: ['annually', 'semi-annually', 'quarterly', 'monthly', 'daily'],
                },
              },
              required: ['principal', 'rate', 'time', 'frequency'],
            },
          },
          {
            name: 'retirement_calculator',
            description: 'Calculate retirement savings projection based on current age, retirement age, savings, contributions, and expected returns.',
            inputSchema: {
              type: 'object',
              properties: {
                current_age: {
                  type: 'number',
                  description: 'Your current age in years.',
                },
                retirement_age: {
                  type: 'number',
                  description: 'Your planned retirement age in years.',
                },
                current_savings: {
                  type: 'number',
                  description: 'Current retirement savings amount in dollars.',
                },
                monthly_contribution: {
                  type: 'number',
                  description: 'Monthly contribution amount in dollars.',
                },
                annual_return: {
                  type: 'number',
                  description: 'Expected annual return rate as a percentage (e.g., 7 for 7%).',
                },
              },
              required: ['current_age', 'retirement_age', 'current_savings', 'monthly_contribution', 'annual_return'],
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
          case 'eight_pillar_stock_analysis':
            result = await this.callAzureFunction('eight_pillar_stock_analysis', { 
              symbol: args.symbol 
            });
            break;
          case 'compound_interest_calculator':
            result = await this.callAzureFunction('compound_interest_calculator', { 
              principal: args.principal,
              rate: args.rate,
              time: args.time,
              frequency: args.frequency
            });
            break;
          case 'retirement_calculator':
            result = await this.callAzureFunction('retirement_calculator', { 
              current_age: args.current_age,
              retirement_age: args.retirement_age,
              current_savings: args.current_savings,
              monthly_contribution: args.monthly_contribution,
              annual_return: args.annual_return
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
        
      case 'eight_pillar_stock_analysis':
        const analysisSymbol = args.symbol || 'UNKNOWN';
        return JSON.stringify({
          symbol: analysisSymbol.toUpperCase(),
          company_name: `${analysisSymbol.toUpperCase()} Corporation`,
          analysis_date: timestamp,
          pillars: {
            pe_ratio: { value: (Math.random() * 30 + 10).toFixed(2), status: "Fair", weight: 12.5 },
            roic: { value: (Math.random() * 20 + 5).toFixed(2) + "%", status: "Good", weight: 12.5 },
            shares_outstanding: { trend: "Stable", status: "Good", weight: 12.5 },
            cash_flow: { value: "$" + (Math.random() * 100 + 50).toFixed(2) + "B", status: "Strong", weight: 12.5 },
            net_income: { value: "$" + (Math.random() * 50 + 20).toFixed(2) + "B", status: "Positive", weight: 12.5 },
            revenue_growth: { value: (Math.random() * 15 + 5).toFixed(2) + "%", status: "Growing", weight: 12.5 },
            liabilities: { ratio: (Math.random() * 0.6 + 0.2).toFixed(2), status: "Manageable", weight: 12.5 },
            price_to_fcf: { value: (Math.random() * 25 + 10).toFixed(2), status: "Fair", weight: 12.5 }
          },
          overall_score: (Math.random() * 30 + 60).toFixed(1) + "/100",
          recommendation: "Hold - Balanced fundamentals",
          status: "success",
          note: "Mock data - Azure MCP integration in progress"
        }, null, 2);
        
      case 'compound_interest_calculator':
        const { principal, rate, time, frequency } = args;
        const frequencies = { annually: 1, 'semi-annually': 2, quarterly: 4, monthly: 12, daily: 365 };
        const n = frequencies[frequency] || 12;
        const r = rate / 100;
        const finalAmount = principal * Math.pow(1 + r / n, n * time);
        const interest = finalAmount - principal;
        
        return JSON.stringify({
          calculation: {
            principal: principal,
            annual_rate: rate + "%",
            time_period: time + " years",
            compounding_frequency: frequency,
            compounds_per_year: n
          },
          results: {
            final_amount: "$" + finalAmount.toFixed(2),
            total_interest: "$" + interest.toFixed(2),
            effective_rate: ((Math.pow(1 + r / n, n) - 1) * 100).toFixed(3) + "%"
          },
          breakdown: `After ${time} years, your $${principal} will grow to $${finalAmount.toFixed(2)}`,
          status: "success",
          note: "Mock data - Azure MCP integration in progress"
        }, null, 2);
        
      case 'retirement_calculator':
        const { current_age, retirement_age, current_savings, monthly_contribution, annual_return } = args;
        const yearsToRetirement = retirement_age - current_age;
        const monthlyRate = (annual_return / 100) / 12;
        const totalMonths = yearsToRetirement * 12;
        
        // Future value calculation
        const futureValueCurrentSavings = current_savings * Math.pow(1 + annual_return / 100, yearsToRetirement);
        const futureValueContributions = monthly_contribution * ((Math.pow(1 + monthlyRate, totalMonths) - 1) / monthlyRate);
        const totalAtRetirement = futureValueCurrentSavings + futureValueContributions;
        
        return JSON.stringify({
          inputs: {
            current_age: current_age,
            retirement_age: retirement_age,
            years_to_retirement: yearsToRetirement,
            current_savings: "$" + current_savings.toLocaleString(),
            monthly_contribution: "$" + monthly_contribution.toLocaleString(),
            annual_return_rate: annual_return + "%"
          },
          projections: {
            total_at_retirement: "$" + totalAtRetirement.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","),
            growth_from_current_savings: "$" + futureValueCurrentSavings.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","),
            growth_from_contributions: "$" + futureValueContributions.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","),
            total_contributions: "$" + (monthly_contribution * totalMonths).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
          },
          summary: `By age ${retirement_age}, your retirement savings could grow to $${totalAtRetirement.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`,
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