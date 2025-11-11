#!/bin/bash
#
# Test HTTP Endpoints - Financi MCP Server
# ========================================
# Tests all HTTP wrapper endpoints with real data
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🧪 Testing Financi HTTP Endpoints"
echo "=================================="
echo ""

# Load API key
if [ ! -f ".env.local" ]; then
    echo -e "${RED}❌ .env.local not found!${NC}"
    echo "Run ./scripts/get-function-keys.sh first"
    exit 1
fi

source .env.local

if [ -z "$DEFAULT_HOST_KEY" ]; then
    echo -e "${RED}❌ DEFAULT_HOST_KEY not set in .env.local${NC}"
    exit 1
fi

BASE_URL="https://financi.azurewebsites.net"
KEY="$DEFAULT_HOST_KEY"

echo -e "${BLUE}Server:${NC} $BASE_URL"
echo -e "${BLUE}Key:${NC} ${KEY:0:20}..."
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test an endpoint
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local params="$3"
    
    echo -e "${YELLOW}Testing:${NC} $name"
    echo -e "${BLUE}Endpoint:${NC} $endpoint"
    
    local url="${BASE_URL}${endpoint}?code=${KEY}&${params}"
    
    # Make request
    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Status: 200 OK${NC}"
        echo "Response preview:"
        echo "$body" | head -c 200
        echo "..."
        echo ""
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ Status: $http_code${NC}"
        echo "Response: $body"
        echo ""
        ((TESTS_FAILED++))
    fi
}

# ============================================================================
# RUN TESTS
# ============================================================================

echo "📊 Stock Price Endpoints"
echo "------------------------"
test_endpoint "Get Stock Price (AAPL)" "/api/stock/price" "symbol=AAPL"
test_endpoint "Get Stock Price (MSFT)" "/api/stock/price" "symbol=MSFT"
echo ""

echo "💰 Portfolio Endpoints"
echo "----------------------"
test_endpoint "Portfolio Value (AAPL x 50)" "/api/stock/portfolio" "symbol=AAPL&amount=50"
test_endpoint "Portfolio Value (TSLA x 10)" "/api/stock/portfolio" "symbol=TSLA&amount=10"
echo ""

echo "📈 Stock Analysis Endpoints"
echo "---------------------------"
test_endpoint "Eight Pillar Analysis (MSFT)" "/api/stock/eight-pillar" "symbol=MSFT"
test_endpoint "Eight Pillar Analysis (GOOGL)" "/api/stock/eight-pillar" "symbol=GOOGL"
echo ""

echo "🧮 Calculator Endpoints"
echo "-----------------------"
test_endpoint "Compound Interest" "/api/calculator/compound-interest" "principal=10000&rate=7&time=20&frequency=monthly"
test_endpoint "Retirement Calculator" "/api/calculator/retirement" "current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "=================================="
echo "🎯 Test Results"
echo "=================================="
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "✅ HTTP endpoints are working with real data"
    echo "✅ Ready to use from any HTTP client"
    echo "✅ Can be integrated into local MCP bridge"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed${NC}"
    echo ""
    echo "Check that:"
    echo "  1. Functions are deployed to Azure"
    echo "  2. API key is valid"
    echo "  3. Internet connection is working"
    exit 1
fi
