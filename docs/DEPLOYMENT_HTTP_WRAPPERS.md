# HTTP Wrappers Deployment Guide

## ✅ What Was Done

### Files Created/Modified

1. **`src/http_wrappers.py`** (NEW)
   - 5 HTTP endpoint wrappers for all MCP tools
   - Complete parameter validation
   - Error handling and JSON responses
   - Supports both GET and POST requests

2. **`src/function_app.py`** (MODIFIED)
   - Added import: `from http_wrappers import create_http_wrappers`
   - Added call: `create_http_wrappers(app)` at end of file
   - Updated health endpoint to show available HTTP endpoints
   - Version bumped to 1.2.0

3. **`scripts/test-http-endpoints.sh`** (NEW)
   - Automated test script for all 5 HTTP endpoints
   - Tests with real data after deployment
   - Color-coded output with pass/fail summary

4. **Documentation**
   - `docs/HTTP_WRAPPERS_GUIDE.md` - Complete API documentation
   - `docs/MCP_REALITY_CHECK.md` - Explanation of MCP limitations

---

## 🚀 Deployment Steps

### Step 1: Review Changes

Check what was modified:
```bash
cd /Users/mohanakrishnavh/Repos/financi
git status
git diff src/function_app.py
```

### Step 2: Commit Changes

```bash
git add src/http_wrappers.py src/function_app.py scripts/test-http-endpoints.sh docs/
git commit -m "Add HTTP wrappers for all MCP tools

- Created http_wrappers.py with 5 RESTful endpoints
- Integrated HTTP wrappers into function_app.py
- All tools now accessible via standard HTTP/REST
- Added test script for endpoint validation
- Updated health endpoint with HTTP endpoint info
- Bumped version to 1.2.0

Endpoints:
- GET/POST /api/stock/price
- GET/POST /api/stock/portfolio
- GET/POST /api/stock/eight-pillar
- GET/POST /api/calculator/compound-interest
- GET/POST /api/calculator/retirement

This enables real data access via HTTP while keeping
experimental MCP triggers for future Azure AI integration."
```

### Step 3: Push to Repositories

```bash
./scripts/push-both.sh
```

### Step 4: Deploy to Azure Functions

**Option A: Using Azure DevOps Pipeline (Recommended)**

The push to Azure DevOps will trigger the CI/CD pipeline automatically:
1. Go to: https://dev.azure.com/mohanakrishnavh/financi/_build
2. Wait for build to complete (~3-5 minutes)
3. Build will automatically deploy to Azure Functions

**Option B: Manual Deployment (If pipeline not set up)**

```bash
# Make sure you have Azure Functions Core Tools installed
func --version

# Deploy directly
func azure functionapp publish financi --python
```

**Option C: Using Azure CLI**

```bash
# Login to Azure
az login

# Deploy the function app
az functionapp deployment source sync \
  --name financi \
  --resource-group rg-financi
```

---

## ✅ Verify Deployment

### Step 1: Check Health Endpoint

```bash
curl https://financi.azurewebsites.net/health
```

Expected response should include `"version": "1.2.0"` and the new `http_endpoints` section.

### Step 2: Run Test Script

```bash
cd /Users/mohanakrishnavh/Repos/financi
./scripts/test-http-endpoints.sh
```

This will test all 5 HTTP endpoints with real data and show pass/fail results.

### Step 3: Manual Testing

Test individual endpoints:

```bash
# Load API key
source .env.local

# Test stock price
curl "https://financi.azurewebsites.net/api/stock/price?code=$DEFAULT_HOST_KEY&symbol=MSFT"

# Test eight pillar analysis
curl "https://financi.azurewebsites.net/api/stock/eight-pillar?code=$DEFAULT_HOST_KEY&symbol=AAPL"

# Test compound interest
curl "https://financi.azurewebsites.net/api/calculator/compound-interest?code=$DEFAULT_HOST_KEY&principal=10000&rate=7&time=20&frequency=monthly"
```

---

## 📊 What You Get

### Before Deployment
❌ MCP tools not accessible via HTTP  
❌ `/runtime/webhooks/mcp` returns 401/403  
❌ Can only use mock data in local bridge  
❌ No way to test with real financial data  

### After Deployment
✅ 5 RESTful HTTP endpoints  
✅ Real Yahoo Finance data  
✅ Accessible from anywhere (curl, Python, JavaScript, etc.)  
✅ Standard Azure Functions authentication  
✅ Full parameter validation and error handling  
✅ Can update local bridge to use real data  

---

## 🔌 API Endpoints Reference

### 1. Get Stock Price
```bash
GET /api/stock/price?symbol=AAPL&code=YOUR_KEY
```

### 2. Calculate Portfolio Value
```bash
GET /api/stock/portfolio?symbol=MSFT&amount=50&code=YOUR_KEY
```

### 3. Eight Pillar Stock Analysis
```bash
GET /api/stock/eight-pillar?symbol=TSLA&code=YOUR_KEY
```

### 4. Compound Interest Calculator
```bash
GET /api/calculator/compound-interest?principal=10000&rate=7&time=20&frequency=monthly&code=YOUR_KEY
```

### 5. Retirement Calculator
```bash
GET /api/calculator/retirement?current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7&code=YOUR_KEY
```

---

## 🔧 Using with Python

```python
import requests
import os

# Load API key
API_KEY = os.getenv("DEFAULT_HOST_KEY")
BASE_URL = "https://financi.azurewebsites.net"

# Get stock price
response = requests.get(
    f"{BASE_URL}/api/stock/price",
    params={
        "code": API_KEY,
        "symbol": "AAPL"
    }
)
print(response.json())

# Eight pillar analysis
response = requests.get(
    f"{BASE_URL}/api/stock/eight-pillar",
    params={
        "code": API_KEY,
        "symbol": "MSFT"
    }
)
print(response.json())
```

---

## 🔧 Using with JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

const API_KEY = process.env.DEFAULT_HOST_KEY;
const BASE_URL = 'https://financi.azurewebsites.net';

// Get stock price
async function getStockPrice(symbol) {
  const url = `${BASE_URL}/api/stock/price?code=${API_KEY}&symbol=${symbol}`;
  const response = await fetch(url);
  return await response.json();
}

// Eight pillar analysis
async function analyzeStock(symbol) {
  const url = `${BASE_URL}/api/stock/eight-pillar?code=${API_KEY}&symbol=${symbol}`;
  const response = await fetch(url);
  return await response.json();
}

// Usage
getStockPrice('AAPL').then(console.log);
analyzeStock('MSFT').then(console.log);
```

---

## 🔄 Update Local MCP Bridge (Optional)

To make the local bridge use real data instead of mock data, see:
- `docs/HTTP_WRAPPERS_GUIDE.md` - Section: "Update Local Bridge (Optional)"

This is optional but recommended if you want Claude Desktop to use real financial data.

---

## 🐛 Troubleshooting

### Issue: 401 Unauthorized

**Cause:** Missing or invalid API key

**Solution:**
```bash
# Regenerate API key
./scripts/get-function-keys.sh

# Verify key is loaded
source .env.local
echo $DEFAULT_HOST_KEY
```

### Issue: 404 Not Found

**Cause:** Functions not deployed or wrong endpoint

**Solution:**
- Verify deployment completed successfully
- Check health endpoint: `curl https://financi.azurewebsites.net/health`
- Ensure version shows 1.2.0 or higher

### Issue: 500 Internal Server Error

**Cause:** Missing dependencies or handler error

**Solution:**
- Check Azure Functions logs:
  ```bash
  func azure functionapp logstream financi
  ```
- Verify all dependencies in requirements.txt
- Check for Python syntax errors

### Issue: Timeout

**Cause:** Cold start or Yahoo Finance API delay

**Solution:**
- Wait 30-60 seconds for cold start
- Retry the request
- Check Yahoo Finance is accessible: `curl https://finance.yahoo.com`

---

## 📈 Performance Notes

- **Cold Start:** First request may take 10-30 seconds
- **Warm Requests:** Subsequent requests ~1-3 seconds
- **Rate Limiting:** Yahoo Finance may rate limit excessive requests
- **Caching:** Consider adding caching for frequently requested stocks

---

## 🎯 Success Criteria

After deployment, you should be able to:

- ✅ Call all 5 HTTP endpoints with curl
- ✅ Get real stock data from Yahoo Finance
- ✅ Perform eight pillar analysis on any stock
- ✅ Calculate compound interest with various frequencies
- ✅ Project retirement savings with custom parameters
- ✅ Integrate endpoints into any application
- ✅ Use from Python, JavaScript, or any HTTP client

---

## 📚 Additional Documentation

- **API Reference:** `docs/HTTP_WRAPPERS_GUIDE.md`
- **MCP Background:** `docs/MCP_REALITY_CHECK.md`
- **Architecture:** `docs/PROJECT_STRUCTURE.md`
- **Testing:** `scripts/test-http-endpoints.sh`

---

## 🚀 Ready to Deploy!

Everything is committed and ready. Just push and deploy:

```bash
# Already committed? Just push:
./scripts/push-both.sh

# Then deploy (via Azure DevOps pipeline or manual)
```

After deployment, run:
```bash
./scripts/test-http-endpoints.sh
```

To verify everything works! 🎉
