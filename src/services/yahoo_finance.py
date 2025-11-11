"""Yahoo Finance data provider implementation (refactored from existing code)."""

import yfinance as yf
from datetime import datetime
from typing import Dict, Any


class YahooFinanceClient:
    """Client for Yahoo Finance data."""
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a stock symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
        
        Returns:
            Dictionary with stock quote data
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or 'regularMarketPrice' not in info:
                # Try getting current price from history
                hist = ticker.history(period='1d')
                if hist.empty:
                    raise ValueError(f"No data found for symbol: {symbol}")
                
                current_price = float(hist['Close'].iloc[-1])
                previous_close = float(hist['Open'].iloc[-1])
            else:
                current_price = info.get('regularMarketPrice') or info.get('currentPrice', 0)
                previous_close = info.get('previousClose', 0)
            
            # Calculate change
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close > 0 else 0
            
            result = {
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'change_percent': f"{change_percent:+.2f}%",
                'previous_close': previous_close,
                'open': info.get('regularMarketOpen', info.get('open', 0)),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'company_name': info.get('longName', info.get('shortName', symbol)),
                'currency': info.get('currency', 'USD'),
                'data_source': 'yahoo_finance',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'status': 'success'
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"Failed to get quote from Yahoo Finance: {str(e)}")
    
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """Get company information from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'forward_pe': info.get('forwardPE', 'N/A'),
                'peg_ratio': info.get('pegRatio', 'N/A'),
                'book_value': info.get('bookValue', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'eps': info.get('trailingEps', 'N/A'),
                'data_source': 'yahoo_finance'
            }
            
        except Exception as e:
            raise ValueError(f"Failed to get company info from Yahoo Finance: {str(e)}")
