#!/usr/bin/env python3
"""
Financi MCP Server Test Client
=============================
A simple test client to verify MCP server functionality.
"""

import json
import os
import sys
import asyncio
import aiohttp
from typing import Dict, Any

class MCPTestClient:
    def __init__(self, server_url: str, function_key: str):
        self.server_url = server_url.rstrip('/')
        self.function_key = function_key
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_mcp_initialize(self) -> Dict[str, Any]:
        """Test MCP initialize handshake"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "financi-test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-functions-key": self.function_key
        }
        
        try:
            async with self.session.post(
                f"{self.server_url}/runtime/webhooks/mcp",
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "body": await response.text()
                }
                
                if response.status == 200:
                    try:
                        result["json"] = await response.json()
                    except:
                        pass
                
                return result
                
        except Exception as e:
            return {"error": str(e)}
    
    async def test_list_tools(self) -> Dict[str, Any]:
        """Test listing available MCP tools"""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-functions-key": self.function_key
        }
        
        try:
            async with self.session.post(
                f"{self.server_url}/runtime/webhooks/mcp",
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "body": await response.text()
                }
                
                if response.status == 200:
                    try:
                        result["json"] = await response.json()
                    except:
                        pass
                
                return result
                
        except Exception as e:
            return {"error": str(e)}
    
    async def test_call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test calling a specific MCP tool"""
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-functions-key": self.function_key
        }
        
        try:
            async with self.session.post(
                f"{self.server_url}/runtime/webhooks/mcp",
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "body": await response.text()
                }
                
                if response.status == 200:
                    try:
                        result["json"] = await response.json()
                    except:
                        pass
                
                return result
                
        except Exception as e:
            return {"error": str(e)}

def load_env():
    """Load environment variables from .env.local"""
    env_file = ".env.local"
    if not os.path.exists(env_file):
        print("❌ .env.local file not found!")
        print("💡 Run ./get-function-keys.sh first to create this file")
        return None, None
    
    function_key = None
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('DEFAULT_HOST_KEY='):
                function_key = line.split('=', 1)[1].strip().strip('"')
                break
    
    if not function_key:
        print("❌ DEFAULT_HOST_KEY not found in .env.local")
        return None, None
    
    return "https://financi.azurewebsites.net", function_key

async def main():
    print("🧪 Testing Financi MCP Server")
    print("=============================")
    
    # Load configuration
    server_url, function_key = load_env()
    if not server_url or not function_key:
        sys.exit(1)
    
    print(f"Server: {server_url}")
    print(f"Key: {function_key[:20]}...")
    print()
    
    async with MCPTestClient(server_url, function_key) as client:
        
        # Test 1: Initialize handshake
        print("🔗 Test 1: Initialize MCP Connection")
        print("===================================")
        result = await client.test_mcp_initialize()
        print(f"Status: {result.get('status_code', 'Error')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result.get('body', 'No response')[:200]}...")
        print()
        
        # Test 2: List available tools
        print("📋 Test 2: List Available Tools")
        print("===============================")
        result = await client.test_list_tools()
        print(f"Status: {result.get('status_code', 'Error')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result.get('body', 'No response')[:200]}...")
            if 'json' in result:
                try:
                    tools = result['json'].get('result', {}).get('tools', [])
                    if tools:
                        print("Available tools:")
                        for tool in tools:
                            print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
                    else:
                        print("No tools found in response")
                except:
                    print("Could not parse tools from response")
        print()
        
        # Test 3: Call hello_financi tool
        print("👋 Test 3: Call hello_financi Tool")
        print("==================================")
        result = await client.test_call_tool("hello_financi")
        print(f"Status: {result.get('status_code', 'Error')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result.get('body', 'No response')}")
        print()
        
        # Test 4: Call get_stock_price tool
        print("📈 Test 4: Call get_stock_price Tool (AAPL)")
        print("==========================================")
        result = await client.test_call_tool("get_stock_price", {"symbol": "AAPL"})
        print(f"Status: {result.get('status_code', 'Error')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result.get('body', 'No response')}")
        print()
        
        # Test 5: Call calculate_portfolio_value tool
        print("💰 Test 5: Call calculate_portfolio_value Tool")
        print("==============================================")
        result = await client.test_call_tool("calculate_portfolio_value", {"symbol": "MSFT", "amount": 10})
        print(f"Status: {result.get('status_code', 'Error')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result.get('body', 'No response')}")
        print()
    
    print("🎯 MCP Testing Complete!")
    print("========================")
    print("💡 If tests show 404 errors, the MCP runtime may not be available")
    print("   in the experimental bundle, or may require different endpoints.")

if __name__ == "__main__":
    asyncio.run(main())