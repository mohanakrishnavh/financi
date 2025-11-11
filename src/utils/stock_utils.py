"""
Stock-related utility functions.
Handles fetching stock data and performing financial analysis using multiple data sources.
"""

import logging
import yfinance as yf
from datetime import datetime
from typing import Dict, Optional

# Import the unified stock data service
try:
    from services.stock_data_service import get_stock_data_service
    USE_UNIFIED_SERVICE = True
except ImportError:
    # Fallback to direct yfinance if service not available
    USE_UNIFIED_SERVICE = False
    logging.warning("StockDataService not available, using direct yfinance")


def fetch_stock_price(symbol: str) -> Optional[Dict]:
    """
    Fetch real-time stock price using configured data source (Alpha Vantage or Yahoo Finance).
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT', 'RELIANCE.NS')
        
    Returns:
        Dictionary with stock data or None if failed
    """
    try:
        if USE_UNIFIED_SERVICE:
            # Use unified service with Alpha Vantage/Yahoo Finance support
            service = get_stock_data_service()
            stock_data = service.get_stock_quote(symbol)
            return stock_data
        else:
            # Fallback to direct yfinance
            return _fetch_stock_price_yfinance(symbol)
            
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {str(e)}")
        # Try fallback to yfinance if unified service fails
        if USE_UNIFIED_SERVICE:
            logging.info(f"Attempting direct yfinance fallback for {symbol}")
            try:
                return _fetch_stock_price_yfinance(symbol)
            except Exception as fallback_error:
                logging.error(f"Fallback also failed: {str(fallback_error)}")
        return None


