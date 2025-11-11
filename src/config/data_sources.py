"""Data source configuration for stock data providers."""

import os
from enum import Enum
from typing import Optional


class DataSource(Enum):
    """Available data sources for stock data."""
    FMP = "fmp"
    ALPHA_VANTAGE = "alpha_vantage"
    YAHOO_FINANCE = "yahoo_finance"


class DataSourceConfig:
    """Configuration for data source selection and API keys."""
    
    def __init__(self):
        # Get primary data source from environment (default: fmp)
        self.primary_source = DataSource(
            os.environ.get('DATA_SOURCE', 'fmp')
        )
        
        # Get fallback sources (default fallback chain: fmp -> alpha_vantage -> yahoo_finance)
        self.fallback_sources = self._parse_fallback_sources()
        
        # FMP API key
        self.fmp_api_key = os.environ.get('FMP_API_KEY')
        
        # Alpha Vantage API key
        self.alpha_vantage_api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        
        # Rate limiting (calls per day for free tier)
        self.alpha_vantage_rate_limit = int(
            os.environ.get('ALPHA_VANTAGE_RATE_LIMIT', '25')
        )
        
        # Cache duration in seconds (default: 1 day)
        self.cache_duration = int(
            os.environ.get('CACHE_DURATION_SECONDS', '86400')
        )
    
    def _parse_fallback_sources(self) -> list:
        """Parse fallback sources from environment or use default chain."""
        fallback_env = os.environ.get('FALLBACK_DATA_SOURCES', '')
        if fallback_env:
            # Parse comma-separated list: "alpha_vantage,yahoo_finance"
            return [DataSource(s.strip()) for s in fallback_env.split(',') if s.strip()]
        else:
            # Default fallback chain: alpha_vantage -> yahoo_finance
            return [DataSource.ALPHA_VANTAGE, DataSource.YAHOO_FINANCE]
    
    def is_fmp_enabled(self) -> bool:
        """Check if FMP is configured and enabled."""
        return (
            self.fmp_api_key is not None and
            self.fmp_api_key != ""
        )
    
    def is_alpha_vantage_enabled(self) -> bool:
        """Check if Alpha Vantage is configured and enabled."""
        return (
            self.alpha_vantage_api_key is not None and
            self.alpha_vantage_api_key != ""
        )
    
    def get_primary_source(self) -> DataSource:
        """Get the primary data source to use."""
        if self.primary_source == DataSource.FMP:
            if not self.is_fmp_enabled():
                print("FMP not configured, falling back to next source")
                return self._get_next_available_source()
        elif self.primary_source == DataSource.ALPHA_VANTAGE:
            if not self.is_alpha_vantage_enabled():
                print("Alpha Vantage not configured, falling back to next source")
                return self._get_next_available_source()
        return self.primary_source
    
    def _get_next_available_source(self) -> DataSource:
        """Get the next available data source from fallback chain."""
        for source in self.fallback_sources:
            if source == DataSource.FMP and self.is_fmp_enabled():
                return source
            elif source == DataSource.ALPHA_VANTAGE and self.is_alpha_vantage_enabled():
                return source
            elif source == DataSource.YAHOO_FINANCE:
                return source
        # Ultimate fallback is always Yahoo Finance (no API key needed)
        return DataSource.YAHOO_FINANCE
    
    def get_fallback_sources(self) -> list:
        """Get the list of fallback data sources in priority order."""
        return self.fallback_sources


# Global configuration instance
_config: Optional[DataSourceConfig] = None


def get_data_source_config() -> DataSourceConfig:
    """Get or create the global data source configuration."""
    global _config
    if _config is None:
        _config = DataSourceConfig()
    return _config
