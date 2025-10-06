# Financi MCP Server Configuration Guide

## Overview

The Financi MCP Server is deployed as an Azure Function App using Microsoft's experimental Model Context Protocol (MCP) support. It provides financial data tools that can be accessed by MCP-compatible clients.

## Server Information

- **Server URL**: `https://financi.azurewebsites.net`
- **Health Check**: `https://financi.azurewebsites.net/api/health`
- **Authentication**: Function key required
- **Protocol**: Model Context Protocol (MCP)

## Available Tools

### 1. hello_financi
- **Description**: Simple greeting from the Financi MCP server
- **Parameters**: None
- **Returns**: Greeting message

### 2. get_stock_price
- **Description**: Get current stock price for a given symbol
- **Parameters**:
  - `symbol` (string): Stock symbol (e.g., "AAPL", "MSFT")
- **Returns**: Stock price information with current price, change, and timestamp

### 3. calculate_portfolio_value
- **Description**: Calculate the total value of shares for a given stock
- **Parameters**:
  - `symbol` (string): Stock symbol
  - `amount` (number): Number of shares
- **Returns**: Portfolio calculation with total value

## Configuration for MCP Clients

### Claude Desktop Configuration

Add this to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "financi": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-fetch",
        "https://financi.azurewebsites.net"
      ],
      "env": {
        "FINANCI_API_KEY": "your-function-key-here"
      }
    }
  }
}
```

### Function Keys

To get your function key:

1. Run the included script:
   ```bash
   ./get-function-keys.sh
   ```

2. Or retrieve manually from Azure:
   ```bash
   az functionapp keys list --name financi --resource-group rg-financi
   ```

The key will be saved in `.env.local` (not committed to git).

### Testing the Server

1. **Health Check** (no authentication required):
   ```bash
   curl https://financi.azurewebsites.net/api/health
   ```

2. **Run Test Script**:
   ```bash
   ./test-functions.sh
   ```

## Important Notes

### ⚠️ Experimental Feature

This MCP server uses `Microsoft.Azure.Functions.ExtensionBundle.Experimental` which includes experimental Model Context Protocol support. The features may:

- Have limited functionality
- Change without notice
- Not be production-ready
- Require specific MCP client implementations

### Authentication

All MCP tools require function key authentication. The health endpoint is publicly accessible for monitoring.

### Tool Access

MCP tools are **NOT** accessible via standard HTTP `/api/` endpoints. They use the `mcpToolTrigger` and are designed to be accessed by MCP-compatible clients through the MCP protocol.

### Current Limitations

As of the current experimental implementation:
- Direct MCP runtime endpoints (`/runtime/webhooks/mcp`) may not be fully functional
- Tools are deployed and working but may require specific MCP client configurations
- Some MCP protocol features may be limited or unavailable

## Troubleshooting

### Common Issues

1. **404 Errors**: MCP tools return 404 when accessed via `/api/` - this is expected behavior
2. **403 Errors**: Missing or invalid function key
3. **Connection Issues**: Ensure MCP client supports Azure Functions MCP integration

### Getting Help

1. Check the health endpoint to verify server status
2. Verify function keys are current and valid
3. Ensure MCP client configuration matches server requirements
4. Check Azure Function App logs for detailed error information

## Example Usage (Conceptual)

When properly configured with an MCP client:

```
User: "What's the current price of Apple stock?"
MCP Client → Financi Server: get_stock_price(symbol="AAPL")
Financi Server → MCP Client: {"symbol":"AAPL","price":150.25,"currency":"USD",...}
MCP Client → User: "Apple (AAPL) is currently trading at $150.25"
```

## Development

To modify or extend the MCP server:

1. Edit `src/function_app.py` to add new tools
2. Deploy using the Azure DevOps pipeline
3. Test using `./test-functions.sh`
4. Update this documentation as needed

## Security

- Function keys provide authentication
- Keys are stored securely in `.env.local` (gitignored)
- Health endpoint is publicly accessible (no sensitive data)
- All tool operations are logged for auditing