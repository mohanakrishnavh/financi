# Deployment Guide - Financi MCP Server

This guide provides step-by-step instructions for deploying the Financi MCP Server to Azure Functions.

## Prerequisites

Before starting the deployment, ensure you have:

- ✅ Azure subscription with appropriate permissions
- ✅ Azure CLI installed and configured
- ✅ Python 3.11+ installed
- ✅ Git installed
- ✅ Alpha Vantage API key (register at [alphavantage.co](https://www.alphavantage.co/support/#api-key))
- ✅ Azure DevOps organization (for CI/CD pipeline)

## Deployment Options

Choose the deployment method that best fits your needs:

1. **[Azure DevOps Pipeline](#option-1-azure-devops-pipeline)** - Recommended for production
2. **[Manual Deployment](#option-2-manual-deployment)** - Good for development/testing
3. **[Local Development](#option-3-local-development)** - For development only

---

## Option 1: Azure DevOps Pipeline

### Step 1: Fork and Clone Repository

```bash
# Fork the repository to your GitHub/Azure DevOps account
# Then clone your fork
git clone https://dev.azure.com/your-org/financi.git
cd financi
```

### Step 2: Create Azure Service Connection

1. Navigate to your Azure DevOps project
2. Go to **Project Settings** > **Service connections**
3. Click **New service connection**
4. Select **Azure Resource Manager**
5. Choose **Service principal (automatic)**
6. Select your Azure subscription
7. Name it `financi-service-connection`
8. Save the connection

### Step 3: Configure Pipeline Variables

In your Azure DevOps project:

1. Go to **Pipelines** > **Library**
2. Create a new variable group named `financi-variables`
3. Add the following variables:

| Variable Name | Value | Secret |
|---------------|--------|---------|
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID | No |
| `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key | Yes ✅ |
| `RESOURCE_GROUP_NAME` | `rg-financi-prod` | No |
| `LOCATION` | `East US 2` | No |

### Step 4: Create and Run Pipeline

1. In Azure DevOps, go to **Pipelines**
2. Click **New pipeline**
3. Select your repository source
4. Choose **Existing Azure Pipelines YAML file**
5. Select `/.azure-pipelines/azure-pipelines.yml`
6. Click **Run**

The pipeline will:
- Build and test the Python code
- Deploy Azure infrastructure using Bicep
- Deploy the Function App code
- Run validation tests

### Step 5: Verify Deployment

After successful pipeline execution:

```bash
# Get the Function App URL from pipeline output
# Test the health endpoint
curl https://your-function-app.azurewebsites.net/api/health

# Expected response:
# {
#   "status": "healthy",
#   "server": "financi-mcp-server",
#   "version": "1.0.0",
#   "timestamp": "2024-01-01T12:00:00.000Z"
# }
```

---

## Option 2: Manual Deployment

### Step 1: Prepare Environment

```bash
# Clone the repository
git clone https://github.com/your-username/financi.git
cd financi

# Install Azure CLI (if not already installed)
# For macOS:
brew install azure-cli

# For Windows:
# Download from https://aka.ms/installazurecliwindows

# Login to Azure
az login

# Set default subscription (optional)
az account set --subscription "Your Subscription Name"
```

### Step 2: Deploy Infrastructure

```bash
# Create resource group
az group create \
  --name rg-financi \
  --location "East US 2"

# Deploy Bicep template
az deployment group create \
  --resource-group rg-financi \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/parameters.json \
  --parameters functionAppName="financi-$(whoami)-$(date +%s)"

# Get deployment outputs
az deployment group show \
  --resource-group rg-financi \
  --name main \
  --query properties.outputs
```

### Step 3: Prepare Function Code

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run tests (optional but recommended)
pytest tests/ -v

# Create deployment package
cd src
zip -r ../function-app.zip . --exclude="*.pyc" "__pycache__/*"
cd ..
```

### Step 4: Deploy Function Code

```bash
# Get Function App name from previous deployment
FUNCTION_APP_NAME=$(az deployment group show \
  --resource-group rg-financi \
  --name main \
  --query properties.outputs.functionAppName.value -o tsv)

echo "Deploying to Function App: $FUNCTION_APP_NAME"

# Deploy using zip file
az functionapp deployment source config-zip \
  --resource-group rg-financi \
  --name $FUNCTION_APP_NAME \
  --src function-app.zip

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
sleep 30
```

### Step 5: Configure API Keys

```bash
# Option 1: Store in Key Vault (Recommended)
KEY_VAULT_NAME=$(az deployment group show \
  --resource-group rg-financi \
  --name main \
  --query properties.outputs.keyVaultName.value -o tsv)

az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "ALPHA-VANTAGE-API-KEY" \
  --value "YOUR_ALPHA_VANTAGE_API_KEY"

# Option 2: Set as Function App setting (Less secure)
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --settings "ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY"
```

### Step 6: Test Deployment

```bash
# Get Function App URL
FUNCTION_URL=$(az functionapp show \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --query defaultHostName -o tsv)

echo "Function App URL: https://$FUNCTION_URL"

# Test health endpoint
curl "https://$FUNCTION_URL/api/health"

# Test MCP tools list
curl -X POST "https://$FUNCTION_URL/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Test stock price tool
curl -X POST "https://$FUNCTION_URL/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_stock_price", 
      "arguments": {"symbol": "AAPL"}
    }
  }'
```

---

## Option 3: Local Development

For local development and testing:

### Step 1: Setup Local Environment

```bash
# Clone repository
git clone https://github.com/your-username/financi.git
cd financi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Azure Functions Core Tools
# For macOS:
brew tap azure/functions
brew install azure-functions-core-tools@4

# For Windows:
# Download from https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local
```

### Step 2: Configure Local Settings

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API keys
nano .env
```

Add to `.env`:
```
ALPHA_VANTAGE_API_KEY=your_actual_api_key_here
MCP_SERVER_NAME=financi
MCP_SERVER_VERSION=1.0.0
LOGGING_LEVEL=DEBUG
```

### Step 3: Run Locally

```bash
# Navigate to source directory
cd src

# Start Azure Functions locally
func start --python

# The function will be available at:
# http://localhost:7071/api/health
# http://localhost:7071/api/mcp
```

### Step 4: Test Local Deployment

```bash
# Test health endpoint
curl http://localhost:7071/api/health

# Test MCP endpoint
curl -X POST http://localhost:7071/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

---

## Post-Deployment Configuration

### 1. Configure Monitoring

```bash
# Enable Application Insights (if not already enabled)
az monitor app-insights component create \
  --app financi-insights \
  --location "East US 2" \
  --resource-group rg-financi

# Link to Function App
INSIGHTS_KEY=$(az monitor app-insights component show \
  --app financi-insights \
  --resource-group rg-financi \
  --query instrumentationKey -o tsv)

az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$INSIGHTS_KEY"
```

### 2. Set Up Custom Domain (Optional)

```bash
# Add custom domain
az functionapp config hostname add \
  --webapp-name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --hostname "api.yourdomain.com"

# Configure SSL certificate
az functionapp config ssl upload \
  --certificate-file /path/to/certificate.pfx \
  --certificate-password "password" \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi
```

### 3. Configure CORS (If needed)

```bash
# Allow specific origins
az functionapp cors add \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --allowed-origins "https://yourdomain.com" "https://app.yourdomain.com"
```

### 4. Set Up Alerts

```bash
# Create alert for function errors
az monitor metrics alert create \
  --name "Financi Function Errors" \
  --resource-group rg-financi \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/rg-financi/providers/Microsoft.Web/sites/$FUNCTION_APP_NAME" \
  --condition "count 'FunctionExecutionCount' > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action email your-email@example.com
```

---

## Troubleshooting

### Common Issues

#### 1. Function App Not Starting

**Symptoms**: Function returns 500 errors or doesn't respond

**Solutions**:
```bash
# Check function app logs
az webapp log tail --name $FUNCTION_APP_NAME --resource-group rg-financi

# Verify Python version
az functionapp config show --name $FUNCTION_APP_NAME --resource-group rg-financi

# Check app settings
az functionapp config appsettings list --name $FUNCTION_APP_NAME --resource-group rg-financi
```

#### 2. API Key Issues

**Symptoms**: "API key not configured" errors

**Solutions**:
```bash
# Verify API key is set
az functionapp config appsettings show \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi \
  --setting-names "ALPHA_VANTAGE_API_KEY"

# Test API key directly
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"
```

#### 3. Deployment Failures

**Symptoms**: Deployment fails or times out

**Solutions**:
```bash
# Check deployment status
az functionapp deployment list-publishing-profiles \
  --name $FUNCTION_APP_NAME \
  --resource-group rg-financi

# Redeploy if needed
az functionapp deployment source config-zip \
  --resource-group rg-financi \
  --name $FUNCTION_APP_NAME \
  --src function-app.zip
```

#### 4. Cold Start Issues

**Symptoms**: First request takes a long time

**Solutions**:
- Upgrade to Premium plan for production
- Implement warming functions
- Use Application Insights to monitor cold starts

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](../README.md#troubleshooting) in the main README
2. Review Azure Function App logs in the Azure portal
3. Check Application Insights for detailed error information
4. Create an issue in the GitHub repository with:
   - Deployment method used
   - Error messages
   - Azure Function App logs
   - Environment details

---

## Next Steps

After successful deployment:

1. **Configure MCP Client**: Update your MCP client configuration to use the new endpoint
2. **Monitor Usage**: Set up monitoring and alerts for API usage and costs
3. **Scale Planning**: Monitor performance and plan scaling strategy
4. **Security Review**: Implement additional security measures for production
5. **Backup Strategy**: Set up backup and disaster recovery procedures

## Security Best Practices

1. **API Keys**: Always use Azure Key Vault for storing sensitive information
2. **HTTPS Only**: Ensure all communications use HTTPS
3. **CORS**: Configure CORS settings appropriately for your use case
4. **Authentication**: Implement proper authentication for production use
5. **Network Security**: Consider using Azure API Management for additional security
6. **Monitoring**: Enable comprehensive logging and monitoring
7. **Updates**: Keep dependencies and Azure services updated