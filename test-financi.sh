#!/bin/bash

# Financi MCP Server Test Script
# Usage: ./test-financi.sh <function_app_url>

if [ -z "$1" ]; then
    echo "Usage: $0 <function_app_url>"
    echo "Example: $0 https://financi-mcp-main-12345.azurewebsites.net"
    exit 1
fi

FUNCTION_URL="$1"

echo "🧪 Testing Financi MCP Server at: $FUNCTION_URL"
echo "================================================"

# Test 1: Health Check
echo "1️⃣  Testing Health Endpoint..."
HEALTH_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" "$FUNCTION_URL/api/health")
HTTP_CODE=$(echo $HEALTH_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
HEALTH_BODY=$(echo $HEALTH_RESPONSE | sed -e 's/HTTPSTATUS:.*//g')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Health check passed"
    echo "Response: $HEALTH_BODY"
else
    echo "❌ Health check failed (HTTP $HTTP_CODE)"
    echo "Response: $HEALTH_BODY"
fi

echo ""

# Test 2: MCP Tools List
echo "2️⃣  Testing MCP Tools List..."
TOOLS_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$FUNCTION_URL/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}')
HTTP_CODE=$(echo $TOOLS_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
TOOLS_BODY=$(echo $TOOLS_RESPONSE | sed -e 's/HTTPSTATUS:.*//g')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Tools list retrieved successfully"
    echo "Response: $TOOLS_BODY" | python3 -m json.tool 2>/dev/null || echo "$TOOLS_BODY"
else
    echo "❌ Tools list failed (HTTP $HTTP_CODE)"
    echo "Response: $TOOLS_BODY"
fi

echo ""

# Test 3: Stock Price Tool (requires API key)
echo "3️⃣  Testing Stock Price Tool..."
STOCK_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$FUNCTION_URL/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_stock_price",
      "arguments": {"symbol": "AAPL"}
    }
  }')
HTTP_CODE=$(echo $STOCK_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
STOCK_BODY=$(echo $STOCK_RESPONSE | sed -e 's/HTTPSTATUS:.*//g')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Stock price tool worked"
    echo "Response: $STOCK_BODY" | python3 -m json.tool 2>/dev/null || echo "$STOCK_BODY"
else
    echo "❌ Stock price tool failed (HTTP $HTTP_CODE)"
    echo "Response: $STOCK_BODY"
fi

echo ""

# Test 4: Crypto Price Tool
echo "4️⃣  Testing Crypto Price Tool..."
CRYPTO_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$FUNCTION_URL/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_crypto_price",
      "arguments": {"symbol": "bitcoin"}
    }
  }')
HTTP_CODE=$(echo $CRYPTO_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
CRYPTO_BODY=$(echo $CRYPTO_RESPONSE | sed -e 's/HTTPSTATUS:.*//g')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Crypto price tool worked"
    echo "Response: $CRYPTO_BODY" | python3 -m json.tool 2>/dev/null || echo "$CRYPTO_BODY"
else
    echo "❌ Crypto price tool failed (HTTP $HTTP_CODE)"
    echo "Response: $CRYPTO_BODY"
fi

echo ""
echo "🎯 Test Summary Complete!"
echo "================================================"