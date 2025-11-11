# Bruno Quick Start Guide 🚀

## ✅ Setup Complete!

Bruno has been installed and your API key is configured. Follow these steps to start testing the Financi API.

---

## 📖 Step-by-Step Instructions

### Step 1: Open the Collection in Bruno

1. **Bruno should now be open** (if not, launch it from Applications)
2. Click **"Open Collection"** button (or use `Cmd + O`)
3. Navigate to: `/Users/mohanakrishnavh/Repos/financi/bruno-collection`
4. Click **"Open"** or press Enter

### Step 2: Select the Production Environment

1. Look at the **top-right corner** of Bruno
2. Find the **Environment dropdown** (currently showing "No Environment")
3. Click it and select **"Production"**
4. ✅ Your API key is already configured!

### Step 3: Test the Health Check (No Auth Required)

This verifies the API is running:

1. In the left sidebar, click **"Health Check"**
2. Click the **"Send"** button (or press `Cmd + Enter`)
3. ✅ You should see:
   ```json
   {
     "status": "healthy",
     "version": "1.2.0",
     "mcp_tools": [...],
     "http_endpoints": [...]
   }
   ```

---

## 🧪 Testing Each Endpoint

### 1️⃣ Get Stock Price (Simple GET Request)

**What it does**: Gets current price and market data for a stock

**Steps**:
1. Click **"Stock" folder** → **"Get Stock Price"**
2. Notice the URL has `symbol=AAPL` (Apple stock)
3. Click **"Send"**
4. ✅ You'll see Apple's current price, market cap, P/E ratio, etc.

**Try different stocks**:
- Change `symbol=AAPL` to `symbol=MSFT` (Microsoft)
- Change to `symbol=GOOGL` (Google)
- Change to `symbol=TSLA` (Tesla)

---

### 2️⃣ Calculate Portfolio Value (POST with JSON)

**What it does**: Calculates total value of your stock holdings

**Steps**:
1. Click **"Stock" folder** → **"Calculate Portfolio Value"**
2. Look at the **"Body"** tab (JSON is already filled in):
   ```json
   {
     "symbol": "AAPL",
     "shares": 100
   }
   ```
3. Click **"Send"**
4. ✅ You'll see the total value of 100 Apple shares

**Try different scenarios**:
- Change `"shares": 100` to `"shares": 50`
- Change `"symbol": "AAPL"` to `"symbol": "MSFT"`
- Try: `{"symbol": "GOOGL", "shares": 25}`

---

### 3️⃣ Eight Pillar Stock Analysis (Comprehensive Analysis)

**What it does**: Deep analysis across 8 investment dimensions

**Steps**:
1. Click **"Stock" folder** → **"Eight Pillar Stock Analysis"**
2. Default symbol is `MSFT` (Microsoft)
3. Click **"Send"**
4. ✅ You'll get a comprehensive report with:
   - Overall score (0-10)
   - 8 pillar scores (Valuation, Financial Health, Profitability, etc.)
   - Detailed metrics for each pillar
   - Investment recommendation (BUY/HOLD/SELL)

**⚠️ Note**: This takes 5-10 seconds as it analyzes lots of data!

**Try analyzing**:
- `symbol=AAPL` (Apple)
- `symbol=JNJ` (Johnson & Johnson)
- `symbol=WMT` (Walmart)

---

### 4️⃣ Compound Interest Calculator

**What it does**: Calculates investment growth with compound interest

**Steps**:
1. Click **"Calculators" folder** → **"Compound Interest Calculator"**
2. Look at the **"Body"** tab:
   ```json
   {
     "principal": 10000,
     "rate": 7,
     "time": 10,
     "frequency": 12
   }
   ```
   This means: $10,000 at 7% for 10 years, compounded monthly
3. Click **"Send"**
4. ✅ You'll see how much your investment grows

