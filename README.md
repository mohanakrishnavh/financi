# Financi - Financial Analysis MCP Server# Financi - Financial Analysis MCP Server



[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)[![Build Status](https://dev.azure.com/your-org/financi/_apis/build/status/financi-ci?branchName=main)](https://dev.azure.com/your-org/financi/_build/latest?definitionId=1&branchName=main)

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![Azure Functions](https://img.shields.io/badge/Azure%20Functions-v4-blue.svg)](https://docs.microsoft.com/en-us/azure/azure-functions/)[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

[![Azure Functions](https://img.shields.io/badge/Azure%20Functions-v4-blue.svg)](https://docs.microsoft.com/en-us/azure/azure-functions/)

Financi is a Python-based financial analysis server providing stock analysis tools through both **Model Context Protocol (MCP)** and **RESTful HTTP APIs**. Deployed as an Azure Function App with real-time Yahoo Finance data integration.

Financi is a Python-based Model Context Protocol (MCP) server deployed as an Azure Function App, providing financial analysis tools for stocks through a standardized MCP interface. Built using Microsoft's Azure Functions MCP integration with `@app.generic_trigger` decorators.

---

## 🚀 Quick Start

## 🚀 Quick Start

**Already Deployed?** Access your Financi MCP server at:

### Already Deployed?- **Health Check**: `https://financi.azurewebsites.net/api/health`

- **MCP Endpoint**: `https://financi.azurewebsites.net/runtime/webhooks/mcp/sse`

**Health Check:** `https://financi.azurewebsites.net/health`

**New Installation?** 

**HTTP API Endpoints:**1. Fork this repository to your Azure DevOps organization

- Stock Price: `https://financi.azurewebsites.net/api/stock/price?symbol=AAPL&code=YOUR_KEY`2. Configure the Azure DevOps pipeline with your subscription details  

- Portfolio Value: `https://financi.azurewebsites.net/api/stock/portfolio?symbol=MSFT&amount=50&code=YOUR_KEY`3. Run the pipeline to automatically deploy infrastructure and code

- Eight Pillar Analysis: `https://financi.azurewebsites.net/api/stock/eight-pillar?symbol=TSLA&code=YOUR_KEY`4. Access your deployed functions at `https://financi.azurewebsites.net`

- Compound Interest: `https://financi.azurewebsites.net/api/calculator/compound-interest?principal=10000&rate=7&time=20&frequency=monthly&code=YOUR_KEY`

- Retirement Calculator: `https://financi.azurewebsites.net/api/calculator/retirement?current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7&code=YOUR_KEY`## 🚀 Features



**Get Your API Key:**### Stock Analysis Tools

```bash- **Real-time Stock Prices**: Get current stock quotes with price, volume, and change data

./scripts/get-function-keys.sh- **Historical Data**: Access historical price data for technical analysis

```- **Technical Indicators**: Calculate RSI, MACD, SMA, EMA, and other technical indicators

- **Financial Ratios**: Retrieve key financial metrics for fundamental analysis

---

### Cryptocurrency Analysis

## ✨ Features- **Crypto Prices**: Real-time cryptocurrency prices and market data

- **Market Metrics**: 24h volume, market cap, and price changes

### 📊 Stock Analysis Tools- **Multi-currency Support**: Price data in various fiat currencies



#### 1. Real-Time Stock Price### Portfolio Management

Get current stock price, change percentage, volume, and company information.- **Portfolio Analysis**: Analyze mixed portfolios of stocks and cryptocurrencies

```bash- **Asset Allocation**: Calculate portfolio diversification and allocation percentages

curl "https://financi.azurewebsites.net/api/stock/price?code=KEY&symbol=AAPL"- **Performance Tracking**: Monitor portfolio value and individual asset performance

```

## 🏗️ Architecture

#### 2. Portfolio Value Calculator

Calculate total portfolio value based on shares owned.```mermaid

```bashgraph TB

curl "https://financi.azurewebsites.net/api/stock/portfolio?code=KEY&symbol=MSFT&amount=50"    A[MCP Client] --> B[Azure Function App]

```    B --> C[Financi MCP Server]

    C --> D[Alpha Vantage API]

#### 3. Eight Pillar Stock Analysis    C --> E[CoinGecko API]

Comprehensive fundamental analysis based on 8 key financial pillars:    B --> F[Azure Key Vault]

- PE Ratio - Price-to-earnings valuation    B --> G[Application Insights]

- ROIC - Return on invested capital      B --> H[Azure Storage]

- Shares Outstanding - Share dilution trends```

- Cash Flow - Operating cash generation

- Net Income - Profitability trends## 📋 Prerequisites

- Revenue Growth - Top-line expansion

- Liabilities - Debt management- **Azure Subscription**: Valid Azure subscription with appropriate permissions

- Price-to-FCF - Free cash flow valuation- **Azure CLI**: Latest version installed and configured

- **Python 3.11+**: For local development and testing

```bash- **Azure DevOps**: For CI/CD pipeline (optional)

curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=KEY&symbol=AAPL"- **API Keys**: 

```  - Alpha Vantage API key for stock data

  - Additional financial APIs (optional)

### 🧮 Financial Calculators

## 🛠️ Installation & Deployment

#### 4. Compound Interest Calculator

Calculate investment growth with customizable compounding frequency.### Repository Structure

- Supports: annually, semi-annually, quarterly, monthly, daily

- Shows final amount, total interest, and effective rate```

financi/

```bash├── src/                    # Azure Function source code

curl "https://financi.azurewebsites.net/api/calculator/compound-interest?code=KEY&principal=10000&rate=7&time=20&frequency=monthly"├── infrastructure/         # Bicep templates for Azure deployment

```├── tests/                  # Unit and integration tests

├── docs/                   # Documentation files

#### 5. Retirement Savings Calculator├── scripts/                # Utility scripts

Project retirement savings with detailed year-by-year breakdown.├── local-server/           # Local MCP server for development

- Accounts for current savings and monthly contributions├── .funcignore            # Files to exclude from deployment

- Shows growth from savings vs. contributions└── README.md              # This file

- Calculates total at retirement```



```bash### Option 1: Automated Deployment via Azure DevOps

curl "https://financi.azurewebsites.net/api/calculator/retirement?code=KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"

```1. **Fork this repository** to your Azure DevOps organization



---2. **Configure Service Connection**:

   ```bash

## 🏗️ Architecture   # In Azure DevOps, create a service connection to your Azure subscription

   # Name it 'financi-service-connection' to match the pipeline configuration

### Dual-Interface Design   ```



```3. **Set Pipeline Variables**:

┌─────────────────────────────────────────────────────────┐   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID

│                  Azure Function App                     │   - `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key (mark as secret)

│                                                         │

│  ┌─────────────────────┐    ┌──────────────────────┐  │4. **Run the Pipeline**:

│  │ MCP Triggers        │    │ HTTP Endpoints       │  │   - The pipeline will automatically deploy infrastructure and function code

│  │ (Experimental)      │    │ (Production Ready)   │  │   - Monitor the deployment in Azure DevOps

│  │ @mcpToolTrigger     │    │ @route("/api/...")   │  │

│  └─────────┬───────────┘    └──────────┬───────────┘  │### Option 2: Manual Deployment

│            │                            │              │

│            └────────────┬───────────────┘              │#### Step 1: Deploy Infrastructure

│                         │                              │

│              ┌──────────▼──────────┐                   │```bash

│              │   Handler Functions │                   │# Clone the repository

│              │  (Business Logic)   │                   │git clone https://github.com/your-username/financi.git

│              └──────────┬──────────┘                   │cd financi

│                         │                              │

│              ┌──────────▼──────────┐                   │# Create resource group

│              │  Yahoo Finance API  │                   │az group create --name rg-financi --location "East US 2"

│              └─────────────────────┘                   │

└─────────────────────────────────────────────────────────┘# Deploy Bicep template

az deployment group create \

External Access:  --resource-group rg-financi \

- HTTP/REST → Any HTTP client (curl, Python, JavaScript, etc.)  --template-file infrastructure/main.bicep \

- MCP → Claude Desktop via local bridge server  --parameters infrastructure/parameters.json

``````



**Data Source:** Yahoo Finance (via `yfinance` Python library)#### Step 2: Deploy Function Code



---```bash

# Install dependencies (from project root)

## 📦 Installation & Setuppip install -r src/requirements.txt



### Prerequisites# Create deployment package

- Python 3.11+cd src

- Azure account with Function Appzip -r ../function-app.zip .

- Azure CLI installed

- Git# Deploy to Azure Functions

az functionapp deployment source config-zip \

### Local Development  --resource-group rg-financi \

  --name your-function-app-name \

```bash  --src ../function-app.zip

# Clone repository```

git clone https://github.com/mohanakrishnavh/financi.git

cd financi#### Step 3: Configure API Keys



# Install dependencies```bash

pip install -r src/requirements.txt# Store API key in Key Vault (recommended)

az keyvault secret set \

# Get function keys  --vault-name your-keyvault-name \

./scripts/get-function-keys.sh  --name "ALPHA-VANTAGE-API-KEY" \

  --value "your-api-key"

# Test endpoints

source .env.local# Or set as Function App setting (less secure)

./scripts/test-http-endpoints.shaz functionapp config appsettings set \

```  --name your-function-app-name \

  --resource-group rg-financi \

### Deployment  --settings "ALPHA_VANTAGE_API_KEY=your-api-key"

```

#### Via Azure DevOps (Automated CI/CD)

```bash## 📖 Usage

# Push to Azure DevOps

./scripts/push-both.sh### Accessing the Deployed MCP Server



# Pipeline auto-deploys on push to main branchAfter successful deployment via the Azure DevOps pipeline, your Financi MCP server will be available at:

# Monitor at: https://dev.azure.com/mohanakrishnavh/financi/_build

```**Function App URL**: `https://financi.azurewebsites.net`



#### Manual Deployment#### Health Check

```bashFirst, verify your deployment is working:

# Deploy using Azure Functions Core Tools```bash

func azure functionapp publish financi --pythoncurl https://financi.azurewebsites.net/api/health

```

# Or use Azure CLI

az functionapp deployment source sync \Expected response:

  --name financi \```json

  --resource-group rg-financi{

```  "status": "healthy",

  "timestamp": "2024-01-01T12:00:00.000Z",

---  "service": "financi-mcp",

  "version": "1.0.0",

## 🔌 API Documentation  "mcp_endpoint": "/runtime/webhooks/mcp/sse"

}

### Authentication```



All endpoints require a function key passed as `code` query parameter:### Using with MCP Clients

```bash

curl "https://financi.azurewebsites.net/api/stock/price?code=YOUR_KEY&symbol=AAPL"#### Option 1: Claude Desktop Configuration

```

Add to your Claude Desktop configuration file (`~/.config/claude-desktop/claude_desktop_config.json`):

Get your key with: `./scripts/get-function-keys.sh`

```json

### Endpoints{

  "mcpServers": {

#### 1. GET `/api/stock/price`    "financi": {

      "command": "node",

**Parameters:**      "args": [

- `symbol` (required): Stock ticker (e.g., AAPL, MSFT, TSLA)        "local-server/mcp-bridge-server.js"

      ],

**Response:**      "env": {

```json        "FINANCI_SERVER_URL": "https://financi.azurewebsites.net",

{        "FINANCI_API_KEY": "your-function-key-here"

  "symbol": "AAPL",      }

  "price": 150.25,    }

  "currency": "USD",  }

  "change": "+2.5%",}

  "volume": 50000000,```

  "company_name": "Apple Inc.",

  "timestamp": "2025-11-10T10:30:00Z",Or copy the provided `claude-desktop-config.json` and update the API key.

  "status": "success"

}#### Option 2: Direct Azure Functions MCP Integration

```

Since this is deployed as Azure Functions with MCP tool triggers, you can interact with it through Azure's built-in MCP runtime:

#### 2. GET `/api/stock/portfolio`

**MCP Endpoint**: `https://financi.azurewebsites.net/runtime/webhooks/mcp/sse`

**Parameters:**

- `symbol` (required): Stock ticker#### Option 3: HTTP API Direct Access

- `amount` (required): Number of shares

You can also call the individual functions directly via HTTP:

**Response:**

```json**Stock Price Example**:

{```bash

  "symbol": "MSFT",# Get current stock price for Apple

  "shares": 50,curl -X POST "https://financi.azurewebsites.net/api/orchestrators/get_stock_price" \

  "price_per_share": 380.50,  -H "Content-Type: application/json" \

  "total_value": 19025.00,  -d '{"symbol": "AAPL"}'

  "currency": "USD",```

  "status": "success"

}**Portfolio Analysis Example**:

``````bash

# Analyze a mixed portfolio

#### 3. GET `/api/stock/eight-pillar`curl -X POST "https://financi.azurewebsites.net/api/orchestrators/calculate_portfolio_value" \

  -H "Content-Type: application/json" \

**Parameters:**  -d '{"symbol": "MSFT", "amount": 10}'

- `symbol` (required): Stock ticker to analyze```



**Response:**### Available MCP Tools

```json

{The Financi MCP server provides the following tools through Azure Functions MCP integration:

  "symbol": "AAPL",

  "company_name": "Apple Inc.",### Available MCP Tools

  "analysis_date": "2025-11-10T10:30:00Z",

  "pillars": {The server provides three main financial analysis tools deployed as Azure Functions:

    "pe_ratio": { "value": 28.5, "status": "Fair", "weight": 12.5 },

    "roic": { "value": "25.3%", "status": "Excellent", "weight": 12.5 }#### 1. Hello Financi (`hello_financi`)

  },Simple greeting tool to verify MCP connectivity.

  "overall_score": "85/100",

  "recommendation": "Strong Buy",**MCP Tool Call:**

  "status": "success"```json

}{

```  "tool": "hello_financi",

  "arguments": {}

#### 4. GET `/api/calculator/compound-interest`}

```

**Parameters:**

- `principal` (required): Initial investment**Response:**

- `rate` (required): Annual interest rate (%)```

- `time` (required): Investment period (years)"Hello! I am the Financi MCP server - your financial data assistant!"

- `frequency` (required): annually | semi-annually | quarterly | monthly | daily```



**Response:**#### 2. Get Stock Price (`get_stock_price`)

```jsonRetrieves current stock price and market data for a given symbol.

{

  "principal": 10000,**MCP Tool Call:**

  "rate": 7,```json

  "time": 20,{

  "frequency": "monthly",  "tool": "get_stock_price", 

  "final_amount": 40387.27,  "arguments": {

  "total_interest": 30387.27,    "symbol": "AAPL"

  "effective_rate": "7.229%",  }

  "status": "success"}

}```

```

