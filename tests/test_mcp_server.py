"""
Unit tests for Financi MCP Server Azure Functions
"""

import pytest
import json
from unittest.mock import MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import azure.functions as func
from function_app import hello_financi, get_stock_price, calculate_portfolio_value, health

class TestMCPFunctions:
    """Test suite for MCP Azure Functions."""
    
    def test_hello_financi(self):
        """Test hello_financi function."""
        result = hello_financi(None)
        
        assert isinstance(result, str)
        assert "Hello! I am the Financi MCP server" in result
        assert "financial data assistant" in result
    
    def test_get_stock_price_valid_symbol(self):
        """Test get_stock_price with valid symbol."""
        # Create mock context with AAPL symbol
        context_data = {
            "arguments": {
                "symbol": "AAPL"
            }
        }
        context = json.dumps(context_data)
        
        result = get_stock_price(context)
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        assert result_data["symbol"] == "AAPL"
        assert "price" in result_data
        assert "currency" in result_data
        assert "timestamp" in result_data
        assert result_data["status"] == "success"
        assert isinstance(result_data["price"], (int, float))
    
    def test_get_stock_price_no_symbol(self):
        """Test get_stock_price with no symbol."""
        # Create mock context with empty symbol
        context_data = {
            "arguments": {
                "symbol": ""
            }
        }
        context = json.dumps(context_data)
        
        result = get_stock_price(context)
        
        # Parse the JSON error response
        result_data = json.loads(result)
        
        assert result_data["error"] == "No stock symbol provided"
        assert result_data["status"] == "error"
        assert "timestamp" in result_data
    
    def test_get_stock_price_invalid_context(self):
        """Test get_stock_price with invalid context."""
        context = "invalid json"
        
        result = get_stock_price(context)
        
        # Parse the JSON error response
        result_data = json.loads(result)
        
        assert result_data["error"] == "Invalid request format"
        assert result_data["status"] == "error"
        assert "timestamp" in result_data
    
    def test_calculate_portfolio_value_valid_inputs(self):
        """Test calculate_portfolio_value with valid inputs."""
        # Create mock context
        context_data = {
            "arguments": {
                "symbol": "MSFT",
                "amount": 10
            }
        }
        context = json.dumps(context_data)
        
        result = calculate_portfolio_value(context)
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        assert result_data["symbol"] == "MSFT"
        assert result_data["shares"] == 10
        assert "price_per_share" in result_data
        assert "total_value" in result_data
        assert result_data["status"] == "success"
        assert isinstance(result_data["total_value"], (int, float))
        assert result_data["total_value"] > 0
    
    def test_calculate_portfolio_value_no_symbol(self):
        """Test calculate_portfolio_value with no symbol."""
        context_data = {
            "arguments": {
                "symbol": "",
                "amount": 10
            }
        }
        context = json.dumps(context_data)
        
        result = calculate_portfolio_value(context)
        
        # Parse the JSON error response
        result_data = json.loads(result)
        
        assert result_data["error"] == "No stock symbol provided"
        assert result_data["status"] == "error"
        assert "timestamp" in result_data
    
    def test_calculate_portfolio_value_invalid_amount(self):
        """Test calculate_portfolio_value with invalid amount."""
        context_data = {
            "arguments": {
                "symbol": "GOOGL",
                "amount": 0
            }
        }
        context = json.dumps(context_data)
        
        result = calculate_portfolio_value(context)
        
        # Parse the JSON error response
        result_data = json.loads(result)
        
        assert result_data["error"] == "Invalid share amount provided. Must be a positive number."
        assert result_data["status"] == "error"
        assert "timestamp" in result_data
    
    def test_calculate_portfolio_value_negative_amount(self):
        """Test calculate_portfolio_value with negative amount."""
        context_data = {
            "arguments": {
                "symbol": "GOOGL",
                "amount": -5
            }
        }
        context = json.dumps(context_data)
        
        result = calculate_portfolio_value(context)
        
        # Parse the JSON error response
        result_data = json.loads(result)
        
        assert result_data["error"] == "Invalid share amount provided. Must be a positive number."
        assert result_data["status"] == "error"
        assert "timestamp" in result_data

class TestHealthEndpoint:
    """Test health check HTTP endpoint."""
    
    def test_health_endpoint_success(self):
        """Test health endpoint returns correct response."""
        # Create a mock HTTP request
        mock_request = MagicMock(spec=func.HttpRequest)
        
        response = health(mock_request)
        
        # Verify response structure
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 200
        
        # Parse response body
        response_data = json.loads(response.get_body())
        
        # Verify response content
        assert response_data["status"] == "healthy"
        assert "timestamp" in response_data
        assert response_data["service"] == "financi-mcp"
        assert response_data["version"] == "1.0.0"
        assert "mcp_endpoint" in response_data
    
    def test_health_endpoint_content_type(self):
        """Test health endpoint returns correct content type."""
        mock_request = MagicMock(spec=func.HttpRequest)
        
        response = health(mock_request)
        
        # Check headers
        headers = dict(response.headers) if hasattr(response, 'headers') else {}
        assert headers.get("Content-Type") == "application/json"

class TestToolProperties:
    """Test tool properties and configuration."""
    
    def test_tool_properties_import(self):
        """Test that tool properties can be imported."""
        from function_app import (
            tool_properties_get_stock_price,
            tool_properties_calculate_portfolio,
            ToolProperty
        )
        
        # Verify tool properties exist
        assert tool_properties_get_stock_price is not None
        assert tool_properties_calculate_portfolio is not None
        assert len(tool_properties_get_stock_price) > 0
        assert len(tool_properties_calculate_portfolio) > 0
    
    def test_tool_property_structure(self):
        """Test ToolProperty class structure."""
        from function_app import ToolProperty
        
        prop = ToolProperty("test_name", "string", "Test description")
        
        assert prop.propertyName == "test_name"
        assert prop.propertyType == "string"
        assert prop.description == "Test description"
        
        # Test to_dict method
        prop_dict = prop.to_dict()
        assert prop_dict["propertyName"] == "test_name"
        assert prop_dict["propertyType"] == "string"
        assert prop_dict["description"] == "Test description"

# Integration tests
class TestIntegration:
    """Integration tests for the complete function app."""
    
    def test_function_app_initialization(self):
        """Test that the function app can be imported without errors."""
        from function_app import app
        
        assert app is not None
        assert hasattr(app, 'function_name')
    
    def test_all_functions_exist(self):
        """Test that all expected functions exist and are callable."""
        from function_app import (
            hello_financi,
            get_stock_price,
            calculate_portfolio_value,
            health
        )
        
        assert callable(hello_financi)
        assert callable(get_stock_price)
        assert callable(calculate_portfolio_value)
        assert callable(health)