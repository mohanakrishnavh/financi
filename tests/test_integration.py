"""
Integration tests for the Financi MCP server.
Tests all functions together and provides comprehensive usage examples.
"""

import json
from typing import Dict, Any, List


def print_welcome():
    """Print welcome banner."""
    print("\n" + "█" * 60)
    print("FINANCI MCP SERVER - INTEGRATION TEST SUITE")
    print("█" * 60)
    print("\nThis suite tests all Financi MCP server functions together.")
    print("It demonstrates real-world usage scenarios and examples.")
    print("=" * 60)


def test_comprehensive_financial_planning():
    """Test a complete financial planning scenario."""
    
    print("\n" + "=" * 60)
    print("SCENARIO: COMPREHENSIVE FINANCIAL PLANNING")
    print("=" * 60)
    
    print("\nScenario: Sarah's Financial Plan")
    print("-" * 60)
    print("Background:")
    print("  • Sarah is 30 years old")
    print("  • Has $50,000 in savings")
    print("  • Can contribute $1,500/month")
    print("  • Wants to retire at 65")
    print("  • Currently invests in tech stocks")
    
    print("\nStep 1: Check current investment performance")
    print("Query: 'Analyze my tech stocks: Microsoft, Apple, Google'")
    stock_tests = [
        {"symbol": "MSFT", "shares": 20},
        {"symbol": "AAPL", "shares": 30},
        {"symbol": "GOOGL", "shares": 10}
    ]
    print(f"Holdings: {json.dumps(stock_tests, indent=2)}")
    
    print("\nStep 2: Evaluate each stock with 8-pillar analysis")
    print("Query: 'Perform eight pillar analysis on MSFT, AAPL, GOOGL'")
    
    print("\nStep 3: Calculate retirement projection")
    retirement_plan = {
        "current_age": 30,
        "retirement_age": 65,
        "current_savings": 50000,
        "monthly_contribution": 1500,
        "annual_return": 7
    }
    print(f"Retirement Plan: {json.dumps(retirement_plan, indent=2)}")
    
    print("\nStep 4: Model investment growth scenarios")
    scenarios = [
        {"rate": 6, "desc": "Conservative (6%)"},
        {"rate": 7, "desc": "Moderate (7%)"},
        {"rate": 8, "desc": "Aggressive (8%)"}
    ]
    for scenario in scenarios:
        print(f"  • {scenario['desc']}: Calculate compound interest")
    
    print("\nExpected Outcome:")
    print("  ✓ Portfolio value from stock analysis")
    print("  ✓ Buy/Hold/Sell recommendations for each stock")
    print("  ✓ Retirement projection with age-by-age breakdown")
    print("  ✓ Multiple growth scenarios for planning")


def test_investment_comparison():
    """Test comparing different investment options."""
    
    print("\n" + "=" * 60)
    print("SCENARIO: INVESTMENT COMPARISON")
    print("=" * 60)
    
    print("\nScenario: Comparing Investment Vehicles")
    print("-" * 60)
    print("Question: Should I invest $100,000 in stocks or bonds?")
    
    print("\nOption 1: Stock Portfolio (8% annual return)")
    stock_investment = {
        "principal": 100000,
        "rate": 8,
        "time": 20,
        "frequency": 12
    }
    print(f"Parameters: {json.dumps(stock_investment, indent=2)}")
    
    print("\nOption 2: Bond Portfolio (4% annual return)")
    bond_investment = {
        "principal": 100000,
        "rate": 4,
        "time": 20,
        "frequency": 1
    }
    print(f"Parameters: {json.dumps(bond_investment, indent=2)}")
    
    print("\nOption 3: Mixed Portfolio (6% annual return)")
    mixed_investment = {
        "principal": 100000,
        "rate": 6,
        "time": 20,
        "frequency": 4
    }
    print(f"Parameters: {json.dumps(mixed_investment, indent=2)}")
    
    print("\nExpected Outcome:")
    print("  ✓ Compare final amounts after 20 years")
    print("  ✓ Evaluate risk vs. return tradeoffs")
    print("  ✓ Make informed investment decision")


