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
_PRINCIPAL_PROPERTY_NAME = "principal"
_RATE_PROPERTY_NAME = "rate"
_TIME_PROPERTY_NAME = "time"
_FREQUENCY_PROPERTY_NAME = "frequency"
_CURRENT_AGE_PROPERTY_NAME = "current_age"
_RETIREMENT_AGE_PROPERTY_NAME = "retirement_age"
_CURRENT_SAVINGS_PROPERTY_NAME = "current_savings"
_MONTHLY_CONTRIBUTION_PROPERTY_NAME = "monthly_contribution"
_ANNUAL_RETURN_PROPERTY_NAME = "annual_return"

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

tool_properties_compound_interest = [
    ToolProperty(_PRINCIPAL_PROPERTY_NAME, "number", "Initial investment amount in dollars."),
    ToolProperty(_RATE_PROPERTY_NAME, "number", "Annual interest rate as a percentage (e.g., 5 for 5%)."),
    ToolProperty(_TIME_PROPERTY_NAME, "number", "Investment period in years."),
    ToolProperty(_FREQUENCY_PROPERTY_NAME, "number", "Compounding frequency per year (1=annual, 4=quarterly, 12=monthly, 365=daily). Default is 12 (monthly).")
]

tool_properties_retirement_calculator = [
    ToolProperty(_CURRENT_AGE_PROPERTY_NAME, "number", "Your current age."),
    ToolProperty(_RETIREMENT_AGE_PROPERTY_NAME, "number", "Your desired retirement age."),
    ToolProperty(_CURRENT_SAVINGS_PROPERTY_NAME, "number", "Current retirement savings amount in dollars."),
    ToolProperty(_MONTHLY_CONTRIBUTION_PROPERTY_NAME, "number", "Monthly contribution amount in dollars."),
    ToolProperty(_ANNUAL_RETURN_PROPERTY_NAME, "number", "Expected annual return rate as a percentage (e.g., 7 for 7%).")
]

tool_properties_eight_pillar_analysis = [
    ToolProperty(_SYMBOL_PROPERTY_NAME, "string", "The stock symbol to analyze (e.g., AAPL, MSFT).")
]

