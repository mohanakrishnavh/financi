# Financi - Financial Analysis MCP Server

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Azure Functions](https://img.shields.io/badge/Azure%20Functions-v4-blue.svg)](https://docs.microsoft.com/en-us/azure/azure-functions/)

Financi is a Python-based financial analysis server providing stock analysis tools through both **Model Context Protocol (MCP)** and **RESTful HTTP APIs**. Deployed as an Azure Function App with multi-source data integration (FMP, Alpha Vantage, Yahoo Finance).

---

## 🚀 Quick Start

### Already Deployed?
Access your Financi server at:
- **Health Check**: `https://financi.azurewebsites.net/api/health`
- **MCP Endpoint**: `https://financi.azurewebsites.net/runtime/webhooks/mcp/sse`

### New Installation?
1. Fork this repository to your Azure DevOps organization
2. Configure the Azure DevOps pipeline with your subscription details
3. Run the pipeline to automatically deploy infrastructure and code
4. Access your deployed functions at `https://financi.azurewebsites.net`

**Get Your API Key:**
```bash
./scripts/get-function-keys.sh
```

---

## ✨ Features

### 📊 Multi-Source Data Integration
- **FMP (Financial Modeling Prep)**: Primary real-time data source
- **Alpha Vantage**: First fallback with global market coverage
- **Yahoo Finance**: Ultimate fallback, always available
- **Smart Fallback**: Automatic source switching on failure
- **1-Day Caching**: Minimizes API calls and improves performance

### 📈 Stock Analysis Tools

#### 1. Real-Time Stock Price
Get current stock price, change percentage, volume, and company information with data source metadata.

```bash
curl "https://financi.azurewebsites.net/api/stock/price?code=KEY&symbol=AAPL"
```

**Response includes:**
- Current price and change
- Volume and market cap
- `data_source`: Which provider returned the data (fmp, alpha_vantage, yahoo_finance)
- `from_cache`: Boolean indicating if data came from cache

#### 2. Portfolio Value Calculator
Calculate total portfolio value based on shares owned.

```bash
curl "https://financi.azurewebsites.net/api/stock/portfolio?code=KEY&symbol=MSFT&amount=50"
```

#### 3. Eight Pillar Stock Analysis
Comprehensive fundamental analysis based on 8 key financial pillars:
- PE Ratio - Price-to-earnings valuation
- ROIC - Return on invested capital
- Shares Outstanding - Share dilution trends
- Cash Flow - Operating cash generation
- Net Income - Profitability trends
- Revenue Growth - Top-line expansion
- Liabilities - Debt management
- Price-to-FCF - Free cash flow valuation

```bash
curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=KEY&symbol=AAPL"
```

### 🧮 Financial Calculators

#### 4. Compound Interest Calculator
Calculate investment growth with customizable compounding frequency.
- Supports: annually, semi-annually, quarterly, monthly, daily
- Shows final amount, total interest, and effective rate

```bash
curl "https://financi.azurewebsites.net/api/calculator/compound-interest?code=KEY&principal=10000&rate=7&time=20&frequency=monthly"
```

#### 5. Retirement Savings Calculator
Project retirement savings with detailed year-by-year breakdown.
- Accounts for current savings and monthly contributions
- Shows growth from savings vs. contributions
- Calculates total at retirement

```bash
curl "https://financi.azurewebsites.net/api/calculator/retirement?code=KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"
```

---

## 🏗️ Architecture

### Multi-Source Data Flow

```
Client Request
    ↓
Check Cache?
    ↓
Cache Hit → Return Cached Data (with from_cache: true)
    ↓
Cache Miss → Try FMP (Primary)
    ↓
FMP Success → Cache & Return (data_source: fmp)
    ↓
FMP Fail → Try Alpha Vantage (Fallback 1)
    ↓
AV Success → Cache & Return (data_source: alpha_vantage, fallback_used: true)
    ↓
AV Fail → Try Yahoo Finance (Fallback 2)
    ↓
YF Success → Cache & Return (data_source: yahoo_finance, fallback_used: true)
    ↓
All Fail → Return Error
```

### Data Source Priority
1. **FMP (Primary)** → 2. **Alpha Vantage (Fallback)** → 3. **Yahoo Finance (Ultimate Fallback)**

**Benefits:**
- Triple redundancy ensures high availability
- Automatic failover with no user impact
- Transparent metadata shows which source provided data
- 1-day cache minimizes API costs

---

## 📋 Prerequisites

- **Azure Subscription**: Valid Azure subscription with appropriate permissions
- **Azure CLI**: Latest version installed and configured
- **Python 3.11+**: For local development and testing
- **Azure DevOps**: For CI/CD pipeline (optional)
- **API Keys**: 
  - FMP API key (recommended)
  - Alpha Vantage API key (optional)
  - Yahoo Finance works without API key

---

## 🛠️ Installation & Deployment

### Option 1: Automated Deployment via Azure DevOps

1. **Fork this repository** to your Azure DevOps organization

2. **Configure Service Connection**:
   ```bash
   # In Azure DevOps, create a service connection to your Azure subscription
   # Name it 'financi-service-connection' to match the pipeline configuration
   ```

3. **Set Pipeline Variables**:
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
   - `FMP_API_KEY`: Your FMP API key (recommended)
   - `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key (optional)

4. **Run the Pipeline**:
   - The pipeline will automatically deploy infrastructure and function code
   - Monitor the deployment in Azure DevOps

### Option 2: Manual Deployment

#### Step 1: Deploy Infrastructure

```bash
# Clone the repository
git clone https://github.com/your-username/financi.git
cd financi

# Create resource group
az group create --name rg-financi --location "East US 2"

# Deploy Bicep template
az deployment group create \
  --resource-group rg-financi \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/parameters.json
```

#### Step 2: Deploy Function Code

```bash
# Install dependencies
pip install -r src/requirements.txt

# Create deployment package
cd src
zip -r ../function-app.zip .

# Deploy to Azure Functions
az functionapp deployment source config-zip \
  --resource-group rg-financi \
  --name financi \
  --src ../function-app.zip
```

#### Step 3: Configure API Keys

```bash
# Set FMP API key (recommended)
az functionapp config appsettings set \
  --name financi \
  --resource-group rg-financi \
  --settings "FMP_API_KEY=your-fmp-api-key" \
             "DATA_SOURCE=fmp" \
             "FALLBACK_DATA_SOURCES=alpha_vantage,yahoo_finance"

# Set Alpha Vantage API key (optional)
az functionapp config appsettings set \
  --name financi \
  --resource-group rg-financi \
  --settings "ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key"

# Set cache duration (default: 1 day)
az functionapp config appsettings set \
  --name financi \
  --resource-group rg-financi \
  --settings "CACHE_DURATION_SECONDS=86400"
```

---

## 📖 Usage

### Health Check

Verify your deployment is working:
```bash
curl https://financi.azurewebsites.net/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "service": "financi-mcp",
  "version": "1.4.0"
}
```

### Using with Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "financi": {
      "command": "node",
      "args": [
        "/path/to/financi/local-server/mcp-bridge-server.js"
      ],
      "env": {
        "FINANCI_SERVER_URL": "https://financi.azurewebsites.net",
        "FINANCI_API_KEY": "your-function-key-here"
      }
    }
  }
}
```

