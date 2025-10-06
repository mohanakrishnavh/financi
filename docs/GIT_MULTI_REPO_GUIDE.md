# Git Multi-Repository Setup for Financi

## 🎯 Current Configuration:
- **GitHub**: https://github.com/mohanakrishnavh/financi.git (Primary/Public)
- **Azure DevOps**: https://dev.azure.com/mohanakrishnavh/financi/_git/financi (Pipeline Source)

## 🚀 Quick Push Methods:

### Method 1: Separate Commands (Current Setup)
```bash
git push origin main    # Push to GitHub
git push azdo main      # Push to Azure DevOps
```

### Method 2: Automated Script
```bash
#!/bin/bash
echo "Pushing to GitHub..."
git push origin main
echo "Pushing to Azure DevOps..."  
git push azdo main
echo "✅ Pushed to both repositories!"
```

### Method 3: Single Command (Requires PAT Setup)
1. Create Azure DevOps Personal Access Token
2. Configure multiple push URLs
3. Use: `git push origin main` (pushes to both)

## 🔐 Personal Access Token Setup:
1. Go to: https://dev.azure.com/mohanakrishnavh/_usersSettings/tokens
2. Create token with Code (read & write) permissions
3. Configure: `git remote set-url --add --push origin https://PAT@dev.azure.com/mohanakrishnavh/financi/_git/financi`

## 💡 Why Both Repositories?
- **GitHub**: Public, documentation, open source
- **Azure DevOps**: CI/CD pipelines, private features
- **Sync**: Keep both repositories synchronized
- **Pipeline**: Azure DevOps pipeline requires Azure DevOps repository

## 🛠 Troubleshooting:
- Authentication issues: Check PAT expiration
- Push failures: Test each repository separately
- Sync issues: Use consistent push commands

