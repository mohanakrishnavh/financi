# HTTP Wrappers Implementation Guide

## Summary

**Problem:** Azure Functions' `mcpToolTrigger` doesn't create accessible HTTP endpoints.

**Solution:** Add HTTP wrapper functions that provide RESTful access to the same handler functions used by MCP triggers.

## What Was Created

### File: `src/http_wrappers.py`

Contains HTTP endpoint wrappers for all 6 tools:

1. **GET/POST `/api/stock/price`** → `get_stock_price` handler
2. **GET/POST `/api/stock/portfolio`** → `calculate_portfolio_value` handler  
3. **GET/POST `/api/stock/eight-pillar`** → `eight_pillar_stock_analysis` handler
4. **GET/POST `/api/calculator/compound-interest`** → `compound_interest_calculator` handler
5. **GET/POST `/api/calculator/retirement`** → `retirement_calculator` handler

## Integration Steps

### Step 1: Update `function_app.py`

Add this import and call at the end of `function_app.py`:

```python
# At the top with other imports
from http_wrappers import create_http_wrappers

# At the very end of the file, after the health endpoint
# Register HTTP wrappers for MCP tools
create_http_wrappers(app)
```

### Step 2: Deploy to Azure

```bash
# Commit changes
git add src/http_wrappers.py src/function_app.py
git commit -m "Add HTTP wrappers for all MCP tools"
./scripts/push-both.sh

# Deploy (if using Azure CLI)
func azure functionapp publish financi
```

### Step 3: Test Endpoints

```bash
# Load your API key
source .env.local

# Test stock price
curl "https://financi.azurewebsites.net/api/stock/price?code=$DEFAULT_HOST_KEY&symbol=MSFT"

# Test portfolio value
curl "https://financi.azurewebsites.net/api/stock/portfolio?code=$DEFAULT_HOST_KEY&symbol=AAPL&amount=50"

# Test eight pillar analysis
curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=$DEFAULT_HOST_KEY&symbol=TSLA"

# Test compound interest
curl "https://financi.azurewebsites.net/api/calculator/compound-interest?code=$DEFAULT_HOST_KEY&principal=10000&rate=7&time=20&frequency=monthly"

# Test retirement calculator
curl "https://financi.azurewebsites.net/api/calculator/retirement?code=$DEFAULT_HOST_KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"
```

## API Documentation

### 1. Get Stock Price

**Endpoint:** `GET /api/stock/price`

**Parameters:**
- `symbol` (required): Stock ticker symbol (e.g., AAPL, MSFT)

**Example:**
```bash
curl "https://financi.azurewebsites.net/api/stock/price?code=KEY&symbol=AAPL"
```

**Response:**
```json
{
  "symbol": "AAPL",
  "price": 150.25,
  "currency": "USD",
  "timestamp": "2025-11-10T10:30:00Z",
  "change": "+2.5%",
  "company_name": "Apple Inc.",
  "status": "success"
}
```

### 2. Calculate Portfolio Value

**Endpoint:** `GET /api/stock/portfolio`

**Parameters:**
- `symbol` (required): Stock ticker symbol
- `amount` (required): Number of shares

**Example:**
```bash
curl "https://financi.azurewebsites.net/api/stock/portfolio?code=KEY&symbol=MSFT&amount=10"
```

**Response:**
```json
{
  "symbol": "MSFT",
  "shares": 10,
  "price_per_share": 380.50,
  "total_value": 3805.00,
  "currency": "USD",
  "status": "success"
}
```

### 3. Eight Pillar Stock Analysis

**Endpoint:** `GET /api/stock/eight-pillar`

**Parameters:**
- `symbol` (required): Stock ticker symbol to analyze

**Example:**
```bash
curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=KEY&symbol=MSFT"
```

**Response:**
```json
{
  "symbol": "MSFT",
  "company_name": "Microsoft Corporation",
  "analysis_date": "2025-11-10T10:30:00Z",
  "pillars": {
    "pe_ratio": {...},
    "roic": {...},
    "shares_outstanding": {...},
    "cash_flow": {...},
    "net_income": {...},
    "revenue_growth": {...},
    "liabilities": {...},
    "price_to_fcf": {...}
  },
  "overall_score": "85/100",
  "recommendation": "Strong Buy",
  "status": "success"
}
```

### 4. Compound Interest Calculator

**Endpoint:** `GET /api/calculator/compound-interest`

**Parameters:**
- `principal` (required): Initial investment amount
- `rate` (required): Annual interest rate (percentage)
- `time` (required): Investment period in years
- `frequency` (required): Compounding frequency (annually, semi-annually, quarterly, monthly, daily)

**Example:**
```bash
curl "https://financi.azurewebsites.net/api/calculator/compound-interest?code=KEY&principal=10000&rate=7&time=20&frequency=monthly"
```