**Response:**

#### 5. GET `/api/calculator/retirement````json

{

**Parameters:**  "symbol": "AAPL",

- `current_age` (required): Your current age  "price": 150.25,

- `retirement_age` (required): Planned retirement age  "currency": "USD",

- `current_savings` (required): Current retirement savings  "timestamp": "2024-01-01T12:00:00.000Z",

- `monthly_contribution` (required): Monthly contribution  "change": "+2.5%",

- `annual_return` (required): Expected annual return (%)  "status": "success"

}

**Response:**```

```json

{#### 3. Calculate Portfolio Value (`calculate_portfolio_value`)

  "current_age": 30,Calculates the total value of shares for a given stock position.

  "retirement_age": 65,

  "years_to_retirement": 35,**MCP Tool Call:**

  "total_at_retirement": 1234567.89,```json

  "status": "success"{

}  "tool": "calculate_portfolio_value",

```  "arguments": {

    "symbol": "MSFT",

---    "amount": 10

  }

## 🔧 Usage Examples}

```

### Using with Python

**Response:**

```python```json

import requests{

import os  "symbol": "MSFT",

  "shares": 10,

API_KEY = os.getenv("DEFAULT_HOST_KEY")  "price_per_share": 150.25,

BASE_URL = "https://financi.azurewebsites.net"  "total_value": 1502.50,

  "currency": "USD",

# Get stock price  "timestamp": "2024-01-01T12:00:00.000Z",

response = requests.get(  "status": "success"

    f"{BASE_URL}/api/stock/price",}

    params={"code": API_KEY, "symbol": "AAPL"}```

)

