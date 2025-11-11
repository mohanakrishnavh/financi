# Local MCP Tools - Troubleshooting Guide

## Problem: Newly Added Tools Not Available Locally

### Root Cause
The **local MCP bridge server** (`local-server/mcp-bridge-server.js`) was out of sync with the Azure Functions app. While the Azure Functions had 6 tools, the local bridge only exposed 3.

### Solution Applied ✅

Updated `mcp-bridge-server.js` to include all 6 tools:

**Original (3 tools):**
1. ✅ hello_financi
2. ✅ get_stock_price  
3. ✅ calculate_portfolio_value

**Updated (6 tools):**
1. ✅ hello_financi
2. ✅ get_stock_price
3. ✅ calculate_portfolio_value
4. ✅ **eight_pillar_stock_analysis** ← NEW
5. ✅ **compound_interest_calculator** ← NEW
6. ✅ **retirement_calculator** ← NEW

---

## How to See the New Tools in Claude Desktop

### Step 1: Quit Claude Desktop Completely
```bash
# Option 1: Use Cmd+Q while Claude Desktop is active
# Option 2: Right-click Claude in Dock > Quit
# Option 3: Use Activity Monitor to force quit if needed
```

### Step 2: Restart Claude Desktop
```bash
# Open from Applications or Spotlight
open -a "Claude"
```

### Step 3: Verify Tools Are Available

The MCP bridge server will automatically start when Claude Desktop launches. You should now see all 6 tools available.

**Test in Claude Desktop:**
```
Can you list all available Financi MCP tools?
```

Expected response should show all 6 tools.

---

## Architecture: How Local MCP Works

```
┌─────────────────┐
│ Claude Desktop  │
│   (MCP Client)  │
└────────┬────────┘
         │
         │ stdio (MCP protocol)
         │
┌────────▼────────────────────┐
│  mcp-bridge-server.js       │
│  (Local MCP Server)         │
│  - Exposes tool definitions │
│  - Returns mock data        │
└─────────────────────────────┘
```

**Important Notes:**
- The local bridge uses **mock data** for development
- Real data comes from Azure Functions when deployed
- Tools must be manually kept in sync between bridge and Azure Functions
- Each tool needs: definition, handler case, and mock data implementation

---

## Available Tools

### 1. hello_financi
**Description:** Hello world from Financi MCP server.
**Parameters:** None
**Example:**
```
Test hello_financi
```

### 2. get_stock_price
**Description:** Get current stock price for a given symbol.
**Parameters:**
- `symbol` (string, required): Stock symbol (e.g., AAPL, MSFT)

**Example:**
```
Get the current price of AAPL
```

### 3. calculate_portfolio_value
**Description:** Calculate the value of shares for a given stock.
**Parameters:**
- `symbol` (string, required): Stock symbol
- `amount` (number, required): Number of shares

**Example:**
```
Calculate the value of 50 shares of MSFT
```

### 4. eight_pillar_stock_analysis
**Description:** Perform comprehensive Eight Pillar Stock Analysis.
**Parameters:**
- `symbol` (string, required): Stock symbol to analyze

**Analysis Pillars:**
1. PE Ratio - Price-to-earnings valuation
2. ROIC - Return on invested capital
3. Shares Outstanding - Share dilution trends
4. Cash Flow - Operating cash generation
5. Net Income - Profitability trends
6. Revenue Growth - Top-line expansion
7. Liabilities - Debt management
8. Price-to-FCF - Free cash flow valuation

**Example:**
```
Perform eight pillar analysis on AAPL
```

### 5. compound_interest_calculator
**Description:** Calculate compound interest with customizable frequency.
**Parameters:**
- `principal` (number, required): Initial investment in dollars
- `rate` (number, required): Annual interest rate as percentage (e.g., 5 for 5%)
- `time` (number, required): Investment period in years
- `frequency` (string, required): Compounding frequency
  - Options: `annually`, `semi-annually`, `quarterly`, `monthly`, `daily`

**Example:**
```
Calculate compound interest on $10,000 at 7% for 20 years with monthly compounding
```

