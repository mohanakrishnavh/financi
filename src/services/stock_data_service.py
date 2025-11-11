"""Unified stock data service with multiple data source support."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.data_sources import get_data_source_config, DataSource
from services.alpha_vantage import AlphaVantageClient
from services.yahoo_finance import YahooFinanceClient


class StockDataService:
    """Unified service for fetching stock data from multiple sources."""
    
    def __init__(self):
        self.config = get_data_source_config()
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        
        # Initialize clients
        self.alpha_vantage_client = None
        if self.config.is_alpha_vantage_enabled():
            self.alpha_vantage_client = AlphaVantageClient(
                self.config.alpha_vantage_api_key
            )
        
        self.yahoo_finance_client = YahooFinanceClient()
    
    def _get_cache_key(self, operation: str, symbol: str) -> str:
        """Generate cache key for operation and symbol."""
        return f"{operation}:{symbol}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self.cache_timestamps:
            return False
        
        age = datetime.utcnow() - self.cache_timestamps[cache_key]
        return age.total_seconds() < self.config.cache_duration
    
    def _set_cache(self, cache_key: str, data: Dict[str, Any]):
        """Store data in cache."""
        self.cache[cache_key] = data
        self.cache_timestamps[cache_key] = datetime.utcnow()
    
    def _get_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache if valid."""
        if self._is_cache_valid(cache_key):
            return self.cache.get(cache_key)
        return None
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get stock quote from configured data source with fallback.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with stock quote data
        """
        cache_key = self._get_cache_key('quote', symbol)
        
        # Check cache first
        cached_data = self._get_cache(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
        
        primary_source = self.config.get_primary_source()
        
        # Try primary source
        try:
            if primary_source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
                print(f"Fetching quote for {symbol} from Alpha Vantage...")
                data = self.alpha_vantage_client.get_quote(symbol)
                self._set_cache(cache_key, data)
                return data
            else:
                print(f"Fetching quote for {symbol} from Yahoo Finance...")
                data = self.yahoo_finance_client.get_quote(symbol)
                self._set_cache(cache_key, data)
                return data
        except Exception as e:
            print(f"⚠️  Primary source ({primary_source.value}) failed: {str(e)}")
            
            # Try fallback source
            fallback_source = self.config.get_fallback_source()
            if fallback_source and fallback_source != primary_source:
                try:
                    print(f"Attempting fallback to {fallback_source.value}...")
                    if fallback_source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
                        data = self.alpha_vantage_client.get_quote(symbol)
                        data['fallback_used'] = True
                        data['primary_source_error'] = str(e)
                        self._set_cache(cache_key, data)
                        return data
                    else:
                        data = self.yahoo_finance_client.get_quote(symbol)
                        data['fallback_used'] = True
                        data['primary_source_error'] = str(e)
                        self._set_cache(cache_key, data)
                        print(f"✅ Fallback to {fallback_source.value} successful")
                        return data
                except Exception as fallback_error:
                    print(f"❌ Fallback source ({fallback_source.value}) also failed: {str(fallback_error)}")
            
            # Both failed, raise original error
            raise
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Get company overview and fundamental data.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with company data
        """
        cache_key = self._get_cache_key('overview', symbol)
        
        # Check cache first
        cached_data = self._get_cache(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
        
        primary_source = self.config.get_primary_source()
        
        try:
            if primary_source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
                print(f"Fetching company overview for {symbol} from Alpha Vantage...")
                data = self.alpha_vantage_client.get_company_overview(symbol)
                self._set_cache(cache_key, data)
                return data
            else:
                print(f"Fetching company info for {symbol} from Yahoo Finance...")
                data = self.yahoo_finance_client.get_company_info(symbol)
                self._set_cache(cache_key, data)
                return data
        except Exception as e:
            print(f"⚠️  Primary source failed: {str(e)}")
            
            # Try fallback
            fallback_source = self.config.get_fallback_source()
            if fallback_source and fallback_source != primary_source:
                try:
                    print(f"Attempting fallback to {fallback_source.value}...")
                    if fallback_source == DataSource.YAHOO_FINANCE:
                        data = self.yahoo_finance_client.get_company_info(symbol)
                        data['fallback_used'] = True
                        data['primary_source_error'] = str(e)
                        self._set_cache(cache_key, data)
                        print(f"✅ Fallback to {fallback_source.value} successful")
                        return data
                    elif fallback_source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
                        data = self.alpha_vantage_client.get_company_overview(symbol)
                        data['fallback_used'] = True
                        data['primary_source_error'] = str(e)
                        self._set_cache(cache_key, data)
                        return data
                except Exception as fallback_error:
                    print(f"❌ Fallback also failed: {str(fallback_error)}")
            
            raise


# Global service instance
_service: Optional[StockDataService] = None


def get_stock_data_service() -> StockDataService:
    """Get or create the global stock data service instance."""
    global _service
    if _service is None:
        _service = StockDataService()
    return _service