Restart Claude Desktop after configuration.

### Using with Python

```python
import requests
import os

API_KEY = os.getenv("FINANCI_API_KEY")
BASE_URL = "https://financi.azurewebsites.net"

# Get stock price with metadata
response = requests.get(
    f"{BASE_URL}/api/stock/price",
    params={"code": API_KEY, "symbol": "AAPL"}
)
data = response.json()

print(f"Price: ${data['price']}")
print(f"Data Source: {data['data_source']}")
print(f"From Cache: {data['from_cache']}")

# Eight pillar analysis
response = requests.get(
    f"{BASE_URL}/api/stock/eight-pillar",
    params={"code": API_KEY, "symbol": "MSFT"}
)
analysis = response.json()
print(f"Overall Score: {analysis['overall_score']}")
```

---

## 🧪 Testing

### Quick Test

```bash
# Get function keys (creates .env.local)
./scripts/get-function-keys.sh

# Test all HTTP endpoints
./scripts/test-functions.sh

# Run unit tests
pytest tests/ -v
```

### Manual Testing

```bash
# Load environment
source .env.local

# Test stock price
curl "https://financi.azurewebsites.net/api/stock/price?code=$DEFAULT_HOST_KEY&symbol=AAPL"

# Test eight pillar analysis
curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=$DEFAULT_HOST_KEY&symbol=TSLA"

# Test retirement calculator
curl "https://financi.azurewebsites.net/api/calculator/retirement?code=$DEFAULT_HOST_KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"
```

