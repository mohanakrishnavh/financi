"""
Unit tests for Financi MCP Server
"""

import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from function_app import FinanciMCPServer

class TestFinanciMCPServer:
    """Test suite for Financi MCP Server."""
    
    @pytest.fixture
    def mcp_server(self):
        """Create MCP server instance for testing."""
        return FinanciMCPServer()
    
    def test_server_initialization(self, mcp_server):
        """Test that server initializes correctly."""
        assert mcp_server.server.name == "financi"
        assert hasattr(mcp_server, 'server')
    
    @pytest.mark.asyncio
    async def test_get_stock_price_success(self, mcp_server):
        """Test successful stock price retrieval."""
        mock_response_data = {
            "Global Quote": {
                "01. symbol": "AAPL",
                "05. price": "150.00",
                "09. change": "2.50",
                "10. change percent": "+1.69%",
                "06. volume": "1000000",
                "07. latest trading day": "2024-01-01",
                "08. previous close": "147.50"
            }
        }
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_get.return_value.__aenter__.return_value = mock_response
            
            with patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'}):
                result = await mcp_server._get_stock_price("AAPL")
                
                assert result["symbol"] == "AAPL"
                assert result["price"] == 150.00
                assert result["change"] == 2.50
    
    @pytest.mark.asyncio
    async def test_get_stock_price_no_api_key(self, mcp_server):
        """Test stock price retrieval without API key."""
        with patch.dict(os.environ, {}, clear=True):
            result = await mcp_server._get_stock_price("AAPL")
            
            assert "error" in result
            assert "API key not configured" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_crypto_price_success(self, mcp_server):
        """Test successful crypto price retrieval."""
        mock_response_data = {
            "bitcoin": {
                "usd": 45000.00,
                "usd_24h_change": 2.5,
                "usd_24h_vol": 25000000000,
                "usd_market_cap": 850000000000
            }
        }
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await mcp_server._get_crypto_price("bitcoin")
            
            assert result["symbol"] == "BITCOIN"
            assert result["price"] == 45000.00
            assert result["change_24h"] == 2.5
    
    def test_calculate_rsi(self, mcp_server):
        """Test RSI calculation."""
        # Sample price data for RSI calculation
        prices = [100, 102, 101, 103, 102, 105, 104, 106, 105, 107, 106, 108, 107, 109, 108]
        
        rsi = mcp_server._calculate_rsi(prices, 14)
        
        assert rsi is not None
        assert 0 <= rsi <= 100
        assert isinstance(rsi, float)
    
    def test_calculate_sma(self, mcp_server):
        """Test Simple Moving Average calculation."""
        prices = [100, 102, 101, 103, 102, 105, 104, 106, 105, 107]
        
        sma_5 = mcp_server._calculate_sma(prices, 5)
        
        assert sma_5 is not None
        assert sma_5 == sum(prices[-5:]) / 5
    
    def test_calculate_ema(self, mcp_server):
        """Test Exponential Moving Average calculation."""
        prices = [100, 102, 101, 103, 102, 105, 104, 106, 105, 107]
        
        ema = mcp_server._calculate_ema(prices, 5)
        
        assert ema is not None
        assert isinstance(ema, float)
    
    @pytest.mark.asyncio
    async def test_portfolio_analysis_mixed(self, mcp_server):
        """Test portfolio analysis with mixed assets."""
        holdings = [
            {"symbol": "AAPL", "quantity": 10, "type": "stock"},
            {"symbol": "bitcoin", "quantity": 0.5, "type": "crypto"}
        ]
        
        stock_mock_data = {
            "symbol": "AAPL",
            "price": 150.00,
            "change_percent": "+1.69%"
        }
        
        crypto_mock_data = {
            "symbol": "BITCOIN",
            "price": 45000.00,
            "change_24h": 2.5
        }
        
        with patch.object(mcp_server, '_get_stock_price', return_value=stock_mock_data) as mock_stock, \
             patch.object(mcp_server, '_get_crypto_price', return_value=crypto_mock_data) as mock_crypto:
            
            result = await mcp_server._portfolio_analysis(holdings)
            
            assert "total_value" in result
            assert "holdings" in result
            assert "diversification" in result
            assert len(result["holdings"]) == 2
            
            # Check that both methods were called
            mock_stock.assert_called_once_with("AAPL")
            mock_crypto.assert_called_once_with("bitcoin")

class TestHealthCheck:
    """Test health check functionality."""
    
    def test_health_endpoint_structure(self):
        """Test that health check returns proper structure."""
        # This would test the actual HTTP function, but we need a mock Azure Functions context
        # For now, just test the basic functionality
        from function_app import health_check
        
        # Create a mock request
        mock_req = MagicMock()
        
        response = health_check(mock_req)
        
        assert response.status_code == 200
        assert response.mimetype == "application/json"
        
        # Parse the JSON response
        response_data = json.loads(response.get_body())
        assert "status" in response_data
        assert response_data["status"] == "healthy"
        assert "server" in response_data
        assert "version" in response_data