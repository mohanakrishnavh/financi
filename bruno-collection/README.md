# Financi API - Bruno Collection

This directory contains a [Bruno](https://www.usebruno.com/) API collection for testing the Financi API endpoints.

## What is Bruno?

Bruno is a fast, Git-friendly, open-source API client alternative to Postman. It stores collections directly in your filesystem using plain text files, making it perfect for version control.

## Installation

1. **Install Bruno Desktop**
   - Download from: https://www.usebruno.com/downloads
   - Or via Homebrew: `brew install bruno`

2. **Open the Collection**
   - Launch Bruno
   - Click "Open Collection"
   - Navigate to this `bruno-collection` directory
   - Select the folder

## Configuration

### Set Your Function Key

Before using the API, you need to set your Azure Function key:

1. Get your function key:
   ```bash
   cd /Users/mohanakrishnavh/Repos/financi
   ./scripts/get-function-keys.sh
   ```

2. In Bruno:
   - Click on "Environments" in the sidebar
   - Select "Production" environment
   - Replace `your-function-key-here` with your actual function key
   - Save the environment

### Environments

The collection includes two pre-configured environments:

- **Production**: Points to `https://financi.azurewebsites.net`
- **Local**: Points to `http://localhost:7071` (for local development)

Switch between environments using the dropdown in Bruno's top bar.

## Available Endpoints

### Health Check
- **Method**: GET
- **URL**: `/health`
- **Auth**: None required
- **Purpose**: Check API health and available endpoints

### Stock Endpoints

#### Get Stock Price
- **Method**: GET
- **URL**: `/api/stock/price?symbol=AAPL`
- **Auth**: Function key required
- **Purpose**: Get current stock price and market data

#### Calculate Portfolio Value
- **Method**: POST
- **URL**: `/api/stock/portfolio`
- **Auth**: Function key required
- **Body**: `{ "symbol": "AAPL", "shares": 100 }`
- **Purpose**: Calculate total value of stock holdings

#### Eight Pillar Stock Analysis
- **Method**: GET
- **URL**: `/api/stock/eight-pillar?symbol=MSFT`
- **Auth**: Function key required
- **Purpose**: Comprehensive stock analysis across 8 dimensions

### Calculator Endpoints

#### Compound Interest Calculator
- **Method**: POST
- **URL**: `/api/calculator/compound-interest`
- **Auth**: Function key required
- **Body**: 
  ```json
  {
    "principal": 10000,
    "rate": 7,
    "time": 10,
    "frequency": 12
  }
  ```
- **Purpose**: Calculate compound interest growth

#### Retirement Calculator
- **Method**: POST
- **URL**: `/api/calculator/retirement`
- **Auth**: Function key required
- **Body**: 
  ```json
  {
    "current_age": 30,
    "retirement_age": 65,
    "current_savings": 50000,
    "monthly_contribution": 1000,
    "annual_return": 7,
    "inflation_rate": 2.5
  }
  ```
- **Purpose**: Calculate retirement savings projections

## Quick Start

1. **Test the API is working**:
   - Open "Health Check" request
   - Click "Send"
   - Should return status: "healthy"

2. **Get a stock price**:
   - Open "Get Stock Price" request
   - Make sure the Production environment is selected
   - Click "Send"
   - Should return Apple stock data

3. **Try the Eight Pillar Analysis**:
   - Open "Eight Pillar Stock Analysis" request
   - Change the symbol parameter if desired (MSFT, AAPL, GOOGL, etc.)
   - Click "Send"
   - Review the comprehensive analysis

## Features

- ✅ All 6 API endpoints configured
- ✅ Environment variables for easy switching (Production/Local)
- ✅ Request documentation in each endpoint
- ✅ Example payloads pre-configured
- ✅ Query parameters pre-filled
- ✅ Git-friendly plain text format

## Tips

- **Change stock symbols**: Edit the `symbol` query parameter in any stock endpoint
- **Modify calculations**: Edit the JSON body in calculator endpoints
- **Test different scenarios**: Use the provided example values in the docs
- **View responses**: Bruno displays responses in a formatted JSON viewer
- **Save responses**: Use Bruno's "Save Response" feature to compare results

## Troubleshooting

### 401 Unauthorized Error
- Make sure you've set the correct function key in the environment variables
- Verify the key is valid by running `./scripts/get-function-keys.sh`

### Connection Refused (Local)
- Make sure Azure Functions is running locally: `func start` in the project root
- Verify the local URL is `http://localhost:7071`

### Invalid Symbol Error
- Ensure you're using valid stock ticker symbols (e.g., AAPL, MSFT, GOOGL)
- Symbols are case-insensitive but should be valid Yahoo Finance tickers

## Documentation

For more details on the API:
- See `README.md` in the project root
- See `docs/HTTP_WRAPPERS_GUIDE.md` for detailed API documentation
- See `docs/DEPLOYMENT_HTTP_WRAPPERS.md` for deployment information

## Version Control

Since Bruno collections are plain text files, they can be:
- ✅ Committed to Git
- ✅ Shared with team members
- ✅ Tracked for changes
- ✅ Reviewed in pull requests

Just add and commit this `bruno-collection` directory to your repository!
