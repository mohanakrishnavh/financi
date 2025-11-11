"""Unified stock data service with multiple data source support."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.data_sources import get_data_source_config, DataSource
from services.fmp import FMPClient
from services.alpha_vantage import AlphaVantageClient
from services.yahoo_finance import YahooFinanceClient


class StockDataService:
    """Unified service for fetching stock data from multiple sources."""
    
    def __init__(self):
        self.config = get_data_source_config()
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        
        # Initialize FMP client
        self.fmp_client = None
        if self.config.is_fmp_enabled():
            self.fmp_client = FMPClient(self.config.fmp_api_key)
        
        # Initialize Alpha Vantage client
        self.alpha_vantage_client = None
        if self.config.is_alpha_vantage_enabled():
            self.alpha_vantage_client = AlphaVantageClient(
                self.config.alpha_vantage_api_key
            )
        
        # Initialize Yahoo Finance client (always available, no API key needed)
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
        Get stock quote from configured data source with fallback chain.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with stock quote data including metadata
        """
        cache_key = self._get_cache_key('quote', symbol)
        
        # Check cache first
        cached_data = self._get_cache(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            print(f"✅ Returning cached data for {symbol} (source: {cached_data.get('data_source', 'unknown')})")
            return cached_data
        
        # Get primary source and fallback chain
        primary_source = self.config.get_primary_source()
        fallback_sources = self.config.get_fallback_sources()
        
        # Create complete source chain: primary + fallbacks
        source_chain = [primary_source] + [s for s in fallback_sources if s != primary_source]
        
        # Try each source in order
        last_error = None
        for idx, source in enumerate(source_chain):
            try:
                is_primary = (idx == 0)
                data = self._fetch_quote_from_source(symbol, source, is_primary)
                
                if data:
                    # Add metadata
                    data['from_cache'] = False
                    data['data_source'] = source.value
                    if not is_primary:
                        data['fallback_used'] = True
                        data['primary_source'] = primary_source.value
                        if last_error:
                            data['primary_source_error'] = str(last_error)
                    
                    # Cache the successful result
                    self._set_cache(cache_key, data)
                    print(f"✅ Successfully fetched {symbol} from {source.value}")
                    return data
                    
            except Exception as e:
                last_error = e
                source_name = source.value
                print(f"⚠️  {source_name} failed for {symbol}: {str(e)}")
                if idx < len(source_chain) - 1:
                    next_source = source_chain[idx + 1].value
                    print(f"   Trying next source: {next_source}...")
        
        # All sources failed
        error_msg = f"All data sources failed for {symbol}. Last error: {str(last_error)}"
        print(f"❌ {error_msg}")
        raise ValueError(error_msg)
    
    def _fetch_quote_from_source(self, symbol: str, source: DataSource, is_primary: bool) -> Dict[str, Any]:
        """
        Fetch quote from a specific data source.
        
        Args:
            symbol: Stock ticker symbol
            source: Data source to use
            is_primary: Whether this is the primary source
        
        Returns:
            Quote data dictionary
        """
        source_label = "primary" if is_primary else "fallback"
        print(f"Fetching quote for {symbol} from {source.value} ({source_label})...")
        
        if source == DataSource.FMP and self.fmp_client:
            return self.fmp_client.get_quote(symbol)
        elif source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
            return self.alpha_vantage_client.get_quote(symbol)
        elif source == DataSource.YAHOO_FINANCE:
            return self.yahoo_finance_client.get_quote(symbol)
        else:
            raise ValueError(f"Data source {source.value} is not available or not configured")
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Get company overview and fundamental data with fallback chain.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with company data including metadata
        """
        cache_key = self._get_cache_key('overview', symbol)
        
        # Check cache first
        cached_data = self._get_cache(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            print(f"✅ Returning cached overview for {symbol} (source: {cached_data.get('data_source', 'unknown')})")
            return cached_data
        
        # Get primary source and fallback chain
        primary_source = self.config.get_primary_source()
        fallback_sources = self.config.get_fallback_sources()
        
        # Create complete source chain
        source_chain = [primary_source] + [s for s in fallback_sources if s != primary_source]
        
        # Try each source in order
        last_error = None
        for idx, source in enumerate(source_chain):
            try:
                is_primary = (idx == 0)
                data = self._fetch_overview_from_source(symbol, source, is_primary)
                
                if data:
                    # Add metadata
                    data['from_cache'] = False
                    data['data_source'] = source.value
                    if not is_primary:
                        data['fallback_used'] = True
                        data['primary_source'] = primary_source.value
                        if last_error:
                            data['primary_source_error'] = str(last_error)
                    
                    # Cache the successful result
                    self._set_cache(cache_key, data)
                    print(f"✅ Successfully fetched overview for {symbol} from {source.value}")
                    return data
                    
            except Exception as e:
                last_error = e
                source_name = source.value
                print(f"⚠️  {source_name} failed for {symbol}: {str(e)}")
                if idx < len(source_chain) - 1:
                    next_source = source_chain[idx + 1].value
                    print(f"   Trying next source: {next_source}...")
        
        # All sources failed
        error_msg = f"All data sources failed for {symbol}. Last error: {str(last_error)}"
        print(f"❌ {error_msg}")
        raise ValueError(error_msg)
    
    def _fetch_overview_from_source(self, symbol: str, source: DataSource, is_primary: bool) -> Dict[str, Any]:
        """
        Fetch company overview from a specific data source.
        
        Args:
            symbol: Stock ticker symbol
            source: Data source to use
            is_primary: Whether this is the primary source
        
        Returns:
            Company overview data dictionary
        """
        source_label = "primary" if is_primary else "fallback"
        print(f"Fetching overview for {symbol} from {source.value} ({source_label})...")
        
        if source == DataSource.FMP and self.fmp_client:
            return self.fmp_client.get_company_profile(symbol)
        elif source == DataSource.ALPHA_VANTAGE and self.alpha_vantage_client:
            return self.alpha_vantage_client.get_company_overview(symbol)
        elif source == DataSource.YAHOO_FINANCE:
            return self.yahoo_finance_client.get_company_info(symbol)
        else:
            raise ValueError(f"Data source {source.value} is not available or not configured")


# Global service instance
_service: Optional[StockDataService] = None


def get_stock_data_service() -> StockDataService:
    """Get or create the global stock data service instance."""
    global _service
    if _service is None:
        _service = StockDataService()
    return _service
