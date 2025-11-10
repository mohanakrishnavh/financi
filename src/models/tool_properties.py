"""
Tool property definitions for MCP tools.
Defines the schema for each tool's input parameters.
"""

import json


class ToolProperty:
    """Represents a property/parameter for an MCP tool."""
    
    def __init__(self, property_name: str, property_type: str, description: str):
        """
        Initialize a tool property.
        
        Args:
            property_name: The name of the property
            property_type: The data type (e.g., 'string', 'number')
            description: Human-readable description of the property
        """
        self.propertyName = property_name
        self.propertyType = property_type
        self.description = description

    def to_dict(self):
        """Convert the property to a dictionary."""
        return {
            "propertyName": self.propertyName,
            "propertyType": self.propertyType,
            "description": self.description,
        }


# Constants for property names
SYMBOL_PROPERTY = "symbol"
AMOUNT_PROPERTY = "amount"
PRINCIPAL_PROPERTY = "principal"
RATE_PROPERTY = "rate"
TIME_PROPERTY = "time"
FREQUENCY_PROPERTY = "frequency"
CURRENT_AGE_PROPERTY = "current_age"
RETIREMENT_AGE_PROPERTY = "retirement_age"
CURRENT_SAVINGS_PROPERTY = "current_savings"
MONTHLY_CONTRIBUTION_PROPERTY = "monthly_contribution"
ANNUAL_RETURN_PROPERTY = "annual_return"


# Stock-related tool properties
STOCK_PRICE_PROPERTIES = [
    ToolProperty(SYMBOL_PROPERTY, "string", "The stock symbol to get the price for (e.g., AAPL, MSFT).")
]

PORTFOLIO_PROPERTIES = [
    ToolProperty(SYMBOL_PROPERTY, "string", "The stock symbol."),
    ToolProperty(AMOUNT_PROPERTY, "number", "The number of shares.")
]

EIGHT_PILLAR_PROPERTIES = [
    ToolProperty(SYMBOL_PROPERTY, "string", "The stock symbol to analyze (e.g., AAPL, MSFT).")
]


# Financial calculator tool properties
COMPOUND_INTEREST_PROPERTIES = [
    ToolProperty(PRINCIPAL_PROPERTY, "number", "Initial investment amount in dollars."),
    ToolProperty(RATE_PROPERTY, "number", "Annual interest rate as a percentage (e.g., 5 for 5%)."),
    ToolProperty(TIME_PROPERTY, "number", "Investment period in years."),
    ToolProperty(FREQUENCY_PROPERTY, "number", "Compounding frequency per year (1=annual, 4=quarterly, 12=monthly, 365=daily). Default is 12 (monthly).")
]

RETIREMENT_CALCULATOR_PROPERTIES = [
    ToolProperty(CURRENT_AGE_PROPERTY, "number", "Your current age."),
    ToolProperty(RETIREMENT_AGE_PROPERTY, "number", "Your desired retirement age."),
    ToolProperty(CURRENT_SAVINGS_PROPERTY, "number", "Current retirement savings amount in dollars."),
    ToolProperty(MONTHLY_CONTRIBUTION_PROPERTY, "number", "Monthly contribution amount in dollars."),
    ToolProperty(ANNUAL_RETURN_PROPERTY, "number", "Expected annual return rate as a percentage (e.g., 7 for 7%).")
]


# Convert tool properties to JSON strings (required by Azure Functions)
def properties_to_json(properties):
    """Convert a list of ToolProperty objects to a JSON string."""
    return json.dumps([prop.to_dict() for prop in properties])


# Pre-computed JSON strings for each tool
STOCK_PRICE_JSON = properties_to_json(STOCK_PRICE_PROPERTIES)
PORTFOLIO_JSON = properties_to_json(PORTFOLIO_PROPERTIES)
EIGHT_PILLAR_JSON = properties_to_json(EIGHT_PILLAR_PROPERTIES)
COMPOUND_INTEREST_JSON = properties_to_json(COMPOUND_INTEREST_PROPERTIES)
RETIREMENT_CALCULATOR_JSON = properties_to_json(RETIREMENT_CALCULATOR_PROPERTIES)
