#!/bin/bash

# Financi - Push to Both Repositories Script
echo "🚀 Financi Multi-Repository Push"
echo "================================"

# Push to GitHub
echo "📱 Pushing to GitHub..."
if git push origin main; then
    echo "✅ GitHub push successful"
else
    echo "❌ GitHub push failed"
    exit 1
fi

echo ""

# Push to Azure DevOps  
echo "🔷 Pushing to Azure DevOps..."
if git push azdo main; then
    echo "✅ Azure DevOps push successful"
else
    echo "❌ Azure DevOps push failed"
    echo "💡 See GIT_MULTI_REPO_GUIDE.md for setup help"
    exit 1
fi

echo ""
echo "🎉 Successfully pushed to both repositories!"
echo "📍 GitHub: https://github.com/mohanakrishnavh/financi"
echo "📍 Azure DevOps: https://dev.azure.com/mohanakrishnavh/financi"