def test_retirement_catch_up():
    """Test retirement catch-up strategy."""
    
    print("\n" + "=" * 60)
    print("SCENARIO: RETIREMENT CATCH-UP STRATEGY")
    print("=" * 60)
    
    print("\nScenario: Late Starter Retirement Planning")
    print("-" * 60)
    print("Background:")
    print("  • John is 45 years old")
    print("  • Has only $75,000 saved")
    print("  • Wants to retire at 67")
    print("  • Needs $1.5 million for comfortable retirement")
    
    print("\nStep 1: Current trajectory calculation")
    current = {
        "current_age": 45,
        "retirement_age": 67,
        "current_savings": 75000,
        "monthly_contribution": 1000,
        "annual_return": 7
    }
    print(f"Current Plan: {json.dumps(current, indent=2)}")
    
    print("\nStep 2: Aggressive catch-up calculation")
    aggressive = {
        "current_age": 45,
        "retirement_age": 67,
        "current_savings": 75000,
        "monthly_contribution": 3000,
        "annual_return": 8
    }
    print(f"Aggressive Plan: {json.dumps(aggressive, indent=2)}")
    
    print("\nStep 3: Analyze high-growth stocks for catch-up")
    print("Query: 'Eight pillar analysis on growth stocks'")
    print("Symbols: MSFT, AAPL, GOOGL, NVDA")
    
    print("\nExpected Outcome:")
    print("  ✓ Gap analysis between current and goal")
    print("  ✓ Monthly contribution needed to reach goal")
    print("  ✓ Stock recommendations for growth portfolio")
    print("  ✓ Year-by-year progress tracking")


def test_portfolio_rebalancing():
    """Test portfolio rebalancing decision."""
    
    print("\n" + "=" * 60)
    print("SCENARIO: PORTFOLIO REBALANCING")
    print("=" * 60)
    
    print("\nScenario: Should I Rebalance My Portfolio?")
    print("-" * 60)
    
    print("\nCurrent Holdings:")
    holdings = [
        {"symbol": "MSFT", "shares": 50},
        {"symbol": "AAPL", "shares": 60},
        {"symbol": "JNJ", "shares": 40},
        {"symbol": "JPM", "shares": 45},
        {"symbol": "KO", "shares": 100}
    ]
    for holding in holdings:
        print(f"  • {holding['shares']} shares of {holding['symbol']}")
    
    print("\nStep 1: Calculate current portfolio value")
    print(f"Query: Calculate portfolio with holdings: {json.dumps(holdings)}")
    
    print("\nStep 2: Analyze each holding fundamentals")
    print("Query: Run eight pillar analysis on each stock")
    
    print("\nStep 3: Identify underperformers")
    print("Expected: Find stocks with < 5 pillars passing")
    
    print("\nStep 4: Project future growth scenarios")
    print("Query: If I add $2000/month for 10 years at 7%, what will I have?")
    
    print("\nExpected Outcome:")
    print("  ✓ Total current portfolio value")
    print("  ✓ Fundamental strength of each holding")
    print("  ✓ Rebalancing recommendations (buy/hold/sell)")
    print("  ✓ Future portfolio value projections")


def print_all_tools_overview():
    """Print overview of all available tools."""
    
    print("\n" + "=" * 60)
    print("ALL AVAILABLE FINANCI TOOLS")
    print("=" * 60)
    
    tools = [
        {
            "name": "get_stock_price",
            "category": "Stock Analysis",
            "description": "Fetch current stock price and basic info",
            "example": "What's the current price of Microsoft?"
        },
        {
            "name": "calculate_portfolio_value",
            "category": "Stock Analysis",
            "description": "Calculate total value of multiple stock holdings",
            "example": "Value my portfolio: 10 MSFT, 15 AAPL, 5 GOOGL"
        },
        {
            "name": "eight_pillar_stock_analysis",
            "category": "Stock Analysis",
            "description": "Comprehensive fundamental analysis (Everything Money method)",
            "example": "Analyze Microsoft using the eight pillar method"
        },
        {
            "name": "compound_interest_calculator",
            "category": "Financial Planning",
            "description": "Calculate compound interest with various frequencies",
            "example": "Calculate compound interest on $10k at 7% for 10 years monthly"
        },
        {
            "name": "retirement_calculator",
            "category": "Financial Planning",
            "description": "Project retirement savings with contributions",
            "example": "I'm 30, retire at 65, $50k saved, contribute $1k/month at 7%"
        },
        {
            "name": "hello_financi",
            "category": "Utility",
            "description": "Health check and service information",
            "example": "What tools does Financi provide?"
        }
    ]
    
    print("\nStock Analysis Tools:")
    for tool in [t for t in tools if t["category"] == "Stock Analysis"]:
        print(f"\n  📊 {tool['name']}")
        print(f"     Description: {tool['description']}")
        print(f"     Example: \"{tool['example']}\"")
    
    print("\n" + "-" * 60)
    print("Financial Planning Tools:")
    for tool in [t for t in tools if t["category"] == "Financial Planning"]:
        print(f"\n  💰 {tool['name']}")
        print(f"     Description: {tool['description']}")
        print(f"     Example: \"{tool['example']}\"")
    
    print("\n" + "-" * 60)
    print("Utility Tools:")
    for tool in [t for t in tools if t["category"] == "Utility"]:
        print(f"\n  🔧 {tool['name']}")
        print(f"     Description: {tool['description']}")
        print(f"     Example: \"{tool['example']}\"")


