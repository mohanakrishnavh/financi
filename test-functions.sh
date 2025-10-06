#!/bin/bash

# Financi MCP Function Tester
# ==========================
# Uses keys from .env.local to test Azure Functions

# Load environment variables from .env.local
if [ -f ".env.local" ]; then
    source .env.local
else
    echo "❌ .env.local file not found!"
    echo "💡 Run ./get-function-keys.sh first to create this file"
    exit 1
fi

# Configuration
FUNCTION_APP_URL="https://financi.azurewebsites.net"
KEY="$DEFAULT_HOST_KEY"

if [ -z "$KEY" ]; then
    echo "❌ DEFAULT_HOST_KEY not found in .env.local"
    exit 1
fi

echo "🧪 Testing Financi MCP Functions"
echo "================================"
echo "Function App: $FUNCTION_APP_URL"
echo "Using key: ${KEY:0:20}..."
echo ""

# Function to test endpoints
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local data="$3"
    local auth_required="$4"
    
    echo "🔍 Testing: $name"
    echo "Endpoint: $endpoint"
    
    if [ "$auth_required" = "true" ]; then
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
            -X POST "$FUNCTION_APP_URL$endpoint" \
            -H "x-functions-key: $KEY" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$FUNCTION_APP_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo "$response" | sed -e 's/HTTPSTATUS:.*//g')
    
    if [ "$http_code" -eq 200 ]; then
        echo "✅ SUCCESS (HTTP $http_code)"
        echo "Response: $body"
    else
        echo "❌ FAILED (HTTP $http_code)"
        echo "Response: $body"
    fi
    echo ""
}

# Test 1: Health Check (no auth)
test_endpoint "Health Check" "/api/health" "" "false"

# Test 2: Hello Financi
test_endpoint "Hello Financi" "/api/hello_financi" "{}" "true"

# Test 3: Get Stock Price
test_endpoint "Get Stock Price (AAPL)" "/api/get_stock_price" '{"arguments": {"symbol": "AAPL"}}' "true"

# Test 4: Calculate Portfolio Value
test_endpoint "Portfolio Value (MSFT x10)" "/api/calculate_portfolio_value" '{"arguments": {"symbol": "MSFT", "amount": 10}}' "true"

echo "🎯 Testing Complete!"
echo ""
echo "💡 Tips:"
echo "• All MCP functions require authentication except /api/health"
echo "• Keys are stored securely in .env.local (not committed to git)"
echo "• Update keys by running ./get-function-keys.sh"
echo "• Check Azure Portal → Function App → App Keys for key management"