print(response.json())### Direct HTTP Access



# Eight pillar analysisYou can also call these functions directly via HTTP without MCP:

response = requests.get(

    f"{BASE_URL}/api/stock/eight-pillar",#### Hello Financi

    params={"code": API_KEY, "symbol": "MSFT"}```bash

)curl -X POST "https://financi.azurewebsites.net/api/hello_financi" \

analysis = response.json()  -H "Content-Type: application/json" \

print(f"Overall Score: {analysis['overall_score']}")  -d '{}'

print(f"Recommendation: {analysis['recommendation']}")```

```

#### Get Stock Price  

### Using with JavaScript/Node.js```bash

curl -X POST "https://financi.azurewebsites.net/api/get_stock_price" \

```javascript  -H "Content-Type: application/json" \

const fetch = require('node-fetch');  -d '{"arguments": {"symbol": "AAPL"}}'

```

const API_KEY = process.env.DEFAULT_HOST_KEY;

const BASE_URL = 'https://financi.azurewebsites.net';#### Calculate Portfolio Value

```bash

async function getStockPrice(symbol) {curl -X POST "https://financi.azurewebsites.net/api/calculate_portfolio_value" \

  const url = `${BASE_URL}/api/stock/price?code=${API_KEY}&symbol=${symbol}`;  -H "Content-Type: application/json" \

  const response = await fetch(url);  -d '{"arguments": {"symbol": "MSFT", "amount": 10}}'

  return await response.json();```

}

