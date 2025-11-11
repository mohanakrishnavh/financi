"""
HTTP Wrappers for MCP Tools
============================
These HTTP endpoints make the MCP tool handlers accessible via standard HTTP requests.
Each endpoint wraps an existing handler function and provides RESTful access.
"""

import json
import logging
from types import SimpleNamespace
import azure.functions as func

# Import existing handlers
from handlers.stock_handlers import (
    handle_get_stock_price,
    handle_calculate_portfolio_value,
    handle_eight_pillar_stock_analysis
)
from handlers.financial_calculators import (
    handle_compound_interest_calculator,
    handle_retirement_calculator
)


def create_http_wrappers(app: func.FunctionApp):
    """
    Register HTTP wrapper functions for all MCP tools.
    Call this function from function_app.py after creating the FunctionApp instance.
    """
    
    # ============================================================================
    # STOCK TOOLS HTTP ENDPOINTS
    # ============================================================================
    
    @app.route(route="stock/price", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])
    def get_stock_price_http(req: func.HttpRequest) -> func.HttpResponse:
        """
        HTTP endpoint for get_stock_price tool
        
        GET  /api/stock/price?symbol=AAPL
        POST /api/stock/price {"symbol": "AAPL"}
        """
        try:
            # Parse parameters
            req_body = {}
            try:
                req_body = req.get_json()
            except:
                pass
            
            symbol = req.params.get('symbol') or req_body.get('symbol')
            
            if not symbol:
                return func.HttpResponse(
                    json.dumps({"error": "Missing required parameter: symbol"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Create context object
            context = SimpleNamespace(symbol=symbol)
            
            # Call existing handler
            result = handle_get_stock_price(context)
            
            return func.HttpResponse(
                result,
                mimetype="application/json",
                status_code=200
            )
            
        except Exception as e:
            logging.error(f"Error in get_stock_price_http: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=500
            )
    
    
    @app.route(route="stock/portfolio", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])
    def calculate_portfolio_value_http(req: func.HttpRequest) -> func.HttpResponse:
        """
        HTTP endpoint for calculate_portfolio_value tool
        
        GET  /api/stock/portfolio?symbol=MSFT&amount=10
        POST /api/stock/portfolio {"symbol": "MSFT", "amount": 10}
        """
        try:
            # Parse parameters
            req_body = {}
            try:
                req_body = req.get_json()
            except:
                pass
            
            symbol = req.params.get('symbol') or req_body.get('symbol')
            amount_str = req.params.get('amount') or req_body.get('amount')
            
            if not symbol:
                return func.HttpResponse(
                    json.dumps({"error": "Missing required parameter: symbol"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            if not amount_str:
                return func.HttpResponse(
                    json.dumps({"error": "Missing required parameter: amount"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            try:
                amount = float(amount_str)
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid amount value, must be a number"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Create context object
            context = SimpleNamespace(symbol=symbol, amount=amount)
            
            # Call existing handler
            result = handle_calculate_portfolio_value(context)
            
            return func.HttpResponse(
                result,
                mimetype="application/json",
                status_code=200
            )
            
        except Exception as e:
            logging.error(f"Error in calculate_portfolio_value_http: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=500
            )
    
    
    @app.route(route="stock/eight-pillar", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])
    def eight_pillar_stock_analysis_http(req: func.HttpRequest) -> func.HttpResponse:
        """
        HTTP endpoint for eight_pillar_stock_analysis tool
        
        GET  /api/stock/eight-pillar?symbol=AAPL
        POST /api/stock/eight-pillar {"symbol": "AAPL"}
        """
        try:
            # Parse parameters
            req_body = {}
            try:
                req_body = req.get_json()
            except:
                pass
            
            symbol = req.params.get('symbol') or req_body.get('symbol')
            
            if not symbol:
                return func.HttpResponse(
                    json.dumps({"error": "Missing required parameter: symbol"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Create context object
            context = SimpleNamespace(symbol=symbol)
            
            # Call existing handler
            result = handle_eight_pillar_stock_analysis(context)
            
            return func.HttpResponse(
                result,
                mimetype="application/json",
                status_code=200
            )
            
        except Exception as e:
            logging.error(f"Error in eight_pillar_stock_analysis_http: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=500
            )
    
    
    # ============================================================================
    # FINANCIAL CALCULATOR TOOLS HTTP ENDPOINTS
    # ============================================================================
    
    @app.route(route="calculator/compound-interest", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])
    def compound_interest_calculator_http(req: func.HttpRequest) -> func.HttpResponse:
        """
        HTTP endpoint for compound_interest_calculator tool
        
        GET  /api/calculator/compound-interest?principal=10000&rate=7&time=20&frequency=monthly
        POST /api/calculator/compound-interest {"principal": 10000, "rate": 7, "time": 20, "frequency": "monthly"}
        """
        try:
            # Parse parameters
            req_body = {}
            try:
                req_body = req.get_json()
            except:
                pass
            
            principal_str = req.params.get('principal') or req_body.get('principal')
            rate_str = req.params.get('rate') or req_body.get('rate')
            time_str = req.params.get('time') or req_body.get('time')
            frequency = req.params.get('frequency') or req_body.get('frequency')
            
            # Validate required parameters
            if not all([principal_str, rate_str, time_str, frequency]):
                return func.HttpResponse(
                    json.dumps({"error": "Missing required parameters. Required: principal, rate, time, frequency"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Convert to correct types
            try:
                principal = float(principal_str)
                rate = float(rate_str)
                time = float(time_str)
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid numeric values for principal, rate, or time"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Validate frequency
            valid_frequencies = ['annually', 'semi-annually', 'quarterly', 'monthly', 'daily']
            if frequency not in valid_frequencies:
                return func.HttpResponse(
                    json.dumps({"error": f"Invalid frequency. Must be one of: {', '.join(valid_frequencies)}"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Create context object
            context = SimpleNamespace(
                principal=principal,
                rate=rate,
                time=time,
                frequency=frequency
            )
            
            # Call existing handler
            result = handle_compound_interest_calculator(context)
            
            return func.HttpResponse(
                result,
                mimetype="application/json",
                status_code=200
            )
            
        except Exception as e:
            logging.error(f"Error in compound_interest_calculator_http: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=500
            )
    
    
    @app.route(route="calculator/retirement", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])
    def retirement_calculator_http(req: func.HttpRequest) -> func.HttpResponse:
        """
        HTTP endpoint for retirement_calculator tool
        
        GET  /api/calculator/retirement?current_age=30&retirement_age=65&current_savings=50000&monthly_contribution=500&annual_return=7
        POST /api/calculator/retirement {"current_age": 30, "retirement_age": 65, ...}
        """
        try:
            # Parse parameters
            req_body = {}
            try:
                req_body = req.get_json()
            except:
                pass
            
            current_age_str = req.params.get('current_age') or req_body.get('current_age')
            retirement_age_str = req.params.get('retirement_age') or req_body.get('retirement_age')
            current_savings_str = req.params.get('current_savings') or req_body.get('current_savings')
            monthly_contribution_str = req.params.get('monthly_contribution') or req_body.get('monthly_contribution')
            annual_return_str = req.params.get('annual_return') or req_body.get('annual_return')
            
            # Validate required parameters
            if not all([current_age_str, retirement_age_str, current_savings_str, 
                       monthly_contribution_str, annual_return_str]):
                return func.HttpResponse(
                    json.dumps({
                        "error": "Missing required parameters",
                        "required": ["current_age", "retirement_age", "current_savings", 
                                   "monthly_contribution", "annual_return"]
                    }),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Convert to correct types
            try:
                current_age = int(current_age_str)
                retirement_age = int(retirement_age_str)
                current_savings = float(current_savings_str)
                monthly_contribution = float(monthly_contribution_str)
                annual_return = float(annual_return_str)
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid numeric values for one or more parameters"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Validate logic
            if current_age >= retirement_age:
                return func.HttpResponse(
                    json.dumps({"error": "Current age must be less than retirement age"}),
                    mimetype="application/json",
                    status_code=400
                )
            
            # Create context object
            context = SimpleNamespace(
                current_age=current_age,
                retirement_age=retirement_age,
                current_savings=current_savings,
                monthly_contribution=monthly_contribution,
                annual_return=annual_return
            )
            
            # Call existing handler
            result = handle_retirement_calculator(context)
            
            return func.HttpResponse(
                result,
                mimetype="application/json",
                status_code=200
            )
            
        except Exception as e:
            logging.error(f"Error in retirement_calculator_http: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=500
            )
    
    logging.info("HTTP wrappers registered successfully")
