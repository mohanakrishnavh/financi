#!/bin/bash

# Script to retrieve Azure Function keys
# Usage: ./get-function-keys.sh

RESOURCE_GROUP="rg-financi"
FUNCTION_APP_NAME="financi"

echo "🔑 Retrieving Azure Function keys for $FUNCTION_APP_NAME"
echo "=================================================="

# Check if function app exists
if ! az functionapp show --name "$FUNCTION_APP_NAME" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
    echo "❌ Function app '$FUNCTION_APP_NAME' not found in resource group '$RESOURCE_GROUP'"
    echo "💡 Make sure the function app is deployed and the names are correct"
    exit 1
fi

echo "✅ Function app found!"
echo ""

# Get the default host key (works for all functions)
echo "🔐 Default Host Key (recommended for testing):"
echo "============================================"
DEFAULT_KEY=$(az functionapp keys list \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "functionKeys.default" \
    --output tsv 2>/dev/null)

if [ -n "$DEFAULT_KEY" ]; then
    echo "Key: $DEFAULT_KEY"
    echo ""
    echo "📝 Usage example:"
    echo "curl -H \"x-functions-key: $DEFAULT_KEY\" \\"
    echo "     \"https://$FUNCTION_APP_NAME.azurewebsites.net/api/get_stock_price\""
    echo ""
else
    echo "⚠️  Could not retrieve default key. Trying alternative method..."
    
    # Alternative: Get master key (higher privilege)
    MASTER_KEY=$(az functionapp keys list \
        --name "$FUNCTION_APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "masterKey" \
        --output tsv 2>/dev/null)
    
    if [ -n "$MASTER_KEY" ]; then
        echo "🔓 Master Key (use with caution):"
        echo "Key: $MASTER_KEY"
        echo ""
    else
        echo "❌ Unable to retrieve function keys"
        echo "💡 Try accessing via Azure Portal: Functions → App Keys"
    fi
fi

# List all available keys
echo "📋 All Available Keys:"
echo "===================="
az functionapp keys list \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --output table 2>/dev/null || echo "❌ Could not list all keys"

echo ""
echo "🌐 Function App URL: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "📊 Health Check: https://$FUNCTION_APP_NAME.azurewebsites.net/api/health"
echo ""
echo "🛡️  Security Note: Keep these keys secure and don't commit them to git!"