### Authentication

async function analyzeStock(symbol) {

  const url = `${BASE_URL}/api/stock/eight-pillar?code=${API_KEY}&symbol=${symbol}`;Currently, the MCP tool functions require function-level authentication. The health endpoint is publicly accessible for monitoring purposes.

  const response = await fetch(url);

  return await response.json();**Note**: The current implementation uses placeholder data for demonstration. To enable real financial data, configure the `ALPHA_VANTAGE_API_KEY` environment variable in the Azure Function App settings.

}

### Testing Your Deployment

// Usage

getStockPrice('AAPL').then(console.log);#### Verify Function App Health

analyzeStock('MSFT').then(console.log);```bash

```# Test health endpoint (no authentication required)

curl https://financi.azurewebsites.net/api/health

### Using with curl```



```bash#### Test MCP Tools

# Load API key```bash

source .env.local# Test the hello function

curl -X POST "https://financi.azurewebsites.net/api/hello_financi" \

# Get stock price  -H "Content-Type: application/json" \

curl "https://financi.azurewebsites.net/api/stock/price?code=$DEFAULT_HOST_KEY&symbol=AAPL"  -d '{}'



# Analyze stock# Test stock price with authentication

curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=$DEFAULT_HOST_KEY&symbol=TSLA"curl -X POST "https://financi.azurewebsites.net/api/get_stock_price" \

  -H "Content-Type: application/json" \

