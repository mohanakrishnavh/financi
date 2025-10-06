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

echo "🧪 Testing Financi MCP Server"
echo "============================="
echo "Function App: $FUNCTION_APP_URL"
echo "Using key: ${KEY:0:20}..."
echo ""

# Function to test HTTP endpoints
test_http_endpoint() {
    local name="$1"
    local endpoint="$2"
    
    echo "🔍 Testing: $name"
    echo "Endpoint: $endpoint"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$FUNCTION_APP_URL$endpoint")
    
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

# Function to test MCP runtime endpoints
test_mcp_endpoint() {
    local name="$1"
    local endpoint="$2"
    
    echo "🔍 Testing MCP: $name"
    echo "Endpoint: $endpoint"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -H "x-functions-key: $KEY" \
        -H "Accept: text/event-stream" \
        "$FUNCTION_APP_URL$endpoint")
    
    http_code=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo "$response" | sed -e 's/HTTPSTATUS:.*//g')
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 204 ]; then
        echo "✅ MCP ENDPOINT ACCESSIBLE (HTTP $http_code)"
        if [ ! -z "$body" ]; then
            echo "Response: $body"
        fi
    else
        echo "❌ MCP ENDPOINT FAILED (HTTP $http_code)"
        echo "Response: $body"
    fi
    echo ""
}

echo "📡 TESTING HTTP ENDPOINTS"
echo "========================"

# Test 1: Health Check (no auth required)
test_http_endpoint "Health Check" "/api/health"

echo "🔗 TESTING MCP RUNTIME ENDPOINTS"
echo "================================"

# Test 2: MCP Server Endpoint (experimental)
test_mcp_endpoint "MCP Runtime Base" "/runtime/webhooks/mcp"

# Test 3: MCP SSE Endpoint
test_mcp_endpoint "MCP SSE Stream" "/runtime/webhooks/mcp/sse"

echo "📋 MCP TOOLS DEPLOYED (Not HTTP accessible)"
echo "==========================================="
echo "✅ hello_financi - Simple greeting tool"
echo "✅ get_stock_price - Get stock price by symbol" 
echo "✅ calculate_portfolio_value - Calculate portfolio value"
echo ""
echo "⚠️  NOTE: MCP tools are NOT accessible via /api/ endpoints!"
echo "   They use mcpToolTrigger and require MCP client connection."
echo ""

echo "🎯 Testing Complete!"
echo ""
echo "💡 MCP Server Configuration:"
echo "• Health endpoint: $FUNCTION_APP_URL/api/health"
echo "• MCP endpoint: $FUNCTION_APP_URL/runtime/webhooks/mcp"
echo "• Authentication: Function key required for MCP endpoints"
echo "• Tools: Use MCP-compatible client (Claude Desktop, etc.)"
echo ""
echo "📚 Next Steps:"
echo "• Configure MCP client to connect to this server"
echo "• Use server URL: $FUNCTION_APP_URL/runtime/webhooks/mcp"
echo "• Provide function key for authentication"