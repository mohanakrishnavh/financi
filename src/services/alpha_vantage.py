"""Alpha Vantage data provider implementation."""

import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional


class AlphaVantageClient:
    """Client for Alpha Vantage API."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a stock symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
        
        Returns:
            Dictionary with stock quote data
        """
        # For Indian stocks, Alpha Vantage uses different format
        av_symbol = symbol.upper()
        if '.NS' in av_symbol:
            # NSE stocks - remove .NS suffix
            av_symbol = av_symbol.replace('.NS', '.BSE')
        elif '.BO' in av_symbol:
            # BSE stocks - use .BSE suffix
            av_symbol = av_symbol.replace('.BO', '.BSE')
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': av_symbol,
            'apikey': self.api_key
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                raise ValueError(f"Alpha Vantage API error: {data['Error Message']}")
            
            if 'Note' in data:
                # Rate limit hit
                raise ValueError("Alpha Vantage rate limit exceeded (25 calls/day). Falling back to Yahoo Finance.")
            
            if 'Information' in data:
                # API limit message
                raise ValueError(f"Alpha Vantage: {data['Information']}")
            
            if 'Global Quote' not in data or not data['Global Quote']:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            quote = data['Global Quote']
            
            # Parse the response
            price = float(quote.get('05. price', 0))
            previous_close = float(quote.get('08. previous close', 0))
            change = float(quote.get('09. change', 0))
            change_percent_str = quote.get('10. change percent', '0%').rstrip('%')
            
            result = {
                'symbol': symbol,
                'price': price,
                'change': change,
                'change_percent': change_percent_str,
                'volume': int(float(quote.get('06. volume', 0))),
                'previous_close': previous_close,
                'open': float(quote.get('02. open', 0)),
                'high': float(quote.get('03. high', 0)),
                'low': float(quote.get('04. low', 0)),
                'latest_trading_day': quote.get('07. latest trading day', ''),
                'data_source': 'alpha_vantage',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'status': 'success'
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage: {str(e)}")
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Get company overview and fundamental data.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with company data
        """
        av_symbol = symbol.upper().replace('.NS', '.BSE').replace('.BO', '.BSE')
        
        params = {
            'function': 'OVERVIEW',
            'symbol': av_symbol,
            'apikey': self.api_key
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Error Message' in data:
                raise ValueError(f"Alpha Vantage API error: {data['Error Message']}")
            
            if 'Note' in data or 'Information' in data:
                raise ValueError("Alpha Vantage rate limit exceeded. Falling back to Yahoo Finance.")
            
            if not data or 'Symbol' not in data:
                raise ValueError(f"No company data found for symbol: {symbol}")
            
            return {
                'symbol': symbol,
                'name': data.get('Name', 'N/A'),
                'description': data.get('Description', 'N/A'),
                'sector': data.get('Sector', 'N/A'),
                'industry': data.get('Industry', 'N/A'),
                'market_cap': data.get('MarketCapitalization', 'N/A'),
                'pe_ratio': data.get('PERatio', 'N/A'),
                'peg_ratio': data.get('PEGRatio', 'N/A'),
                'book_value': data.get('BookValue', 'N/A'),
                'dividend_yield': data.get('DividendYield', 'N/A'),
                'eps': data.get('EPS', 'N/A'),
                'revenue_ttm': data.get('RevenueTTM', 'N/A'),
                'profit_margin': data.get('ProfitMargin', 'N/A'),
                'operating_margin': data.get('OperatingMarginTTM', 'N/A'),
                'return_on_assets': data.get('ReturnOnAssetsTTM', 'N/A'),
                'return_on_equity': data.get('ReturnOnEquityTTM', 'N/A'),
                'fifty_two_week_high': data.get('52WeekHigh', 'N/A'),
                'fifty_two_week_low': data.get('52WeekLow', 'N/A'),
                'data_source': 'alpha_vantage'
            }
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage: {str(e)}")