**Try different scenarios**:
- Long-term: `{"principal": 5000, "rate": 8, "time": 30, "frequency": 12}`
- High frequency: `{"principal": 10000, "rate": 7, "time": 10, "frequency": 365}` (daily)
- Conservative: `{"principal": 20000, "rate": 4, "time": 5, "frequency": 4}` (quarterly)

---

### 5️⃣ Retirement Calculator

**What it does**: Projects retirement savings with monthly contributions

**Steps**:
1. Click **"Calculators" folder** → **"Retirement Calculator"**
2. Look at the **"Body"** tab:
   ```json
   {
     "current_age": 30,
     "retirement_age": 65,
     "current_savings": 50000,
     "monthly_contribution": 1000,
     "annual_return": 7,
     "inflation_rate": 2.5
   }
   ```
3. Click **"Send"**
4. ✅ You'll see:
   - Total at retirement (nominal and inflation-adjusted)
   - Monthly income in retirement
   - Inflation impact

**Try different scenarios**:
- Starting younger: `{"current_age": 25, "retirement_age": 60, ...}`
- Higher contributions: Change `"monthly_contribution": 1000` to `2000`
- Different returns: Change `"annual_return": 7` to `10` (aggressive) or `5` (conservative)

---

## 💡 Pro Tips

### Viewing Responses
- Click the **"Response"** tab to see JSON results
- Use the **"Timeline"** tab to see request timing
- Check **"Headers"** to see response headers

### Organizing Your Tests
- **Star** your favorite requests (click the ★ icon)
- Use **"Folders"** to keep requests organized
- **Duplicate** requests to save different scenarios (right-click → Duplicate)

### Keyboard Shortcuts
- `Cmd + Enter` - Send request
- `Cmd + N` - New request
- `Cmd + K` - Quick search
- `Cmd + O` - Open collection

### Editing Requests
1. Click on any **parameter** in the URL to edit it
2. Edit **JSON body** directly in the Body tab
3. Add **query parameters** in the Params section
4. View **documentation** in the Docs tab (scroll down)

---

## 🎯 Recommended Testing Flow

**For first-time users**:
1. ✅ Health Check (verify API is up)
2. ✅ Get Stock Price (simple GET request)
3. ✅ Calculate Portfolio Value (simple POST)
4. ✅ Compound Interest Calculator (financial calc)
5. ✅ Retirement Calculator (complex calc)
6. ✅ Eight Pillar Analysis (comprehensive, takes longer)

---

## 🔍 Troubleshooting

### "401 Unauthorized" Error
- Check that **Production environment is selected** (top-right)
- Verify the `functionKey` is correct in the environment
- Get your key by running: `./scripts/get-function-keys.sh`

### "Invalid Symbol" Error
- Make sure you're using valid stock tickers (AAPL, MSFT, GOOGL, etc.)
- Check the ticker exists on Yahoo Finance
- Symbols are case-insensitive

### "Connection Refused"
- If using **Local environment**: Make sure Azure Functions is running (`func start`)
- If using **Production environment**: Check your internet connection

### Request Takes Too Long
- Eight Pillar Analysis takes 5-10 seconds (this is normal)
- Other requests should respond in < 2 seconds
- Check the Azure Functions status if it's slower

---

## 📚 Next Steps

1. **Experiment** with different stock symbols and parameters
2. **Save responses** for comparison (right-click response → Copy)
3. **Create custom requests** based on the examples
4. **Test error cases** (invalid symbols, negative numbers, etc.)
5. **Check the docs** in each request for detailed parameter info

---

## 🆘 Need Help?

- **Bruno Docs**: https://docs.usebruno.com/
- **API Documentation**: See `../docs/HTTP_WRAPPERS_GUIDE.md`
- **Financi README**: See `../README.md`

---

## 🎉 You're All Set!

Your Bruno collection is configured and ready to use. Start with the Health Check and work your way through the endpoints. Have fun testing! 🚀
