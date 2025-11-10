"""
Stock-related MCP handler functions.
Handles stock price queries, portfolio calculations, and eight pillar analysis.
"""

import json
import logging
from datetime import datetime

from ..models.tool_properties import SYMBOL_PROPERTY, AMOUNT_PROPERTY
from ..utils.stock_utils import fetch_stock_price, perform_eight_pillar_analysis


def handle_get_stock_price(context: str) -> str:
    """
    Retrieves the current stock price for a given symbol.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The stock price information or an error message.
    """
    try:
        content = json.loads(context)
        symbol = content["arguments"][SYMBOL_PROPERTY]
        
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


def handle_calculate_portfolio_value(context: str) -> str:
    """
    Calculates the total value of shares for a given stock.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The portfolio value calculation or an error message.
    """
    try:
        content = json.loads(context)
        symbol = content["arguments"][SYMBOL_PROPERTY]
        amount = content["arguments"][AMOUNT_PROPERTY]
        
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


def handle_eight_pillar_stock_analysis(context: str) -> str:
    """
    Performs Eight Pillar Stock Analysis on a given stock symbol.
    
    The Eight Pillars evaluate:
    1. Five-Year PE Ratio (should be < 22.5)
    2. Five-Year ROIC (Return on Invested Capital)
    3. Shares Outstanding (decreasing is better)
    4. Cash Flow Growth (last 5 years)
    5. Net Income Growth (last 5 years)
    6. Revenue Growth (last 5 years)
    7. Long-Term Liabilities (< 5x 5-year average free cash flow)
    8. Five-Year Price-to-Free Cash Flow (< 22.5)

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The eight pillar analysis results or an error message.
    """
    try:
        content = json.loads(context)
        symbol = content["arguments"][SYMBOL_PROPERTY]
        
        if not symbol or not symbol.strip():
            error_result = {
                "error": "No stock symbol provided",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        # Fetch comprehensive stock data
        analysis_result = perform_eight_pillar_analysis(symbol.strip())
        
        if analysis_result is None:
            error_result = {
                "error": f"Unable to fetch sufficient data for symbol: {symbol.upper()}",
                "symbol": symbol.upper(),
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "note": "Stock data may be incomplete or unavailable for comprehensive analysis"
            }
            return json.dumps(error_result, indent=2)
        
        logging.info(f"Completed Eight Pillar Analysis for {symbol}: {analysis_result['summary']['total_checks_passed']}/8 checks")
        return json.dumps(analysis_result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in eight_pillar_stock_analysis: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in eight_pillar_stock_analysis: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
