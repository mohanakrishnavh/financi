# Financi Documentation Index

## 📚 Getting Started

**Start here if you're new to Financi:**

1. **[README.md](../README.md)** - Main project overview
   - Quick start guide
   - Feature list with examples
   - Installation and setup
   - API documentation
   - Usage examples (Python, JavaScript, curl)

2. **[DEPLOYMENT_HTTP_WRAPPERS.md](DEPLOYMENT_HTTP_WRAPPERS.md)** - Deployment guide
   - What was implemented
   - Step-by-step deployment instructions
   - Verification procedures
   - Usage examples
   - Troubleshooting

---

## 🔌 API & Integration

**Learn how to use the Financi API:**

3. **[HTTP_WRAPPERS_GUIDE.md](HTTP_WRAPPERS_GUIDE.md)** - Complete HTTP API reference
   - Implementation details
   - All 5 API endpoints documented
   - Request/response examples
   - Architecture diagram
   - Integration guide for MCP bridge

4. **[LOCAL_MCP_TOOLS.md](LOCAL_MCP_TOOLS.md)** - MCP integration guide
   - Claude Desktop setup
   - All 6 MCP tools documented with examples
   - Troubleshooting MCP issues
   - Maintenance tips for adding new tools
   - Local bridge architecture

---

## 🏗️ Architecture & Technical Details

**Understand how Financi works:**

5. **[MCP_REALITY_CHECK.md](MCP_REALITY_CHECK.md)** - MCP architecture deep dive
   - Why Azure MCP triggers aren't accessible via HTTP
   - Detailed root cause analysis
   - Solution options comparison
   - Technical decision rationale
   - HTTP wrapper implementation approach

---

## 🚀 DevOps & CI/CD

**Set up deployment pipelines:**

6. **[GIT_MULTI_REPO_GUIDE.md](GIT_MULTI_REPO_GUIDE.md)** - Git multi-repository setup
   - GitHub + Azure DevOps configuration
   - Remote setup and authentication
   - Push to both repositories simultaneously
   - Troubleshooting git issues

7. **[PIPELINE_SETUP.md](PIPELINE_SETUP.md)** - Azure DevOps pipeline
   - CI/CD pipeline configuration
   - Automated deployment process
   - Build and release steps

---

## 📁 Documentation Structure

```
docs/
├── README.md                       # This file - Documentation index
├── DEPLOYMENT_HTTP_WRAPPERS.md     # ⭐ Deployment guide
├── HTTP_WRAPPERS_GUIDE.md          # ⭐ HTTP API reference
├── LOCAL_MCP_TOOLS.md              # ⭐ MCP setup guide
├── MCP_REALITY_CHECK.md            # Technical architecture
├── GIT_MULTI_REPO_GUIDE.md         # Git setup
└── PIPELINE_SETUP.md               # CI/CD pipeline
```

---

## 🎯 Quick Navigation

### I want to...

**...deploy Financi for the first time**
→ Start with [README.md](../README.md), then [DEPLOYMENT_HTTP_WRAPPERS.md](DEPLOYMENT_HTTP_WRAPPERS.md)

**...use the HTTP API**
→ See [HTTP_WRAPPERS_GUIDE.md](HTTP_WRAPPERS_GUIDE.md) for complete API reference

**...integrate with Claude Desktop**
→ Follow [LOCAL_MCP_TOOLS.md](LOCAL_MCP_TOOLS.md) setup guide

**...understand why HTTP wrappers were needed**
→ Read [MCP_REALITY_CHECK.md](MCP_REALITY_CHECK.md) for technical background

**...set up CI/CD**
→ Follow [GIT_MULTI_REPO_GUIDE.md](GIT_MULTI_REPO_GUIDE.md) and [PIPELINE_SETUP.md](PIPELINE_SETUP.md)

**...add a new financial tool**
→ See "Development" section in [README.md](../README.md)

---

## 📖 Documentation by Role

### For Developers
1. [README.md](../README.md) - Project overview and API docs
2. [HTTP_WRAPPERS_GUIDE.md](HTTP_WRAPPERS_GUIDE.md) - API implementation
3. [MCP_REALITY_CHECK.md](MCP_REALITY_CHECK.md) - Architecture decisions
4. [GIT_MULTI_REPO_GUIDE.md](GIT_MULTI_REPO_GUIDE.md) - Version control

### For DevOps Engineers
1. [DEPLOYMENT_HTTP_WRAPPERS.md](DEPLOYMENT_HTTP_WRAPPERS.md) - Deployment process
2. [PIPELINE_SETUP.md](PIPELINE_SETUP.md) - CI/CD configuration
3. [GIT_MULTI_REPO_GUIDE.md](GIT_MULTI_REPO_GUIDE.md) - Repository setup

### For End Users
1. [README.md](../README.md) - Quick start and usage examples
2. [HTTP_WRAPPERS_GUIDE.md](HTTP_WRAPPERS_GUIDE.md) - API reference
3. [LOCAL_MCP_TOOLS.md](LOCAL_MCP_TOOLS.md) - Claude Desktop integration

---

## 🔄 Documentation Updates

### Recent Changes

**November 10, 2025**
- ✅ Added HTTP wrapper implementation documentation
- ✅ Updated README with current architecture
- ✅ Removed obsolete MCP_CONFIGURATION.md and MCP_TROUBLESHOOTING.md
- ✅ Created comprehensive DEPLOYMENT_HTTP_WRAPPERS.md guide
- ✅ Updated LOCAL_MCP_TOOLS.md with all 6 tools
- ✅ Added MCP_REALITY_CHECK.md explaining architecture decisions

### Documentation Maintenance

When making changes:
1. Update this index if adding/removing docs
2. Keep README.md in sync with actual features
3. Update version numbers in deployment guides
4. Add dated notes to changelog sections
5. Cross-reference related documents

---

## ❓ Need Help?

- **Can't find what you're looking for?** Check the main [README.md](../README.md)
- **Found an issue?** Create a GitHub issue
- **Have a question?** Start a GitHub discussion
- **Want to contribute?** See contributing guidelines in [README.md](../README.md)

---

**Last Updated:** November 10, 2025  
**Version:** 1.2.0  
**Maintainer:** Mohanakrishna VH