# Calculate retirement  -H "x-functions-key: YOUR_FUNCTION_KEY" \

curl "https://financi.azurewebsites.net/api/calculator/retirement?code=$DEFAULT_HOST_KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"  -d '{"arguments": {"symbol": "AAPL"}}'

``````



---**Getting Function Keys**: 

- Go to Azure Portal → Function App → App Keys

## 🧪 Testing- Use the default host key for testing

- For production, create specific function keys

### Automated Testing

### Troubleshooting Access Issues

```bash

# Test all HTTP endpoints#### 401 Unauthorized Errors

./scripts/test-http-endpoints.sh```bash

# The MCP tool functions require authentication

# Run unit tests# Get function keys from Azure Portal:

pytest tests/# Functions → App Keys → Show values → Copy default key



# Test specific modules# Use the key in requests:

python tests/test_stock_handlers.pycurl -H "x-functions-key: YOUR_KEY_HERE" \

python tests/test_financial_calculators.py  "https://financi.azurewebsites.net/api/get_stock_price"

``````



---#### Function Not Found (404)

```bash

## 🤖 Model Context Protocol (MCP) Integration# Verify function names match exactly:

# ✅ Correct: /api/hello_financi

### Using with Claude Desktop# ❌ Wrong:   /api/hello-financi



Financi provides a local MCP bridge server for Claude Desktop integration:# Check deployment status:

az functionapp show --name financi --resource-group rg-financi --query state

**Configuration:**```

