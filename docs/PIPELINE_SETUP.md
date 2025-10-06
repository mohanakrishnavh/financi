# Azure DevOps Pipeline Setup Guide

## 🚀 Quick Setup Steps

### Step 1: Push Code to Azure DevOps

Since we have authentication issues from the command line, please do this manually:

1. **Go to your Azure DevOps project**: https://dev.azure.com/mohanakrishnavh/financi
2. **Go to Repos** → **Files**
3. **Upload files** or **Import repository** from your local folder
4. **Make sure all these files are uploaded**:
   - `.azure-pipelines/azure-pipelines.yml`
   - `infrastructure/main.bicep`
   - `infrastructure/parameters.json`
   - `src/function_app.py`
   - `src/host.json`
   - `src/requirements.txt`
   - All other project files

### Step 2: Configure Pipeline Variables

1. **Go to Azure DevOps** → **Pipelines** → **Library**
2. **Create Variable Group** named: `financi-variables`
3. **Add these variables**:

| Variable Name | Value | Secret |
|---------------|-------|---------|
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID: `cc46f13d-94a3-4bf2-970a-15b46f9d821a` | No |
| `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key (get from https://www.alphavantage.co/support/#api-key) | ✅ **Yes** |

### Step 3: Create Pipeline

1. **Go to Pipelines** → **New pipeline**
2. **Select**: Azure Repos Git
3. **Select your repository**: financi
4. **Select**: Existing Azure Pipelines YAML file
5. **Path**: `/.azure-pipelines/azure-pipelines.yml`
6. **Save and run**

### Step 4: Pipeline Configuration

The pipeline will:
- ✅ Build and test Python code
- ✅ Deploy Bicep infrastructure 
- ✅ Deploy Function App code
- ✅ Configure environment variables
- ✅ Run health checks

## 🔧 Current Infrastructure Status

**Already Deployed Manually**:
- Resource Group: `rg-financi-linux`
- Function App: `financi-linux-1759692345`
- Function URL: `https://financi-linux-1759692345.azurewebsites.net`

**Pipeline Will Create New**:
- Resource Group: `rg-financi-main` (for main branch)
- Function App: `financi-mcp-main-[BUILD_ID]`

## 📋 Pre-Pipeline Checklist

- [ ] ✅ Service connection created (`financi-service-connection`)
- [ ] 📁 Code pushed to Azure DevOps repos
- [ ] 🔑 Alpha Vantage API key obtained
- [ ] 📊 Pipeline variables configured
- [ ] 🚀 Pipeline created and ready to run

## 🧪 Testing After Pipeline

Once the pipeline runs successfully:

```bash
# Test the new function app (URL will be in pipeline output)
curl https://[NEW_FUNCTION_APP_URL]/api/health

# Test MCP tools
curl -X POST https://[NEW_FUNCTION_APP_URL]/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Test stock price tool
curl -X POST https://[NEW_FUNCTION_APP_URL]/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_stock_price",
      "arguments": {"symbol": "AAPL"}
    }
  }'
```

## 🐛 Troubleshooting

If the pipeline fails:

1. **Check Service Connection**: Ensure it has Contributor access to your subscription
2. **Check Variables**: Ensure `ALPHA_VANTAGE_API_KEY` is set and marked as secret
3. **Check Logs**: Pipeline will show detailed error messages for each step
4. **Resource Names**: Pipeline creates unique names to avoid conflicts

## 🎯 Expected Pipeline Outputs

When successful, the pipeline will output:
- **Function App Name**: `financi-mcp-main-[BUILD_ID]`
- **Function App URL**: `https://financi-mcp-main-[BUILD_ID].azurewebsites.net`
- **Resource Group**: `rg-financi-main`
- **Health Check**: ✅ Passed
- **MCP Endpoint**: Ready for use

---

**Next**: Upload the code to Azure DevOps and run the pipeline!