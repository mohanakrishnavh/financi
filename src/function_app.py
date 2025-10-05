import json
import logging
from datetime import datetime

import azure.functions as func

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
        
        if not symbol:
            return "No stock symbol provided"
        
        # TODO: Implement real stock price API integration (e.g., Alpha Vantage, Yahoo Finance)
        # For now, return placeholder data
        result = {
            "symbol": symbol.upper(),
            "price": 150.25,  # Placeholder price
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat(),
            "change": "+2.5%",
            "status": "success"
        }
        
        logging.info(f"Retrieved stock price for {symbol}: ${result['price']}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logging.error(f"Error getting stock price: {str(e)}")
        return f"Error retrieving stock price: {str(e)}"


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
        
        if not symbol:
            return "No stock symbol provided"
        
        if not amount or amount <= 0:
            return "Invalid share amount provided"
        
        # TODO: Use real stock price from API
        # For now, use placeholder price
        price_per_share = 150.25  # Placeholder
        total_value = price_per_share * amount
        
        result = {
            "symbol": symbol.upper(),
            "shares": amount,
            "price_per_share": price_per_share,
            "total_value": total_value,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        }
        
        logging.info(f"Calculated portfolio value for {amount} shares of {symbol}: ${total_value}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logging.error(f"Error calculating portfolio value: {str(e)}")
        return f"Error calculating portfolio value: {str(e)}"


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