```json

{#### Cold Start Delays

  "mcpServers": {- First request may take 10-30 seconds (cold start)

    "financi": {- Subsequent requests should be fast

      "command": "bash",- Consider Premium plan for production to eliminate cold starts

      "args": [

        "-c",## 🧪 Testing

        "source .env.local && FINANCI_API_KEY=\"$DEFAULT_HOST_KEY\" node local-server/mcp-bridge-server.js"

      ],### Test Organization

      "env": {

        "FINANCI_SERVER_URL": "https://financi.azurewebsites.net"The test suite is organized by handler modules, mirroring the code structure:

      }

    }```

  }tests/

}├── test_new_functions.py          # Master test runner (interactive)

```├── test_stock_handlers.py         # Stock-related function tests

├── test_financial_calculators.py  # Financial calculator tests

Copy to: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)├── test_integration.py            # Integration & real-world scenarios

├── test_mcp_server.py            # Original MCP server tests

**Restart Claude Desktop** after configuration.└── __init__.py

```

**Usage in Claude:**

```**Quick Start:**

Analyze Apple stock using eight pillar analysis```bash

Calculate the value of 50 shares of Microsoft# Interactive test runner (recommended)

How much will $10,000 grow in 20 years at 7% with monthly compounding?python tests/test_new_functions.py

```

# Run specific test modules

See `docs/LOCAL_MCP_TOOLS.md` for detailed MCP setup.python tests/test_stock_handlers.py

python tests/test_financial_calculators.py

---python tests/test_integration.py

```

## 📁 Project Structure

See [docs/TEST_ORGANIZATION.md](docs/TEST_ORGANIZATION.md) for detailed test documentation.

```

financi/### Local Development

├── src/

│   ├── function_app.py           # Main Azure Functions entry point```bash

│   ├── http_wrappers.py           # HTTP endpoint wrappers# Install Azure Function dependencies

│   ├── requirements.txt           # Python dependenciespip install -r src/requirements.txt

│   ├── handlers/

│   │   ├── stock_handlers.py      # Stock analysis handlers# Install local server dependencies (for MCP bridge)

│   │   └── financial_calculators.py  # Calculator handlerscd local-server

│   └── models/npm install

│       └── tool_properties.py     # MCP tool definitionscd ..

├── tests/

│   ├── test_stock_handlers.py     # Stock handler tests# Run all tests interactively

│   ├── test_financial_calculators.py  # Calculator testspython tests/test_new_functions.py

│   └── test_integration.py        # Integration tests

├── local-server/# Run specific test module

│   ├── mcp-bridge-server.js       # Local MCP bridgepython tests/test_stock_handlers.py

│   └── package.json               # Node dependencies

├── scripts/# Run legacy pytest tests

│   ├── get-function-keys.sh       # Get Azure function keyspytest tests/ -v --cov=src

│   ├── test-http-endpoints.sh     # Test HTTP endpoints

│   ├── push-both.sh               # Push to GitHub & Azure DevOps# Run with coverage report

│   └── setup-azure-devops-auth.sh # Azure DevOps PAT setuppytest tests/ --cov=src --cov-report=html

├── infrastructure/

│   ├── main.bicep                 # Azure infrastructure# Run local MCP server for testing

│   └── parameters.json            # Deployment parameterscd local-server

└── docs/node mcp-bridge-server.js

    ├── HTTP_WRAPPERS_GUIDE.md     # HTTP API documentation```

    ├── DEPLOYMENT_HTTP_WRAPPERS.md  # Deployment guide

    ├── LOCAL_MCP_TOOLS.md         # MCP setup guide### Integration Testing

    └── MCP_REALITY_CHECK.md       # MCP architecture notes

```#### Using Provided Test Scripts



---```bash

# Get function keys from Azure (creates .env.local)

## 📚 Documentation./scripts/get-function-keys.sh



- **[HTTP API Guide](docs/HTTP_WRAPPERS_GUIDE.md)** - Complete HTTP API reference# Test MCP server functionality

- **[Deployment Guide](docs/DEPLOYMENT_HTTP_WRAPPERS.md)** - Step-by-step deployment./scripts/verify-mcp-server.sh

- **[MCP Setup](docs/LOCAL_MCP_TOOLS.md)** - Claude Desktop integration

- **[MCP Architecture](docs/MCP_REALITY_CHECK.md)** - Technical background# Test function endpoints

- **[Git Multi-Repo](docs/GIT_MULTI_REPO_GUIDE.md)** - GitHub + Azure DevOps setup./scripts/test-functions.sh



---# Run Python MCP client tests

cd local-server

## 🛠️ Developmentpython test-mcp-client.py

```

### Adding New Tools

#### Manual Testing

1. **Create handler** in `src/handlers/`

2. **Add HTTP wrapper** in `src/http_wrappers.py````bash

3. **Add MCP trigger** in `src/function_app.py`# Test health endpoint

4. **Create tests** in `tests/`curl https://your-function-app.azurewebsites.net/api/health

5. **Update documentation**

# Test MCP endpoint with sample request

---curl -X POST https://your-function-app.azurewebsites.net/api/mcp \

  -H "Content-Type: application/json" \

## 🐛 Troubleshooting  -d '{

    "method": "tools/list"

### Common Issues  }'

