# API Documentation - Financi MCP Server

## Overview

The Financi MCP Server provides a RESTful HTTP interface following the Model Context Protocol specification. All endpoints return JSON responses and use standard HTTP status codes.

## Base URL

```
https://your-function-app.azurewebsites.net/api
```

## Authentication

Currently, the server uses Azure Function App's built-in authentication. For production deployments, consider implementing:
- API Key authentication
- Azure Active Directory integration
- OAuth 2.0 / OpenID Connect

## Endpoints

### Health Check

**GET** `/health`

Returns the server health status and basic information.

**Response:**
```json
{
  "status": "healthy",
  "server": "financi-mcp-server",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### MCP Protocol

**POST** `/mcp`

Main endpoint for Model Context Protocol communication.

**Request Headers:**
```
Content-Type: application/json
```

## MCP Tools Reference

### 1. get_stock_price

Retrieves current stock price and basic market data.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol (e.g., "AAPL", "MSFT")

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_stock_price",
    "arguments": {
      "symbol": "AAPL"
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"symbol\": \"AAPL\", \"price\": 150.00, \"change\": 2.50, \"change_percent\": \"+1.69%\", \"volume\": 1000000, \"latest_trading_day\": \"2024-01-01\", \"previous_close\": 147.50}"
    }
  ]
}
```

### 2. get_stock_history

Retrieves historical stock price data for technical analysis.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `period` (string, optional): Time period for historical data
  - Allowed values: `"1d"`, `"5d"`, `"1mo"`, `"3mo"`, `"6mo"`, `"1y"`, `"2y"`, `"5y"`, `"10y"`, `"ytd"`, `"max"`
  - Default: `"1mo"`

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_stock_history",
    "arguments": {
      "symbol": "MSFT",
      "period": "1mo"
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"symbol\": \"MSFT\", \"period\": \"1mo\", \"data\": [{\"date\": \"2024-01-01\", \"open\": 100.00, \"high\": 105.00, \"low\": 98.00, \"close\": 104.00, \"volume\": 500000}]}"
    }
  ]
}
```

### 3. get_crypto_price

Retrieves current cryptocurrency price and market data.

**Parameters:**
- `symbol` (string, required): Cryptocurrency symbol (e.g., "bitcoin", "ethereum")
- `vs_currency` (string, optional): Base currency for price comparison
  - Default: `"usd"`

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_crypto_price",
    "arguments": {
      "symbol": "bitcoin",
      "vs_currency": "usd"
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"symbol\": \"BITCOIN\", \"price\": 45000.00, \"change_24h\": 2.5, \"volume_24h\": 25000000000, \"market_cap\": 850000000000, \"vs_currency\": \"USD\"}"
    }
  ]
}
```

### 4. calculate_technical_indicators

Calculates technical indicators for stock analysis.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `indicators` (array, required): List of technical indicators to calculate
  - Allowed values: `"rsi"`, `"macd"`, `"sma_20"`, `"sma_50"`, `"ema_12"`, `"ema_26"`
- `period` (string, optional): Time period for analysis
  - Default: `"3mo"`

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "calculate_technical_indicators",
    "arguments": {
      "symbol": "TSLA",
      "indicators": ["rsi", "sma_20", "macd"],
      "period": "3mo"
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"symbol\": \"TSLA\", \"indicators\": {\"rsi\": 65.23, \"sma_20\": 245.67, \"macd\": {\"macd_line\": 2.34, \"ema_12\": 248.90, \"ema_26\": 246.56}}}"
    }
  ]
}
```

### 5. get_financial_ratios

Retrieves key financial ratios and metrics for fundamental analysis.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_financial_ratios",
    "arguments": {
      "symbol": "AAPL"
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"symbol\": \"AAPL\", \"ratios\": {\"pe_ratio\": \"N/A - Requires premium API\", \"pb_ratio\": \"N/A - Requires premium API\", \"debt_to_equity\": \"N/A - Requires premium API\", \"return_on_equity\": \"N/A - Requires premium API\", \"current_ratio\": \"N/A - Requires premium API\"}, \"note\": \"Financial ratios require premium API access. Consider integrating with Financial Modeling Prep, IEX Cloud, or similar service.\"}"
    }
  ]
}
```

