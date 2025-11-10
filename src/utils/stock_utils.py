"""
Stock-related utility functions.
Handles fetching stock data and performing financial analysis.
"""

import logging
from datetime import datetime
from typing import Dict, Optional

import yfinance as yf


def fetch_stock_price(symbol: str) -> Optional[Dict]:
    """
    Fetch real-time stock price using Yahoo Finance API.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with stock data or None if failed
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get current data
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty or not info:
            logging.warning(f"No data found for symbol: {symbol}")
            return None
            
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        
        # Calculate change
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
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {str(e)}")
        return None


def perform_eight_pillar_analysis(symbol: str) -> Optional[Dict]:
    """
    Perform comprehensive Eight Pillar Stock Analysis.
    
    The Eight Pillars evaluate:
    1. Five-Year PE Ratio (< 22.5)
    2. Five-Year ROIC (Return on Invested Capital)
    3. Shares Outstanding (decreasing preferred)
    4. Cash Flow Growth (5-year trend)
    5. Net Income Growth (5-year trend)
    6. Revenue Growth (5-year trend)
    7. Long-Term Liabilities (< 5x FCF)
    8. Price-to-Free Cash Flow (< 22.5)
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with detailed eight pillar analysis or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get financial statements
        try:
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
        except Exception as e:
            logging.error(f"Error fetching financial statements for {symbol}: {str(e)}")
            return None
        
        if financials.empty or balance_sheet.empty or cashflow.empty:
            logging.warning(f"Incomplete financial data for {symbol}")
            return None
        
        # Get current market cap
        market_cap = info.get('marketCap', 0)
        company_name = info.get('longName', symbol.upper())
        
        pillars = {}
        checks_passed = 0
        
        # PILLAR 1: Five-Year PE Ratio (< 22.5)
        try:
            net_incomes = financials.loc['Net Income'].head(5) if 'Net Income' in financials.index else None
            if net_incomes is not None and len(net_incomes) >= 1:
                total_5yr_earnings = net_incomes.sum()
                five_year_pe = market_cap / total_5yr_earnings if total_5yr_earnings > 0 else None
                
                if five_year_pe is not None:
                    check_passed = five_year_pe < 22.5
                    checks_passed += 1 if check_passed else 0
                    pillars['pillar_1_five_year_pe_ratio'] = {
                        "value": round(five_year_pe, 2),
                        "threshold": "< 22.5",
                        "check": "✓" if check_passed else "✗",
                        "description": "Five-year PE ratio measures valuation efficiency",
                        "interpretation": "Good value" if check_passed else "Potentially overvalued"
                    }
                else:
                    pillars['pillar_1_five_year_pe_ratio'] = {
                        "value": "N/A",
                        "threshold": "< 22.5",
                        "check": "?",
                        "description": "Insufficient data for calculation"
                    }
            else:
                pillars['pillar_1_five_year_pe_ratio'] = {
                    "value": "N/A",
                    "threshold": "< 22.5", 
                    "check": "?",
                    "description": "Net income data not available"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 1 for {symbol}: {str(e)}")
            pillars['pillar_1_five_year_pe_ratio'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 2: Five-Year ROIC (Return on Invested Capital)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            total_equity = balance_sheet.loc['Stockholders Equity'].iloc[0] if 'Stockholders Equity' in balance_sheet.index else 0
            total_debt = balance_sheet.loc['Total Debt'].iloc[0] if 'Total Debt' in balance_sheet.index else 0
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                total_5yr_fcf = free_cashflows.sum()
                invested_capital = total_equity + total_debt
                
                if invested_capital > 0:
                    roic = (total_5yr_fcf / invested_capital) * 100
                    check_passed = roic > 10  # Good ROIC threshold
                    checks_passed += 1 if check_passed else 0
                    pillars['pillar_2_five_year_roic'] = {
                        "value": f"{round(roic, 2)}%",
                        "threshold": "> 10% (good)",
                        "check": "✓" if check_passed else "✗",
                        "description": "Return on Invested Capital measures capital efficiency",
                        "interpretation": "Strong capital efficiency" if check_passed else "Weak capital efficiency"
                    }
                else:
                    pillars['pillar_2_five_year_roic'] = {
                        "value": "N/A",
                        "threshold": "> 10%",
                        "check": "?",
                        "description": "Insufficient capital data"
                    }
            else:
                pillars['pillar_2_five_year_roic'] = {
                    "value": "N/A",
                    "threshold": "> 10%",
                    "check": "?",
                    "description": "Free cash flow data not available"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 2 for {symbol}: {str(e)}")
            pillars['pillar_2_five_year_roic'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 3: Shares Outstanding (decreasing is better)
        try:
            shares_outstanding = balance_sheet.loc['Ordinary Shares Number'] if 'Ordinary Shares Number' in balance_sheet.index else None
            
            if shares_outstanding is not None and len(shares_outstanding) >= 2:
                current_shares = shares_outstanding.iloc[0]
                old_shares = shares_outstanding.iloc[-1] if len(shares_outstanding) >= 5 else shares_outstanding.iloc[-1]
                
                change_pct = ((current_shares - old_shares) / old_shares) * 100
                check_passed = current_shares < old_shares
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_3_shares_outstanding'] = {
                    "current_shares": f"{current_shares:,.0f}",
                    "change_percent": f"{change_pct:+.2f}%",
                    "threshold": "Decreasing",
                    "check": "✓" if check_passed else "✗",
                    "description": "Share buybacks indicate management confidence",
                    "interpretation": "Shareholder-friendly buybacks" if check_passed else "Dilution occurring"
                }
            else:
                pillars['pillar_3_shares_outstanding'] = {
                    "value": "N/A",
                    "threshold": "Decreasing",
                    "check": "?",
                    "description": "Insufficient shares data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 3 for {symbol}: {str(e)}")
            pillars['pillar_3_shares_outstanding'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 4: Cash Flow Growth (Last 5 Years)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 2:
                latest_fcf = free_cashflows.iloc[0]
                oldest_fcf = free_cashflows.iloc[-1]
                
                check_passed = latest_fcf > oldest_fcf
                growth_pct = ((latest_fcf - oldest_fcf) / abs(oldest_fcf)) * 100 if oldest_fcf != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_4_cash_flow_growth'] = {
                    "latest_fcf": f"${latest_fcf:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Cash flow growth indicates financial health",
                    "interpretation": "Growing cash generation" if check_passed else "Declining cash generation"
                }
            else:
                pillars['pillar_4_cash_flow_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 4 for {symbol}: {str(e)}")
            pillars['pillar_4_cash_flow_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 5: Net Income Growth (Last 5 Years)
        try:
            net_incomes = financials.loc['Net Income'].head(5) if 'Net Income' in financials.index else None
            
            if net_incomes is not None and len(net_incomes) >= 2:
                latest_ni = net_incomes.iloc[0]
                oldest_ni = net_incomes.iloc[-1]
                
                check_passed = latest_ni > oldest_ni
                growth_pct = ((latest_ni - oldest_ni) / abs(oldest_ni)) * 100 if oldest_ni != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_5_net_income_growth'] = {
                    "latest_net_income": f"${latest_ni:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Net income growth shows profitability improvement",
                    "interpretation": "Growing profitability" if check_passed else "Declining profitability"
                }
            else:
                pillars['pillar_5_net_income_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient net income data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 5 for {symbol}: {str(e)}")
            pillars['pillar_5_net_income_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 6: Revenue Growth (Last 5 Years)
        try:
            revenues = financials.loc['Total Revenue'].head(5) if 'Total Revenue' in financials.index else None
            
            if revenues is not None and len(revenues) >= 2:
                latest_rev = revenues.iloc[0]
                oldest_rev = revenues.iloc[-1]
                
                check_passed = latest_rev > oldest_rev
                growth_pct = ((latest_rev - oldest_rev) / oldest_rev) * 100 if oldest_rev != 0 else 0
                checks_passed += 1 if check_passed else 0
                
                pillars['pillar_6_revenue_growth'] = {
                    "latest_revenue": f"${latest_rev:,.0f}",
                    "growth_percent": f"{growth_pct:+.2f}%",
                    "threshold": "Positive growth",
                    "check": "✓" if check_passed else "✗",
                    "description": "Revenue growth shows business expansion",
                    "interpretation": "Expanding business" if check_passed else "Contracting business"
                }
            else:
                pillars['pillar_6_revenue_growth'] = {
                    "value": "N/A",
                    "threshold": "Positive growth",
                    "check": "?",
                    "description": "Insufficient revenue data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 6 for {symbol}: {str(e)}")
            pillars['pillar_6_revenue_growth'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 7: Long-Term Liabilities (< 5x 5-Year Average Free Cash Flow)
        try:
            long_term_debt = balance_sheet.loc['Long Term Debt'].iloc[0] if 'Long Term Debt' in balance_sheet.index else 0
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                avg_5yr_fcf = free_cashflows.mean()
                
                if avg_5yr_fcf > 0:
                    liability_ratio = long_term_debt / avg_5yr_fcf
                    check_passed = liability_ratio < 5
                    checks_passed += 1 if check_passed else 0
                    
                    pillars['pillar_7_long_term_liabilities'] = {
                        "long_term_debt": f"${long_term_debt:,.0f}",
                        "avg_free_cash_flow": f"${avg_5yr_fcf:,.0f}",
                        "liability_ratio": f"{liability_ratio:.2f}x",
                        "threshold": "< 5x",
                        "check": "✓" if check_passed else "✗",
                        "description": "Debt coverage measures financial stability",
                        "interpretation": f"Can pay off debt in {liability_ratio:.1f} years" if check_passed else "High debt burden"
                    }
                else:
                    pillars['pillar_7_long_term_liabilities'] = {
                        "value": "N/A",
                        "threshold": "< 5x",
                        "check": "?",
                        "description": "Negative or zero free cash flow"
                    }
            else:
                pillars['pillar_7_long_term_liabilities'] = {
                    "value": "N/A",
                    "threshold": "< 5x",
                    "check": "?",
                    "description": "Insufficient free cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 7 for {symbol}: {str(e)}")
            pillars['pillar_7_long_term_liabilities'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # PILLAR 8: Five-Year Price-to-Free Cash Flow (< 22.5)
        try:
            free_cashflows = cashflow.loc['Free Cash Flow'].head(5) if 'Free Cash Flow' in cashflow.index else None
            
            if free_cashflows is not None and len(free_cashflows) >= 1:
                total_5yr_fcf = free_cashflows.sum()
                
                if total_5yr_fcf > 0:
                    price_to_fcf = market_cap / total_5yr_fcf
                    check_passed = price_to_fcf < 22.5
                    checks_passed += 1 if check_passed else 0
                    
                    pillars['pillar_8_price_to_fcf'] = {
                        "value": round(price_to_fcf, 2),
                        "threshold": "< 22.5",
                        "check": "✓" if check_passed else "✗",
                        "description": "Price-to-FCF measures cash flow valuation",
                        "interpretation": "Reasonable valuation" if check_passed else "Potentially expensive"
                    }
                else:
                    pillars['pillar_8_price_to_fcf'] = {
                        "value": "N/A",
                        "threshold": "< 22.5",
                        "check": "?",
                        "description": "Negative free cash flow"
                    }
            else:
                pillars['pillar_8_price_to_fcf'] = {
                    "value": "N/A",
                    "threshold": "< 22.5",
                    "check": "?",
                    "description": "Insufficient free cash flow data"
                }
        except Exception as e:
            logging.error(f"Error calculating pillar 8 for {symbol}: {str(e)}")
            pillars['pillar_8_price_to_fcf'] = {"value": "Error", "check": "?", "error": str(e)}
        
        # Calculate overall score
        total_checks = sum(1 for p in pillars.values() if p.get("check") in ["✓", "✗"])
        score_percentage = (checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        # Overall assessment
        if score_percentage >= 87.5:  # 7-8 checks
            assessment = "Excellent - Strong buy candidate"
            recommendation = "Consider for investment"
        elif score_percentage >= 62.5:  # 5-6 checks
            assessment = "Good - Worth further research"
            recommendation = "Research further before investing"
        elif score_percentage >= 37.5:  # 3-4 checks
            assessment = "Fair - Proceed with caution"
            recommendation = "Significant concerns, investigate thoroughly"
        else:  # 0-2 checks
            assessment = "Poor - High risk investment"
            recommendation = "Avoid or wait for better conditions"
        
        result = {
            "symbol": symbol.upper(),
            "company_name": company_name,
            "market_cap": f"${market_cap:,.0f}",
            "analysis_date": datetime.utcnow().isoformat() + "Z",
            "pillars": pillars,
            "summary": {
                "total_checks_passed": checks_passed,
                "total_checks_evaluated": total_checks,
                "score_percentage": round(score_percentage, 1),
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
