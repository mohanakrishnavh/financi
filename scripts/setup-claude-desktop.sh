#!/bin/bash

# Financi MCP Claude Desktop Configuration Setup
# ==============================================
# This script updates your Claude Desktop configuration to use the real Azure Functions

set -e

echo "🔧 Financi MCP Configuration Setup"
echo "=================================="

# Check if .env.local exists
if [[ ! -f .env.local ]]; then
    echo "❌ .env.local file not found!"
    echo "💡 Run ./scripts/get-function-keys.sh first to create this file"
    exit 1
fi

# Extract the API key from .env.local
API_KEY=$(grep "DEFAULT_HOST_KEY=" .env.local | cut -d'=' -f2)

if [[ -z "$API_KEY" ]]; then
    echo "❌ Could not find DEFAULT_HOST_KEY in .env.local"
    exit 1
fi

echo "✅ Found API key: ${API_KEY:0:20}..."

# Create the Claude Desktop configuration
CONFIG_DIR="$HOME/.config/claude-desktop"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Backup existing config if it exists
if [[ -f "$CONFIG_FILE" ]]; then
    echo "📋 Backing up existing configuration to claude_desktop_config.json.backup"
    cp "$CONFIG_FILE" "$CONFIG_DIR/claude_desktop_config.json.backup"
fi

# Create the new configuration
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "financi": {
      "command": "node",
      "args": [
        "$(pwd)/local-server/mcp-bridge-server.js"
      ],
      "env": {
        "FINANCI_SERVER_URL": "https://financi.azurewebsites.net",
        "FINANCI_API_KEY": "$API_KEY"
      }
    }
  }
}
EOF

echo "✅ Claude Desktop configuration created at: $CONFIG_FILE"
echo ""
echo "📋 Configuration Summary:"
echo "  • Server: https://financi.azurewebsites.net"
echo "  • Bridge Script: $(pwd)/local-server/mcp-bridge-server.js"
echo "  • API Key: ${API_KEY:0:20}..."
echo ""
echo "🎯 Next Steps:"
echo "  1. Restart Claude Desktop application"
echo "  2. The Financi MCP server will now call real Azure Functions"
echo "  3. Test with: /mcp_financi_get_stock_price AAPL"
echo ""
echo "🔐 Security Notes:"
echo "  • Your API key is stored in Claude Desktop's config"
echo "  • This gives Claude access to your Azure Functions"
echo "  • Keep your API key secure and rotate it regularly"