# Convert tool properties to JSON
tool_properties_get_stock_price_json = json.dumps([prop.to_dict() for prop in tool_properties_get_stock_price])
tool_properties_calculate_portfolio_json = json.dumps([prop.to_dict() for prop in tool_properties_calculate_portfolio])
tool_properties_compound_interest_json = json.dumps([prop.to_dict() for prop in tool_properties_compound_interest])
tool_properties_retirement_calculator_json = json.dumps([prop.to_dict() for prop in tool_properties_retirement_calculator])
tool_properties_eight_pillar_analysis_json = json.dumps([prop.to_dict() for prop in tool_properties_eight_pillar_analysis])


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


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="compound_interest_calculator",
    description="Calculate compound interest for an investment with customizable compounding frequency.",
    toolProperties=tool_properties_compound_interest_json,
)
def compound_interest_calculator(context) -> str:
    """
    Calculates compound interest for an investment.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The compound interest calculation results or an error message.
    """
    try:
        content = json.loads(context)
        args = content["arguments"]
        
        principal = args.get(_PRINCIPAL_PROPERTY_NAME)
        rate = args.get(_RATE_PROPERTY_NAME)
        time = args.get(_TIME_PROPERTY_NAME)
        frequency = args.get(_FREQUENCY_PROPERTY_NAME, 12)  # Default to monthly
        
        # Validation
        if principal is None or principal <= 0:
            error_result = {
                "error": "Principal amount must be a positive number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if rate is None or rate < 0:
            error_result = {
                "error": "Interest rate must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if time is None or time <= 0:
            error_result = {
                "error": "Time period must be a positive number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if frequency not in [1, 4, 12, 365]:
            error_result = {
                "error": "Frequency must be 1 (annual), 4 (quarterly), 12 (monthly), or 365 (daily)",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        # Calculate compound interest: A = P(1 + r/n)^(nt)
        rate_decimal = rate / 100
        amount = principal * ((1 + rate_decimal / frequency) ** (frequency * time))
        interest_earned = amount - principal
        
        # Calculate year-by-year breakdown
        yearly_breakdown = []
        for year in range(1, int(time) + 1):
            year_amount = principal * ((1 + rate_decimal / frequency) ** (frequency * year))
            year_interest = year_amount - principal
            yearly_breakdown.append({
                "year": year,
                "amount": round(year_amount, 2),
                "interest_earned": round(year_interest, 2)
            })
        
        frequency_map = {1: "Annual", 4: "Quarterly", 12: "Monthly", 365: "Daily"}
        
        result = {
            "principal": round(principal, 2),
            "interest_rate": rate,
            "time_period_years": time,
            "compounding_frequency": frequency_map[frequency],
            "final_amount": round(amount, 2),
            "total_interest_earned": round(interest_earned, 2),
            "effective_annual_rate": round(((1 + rate_decimal / frequency) ** frequency - 1) * 100, 2),
            "yearly_breakdown": yearly_breakdown,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success"
        }
        
        logging.info(f"Calculated compound interest: ${amount:.2f} from ${principal} at {rate}% for {time} years")
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in compound_interest_calculator: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in compound_interest_calculator: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="retirement_calculator",
    description="Calculate retirement savings projection based on current age, retirement age, savings, contributions, and expected returns.",
    toolProperties=tool_properties_retirement_calculator_json,
)
def retirement_calculator(context) -> str:
    """
    Calculates retirement savings projection with detailed year-by-year breakdown.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The retirement calculation results or an error message.
    """
    try:
        content = json.loads(context)
        args = content["arguments"]
        
        current_age = args.get(_CURRENT_AGE_PROPERTY_NAME)
        retirement_age = args.get(_RETIREMENT_AGE_PROPERTY_NAME)
        current_savings = args.get(_CURRENT_SAVINGS_PROPERTY_NAME, 0)
        monthly_contribution = args.get(_MONTHLY_CONTRIBUTION_PROPERTY_NAME)
        annual_return = args.get(_ANNUAL_RETURN_PROPERTY_NAME)
        
        # Validation
        if current_age is None or current_age < 18 or current_age > 100:
            error_result = {
                "error": "Current age must be between 18 and 100",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if retirement_age is None or retirement_age <= current_age or retirement_age > 100:
            error_result = {
                "error": "Retirement age must be greater than current age and less than or equal to 100",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if current_savings < 0:
            error_result = {
                "error": "Current savings cannot be negative",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if monthly_contribution is None or monthly_contribution < 0:
            error_result = {
                "error": "Monthly contribution must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if annual_return is None or annual_return < 0:
            error_result = {
                "error": "Annual return must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        years_until_retirement = retirement_age - current_age
        monthly_rate = (annual_return / 100) / 12
        total_months = years_until_retirement * 12
        
        # Calculate future value
        # FV = PV(1+r)^n + PMT × [((1+r)^n - 1) / r]
        balance = current_savings
        total_contributions = current_savings
        yearly_breakdown = []
        
        for year in range(1, years_until_retirement + 1):
            year_start_balance = balance
            year_contributions = 0
            
            for month in range(12):
                # Add monthly contribution
                balance += monthly_contribution
                year_contributions += monthly_contribution
                total_contributions += monthly_contribution
                
                # Apply monthly return
                balance *= (1 + monthly_rate)
            
            year_age = current_age + year
            yearly_breakdown.append({
                "year": year,
                "age": year_age,
                "year_start_balance": round(year_start_balance, 2),
                "contributions_this_year": round(year_contributions, 2),
                "year_end_balance": round(balance, 2),
                "interest_earned_this_year": round(balance - year_start_balance - year_contributions, 2)
            })
        
        total_interest = balance - total_contributions
        
        # Calculate monthly withdrawal for 30 years in retirement (4% rule approximation)
        monthly_withdrawal_4percent = (balance * 0.04) / 12
        
        result = {
            "current_age": current_age,
            "retirement_age": retirement_age,
            "years_until_retirement": years_until_retirement,
            "current_savings": round(current_savings, 2),
            "monthly_contribution": round(monthly_contribution, 2),
            "annual_contribution": round(monthly_contribution * 12, 2),
            "annual_return_rate": annual_return,
            "projected_retirement_balance": round(balance, 2),
            "total_contributions": round(total_contributions, 2),
            "total_interest_earned": round(total_interest, 2),
            "estimated_monthly_withdrawal_4percent_rule": round(monthly_withdrawal_4percent, 2),
            "estimated_annual_withdrawal_4percent_rule": round(monthly_withdrawal_4percent * 12, 2),
            "yearly_breakdown": yearly_breakdown,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success",
            "notes": [
                "4% rule: Withdraw 4% of retirement balance annually (adjusted for inflation)",
                "Assumes consistent monthly contributions and returns",
                "Does not account for inflation, taxes, or fees",
                "Consider consulting a financial advisor for personalized planning"
            ]
        }
        
        logging.info(f"Calculated retirement: ${balance:.2f} at age {retirement_age}")
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in retirement_calculator: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in retirement_calculator: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="eight_pillar_stock_analysis",
    description="Perform comprehensive Eight Pillar Stock Analysis to evaluate investment quality based on PE ratio, ROIC, shares outstanding, cash flow, net income, revenue growth, liabilities, and price-to-free-cash-flow.",
    toolProperties=tool_properties_eight_pillar_analysis_json,
)
def eight_pillar_stock_analysis(context) -> str:
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
        symbol = content["arguments"][_SYMBOL_PROPERTY_NAME]
        
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
        
        logging.info(f"Completed Eight Pillar Analysis for {symbol}: {analysis_result['total_checks']}/8 checks")
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


def perform_eight_pillar_analysis(symbol: str) -> Optional[Dict]:
    """
    Perform comprehensive Eight Pillar Stock Analysis.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with detailed eight pillar analysis or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get financial statements
        try:
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
        except Exception as e:
            logging.error(f"Error fetching financial statements for {symbol}: {str(e)}")
            return None
        
        if financials.empty or balance_sheet.empty or cashflow.empty:
            logging.warning(f"Incomplete financial data for {symbol}")
            return None
        
        # Get current market cap
        market_cap = info.get('marketCap', 0)
        company_name = info.get('longName', symbol.upper())
        
        pillars = {}
        checks_passed = 0
        
        # PILLAR 1: Five-Year PE Ratio (< 22.5)
        try:
            # Get last 5 years of net income
            net_incomes = financials.loc['Net Income'].head(5) if 'Net Income' in financials.index else None
            if net_incomes is not None and len(net_incomes) >= 1:
                total_5yr_earnings = net_incomes.sum()
                five_year_pe = market_cap / total_5yr_earnings if total_5yr_earnings > 0 else None
                
                if five_year_pe is not None:
                    check_passed = five_year_pe < 22.5
                    checks_passed += 1 if check_passed else 0
                    pillars['pillar_1_five_year_pe_ratio'] = {
                        "value": round(five_year_pe, 2),
                        "threshold": "< 22.5",
                        "check": "✓" if check_passed else "✗",
                        "description": "Five-year PE ratio measures valuation efficiency",
                        "interpretation": "Good value" if check_passed else "Potentially overvalued"
                    }
                else:
                    pillars['pillar_1_five_year_pe_ratio'] = {
                        "value": "N/A",
                        "threshold": "< 22.5",
                        "check": "?",
                        "description": "Insufficient data for calculation"
                    }
            else:
                pillars['pillar_1_five_year_pe_ratio'] = {
                    "value": "N/A",
                    "threshold": "< 22.5", 
                    "check": "?",
                    "description": "Net income data not available"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 1 for {symbol}: {str(e)}")
            pillars['pillar_1_five_year_pe_ratio'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 2: Five-Year ROIC (Return on Invested Capital)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            total_equity = balance_sheet.loc['Stockholders Equity'].iloc[0] if 'Stockholders Equity' in balance_sheet.index else 0
            total_debt = balance_sheet.loc['Total Debt'].iloc[0] if 'Total Debt' in balance_sheet.index else 0
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                total_5yr_fcf = free_cashflows.sum()
                invested_capital = total_equity + total_debt
                
                if invested_capital > 0:
                    roic = (total_5yr_fcf / invested_capital) * 100
                    check_passed = roic > 10  # Good ROIC threshold
                    checks_passed += 1 if check_passed else 0
                    pillars['pillar_2_five_year_roic'] = {
                        "value": f"{round(roic, 2)}%",
                        "threshold": "> 10% (good)",
                        "check": "✓" if check_passed else "✗",
                        "description": "Return on Invested Capital measures capital efficiency",
                        "interpretation": "Strong capital efficiency" if check_passed else "Weak capital efficiency"
                    }
                else:
                    pillars['pillar_2_five_year_roic'] = {
                        "value": "N/A",
                        "threshold": "> 10%",
                        "check": "?",
                        "description": "Insufficient capital data"
                    }
            else:
                pillars['pillar_2_five_year_roic'] = {
                    "value": "N/A",
                    "threshold": "> 10%",
                    "check": "?",
                    "description": "Free cash flow data not available"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 2 for {symbol}: {str(e)}")
            pillars['pillar_2_five_year_roic'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 3: Shares Outstanding (decreasing is better)
        try:
            shares_outstanding = balance_sheet.loc['Ordinary Shares Number'] if 'Ordinary Shares Number' in balance_sheet.index else None
            
            if shares_outstanding is not None and len(shares_outstanding) >= 2:
                current_shares = shares_outstanding.iloc[0]
                old_shares = shares_outstanding.iloc[-1] if len(shares_outstanding) >= 5 else shares_outstanding.iloc[-1]
                
                change_pct = ((current_shares - old_shares) / old_shares) * 100
                check_passed = current_shares < old_shares
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_3_shares_outstanding'] = {
                    "current_shares": f"{current_shares:,.0f}",
                    "change_percent": f"{change_pct:+.2f}%",
                    "threshold": "Decreasing",
                    "check": "✓" if check_passed else "✗",
                    "description": "Share buybacks indicate management confidence",
                    "interpretation": "Shareholder-friendly buybacks" if check_passed else "Dilution occurring"
                }
            else:
                pillars['pillar_3_shares_outstanding'] = {
                    "value": "N/A",
                    "threshold": "Decreasing",
                    "check": "?",
                    "description": "Insufficient shares data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 3 for {symbol}: {str(e)}")
            pillars['pillar_3_shares_outstanding'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 4: Cash Flow Growth (Last 5 Years)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 2:
                latest_fcf = free_cashflows.iloc[0]
                oldest_fcf = free_cashflows.iloc[-1]
                
                check_passed = latest_fcf > oldest_fcf
                growth_pct = ((latest_fcf - oldest_fcf) / abs(oldest_fcf)) * 100 if oldest_fcf != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_4_cash_flow_growth'] = {
                    "latest_fcf": f"${latest_fcf:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Cash flow growth indicates financial health",
                    "interpretation": "Growing cash generation" if check_passed else "Declining cash generation"
                }
            else:
                pillars['pillar_4_cash_flow_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 4 for {symbol}: {str(e)}")
            pillars['pillar_4_cash_flow_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 5: Net Income Growth (Last 5 Years)
        try:
            net_incomes = financials.loc['Net Income'].head(5) if 'Net Income' in financials.index else None
            
            if net_incomes is not None and len(net_incomes) >= 2:
                latest_ni = net_incomes.iloc[0]
                oldest_ni = net_incomes.iloc[-1]
                
                check_passed = latest_ni > oldest_ni
                growth_pct = ((latest_ni - oldest_ni) / abs(oldest_ni)) * 100 if oldest_ni != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_5_net_income_growth'] = {
                    "latest_net_income": f"${latest_ni:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Net income growth shows profitability improvement",
                    "interpretation": "Growing profitability" if check_passed else "Declining profitability"
                }
            else:
                pillars['pillar_5_net_income_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient net income data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 5 for {symbol}: {str(e)}")
            pillars['pillar_5_net_income_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 6: Revenue Growth (Last 5 Years)
        try:
            revenues = financials.loc['Total Revenue'].head(5) if 'Total Revenue' in financials.index else None
            
            if revenues is not None and len(revenues) >= 2:
                latest_rev = revenues.iloc[0]
                oldest_rev = revenues.iloc[-1]
                
                check_passed = latest_rev > oldest_rev
                growth_pct = ((latest_rev - oldest_rev) / oldest_rev) * 100 if oldest_rev != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_6_revenue_growth'] = {
                    "latest_revenue": f"${latest_rev:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Revenue growth shows business expansion",
                    "interpretation": "Expanding business" if check_passed else "Contracting business"
                }
            else:
                pillars['pillar_6_revenue_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient revenue data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 6 for {symbol}: {str(e)}")
            pillars['pillar_6_revenue_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 7: Long-Term Liabilities (< 5x 5-Year Average Free Cash Flow)
        try:
            long_term_debt = balance_sheet.loc['Long Term Debt'].iloc[0] if 'Long Term Debt' in balance_sheet.index else 0
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                avg_5yr_fcf = free_cashflows.mean()
                
                if avg_5yr_fcf > 0:
                    liability_ratio = long_term_debt / avg_5yr_fcf
                    check_passed = liability_ratio < 5
                    checks_passed += 1 if check_passed else 0
                    
                    pillars['pillar_7_long_term_liabilities'] = {
                        "long_term_debt": f"${long_term_debt:,.0f}",
                        "avg_free_cash_flow": f"${avg_5yr_fcf:,.0f}",
                        "liability_ratio": f"{liability_ratio:.2f}x",
                        "threshold": "< 5x",
                        "check": "✓" if check_passed else "✗",
                        "description": "Debt coverage measures financial stability",
                        "interpretation": f"Can pay off debt in {liability_ratio:.1f} years" if check_passed else "High debt burden"
                    }
                else:
                    pillars['pillar_7_long_term_liabilities'] = {
                        "value": "N/A",
                        "threshold": "< 5x",
                        "check": "?",
                        "description": "Negative or zero free cash flow"
                    }
            else:
                pillars['pillar_7_long_term_liabilities'] = {
                    "value": "N/A",
                    "threshold": "< 5x",
                    "check": "?",
                    "description": "Insufficient free cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 7 for {symbol}: {str(e)}")
            pillars['pillar_7_long_term_liabilities'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 8: Five-Year Price-to-Free Cash Flow (< 22.5)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                total_5yr_fcf = free_cashflows.sum()
                
                if total_5yr_fcf > 0:
                    price_to_fcf = market_cap / total_5yr_fcf
                    check_passed = price_to_fcf < 22.5
                    checks_passed += 1 if check_passed else 0
                    
                    pillars['pillar_8_price_to_fcf'] = {
                        "value": round(price_to_fcf, 2),
                        "threshold": "< 22.5",
                        "check": "✓" if check_passed else "✗",
                        "description": "Price-to-FCF measures cash flow valuation",
                        "interpretation": "Reasonable valuation" if check_passed else "Potentially expensive"
                    }
                else:
                    pillars['pillar_8_price_to_fcf'] = {
                        "value": "N/A",
                        "threshold": "< 22.5",
                        "check": "?",
                        "description": "Negative free cash flow"
                    }
            else:
                pillars['pillar_8_price_to_fcf'] = {
                    "value": "N/A",
                    "threshold": "< 22.5",
                    "check": "?",
                    "description": "Insufficient free cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 8 for {symbol}: {str(e)}")
            pillars['pillar_8_price_to_fcf'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # Calculate overall score
        total_checks = sum(1 for p in pillars.values() if p.get("check") in ["✓", "✗"])
        score_percentage = (checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        # Overall assessment
        if score_percentage >= 87.5:  # 7-8 checks
            assessment = "Excellent - Strong buy candidate"
            recommendation = "Consider for investment"
        elif score_percentage >= 62.5:  # 5-6 checks
            assessment = "Good - Worth further research"
            recommendation = "Research further before investing"
        elif score_percentage >= 37.5:  # 3-4 checks
            assessment = "Fair - Proceed with caution"
            recommendation = "Significant concerns, investigate thoroughly"
        else:  # 0-2 checks
            assessment = "Poor - High risk investment"
            recommendation = "Avoid or wait for better conditions"
        
        result = {
            "symbol": symbol.upper(),
            "company_name": company_name,
            "market_cap": f"${market_cap:,.0f}",
            "analysis_date": datetime.utcnow().isoformat() + "Z",
            "pillars": pillars,
            "summary": {
                "total_checks_passed": checks_passed,
                "total_checks_evaluated": total_checks,
                "score_percentage": round(score_percentage, 1),
                "overall_assessment": assessment,
                "recommendation": recommendation
            },
            "methodology": {
                "name": "Eight Pillar Stock Analysis",
                "source": "Everything Money (everythingmoney.com)",
                "description": "Systematic evaluation of company fundamentals across 8 key financial metrics"
            },
            "disclaimer": "This analysis is for educational purposes only and should not be considered financial advice. Always do your own research and consult with a financial advisor.",
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        logging.error(f"Error performing eight pillar analysis for {symbol}: {str(e)}")
        return None


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