```

**401/403 Errors**

- Verify API key: `source .env.local && echo $DEFAULT_HOST_KEY`## 🔧 Configuration

- Regenerate key: `./scripts/get-function-keys.sh`

### Environment Variables

**404 Errors**

- Check deployment status| Variable | Description | Required | Default |

- Verify endpoint URL|----------|-------------|----------|---------|

- Check health endpoint first| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key for stock data | Yes | - |

| `MCP_SERVER_NAME` | Server identification name | No | `financi` |

**Timeout Errors**| `MCP_SERVER_VERSION` | Server version | No | `1.0.0` |

- Cold start takes 10-30 seconds| `LOGGING_LEVEL` | Python logging level | No | `INFO` |

- Retry the request

### API Rate Limits

---

- **Alpha Vantage Free**: 5 requests per minute, 500 per day

## 📄 License- **CoinGecko**: 10-50 requests per minute (depending on plan)



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.Consider upgrading to premium plans for production usage.



---## 🔐 Security



## 🙏 Acknowledgments### API Key Management

- Store sensitive API keys in Azure Key Vault

- **Yahoo Finance** - Real-time financial data- Use Azure Function App's managed identity for Key Vault access

- **Azure Functions** - Serverless hosting platform- Rotate API keys regularly

- **Model Context Protocol** - AI assistant integration

- **yfinance** - Python Yahoo Finance API wrapper### Network Security

- Enable HTTPS-only for Function App

---- Configure CORS settings appropriately

- Consider using Azure API Management for additional security layers

**Built with ❤️ using Python, Azure Functions, and Yahoo Finance**

### Monitoring
- Application Insights enabled by default
- Monitor API usage and costs
- Set up alerts for errors and rate limit exceeded

## 📊 Monitoring & Observability

### Azure Application Insights

The Function App is configured with Application Insights for comprehensive monitoring:

- **Performance Metrics**: Response times, throughput, and availability
- **Error Tracking**: Automatic exception capture and logging
- **Custom Metrics**: API usage patterns and financial data requests
- **Live Metrics**: Real-time performance monitoring

### Log Analytics

Query logs using Kusto Query Language (KQL):

```kusto
// Failed requests in last 24 hours
requests
| where timestamp > ago(24h)
| where success == false
| summarize count() by resultCode, name

// Top requested financial symbols
traces
| where message contains "get_stock_price"
| extend symbol = extract(@"symbol: ([A-Z]+)", 1, message)
| where isnotempty(symbol)
| summarize count() by symbol
| top 10 by count_
```

### Alerting

Set up alerts for:
- Function App errors > 5% over 5 minutes
- Response time > 30 seconds
- API rate limit exceeded
- High cost consumption

## 🚀 Performance Optimization

### Caching Strategy
- Implement Redis cache for frequently requested stock prices
- Cache technical indicator calculations
- Use appropriate TTL based on data freshness requirements

### Scaling Configuration
```json
{
  "functionTimeout": "00:05:00",
  "extensions": {
    "http": {
      "maxOutstandingRequests": 200,
      "maxConcurrentRequests": 100,
      "dynamicThrottlesEnabled": true
    }
  }
}
```

### Cost Optimization
- Use Consumption plan for variable workloads
- Monitor API call costs and optimize requests
- Implement intelligent caching to reduce external API calls

## 🛣️ Roadmap

### Version 1.1
- [ ] Redis caching implementation
- [ ] Additional financial APIs (IEX Cloud, Financial Modeling Prep)
- [ ] Options and derivatives support
- [ ] News sentiment analysis

### Version 1.2
- [ ] Real-time streaming data via WebSockets
- [ ] Advanced portfolio optimization algorithms
- [ ] ESG (Environmental, Social, Governance) scoring
- [ ] Backtesting capabilities

### Version 2.0
- [ ] Machine learning predictions
- [ ] Custom indicator development
- [ ] Multi-region deployment
- [ ] GraphQL API support

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)

### Getting Help
- Create an [issue](https://github.com/your-username/financi/issues) for bugs or feature requests
- Check [existing issues](https://github.com/your-username/financi/issues) before creating new ones
- Join discussions in the [Discussions](https://github.com/your-username/financi/discussions) section

### Troubleshooting

#### Common Issues

**1. API Key Not Working**
```bash
# Verify API key is set correctly
az functionapp config appsettings list --name your-function-app --resource-group rg-financi
```

**2. Function App Cold Start**
- Use Premium plan for production to avoid cold starts
- Implement warming strategies for Consumption plan

**3. Rate Limit Exceeded**
- Monitor API usage in Application Insights
- Implement caching to reduce API calls
- Consider premium API plans

## 📞 Contact

**Project Maintainer**: Your Name  
**Email**: your.email@example.com  
**LinkedIn**: [your-linkedin-profile](https://linkedin.com/in/your-profile)

---

⭐ If you found this project helpful, please give it a star on GitHub!

Made with ❤️ and ☕ by the Financi team