"""
Financial calculator MCP handler functions.
Handles compound interest and retirement planning calculations.
"""

import json
import logging
from datetime import datetime

from models.tool_properties import (
    PRINCIPAL_PROPERTY,
    RATE_PROPERTY,
    TIME_PROPERTY,
    FREQUENCY_PROPERTY,
    CURRENT_AGE_PROPERTY,
    RETIREMENT_AGE_PROPERTY,
    CURRENT_SAVINGS_PROPERTY,
    MONTHLY_CONTRIBUTION_PROPERTY,
    ANNUAL_RETURN_PROPERTY
)


def handle_compound_interest_calculator(context: str) -> str:
    """
    Calculates compound interest for an investment.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The compound interest calculation results or an error message.
    """
    try:
        content = json.loads(context)
        args = content["arguments"]
        
        principal = args.get(PRINCIPAL_PROPERTY)
        rate = args.get(RATE_PROPERTY)
        time = args.get(TIME_PROPERTY)
        frequency = args.get(FREQUENCY_PROPERTY, 12)  # Default to monthly
        
        # Validation
        if principal is None or principal <= 0:
            error_result = {
                "error": "Principal amount must be a positive number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if rate is None or rate < 0:
            error_result = {
                "error": "Interest rate must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if time is None or time <= 0:
            error_result = {
                "error": "Time period must be a positive number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if frequency not in [1, 4, 12, 365]:
            error_result = {
                "error": "Frequency must be 1 (annual), 4 (quarterly), 12 (monthly), or 365 (daily)",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        # Calculate compound interest: A = P(1 + r/n)^(nt)
        rate_decimal = rate / 100
        amount = principal * ((1 + rate_decimal / frequency) ** (frequency * time))
        interest_earned = amount - principal
        
        # Calculate year-by-year breakdown
        yearly_breakdown = []
        for year in range(1, int(time) + 1):
            year_amount = principal * ((1 + rate_decimal / frequency) ** (frequency * year))
            year_interest = year_amount - principal
            yearly_breakdown.append({
                "year": year,
                "amount": round(year_amount, 2),
                "interest_earned": round(year_interest, 2)
            })
        
        frequency_map = {1: "Annual", 4: "Quarterly", 12: "Monthly", 365: "Daily"}
        
        result = {
            "principal": round(principal, 2),
            "interest_rate": rate,
            "time_period_years": time,
            "compounding_frequency": frequency_map[frequency],
            "final_amount": round(amount, 2),
            "total_interest_earned": round(interest_earned, 2),
            "effective_annual_rate": round(((1 + rate_decimal / frequency) ** frequency - 1) * 100, 2),
            "yearly_breakdown": yearly_breakdown,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success"
        }
        
        logging.info(f"Calculated compound interest: ${amount:.2f} from ${principal} at {rate}% for {time} years")
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in compound_interest_calculator: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in compound_interest_calculator: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)


def handle_retirement_calculator(context: str) -> str:
    """
    Calculates retirement savings projection with detailed year-by-year breakdown.

    Args:
        context: The trigger context containing the input arguments.

    Returns:
        str: The retirement calculation results or an error message.
    """
    try:
        content = json.loads(context)
        args = content["arguments"]
        
        current_age = args.get(CURRENT_AGE_PROPERTY)
        retirement_age = args.get(RETIREMENT_AGE_PROPERTY)
        current_savings = args.get(CURRENT_SAVINGS_PROPERTY, 0)
        monthly_contribution = args.get(MONTHLY_CONTRIBUTION_PROPERTY)
        annual_return = args.get(ANNUAL_RETURN_PROPERTY)
        
        # Validation
        if current_age is None or current_age < 18 or current_age > 100:
            error_result = {
                "error": "Current age must be between 18 and 100",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if retirement_age is None or retirement_age <= current_age or retirement_age > 100:
            error_result = {
                "error": "Retirement age must be greater than current age and less than or equal to 100",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if current_savings < 0:
            error_result = {
                "error": "Current savings cannot be negative",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if monthly_contribution is None or monthly_contribution < 0:
            error_result = {
                "error": "Monthly contribution must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        if annual_return is None or annual_return < 0:
            error_result = {
                "error": "Annual return must be a non-negative number",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return json.dumps(error_result, indent=2)
        
        years_until_retirement = retirement_age - current_age
        monthly_rate = (annual_return / 100) / 12
        total_months = years_until_retirement * 12
        
        # Calculate future value
        # FV = PV(1+r)^n + PMT × [((1+r)^n - 1) / r]
        balance = current_savings
        total_contributions = current_savings
        yearly_breakdown = []
        
        for year in range(1, years_until_retirement + 1):
            year_start_balance = balance
            year_contributions = 0
            
            for month in range(12):
                # Add monthly contribution
                balance += monthly_contribution
                year_contributions += monthly_contribution
                total_contributions += monthly_contribution
                
                # Apply monthly return
                balance *= (1 + monthly_rate)
            
            year_age = current_age + year
            yearly_breakdown.append({
                "year": year,
                "age": year_age,
                "year_start_balance": round(year_start_balance, 2),
                "contributions_this_year": round(year_contributions, 2),
                "year_end_balance": round(balance, 2),
                "interest_earned_this_year": round(balance - year_start_balance - year_contributions, 2)
            })
        
        total_interest = balance - total_contributions
        
        # Calculate monthly withdrawal for 30 years in retirement (4% rule approximation)
        monthly_withdrawal_4percent = (balance * 0.04) / 12
        
        result = {
            "current_age": current_age,
            "retirement_age": retirement_age,
            "years_until_retirement": years_until_retirement,
            "current_savings": round(current_savings, 2),
            "monthly_contribution": round(monthly_contribution, 2),
            "annual_contribution": round(monthly_contribution * 12, 2),
            "annual_return_rate": annual_return,
            "projected_retirement_balance": round(balance, 2),
            "total_contributions": round(total_contributions, 2),
            "total_interest_earned": round(total_interest, 2),
            "estimated_monthly_withdrawal_4percent_rule": round(monthly_withdrawal_4percent, 2),
            "estimated_annual_withdrawal_4percent_rule": round(monthly_withdrawal_4percent * 12, 2),
            "yearly_breakdown": yearly_breakdown,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success",
            "notes": [
                "4% rule: Withdraw 4% of retirement balance annually (adjusted for inflation)",
                "Assumes consistent monthly contributions and returns",
                "Does not account for inflation, taxes, or fees",
                "Consider consulting a financial advisor for personalized planning"
            ]
        }
        
        logging.info(f"Calculated retirement: ${balance:.2f} at age {retirement_age}")
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in retirement_calculator: {str(e)}")
        error_result = {
            "error": "Invalid request format",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        logging.error(f"Unexpected error in retirement_calculator: {str(e)}")
        error_result = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(error_result, indent=2)
