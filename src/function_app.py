"""
Financi MCP Server - Azure Functions Application
Main entry point for the Model Context Protocol (MCP) server providing financial tools.
"""

import json
import logging
from datetime import datetime

import azure.functions as func

# Import tool properties
from models.tool_properties import (
    STOCK_PRICE_JSON,
    PORTFOLIO_JSON,
    EIGHT_PILLAR_JSON,
    COMPOUND_INTEREST_JSON,
    RETIREMENT_CALCULATOR_JSON
)

# Import handlers
from handlers.stock_handlers import (
    handle_get_stock_price,
    handle_calculate_portfolio_value,
    handle_eight_pillar_stock_analysis
)
from handlers.financial_calculators import (
    handle_compound_interest_calculator,
    handle_retirement_calculator
)

# Initialize Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Import and register HTTP wrappers
from http_wrappers import create_http_wrappers


# ============================================================================
# BASIC TOOLS
# ============================================================================

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


# ============================================================================
# STOCK TOOLS
# ============================================================================

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="get_stock_price",
    description="Get current stock price for a given symbol.",
    toolProperties=STOCK_PRICE_JSON,
)
def get_stock_price(context) -> str:
    """
    Retrieves the current stock price for a given symbol.
    Implementation delegated to handlers.stock_handlers.
    """
    return handle_get_stock_price(context)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="calculate_portfolio_value",
    description="Calculate the value of shares for a given stock.",
    toolProperties=PORTFOLIO_JSON,
)
def calculate_portfolio_value(context) -> str:
    """
    Calculates the total value of shares for a given stock.
    Implementation delegated to handlers.stock_handlers.
    """
    return handle_calculate_portfolio_value(context)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="eight_pillar_stock_analysis",
    description="Perform comprehensive Eight Pillar Stock Analysis to evaluate investment quality based on PE ratio, ROIC, shares outstanding, cash flow, net income, revenue growth, liabilities, and price-to-free-cash-flow.",
    toolProperties=EIGHT_PILLAR_JSON,
)
def eight_pillar_stock_analysis(context) -> str:
    """
    Performs Eight Pillar Stock Analysis on a given stock symbol.
    Implementation delegated to handlers.stock_handlers.
    """
    return handle_eight_pillar_stock_analysis(context)


# ============================================================================
# FINANCIAL CALCULATOR TOOLS
# ============================================================================

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="compound_interest_calculator",
    description="Calculate compound interest for an investment with customizable compounding frequency.",
    toolProperties=COMPOUND_INTEREST_JSON,
)
def compound_interest_calculator(context) -> str:
    """
    Calculates compound interest for an investment.
    Implementation delegated to handlers.financial_calculators.
    """
    return handle_compound_interest_calculator(context)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="retirement_calculator",
    description="Calculate retirement savings projection based on current age, retirement age, savings, contributions, and expected returns.",
    toolProperties=RETIREMENT_CALCULATOR_JSON,
)
def retirement_calculator(context) -> str:
    """
    Calculates retirement savings projection with detailed year-by-year breakdown.
    Implementation delegated to handlers.financial_calculators.
    """
    return handle_retirement_calculator(context)


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint for monitoring"""
    logging.info('Health check requested.')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "financi-mcp",
            "version": "1.3.0",
            "mcp_endpoint": "/runtime/webhooks/mcp/sse",
            "http_endpoints": {
                "stock_price": "/api/stock/price",
                "portfolio_value": "/api/stock/portfolio",
                "eight_pillar_analysis": "/api/stock/eight-pillar",
                "compound_interest": "/api/calculator/compound-interest",
                "retirement_calculator": "/api/calculator/retirement"
            },
            "tools": [
                "hello_financi",
                "get_stock_price",
                "calculate_portfolio_value",
                "eight_pillar_stock_analysis",
                "compound_interest_calculator",
                "retirement_calculator"
            ]
        }),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )


# ============================================================================
# HTTP WRAPPERS FOR MCP TOOLS
# ============================================================================
# Register HTTP endpoints that provide RESTful access to MCP tool handlers
create_http_wrappers(app)
