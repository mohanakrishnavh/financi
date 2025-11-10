"""
Master test runner for the Financi MCP server.
This file imports and runs all test modules organized by handler type.

Test Organization:
- test_stock_handlers.py: Tests for stock-related functions
- test_financial_calculators.py: Tests for financial calculation functions
- test_integration.py: Integration tests and real-world scenarios
"""

import sys
from pathlib import Path


def print_banner():
    """Print main test banner."""
    print("\n" + "█" * 70)
    print("FINANCI MCP SERVER - COMPREHENSIVE TEST SUITE")
    print("█" * 70)
    print("\nThis test suite is organized by handler modules:")
    print("  1. Stock Handlers (get_stock_price, portfolio_value, eight_pillar)")
    print("  2. Financial Calculators (compound_interest, retirement)")
    print("  3. Integration Tests (real-world scenarios)")
    print("=" * 70)


def run_test_module(module_name: str, description: str):
    """Run a specific test module."""
    print(f"\n{'=' * 70}")
    print(f"RUNNING: {description}")
    print(f"Module: {module_name}")
    print("=" * 70)
    
    try:
        # Import and run the module
        if module_name == "test_stock_handlers":
            import test_stock_handlers
            test_stock_handlers.__dict__['__name__'] = '__main__'
            exec(open('test_stock_handlers.py').read())
        elif module_name == "test_financial_calculators":
            import test_financial_calculators
            test_financial_calculators.__dict__['__name__'] = '__main__'
            exec(open('test_financial_calculators.py').read())
        elif module_name == "test_integration":
            import test_integration
            test_integration.__dict__['__name__'] = '__main__'
            exec(open('test_integration.py').read())
        
        print(f"\n✅ {description} completed successfully")
        return True
    except Exception as e:
        print(f"\n❌ Error running {description}: {str(e)}")
        return False


def print_summary(results: dict):
    """Print summary of all test runs."""
    print("\n" + "█" * 70)
    print("TEST SUITE SUMMARY")
    print("█" * 70)
    
    print("\nResults:")
    for module, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {module}")
    
    total = len(results)
    passed = sum(1 for success in results.values() if success)
    
    print(f"\nTotal: {passed}/{total} test modules passed")
    
    if passed == total:
        print("\n🎉 All test modules completed successfully!")
    else:
        print("\n⚠️ Some test modules failed. Please review the output above.")


def print_quick_start():
    """Print quick start guide."""
    print("\n" + "=" * 70)
    print("QUICK START GUIDE")
    print("=" * 70)
    
    print("\n📋 Run Individual Test Modules:")
    print("  $ python tests/test_stock_handlers.py")
    print("  $ python tests/test_financial_calculators.py")
    print("  $ python tests/test_integration.py")
    
    print("\n🚀 Deploy to Azure:")
    print("  $ func azure functionapp publish financi")
    
    print("\n🔧 Start MCP Bridge Server:")
    print("  $ cd local-server")
    print("  $ node mcp-bridge-server.js")
    
    print("\n📖 Documentation:")
    print("  • Code Structure: docs/CODE_ORGANIZATION.md")
    print("  • API Reference: docs/NEW_FUNCTIONS.md")
    print("  • Setup Guide: docs/SETUP_COMPLETE.md")
    
    print("\n💬 Test with Claude Desktop:")
    print("  • 'What's the current price of Microsoft?'")
    print("  • 'Calculate compound interest on $10k at 7% for 10 years'")
    print("  • 'I'm 30, retire at 65, have $50k saved, contribute $1k/month'")
    print("  • 'Perform eight pillar analysis on Apple (AAPL)'")


def main():
    """Main test runner."""
    print_banner()
    
    # Define test modules to run
    test_modules = [
        ("test_stock_handlers", "Stock Handlers Test Suite"),
        ("test_financial_calculators", "Financial Calculators Test Suite"),
        ("test_integration", "Integration Test Suite")
    ]
    
    # Track results
    results = {}
    
    # Ask user which tests to run
    print("\nTest Options:")
    print("  1. Run all tests")
    print("  2. Run stock handlers tests only")
    print("  3. Run financial calculators tests only")
    print("  4. Run integration tests only")
    print("  5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5) [default: 1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        choice = "1"  # Default to running all
        print("1")
    
    # Run selected tests
    if choice == "1":
        # Run all tests
        for module_name, description in test_modules:
            results[description] = run_test_module(module_name, description)
    elif choice == "2":
        results["Stock Handlers"] = run_test_module("test_stock_handlers", "Stock Handlers Test Suite")
    elif choice == "3":
        results["Financial Calculators"] = run_test_module("test_financial_calculators", "Financial Calculators Test Suite")
    elif choice == "4":
        results["Integration Tests"] = run_test_module("test_integration", "Integration Test Suite")
    elif choice == "5":
        print("\nExiting test suite.")
        return
    else:
        print(f"\n❌ Invalid choice: {choice}")
        return
    
    # Print summary
    print_summary(results)
    print_quick_start()
    
    print("\n" + "█" * 70)
    print("TEST RUNNER COMPLETE")
    print("█" * 70 + "\n")


if __name__ == "__main__":
    main()
