import azure.functions as func
import json
import logging
import os
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    logging.info('Health check requested.')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "financi-mcp",
            "version": "1.0.0"
        }),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )

@app.route(route="mcp", methods=["GET", "POST"])
def mcp_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """MCP endpoint placeholder - will implement MCP functionality later"""
    logging.info('MCP endpoint called.')
    
    if req.method == "GET":
        return func.HttpResponse(
            json.dumps({
                "message": "MCP endpoint is available",
                "methods": ["GET", "POST"],
                "status": "ready",
                "note": "MCP functionality will be implemented after resolving grpcio build issues"
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    
    elif req.method == "POST":
        try:
            req_body = req.get_json()
            if not req_body:
                return func.HttpResponse(
                    json.dumps({"error": "Request body is required"}),
                    status_code=400,
                    headers={"Content-Type": "application/json"}
                )
            
            # Placeholder for MCP functionality
            response = {
                "message": "MCP endpoint received request",
                "received": req_body,
                "status": "placeholder",
                "note": "Full MCP functionality will be implemented after resolving dependencies"
            }
            
            return func.HttpResponse(
                json.dumps(response),
                status_code=200,
                headers={"Content-Type": "application/json"}
            )
            
        except Exception as e:
            logging.error(f"Error processing MCP request: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": f"Error processing request: {str(e)}"}),
                status_code=500,
                headers={"Content-Type": "application/json"}
            )

@app.route(route="stock-price/{symbol}")
def get_stock_price(req: func.HttpRequest) -> func.HttpResponse:
    """Get stock price - placeholder implementation"""
    logging.info('Stock price endpoint called.')
    
    symbol = req.route_params.get('symbol')
    if not symbol:
        return func.HttpResponse(
            json.dumps({"error": "Stock symbol is required"}),
            status_code=400,
            headers={"Content-Type": "application/json"}
        )
    
    # Placeholder response - will implement Alpha Vantage integration
    response = {
        "symbol": symbol.upper(),
        "price": "123.45",  # Placeholder price
        "currency": "USD",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "placeholder",
        "note": "This is a placeholder response. Real stock data will be implemented."
    }
    
    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )