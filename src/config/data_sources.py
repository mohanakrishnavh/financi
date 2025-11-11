"""Data source configuration for stock data providers."""

import os
from enum import Enum
from typing import Optional


class DataSource(Enum):
    """Available data sources for stock data."""
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"


class DataSourceConfig:
    """Configuration for data source selection and API keys."""
    
    def __init__(self):
        # Get primary data source from environment (default: yahoo_finance)
        self.primary_source = DataSource(
            os.environ.get('DATA_SOURCE', 'yahoo_finance')
        )
        
        # Get fallback source (default: yahoo_finance)
        fallback = os.environ.get('FALLBACK_DATA_SOURCE', 'yahoo_finance')
        self.fallback_source = DataSource(fallback) if fallback else None
        
        # Alpha Vantage API key
        self.alpha_vantage_api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        
        # Rate limiting (calls per day for free tier)
        self.alpha_vantage_rate_limit = int(
            os.environ.get('ALPHA_VANTAGE_RATE_LIMIT', '25')
        )
        
        # Cache duration in seconds (default: 5 minutes)
        self.cache_duration = int(
            os.environ.get('CACHE_DURATION_SECONDS', '300')
        )
    
    def is_alpha_vantage_enabled(self) -> bool:
        """Check if Alpha Vantage is configured and enabled."""
        return (
            self.alpha_vantage_api_key is not None and
            self.alpha_vantage_api_key != ""
        )
    
    def get_primary_source(self) -> DataSource:
        """Get the primary data source to use."""
        if self.primary_source == DataSource.ALPHA_VANTAGE:
            if not self.is_alpha_vantage_enabled():
                print("Alpha Vantage not configured, falling back to Yahoo Finance")
                return DataSource.YAHOO_FINANCE
        return self.primary_source
    
    def get_fallback_source(self) -> Optional[DataSource]:
        """Get the fallback data source."""
        return self.fallback_source


# Global configuration instance
_config: Optional[DataSourceConfig] = None


def get_data_source_config() -> DataSourceConfig:
    """Get or create the global data source configuration."""
    global _config
    if _config is None:
        _config = DataSourceConfig()
    return _config
