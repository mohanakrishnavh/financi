"""Financial Modeling Prep (FMP) API client for stock data."""

import requests
from typing import Dict, Any, Optional
import logging


class FMPClient:
    """Client for Financial Modeling Prep API."""
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self, api_key: str):
        """
        Initialize FMP client.
        
        Args:
            api_key: FMP API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock quote from FMP.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
        
        Returns:
            Dictionary with standardized stock quote data
        
        Raises:
            ValueError: If the request fails or returns invalid data
        """
        try:
            # FMP uses different format for Indian stocks
            # NSE: RELIANCE.NS -> RELIANCE.NSE
            # BSE: INFY.BO -> INFY.BSE
            fmp_symbol = self._convert_symbol_to_fmp(symbol)
            
            url = f"{self.BASE_URL}/quote/{fmp_symbol}"
            params = {'apikey': self.api_key}
            
            self.logger.info(f"Fetching quote for {symbol} (FMP: {fmp_symbol}) from FMP...")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # FMP returns an array with one item for a single symbol
            if not data or len(data) == 0:
                raise ValueError(f"No data returned from FMP for symbol: {symbol}")
            
            quote_data = data[0]
            
            # Check for error messages in response
            if 'Error Message' in quote_data or 'error' in quote_data:
                error_msg = quote_data.get('Error Message') or quote_data.get('error')
                raise ValueError(f"FMP API error: {error_msg}")
            
            # Standardize the response format
            return self._standardize_quote(quote_data, symbol)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"FMP request failed for {symbol}: {str(e)}")
            raise ValueError(f"FMP request failed: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            self.logger.error(f"Failed to parse FMP response for {symbol}: {str(e)}")
            raise ValueError(f"Failed to parse FMP data: {str(e)}")
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile information from FMP.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with company information
        
        Raises:
            ValueError: If the request fails or returns invalid data
        """
        try:
            fmp_symbol = self._convert_symbol_to_fmp(symbol)
            
            url = f"{self.BASE_URL}/profile/{fmp_symbol}"
            params = {'apikey': self.api_key}
            
            self.logger.info(f"Fetching profile for {symbol} from FMP...")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or len(data) == 0:
                raise ValueError(f"No profile data returned from FMP for symbol: {symbol}")
            
            profile_data = data[0]
            
            return self._standardize_profile(profile_data, symbol)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"FMP profile request failed for {symbol}: {str(e)}")
            raise ValueError(f"FMP profile request failed: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            self.logger.error(f"Failed to parse FMP profile for {symbol}: {str(e)}")
            raise ValueError(f"Failed to parse FMP profile data: {str(e)}")
    
    def _convert_symbol_to_fmp(self, symbol: str) -> str:
        """
        Convert symbol to FMP format.
        
        FMP uses:
        - US stocks: AAPL (no change)
        - Indian NSE: RELIANCE.NS -> RELIANCE.NSE
        - Indian BSE: INFY.BO -> INFY.BSE
        
        Args:
            symbol: Original symbol
        
        Returns:
            FMP-formatted symbol
        """
        symbol_upper = symbol.upper()
        
        # Convert Indian stock suffixes
        if symbol_upper.endswith('.NS'):
            return symbol_upper.replace('.NS', '.NSE')
        elif symbol_upper.endswith('.BO'):
            return symbol_upper.replace('.BO', '.BSE')
        
        return symbol_upper
    
    def _standardize_quote(self, data: Dict[str, Any], original_symbol: str) -> Dict[str, Any]:
        """
        Standardize FMP quote response to common format.
        
        Args:
            data: Raw FMP quote data
            original_symbol: Original requested symbol
        
        Returns:
            Standardized quote dictionary
        """
        return {
            'symbol': original_symbol,
            'price': data.get('price'),
            'change': data.get('change'),
            'changesPercentage': data.get('changesPercentage'),
            'dayLow': data.get('dayLow'),
            'dayHigh': data.get('dayHigh'),
            'yearLow': data.get('yearLow'),
            'yearHigh': data.get('yearHigh'),
            'marketCap': data.get('marketCap'),
            'volume': data.get('volume'),
            'avgVolume': data.get('avgVolume'),
            'open': data.get('open'),
            'previousClose': data.get('previousClose'),
            'eps': data.get('eps'),
            'pe': data.get('pe'),
            'timestamp': data.get('timestamp'),
            'name': data.get('name'),
            'exchange': data.get('exchange'),
            'data_source': 'fmp',
            'provider': 'Financial Modeling Prep'
        }
    
    def _standardize_profile(self, data: Dict[str, Any], original_symbol: str) -> Dict[str, Any]:
        """
        Standardize FMP profile response to common format.
        
        Args:
            data: Raw FMP profile data
            original_symbol: Original requested symbol
        
        Returns:
            Standardized profile dictionary
        """
        return {
            'symbol': original_symbol,
            'companyName': data.get('companyName'),
            'sector': data.get('sector'),
            'industry': data.get('industry'),
            'description': data.get('description'),
            'ceo': data.get('ceo'),
            'website': data.get('website'),
            'exchange': data.get('exchange'),
            'country': data.get('country'),
            'marketCap': data.get('mktCap'),
            'employees': data.get('fullTimeEmployees'),
            'data_source': 'fmp',
            'provider': 'Financial Modeling Prep'
        }