### 6. portfolio_analysis

Analyzes a portfolio of stocks and cryptocurrencies.

**Parameters:**
- `holdings` (array, required): List of portfolio holdings
  - Each holding must include:
    - `symbol` (string): Asset symbol
    - `quantity` (number): Number of shares/coins held
    - `type` (string): Asset type - `"stock"` or `"crypto"`

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "portfolio_analysis",
    "arguments": {
      "holdings": [
        {"symbol": "AAPL", "quantity": 10, "type": "stock"},
        {"symbol": "MSFT", "quantity": 5, "type": "stock"},
        {"symbol": "bitcoin", "quantity": 0.5, "type": "crypto"}
      ]
    }
  }
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"total_value\": 25000.00, \"holdings\": [{\"symbol\": \"AAPL\", \"type\": \"stock\", \"quantity\": 10, \"current_price\": 150.00, \"value\": 1500.00, \"allocation_percent\": 6.0, \"change_percent\": \"+1.69%\"}], \"diversification\": {\"stock_allocation\": 80.0, \"crypto_allocation\": 20.0}}"
    }
  ]
}
```

## Error Handling

### Error Response Format

All errors follow a consistent JSON format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Scenarios

#### 1. Invalid Symbol
**Status Code:** 200 (with error in content)
```json
{
  "content": [
    {
      "type": "text", 
      "text": "{\"error\": \"No data found for symbol XYZ\"}"
    }
  ]
}
```

#### 2. Missing API Key
**Status Code:** 200 (with error in content)
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"error\": \"Alpha Vantage API key not configured\"}"
    }
  ]
}
```

#### 3. Invalid Method
**Status Code:** 400
```json
{
  "error": "Unsupported method: invalid_method"
}
```

#### 4. Missing Parameters
**Status Code:** 200 (with error in content)
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"error\": \"Missing required parameter: symbol\"}"
    }
  ]
}
```

## Rate Limiting

The server inherits rate limits from external APIs:

### Alpha Vantage (Stock Data)
- **Free Tier**: 5 requests per minute, 500 per day
- **Premium**: Higher limits available

### CoinGecko (Crypto Data)  
- **Free Tier**: 10-50 requests per minute
- **Pro Plans**: Higher limits and additional features

### Recommendations
- Implement client-side caching to reduce API calls
- Use appropriate polling intervals for real-time data
- Consider premium API plans for production usage

## Authentication & Authorization

### Current Implementation
- Basic Azure Function authentication
- No API key required for testing

### Production Recommendations
```json
{
  "headers": {
    "Authorization": "Bearer <jwt-token>",
    "X-API-Key": "<api-key>",
    "Content-Type": "application/json"
  }
}
```

## SDK and Client Libraries

### JavaScript/TypeScript Client

```typescript
import { MCPClient } from '@modelcontextprotocol/client';

const client = new MCPClient({
  baseUrl: 'https://your-function-app.azurewebsites.net/api/mcp'
});

// Get stock price
const stockPrice = await client.callTool('get_stock_price', {
  symbol: 'AAPL'
});
```

### Python Client

```python
import requests
import json

def call_mcp_tool(tool_name, arguments):
    url = "https://your-function-app.azurewebsites.net/api/mcp"
    payload = {
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

# Get stock price
result = call_mcp_tool('get_stock_price', {'symbol': 'AAPL'})
```

## Testing the API

### Using curl

```bash
# Test health endpoint
curl https://your-function-app.azurewebsites.net/api/health

# List available tools
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Get stock price
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_stock_price",
      "arguments": {"symbol": "AAPL"}
    }
  }'
```

### Using Postman

1. Create a new POST request
2. Set URL to: `https://your-function-app.azurewebsites.net/api/mcp`
3. Add header: `Content-Type: application/json`
4. Set body to raw JSON with the tool call payload

## Best Practices

### 1. Error Handling
Always check for errors in the response content before processing data.

### 2. Caching
Implement client-side caching for frequently requested data to reduce API calls and improve performance.

### 3. Retry Logic
Implement exponential backoff for handling rate limits and temporary failures.

### 4. Data Validation
Validate input parameters before making API calls to avoid unnecessary requests.

### 5. Monitoring
Monitor API usage and costs, especially when using premium financial data services.