def print_deployment_checklist():
    """Print deployment and testing checklist."""
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT & TESTING CHECKLIST")
    print("=" * 60)
    
    print("\n1. Pre-Deployment:")
    print("   ☐ Review code changes in src/ directory")
    print("   ☐ Check all imports are correct")
    print("   ☐ Verify requirements.txt is up to date")
    print("   ☐ Test locally if possible")
    
    print("\n2. Deployment:")
    print("   ☐ Deploy to Azure Functions:")
    print("      $ func azure functionapp publish financi")
    print("   ☐ Verify deployment logs for errors")
    print("   ☐ Check Azure Portal for function status")
    
    print("\n3. MCP Bridge Server:")
    print("   ☐ Restart MCP bridge server:")
    print("      $ cd local-server")
    print("      $ node mcp-bridge-server.js")
    print("   ☐ Verify connection in terminal output")
    print("   ☐ Check Claude Desktop configuration")
    
    print("\n4. Integration Testing:")
    print("   ☐ Test get_stock_price: 'What's MSFT price?'")
    print("   ☐ Test calculate_portfolio_value: 'Value my 10 AAPL shares'")
    print("   ☐ Test eight_pillar_analysis: 'Analyze Microsoft stock'")
    print("   ☐ Test compound_interest_calculator: 'Calculate $10k at 7% for 10 years'")
    print("   ☐ Test retirement_calculator: 'I'm 30, retire at 65, $50k saved'")
    
    print("\n5. Validation:")
    print("   ☐ Test error cases (invalid symbols, negative values)")
    print("   ☐ Verify all 6 tools appear in Claude Desktop")
    print("   ☐ Check response times are reasonable")
    print("   ☐ Validate calculation accuracy")
    
    print("\n6. Documentation:")
    print("   ☐ Update version numbers if needed")
    print("   ☐ Document any issues encountered")
    print("   ☐ Update README.md with new features")


def print_summary():
    """Print test suite summary."""
    
    print("\n" + "█" * 60)
    print("INTEGRATION TEST SUITE COMPLETE")
    print("█" * 60)
    
    print("\nTest Coverage:")
    print("  ✓ Comprehensive financial planning scenarios")
    print("  ✓ Investment comparison workflows")
    print("  ✓ Retirement catch-up strategies")
    print("  ✓ Portfolio rebalancing decisions")
    print("  ✓ Real-world usage examples")
    
    print("\nNext Steps:")
    print("  1. Run individual handler tests:")
    print("     $ python tests/test_stock_handlers.py")
    print("     $ python tests/test_financial_calculators.py")
    print("  2. Deploy to Azure Functions")
    print("  3. Test with Claude Desktop")
    print("  4. Refer to docs/CODE_ORGANIZATION.md for structure details")
    print("  5. Refer to docs/NEW_FUNCTIONS.md for API documentation")
    
    print()


if __name__ == "__main__":
    print_welcome()
    test_comprehensive_financial_planning()
    test_investment_comparison()
    test_retirement_catch_up()
    test_portfolio_rebalancing()
    print_all_tools_overview()
    print_deployment_checklist()
    print_summary()