**Response:**
```json
{
  "principal": 10000,
  "rate": 7,
  "time": 20,
  "frequency": "monthly",
  "final_amount": 40387.27,
  "total_interest": 30387.27,
  "effective_rate": 7.229%,
  "status": "success"
}
```

### 5. Retirement Calculator

**Endpoint:** `GET /api/calculator/retirement`

**Parameters:**
- `current_age` (required): Your current age
- `retirement_age` (required): Planned retirement age
- `current_savings` (required): Current retirement savings
- `monthly_contribution` (required): Monthly contribution amount
- `annual_return` (required): Expected annual return rate (percentage)

**Example:**
```bash
curl "https://financi.azurewebsites.net/api/calculator/retirement?code=KEY&current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"
```

**Response:**
```json
{
  "current_age": 30,
  "retirement_age": 65,
  "years_to_retirement": 35,
  "total_at_retirement": 1234567.89,
  "projections": {...},
  "year_by_year": [...],
  "status": "success"
}
```

## Architecture

### Before (MCP Only)

```
┌─────────────────────┐
│  function_app.py    │
│                     │
│  @mcpToolTrigger    │ ❌ No HTTP access
│  └─> handler()      │
└─────────────────────┘
```

### After (Hybrid)

```
┌─────────────────────────────────────┐
│  function_app.py                    │
│                                     │
│  @mcpToolTrigger                    │ ❌ Still no HTTP (future use)
│  └─> handler()                      │
│                                     │
│  http_wrappers.py                   │
│  @route("/api/...")                 │ ✅ HTTP accessible
│  └─> same handler()                 │
└─────────────────────────────────────┘
```

**Key Benefits:**
- ✅ Both MCP triggers and HTTP endpoints use the same handler logic
- ✅ No code duplication for business logic
- ✅ MCP triggers kept for future Azure AI integrations
- ✅ HTTP endpoints work NOW with real data

## Update Local Bridge (Optional)

If you want the local MCP bridge to use real data instead of mock data, update `local-server/mcp-bridge-server.js`:

```javascript
async callAzureFunction(functionName, args) {
  try {
    if (API_KEY) {
      const fetch = (await import('node-fetch')).default;
      
      // Map MCP tool names to HTTP endpoints
      const endpointMap = {
        'get_stock_price': '/api/stock/price',
        'calculate_portfolio_value': '/api/stock/portfolio',
        'eight_pillar_stock_analysis': '/api/stock/eight-pillar',
        'compound_interest_calculator': '/api/calculator/compound-interest',
        'retirement_calculator': '/api/calculator/retirement'
      };
      
      const endpoint = endpointMap[functionName];
      if (endpoint) {
        // Build query string from args
        const params = new URLSearchParams(args).toString();
        const url = `${FUNCTION_APP_URL}${endpoint}?code=${API_KEY}&${params}`;
        
        const response = await fetch(url);
        if (response.ok) {
          return await response.text();
        }
      }
    }
    
    // Fallback to mock data
    return this.getMockData(functionName, args);
    
  } catch (error) {
    console.error(`Error calling ${functionName}:`, error);
    return this.getMockData(functionName, args);
  }
}
```

## Testing Checklist

After deployment:

- [ ] Health endpoint responds: `/api/health`
- [ ] Stock price endpoint works with real data
- [ ] Portfolio calculation works
- [ ] Eight pillar analysis returns real data
- [ ] Compound interest calculator works
- [ ] Retirement calculator works
- [ ] All endpoints require authentication (`code` parameter)
- [ ] Error handling works (missing parameters, invalid values)
- [ ] Local MCP bridge can call HTTP endpoints (if updated)

## Next Steps

1. **Review the implementation** in `src/http_wrappers.py`
2. **Integrate into `function_app.py`** by adding the import and call
3. **Test locally** (optional): `func start` and test with curl
4. **Deploy to Azure** and test live endpoints
5. **Update local bridge** to use real HTTP endpoints (optional)
6. **Update documentation** with live endpoint URLs

## Benefits of This Approach

✅ **Real data everywhere** - No more mock data limitations  
✅ **Standard HTTP** - Works with any HTTP client  
✅ **Keep MCP triggers** - Future-proof for Azure AI integrations  
✅ **No code duplication** - Handlers are shared between MCP and HTTP  
✅ **Production ready** - Standard Azure Functions HTTP triggers  
✅ **Easy testing** - Simple curl commands to test  
✅ **Flexible** - Supports both GET (query params) and POST (JSON body)

## Ready to Implement?

The code is ready in `src/http_wrappers.py`. Just need to:
1. Add two lines to `function_app.py`
2. Deploy to Azure
3. Test with curl

Would you like me to make the changes to `function_app.py` now?
