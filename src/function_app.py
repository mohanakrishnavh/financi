import json
import logging
from datetime import datetime
from typing import Dict, Optional

import azure.functions as func
import yfinance as yf
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Constants for tool properties
_SYMBOL_PROPERTY_NAME = "symbol"
_AMOUNT_PROPERTY_NAME = "amount"

class ToolProperty:
    def __init__(self, property_name: str, property_type: str, description: str):
        self.propertyName = property_name
        self.propertyType = property_type
        self.description = description

    def to_dict(self):
        return {
            "propertyName": self.propertyName,
            "propertyType": self.propertyType,
            "description": self.description,
        }

# Define tool properties for different MCP tools
tool_properties_get_stock_price = [
    ToolProperty(_SYMBOL_PROPERTY_NAME, "string", "The stock symbol to get the price for (e.g., AAPL, MSFT).")
]

tool_properties_calculate_portfolio = [
    ToolProperty(_SYMBOL_PROPERTY_NAME, "string", "The stock symbol."),
    ToolProperty(_AMOUNT_PROPERTY_NAME, "number", "The number of shares.")
]

# Convert tool properties to JSON
tool_properties_get_stock_price_json = json.dumps([prop.to_dict() for prop in tool_properties_get_stock_price])
tool_properties_calculate_portfolio_json = json.dumps([prop.to_dict() for prop in tool_properties_calculate_portfolio])


def fetch_stock_price(symbol: str) -> Optional[Dict]:
    """
    Fetch real-time stock price using Yahoo Finance API.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with stock data or None if failed
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get current data
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty or not info:
            logging.warning(f"No data found for symbol: {symbol}")
            return None
            
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        
        # Calculate change
        change_value = current_price - previous_close
        change_percent = (change_value / previous_close) * 100 if previous_close != 0 else 0
        change_str = f"{change_percent:+.2f}%"
        
        return {
            "symbol": symbol.upper(),
            "price": round(float(current_price), 2),
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "change": change_str,
            "previous_close": round(float(previous_close), 2),
            "company_name": info.get('longName', 'N/A'),
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {str(e)}")
        return None


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="hello_financi",
    description="Hello world from Financi MCP server.",
    toolProperties="[]",
)
def hello_financi(context) -> str:
    """
    A simple function that returns a greeting message from the Financi MCP server.

    Args:
        context: The trigger context (not used in this function).

    Returns:
        str: A greeting message.
    """
    logging.info("Hello Financi MCP tool called")
    return "Hello! I am the Financi MCP server - your financial data assistant!"


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="get_stock_price",
    description="Get current stock price for a given symbol.",
    toolProperties=tool_properties_get_stock_price_json,
)
def get_stock_price(context) -> str:
    """
    Retrieves the current stock price for a given symbol.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The stock price information or an error message.
    """
    try:
        content = json.loads(context)
        symbol = content["arguments"][_SYMBOL_PROPERTY_NAME]
        
        if not symbol or not symbol.strip():
            error_result = {
                "error": "No stock symbol provided",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        # Fetch real stock price
        stock_data = fetch_stock_price(symbol.strip())
        
        if stock_data is None:
            error_result = {
                "error": f"Unable to fetch stock data for symbol: {symbol.upper()}",
                "symbol": symbol.upper(),
                "status": "error", 
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        logging.info(f"Retrieved stock price for {symbol}: ${stock_data['price']}")
        return json.dumps(stock_data, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in get_stock_price: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in get_stock_price: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="calculate_portfolio_value",
    description="Calculate the value of shares for a given stock.",
    toolProperties=tool_properties_calculate_portfolio_json,
)
def calculate_portfolio_value(context) -> str:
    """
    Calculates the total value of shares for a given stock.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The portfolio value calculation or an error message.
    """
    try:
        content = json.loads(context)
        symbol = content["arguments"][_SYMBOL_PROPERTY_NAME]
        amount = content["arguments"][_AMOUNT_PROPERTY_NAME]
        
        if not symbol or not symbol.strip():
            error_result = {
                "error": "No stock symbol provided",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if not amount or amount <= 0:
            error_result = {
                "error": "Invalid share amount provided. Must be a positive number.",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        # Fetch real stock price
        stock_data = fetch_stock_price(symbol.strip())
        
        if stock_data is None:
            error_result = {
                "error": f"Unable to fetch stock data for symbol: {symbol.upper()}",
                "symbol": symbol.upper(),
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        price_per_share = stock_data["price"]
        total_value = round(price_per_share * amount, 2)
        
        result = {
            "symbol": symbol.upper(),
            "shares": amount,
            "price_per_share": price_per_share,
            "total_value": total_value,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "company_name": stock_data.get("company_name", "N/A"),
            "current_change": stock_data.get("change", "N/A"),
            "status": "success"
        }
        
        logging.info(f"Calculated portfolio value for {amount} shares of {symbol}: ${total_value}")
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in calculate_portfolio_value: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in calculate_portfolio_value: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)


@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint for monitoring"""
    logging.info('Health check requested.')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "financi-mcp",
            "version": "1.0.0",
            "mcp_endpoint": "/runtime/webhooks/mcp/sse"
        }),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )