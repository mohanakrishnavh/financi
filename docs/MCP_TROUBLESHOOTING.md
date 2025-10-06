# MCP Server Troubleshooting Guide

## Issue Diagnosis

Your MCP client (VS Code) isn't able to pull tools from the financi MCP server due to several technical challenges with Azure Functions' experimental MCP support.

## Root Cause Analysis

### 1. **Azure Functions Experimental MCP Limitations**
- Azure Functions uses `mcpToolTrigger` which is experimental
- The `/runtime/webhooks/mcp/sse` endpoint returns 403 Forbidden
- This suggests the experimental MCP runtime isn't designed for direct HTTP access
- Standard MCP clients (like VS Code) expect standard MCP protocol over HTTP or stdio

### 2. **Authentication Issues**
```bash
# Both header and query parameter authentication failed:
curl -H "x-functions-key: KEY" https://financi.azurewebsites.net/runtime/webhooks/mcp/sse
# Returns: 403 Forbidden

curl "https://financi.azurewebsites.net/runtime/webhooks/mcp/sse?code=KEY"
# Returns: 403 Forbidden
```

### 3. **Missing MCP Server Package**
- `@modelcontextprotocol/server-fetch` doesn't exist in npm registry
- No standard bridge exists between Azure Functions experimental MCP and standard MCP clients

## Current Status

✅ **Working:**
- Health endpoint: `https://financi.azurewebsites.net/api/health`
- Azure Functions deployment
- Function keys and authentication for regular HTTP endpoints

❌ **Not Working:**
- Direct MCP endpoint access via HTTP
- Standard MCP client integration
- Tool discovery via VS Code MCP client

## Solutions Implemented

### Solution 1: MCP Bridge Server (Recommended)
Created a Node.js bridge server that:
- Implements standard MCP protocol
- Acts as proxy to Azure Functions
- Provides mock data while Azure Functions MCP support matures

**Configuration:**
```json
"financi": {
    "type": "stdio",
    "command": "node",
    "args": ["/Users/mohanakrishnavh/Repos/financi/mcp-bridge-server.js"],
    "env": {
        "FINANCI_API_KEY": "your-key-here"
    }
}
```

### Solution 2: Direct HTTP (Currently Not Working)
The attempted HTTP configuration:
```json
"financi": {
    "type": "http", 
    "url": "https://financi.azurewebsites.net/runtime/webhooks/mcp/sse",
    "headers": {
        "x-functions-key": "your-key-here"
    }
}
```
**Status:** Returns 403 Forbidden - Azure experimental MCP not ready for standard clients

## Recommendations

### Immediate Actions
1. **Use Bridge Server**: The stdio bridge server provides immediate functionality
2. **Restart VS Code**: After config changes, restart to reload MCP servers
3. **Test Tools**: Try using the tools in GitHub Copilot Chat

### Long-term Solutions
1. **Monitor Azure Updates**: Watch for stable MCP support in Azure Functions
2. **Alternative Deployment**: Consider deploying as standard HTTP MCP server
3. **Custom Client**: Develop custom client for Azure experimental MCP

## Testing the Configuration

1. **Restart VS Code** after updating mcp.json
2. **Check MCP Status** in VS Code output logs
3. **Test in Copilot Chat**:
   ```
   Use the hello_financi tool to greet me
   Use the get_stock_price tool to get Apple's stock price
   Use the calculate_portfolio_value tool for 10 shares of MSFT
   ```

## Next Steps

The bridge server is now configured and should work with VS Code's MCP client. The tools will return mock data until we can either:
- Access the real Azure Functions MCP endpoints
- Implement HTTP wrapper functions that call the existing Azure Functions

Would you like me to create HTTP wrapper functions as an alternative approach?