def _fetch_stock_price_yfinance(symbol: str) -> Optional[Dict]:
    """
    Direct Yahoo Finance implementation (fallback).
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Dictionary with stock data or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty or not info:
            logging.warning(f"No data found for symbol: {symbol}")
            return None
            
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        
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
            "data_source": "yahoo_finance",
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Error in _fetch_stock_price_yfinance for {symbol}: {str(e)}")
        return None


def perform_eight_pillar_analysis(symbol: str) -> Optional[Dict]:
    """
    Perform Eight Pillar Stock Analysis using yfinance.
    
    This function uses Yahoo Finance for comprehensive financial data.
    Alpha Vantage integration for Eight Pillar analysis can be added in future versions.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with analysis results or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get financial statements
        balance_sheet = ticker.balance_sheet
        income_stmt = ticker.income_stmt
        cash_flow = ticker.cashflow
        
        if balance_sheet.empty or income_stmt.empty or cash_flow.empty:
            logging.warning(f"Insufficient financial data for {symbol}")
            return None
        
        # Pillar 1: PE Ratio
        pe_ratio = info.get('trailingPE', 0)
        pe_check = "✓" if pe_ratio < 22.5 else "✗"
        
        # Pillar 2: ROIC (Return on Invested Capital)
        try:
            total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else 0
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0] if 'Total Liabilities Net Minority Interest' in balance_sheet.index else 0
            invested_capital = total_assets - total_liabilities if total_assets and total_liabilities else 0
            
            net_income = income_stmt.loc['Net Income'].iloc[0] if 'Net Income' in income_stmt.index else 0
            roic = (net_income / invested_capital * 100) if invested_capital > 0 else 0
            roic_check = "✓" if roic > 10 else "✗"
        except:
            roic = 0
            roic_check = "✗"
        
        # Pillar 3: Shares Outstanding
        try:
            shares_outstanding = info.get('sharesOutstanding', 0)
            shares_check = "?" if shares_outstanding == 0 else "✓"
        except:
            shares_outstanding = 0
            shares_check = "✗"
        
        # Pillar 4: Cash Flow Growth
        try:
            if 'Operating Cash Flow' in cash_flow.index and len(cash_flow.columns) >= 2:
                latest_cf = cash_flow.loc['Operating Cash Flow'].iloc[0]
                oldest_cf = cash_flow.loc['Operating Cash Flow'].iloc[-1]
                cf_growth = ((latest_cf - oldest_cf) / abs(oldest_cf) * 100) if oldest_cf != 0 else 0
                cf_check = "✓" if cf_growth > 0 else "✗"
            else:
                cf_growth = 0
                cf_check = "✗"
        except:
            cf_growth = 0
            cf_check = "✗"
        
        # Pillar 5: Net Income Growth
        try:
            if 'Net Income' in income_stmt.index and len(income_stmt.columns) >= 2:
                latest_ni = income_stmt.loc['Net Income'].iloc[0]
                oldest_ni = income_stmt.loc['Net Income'].iloc[-1]
                ni_growth = ((latest_ni - oldest_ni) / abs(oldest_ni) * 100) if oldest_ni != 0 else 0
                ni_check = "✓" if ni_growth > 0 else "✗"
            else:
                ni_growth = 0
                ni_check = "✗"
        except:
            ni_growth = 0
            ni_check = "✗"
        
        # Pillar 6: Revenue Growth
        try:
            if 'Total Revenue' in income_stmt.index and len(income_stmt.columns) >= 2:
                latest_rev = income_stmt.loc['Total Revenue'].iloc[0]
                oldest_rev = income_stmt.loc['Total Revenue'].iloc[-1]
                rev_growth = ((latest_rev - oldest_rev) / abs(oldest_rev) * 100) if oldest_rev != 0 else 0
                rev_check = "✓" if rev_growth > 0 else "✗"
            else:
                rev_growth = 0
                rev_check = "✗"
        except:
            rev_growth = 0
            rev_check = "✗"
        
        # Pillar 7: Long-term Liabilities
        try:
            long_term_debt = balance_sheet.loc['Long Term Debt'].iloc[0] if 'Long Term Debt' in balance_sheet.index else 0
            avg_fcf = cash_flow.loc['Free Cash Flow'].mean() if 'Free Cash Flow' in cash_flow.index else 0
            liability_ratio = long_term_debt / avg_fcf if avg_fcf > 0 else 999
            liab_check = "✓" if liability_ratio < 5 else "✗"
        except:
            liability_ratio = 999
            liab_check = "✗"
        
        # Pillar 8: Price to Free Cash Flow
        try:
            market_cap = info.get('marketCap', 0)
            fcf = cash_flow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cash_flow.index else 0
            price_to_fcf = market_cap / fcf if fcf > 0 else 999
            fcf_check = "✓" if price_to_fcf < 22.5 else "✗"
        except:
            price_to_fcf = 999
            fcf_check = "✗"
        
        # Calculate overall score
        checks_passed = sum([
            1 if pe_check == "✓" else 0,
            1 if roic_check == "✓" else 0,
            1 if shares_check == "✓" else 0,
            1 if cf_check == "✓" else 0,
            1 if ni_check == "✓" else 0,
            1 if rev_check == "✓" else 0,
            1 if liab_check == "✓" else 0,
            1 if fcf_check == "✓" else 0
        ])
        score_percentage = (checks_passed / 8) * 100
        
        # Determine recommendation
        if score_percentage >= 75:
            assessment = "Good - Worth further research"
            recommendation = "Research further before investing"
        elif score_percentage >= 50:
            assessment = "Fair - Proceed with caution"
            recommendation = "Thorough due diligence required"
        else:
            assessment = "Poor - High risk"
            recommendation = "Consider alternative investments"
        
        result = {
            "symbol": symbol.upper(),
            "company_name": info.get('longName', 'N/A'),
            "market_cap": f"${info.get('marketCap', 0):,}",
            "analysis_date": datetime.utcnow().isoformat() + "Z",
            "pillars": {
                "pillar_1_five_year_pe_ratio": {
                    "value": round(pe_ratio, 2),
                    "threshold": "< 22.5",
                    "check": pe_check,
                    "description": "Five-year PE ratio measures valuation efficiency",
                    "interpretation": "Good value" if pe_check == "✓" else "Overvalued"
                },
                "pillar_2_five_year_roic": {
                    "value": f"{roic:.1f}%",
                    "threshold": "> 10% (good)",
                    "check": roic_check,
                    "description": "Return on Invested Capital measures capital efficiency",
                    "interpretation": "Strong capital efficiency" if roic_check == "✓" else "Weak capital efficiency"
                },
                "pillar_3_shares_outstanding": {
                    "current_shares": f"{shares_outstanding:,}",
                    "change_percent": "+nan%",
                    "threshold": "Decreasing",
                    "check": shares_check,
                    "description": "Share buybacks indicate management confidence",
                    "interpretation": "Data unavailable" if shares_check == "?" else "Dilution occurring"
                },
                "pillar_4_cash_flow_growth": {
                    "latest_fcf": f"${latest_cf:,}" if 'latest_cf' in locals() else "N/A",
                    "growth_percent": f"+{cf_growth:.2f}%" if cf_growth > 0 else f"{cf_growth:.2f}%",
                    "threshold": "Positive growth",
                    "check": cf_check,
                    "description": "Cash flow growth indicates financial health",
                    "interpretation": "Growing cash generation" if cf_check == "✓" else "Declining cash generation"
                },
                "pillar_5_net_income_growth": {
                    "latest_net_income": f"${latest_ni:,}" if 'latest_ni' in locals() else "N/A",
                    "growth_percent": f"+{ni_growth:.2f}%" if ni_growth > 0 else f"{ni_growth:.2f}%",
                    "threshold": "Positive growth",
                    "check": ni_check,
                    "description": "Net income growth shows profitability improvement",
                    "interpretation": "Growing profitability" if ni_check == "✓" else "Declining profitability"
                },
                "pillar_6_revenue_growth": {
                    "latest_revenue": f"${latest_rev:,}" if 'latest_rev' in locals() else "N/A",
                    "growth_percent": f"+{rev_growth:.2f}%" if rev_growth > 0 else f"{rev_growth:.2f}%",
                    "threshold": "Positive growth",
                    "check": rev_check,
                    "description": "Revenue growth shows business expansion",
                    "interpretation": "Expanding business" if rev_check == "✓" else "Shrinking business"
                },
                "pillar_7_long_term_liabilities": {
                    "long_term_debt": f"${long_term_debt:,}" if 'long_term_debt' in locals() else "N/A",
                    "avg_free_cash_flow": f"${avg_fcf:,}" if 'avg_fcf' in locals() else "N/A",
                    "liability_ratio": f"{liability_ratio:.2f}x",
                    "threshold": "< 5x",
                    "check": liab_check,
                    "description": "Debt coverage measures financial stability",
                    "interpretation": f"Can pay off debt in {liability_ratio:.1f} years" if liability_ratio < 999 else "High debt burden"
                },
                "pillar_8_price_to_fcf": {
                    "value": round(price_to_fcf, 2) if price_to_fcf < 999 else "N/A",
                    "threshold": "< 22.5",
                    "check": fcf_check,
                    "description": "Price-to-FCF measures cash flow valuation",
                    "interpretation": "Reasonable valuation" if fcf_check == "✓" else "Expensive valuation"
                }
            },
            "summary": {
                "total_checks_passed": checks_passed,
                "total_checks_evaluated": 8,
                "score_percentage": score_percentage,
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