---

## 📁 Project Structure

```
financi/
├── src/
│   ├── function_app.py              # Main Azure Functions entry point
│   ├── requirements.txt             # Python dependencies
│   ├── config/
│   │   └── data_sources.py          # Multi-source configuration
│   ├── services/
│   │   ├── fmp.py                   # FMP API client
│   │   ├── alpha_vantage.py         # Alpha Vantage API client
│   │   ├── yahoo_finance.py         # Yahoo Finance client
│   │   └── stock_data_service.py    # Unified service with fallback
│   ├── handlers/
│   │   ├── stock_handlers.py        # Stock analysis handlers
│   │   └── financial_calculators.py # Calculator handlers
│   └── utils/
│       └── stock_utils.py           # Stock utility functions
├── tests/
│   ├── test_stock_handlers.py       # Handler tests
│   └── test_integration.py          # Integration tests
├── local-server/
│   ├── mcp-bridge-server.js         # Local MCP bridge
│   └── package.json                 # Node dependencies
├── scripts/
│   ├── get-function-keys.sh         # Get Azure function keys
│   ├── test-functions.sh            # Test HTTP endpoints
│   └── push-both.sh                 # Push to GitHub & Azure DevOps
├── infrastructure/
│   ├── main.bicep                   # Azure infrastructure
│   └── parameters.json              # Deployment parameters
└── docs/
    ├── ALPHA_VANTAGE_INTEGRATION.md # Alpha Vantage setup guide
    └── MCP_CONFIGURATION.md         # MCP configuration guide
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FMP_API_KEY` | Financial Modeling Prep API key | Recommended | - |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | Optional | - |
| `DATA_SOURCE` | Primary data source | No | `fmp` |
| `FALLBACK_DATA_SOURCES` | Comma-separated fallback sources | No | `alpha_vantage,yahoo_finance` |
| `CACHE_DURATION_SECONDS` | Cache TTL in seconds | No | `86400` (1 day) |
| `MCP_SERVER_NAME` | Server identification | No | `financi` |
| `MCP_SERVER_VERSION` | Server version | No | `1.4.0` |
| `LOGGING_LEVEL` | Python logging level | No | `INFO` |

---

## 🐛 Troubleshooting

### Common Issues

**401 Unauthorized Errors**
- Verify API key: `./scripts/get-function-keys.sh`
- Check key is passed correctly in `code` parameter

**404 Not Found**
- Verify deployment: `az functionapp show --name financi --resource-group rg-financi`
- Check endpoint URL matches deployed function names

**Timeout Errors**
- First request may take 10-30 seconds (cold start)
- Retry the request
- Consider Premium plan for production

**Data Source Errors**
- Check response metadata: `data_source` and `fallback_used` fields
- Verify API keys are set correctly in Azure Function App settings
- Yahoo Finance will always work as ultimate fallback

### API Rate Limits

- **FMP Free**: Varies by plan (check your account)
- **Alpha Vantage Free**: 5 requests per minute, 500 per day
- **Yahoo Finance**: Rate limited but generally generous

**Mitigation**: 1-day cache reduces API calls by 95%+

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Financial Modeling Prep** - Premium financial data API
- **Alpha Vantage** - Real-time and historical market data
- **Yahoo Finance** - Free financial data via yfinance
- **Azure Functions** - Serverless hosting platform
- **Model Context Protocol** - AI assistant integration standard

---

**Built with ❤️ using Python, Azure Functions, and multi-source financial data**

**Version**: 1.4.0  
**Last Updated**: November 2024
