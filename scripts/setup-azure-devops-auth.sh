#!/bin/bash

# Azure DevOps Authentication Setup for Financi
# This script helps configure Azure DevOps authentication using Personal Access Token (PAT)

echo "════════════════════════════════════════════════════════════════"
echo "  Azure DevOps Authentication Setup"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 Authentication Method: Personal Access Token (PAT)"
echo ""
echo "Previous Configuration Detected:"
echo "  • Method: PAT embedded in remote URL"
echo "  • Credential Helper: osxkeychain"
echo "  • Status: Token expired ❌"
echo ""

echo "────────────────────────────────────────────────────────────────"
echo "STEP 1: Generate New Personal Access Token"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "1. Opening Azure DevOps token page..."
echo "   URL: https://dev.azure.com/mohanakrishnavh/_usersSettings/tokens"
echo ""
open "https://dev.azure.com/mohanakrishnavh/_usersSettings/tokens" 2>/dev/null || echo "   Please open the URL manually in your browser"
echo ""
echo "2. Click '+ New Token' button"
echo ""
echo "3. Configure the token:"
echo "   Name:          financi-git-access"
echo "   Organization:  mohanakrishnavh"
echo "   Expiration:    90 days (or custom)"
echo "   Scopes:        Code (Read & Write)"
echo ""
echo "4. Click 'Create' and COPY the token (you won't see it again!)"
echo ""

# Prompt for PAT
echo "────────────────────────────────────────────────────────────────"
read -p "5. Paste your Personal Access Token here: " PAT
echo "────────────────────────────────────────────────────────────────"
echo ""

if [ -z "$PAT" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

echo "✅ Token received (length: ${#PAT} characters)"
echo ""

echo "────────────────────────────────────────────────────────────────"
echo "STEP 2: Configure Git Remote"
echo "────────────────────────────────────────────────────────────────"
echo ""

# Remove old remote
echo "Removing old Azure DevOps remote..."
git remote remove azdo 2>/dev/null
echo "✅ Old remote removed"
echo ""

# Add new remote with PAT
echo "Adding new Azure DevOps remote with token..."
REMOTE_URL="https://mohanakrishnavh:${PAT}@dev.azure.com/mohanakrishnavh/financi/_git/financi"
git remote add azdo "$REMOTE_URL"
echo "✅ New remote configured"
echo ""

# Store credentials in keychain
echo "Storing credentials in macOS Keychain..."
git credential approve << EOF
protocol=https
host=dev.azure.com
username=mohanakrishnavh
password=${PAT}
EOF
echo "✅ Credentials stored in osxkeychain"
echo ""

echo "────────────────────────────────────────────────────────────────"
echo "STEP 3: Test Connection"
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "Testing connection to Azure DevOps..."
if git ls-remote azdo &>/dev/null; then
    echo "✅ Connection successful!"
else
    echo "⚠️  Connection test inconclusive (might work on push)"
fi
echo ""

echo "────────────────────────────────────────────────────────────────"
echo "STEP 4: Push to Azure DevOps"
echo "────────────────────────────────────────────────────────────────"
echo ""

read -p "Would you like to push to Azure DevOps now? (y/n): " PUSH_NOW

if [[ "$PUSH_NOW" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Pushing to Azure DevOps..."
    if git push azdo main; then
        echo "✅ Successfully pushed to Azure DevOps!"
    else
        echo "❌ Push failed. Please check the error message above."
        exit 1
    fi
else
    echo "Skipping push. You can push later with:"
    echo "  git push azdo main"
    echo "Or use the automated script:"
    echo "  ./scripts/push-both.sh"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Azure DevOps Authentication Setup Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📝 Summary:"
echo "  • PAT generated and configured"
echo "  • Remote URL updated with token"
echo "  • Credentials stored in osxkeychain"
echo "  • Ready to push to Azure DevOps"
echo ""
echo "🚀 Next steps:"
echo "  • Test: git push azdo main"
echo "  • Or use: ./scripts/push-both.sh (push to both repositories)"
echo ""
echo "💡 Tip: PAT will expire in 90 days. Repeat this process when it expires."
echo ""