### 6. retirement_calculator
**Description:** Calculate retirement savings projection with year-by-year breakdown.
**Parameters:**
- `current_age` (number, required): Your current age in years
- `retirement_age` (number, required): Your planned retirement age
- `current_savings` (number, required): Current retirement savings in dollars
- `monthly_contribution` (number, required): Monthly contribution in dollars
- `annual_return` (number, required): Expected annual return as percentage (e.g., 7 for 7%)

**Example:**
```
Calculate retirement savings for a 30-year-old planning to retire at 65 with $50,000 saved, contributing $500 monthly at 7% return
```

---

## Testing New Tools

### Quick Test Script
```bash
# Test in terminal (optional - uses mock data)
cd /Users/mohanakrishnavh/Repos/financi
node local-server/mcp-bridge-server.js
```

### Test in Claude Desktop (recommended)

1. **Test Stock Analysis:**
   ```
   Analyze Tesla (TSLA) using eight pillar analysis
   ```

2. **Test Compound Interest:**
   ```
   How much will $5,000 grow in 10 years at 6% annual return with quarterly compounding?
   ```

3. **Test Retirement Planning:**
   ```
   I'm 35 years old with $100,000 saved. If I contribute $1,000 monthly and expect 8% returns, how much will I have at retirement age 67?
   ```

---

## Maintenance Tips

### When Adding New Tools to Azure Functions:

1. **Update Azure Functions** (`src/function_app.py`)
   - Add the function decorator and handler

2. **Update Local Bridge** (`local-server/mcp-bridge-server.js`)
   - Add tool definition in `ListToolsRequestSchema` handler
   - Add case in `CallToolRequestSchema` switch statement
   - Add mock data handler in `getMockData` function

3. **Restart Claude Desktop**
   - Quit completely (Cmd+Q)
   - Reopen from Applications

4. **Commit and Push**
   ```bash
   git add src/function_app.py local-server/mcp-bridge-server.js
   git commit -m "Add [tool_name] to MCP server"
   ./scripts/push-both.sh
   ```

---

## Troubleshooting

### Tools Still Not Showing?

1. **Check Claude Desktop logs:**
   ```bash
   # macOS logs location
   ~/Library/Logs/Claude/
   ```

2. **Verify bridge server is running:**
   - Open Activity Monitor
   - Search for "node" processes
   - Look for `mcp-bridge-server.js`

3. **Check configuration:**
   ```bash
   cat claude-desktop-config.json
   ```
   Should point to: `local-server/mcp-bridge-server.js`

4. **Verify environment:**
   ```bash
   cat .env.local | grep DEFAULT_HOST_KEY
   ```

5. **Manual test:**
   ```bash
   cd /Users/mohanakrishnavh/Repos/financi
   source .env.local
   FINANCI_API_KEY="$DEFAULT_HOST_KEY" node local-server/mcp-bridge-server.js
   ```
   Press Ctrl+C to stop

### Error: "Tool not found"

This means the tool exists in Azure Functions but not in the local bridge.
- Solution: Update `mcp-bridge-server.js` to include the tool

### Error: "Connection refused"

The bridge server isn't starting.
- Check `claude-desktop-config.json` is in the correct location
- Verify Node.js is installed: `node --version`
- Check `.env.local` exists and has `DEFAULT_HOST_KEY`

---

## Files Modified

**Commit:** `201e88d`
- ✅ `local-server/mcp-bridge-server.js` (+172 lines)
  - Added 3 new tool definitions
  - Added 3 new handler cases
  - Added 3 new mock data implementations

**Previous Commits:**
- `a0905a4` - Added Azure DevOps auth setup script
- `112d4b8` - Refactored tests into modular structure

---

## Next Steps

1. ✅ **Restart Claude Desktop** to load new tools
2. ✅ Test each new tool with sample queries
3. 📝 Document any issues or unexpected behavior
4. 🚀 Ready to use all 6 financial tools locally!

---

## Summary

**Problem:** Newly added tools (eight_pillar_stock_analysis, compound_interest_calculator, retirement_calculator) were not available in Claude Desktop.

**Root Cause:** Local MCP bridge server was out of sync with Azure Functions.

**Solution:** Updated bridge server to expose all 6 tools with complete mock data implementations.

**Result:** All tools now available locally after restarting Claude Desktop. ✅
