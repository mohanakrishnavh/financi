# Project Structure Overview

## Root Directory Files

### Essential Files (Keep)
- `README.md` - Main documentation
- `LICENSE` - MIT license file
- `.gitignore` - Git ignore patterns
- `.funcignore` - Azure Functions deployment ignore patterns
- `pytest.ini` - Python testing configuration
- `claude-desktop-config.json` - Claude Desktop MCP configuration

### Environment & Credentials (Keep - Required)
- `.env.example` - Example environment variables
- `.env.local` - Local environment (created by scripts)
- `.azure-credentials` - Azure login credentials (created by scripts)

## Organized Directories

### `src/` - Azure Function Source Code
- `function_app.py` - Main Azure Functions code
- `requirements.txt` - Python dependencies
- `host.json` - Azure Functions host configuration

### `infrastructure/` - Azure Infrastructure
- `main.bicep` - Infrastructure as Code
- `parameters.json` - Deployment parameters

### `tests/` - Test Suite
- `__init__.py` - Python package marker
- `test_mcp_server.py` - MCP server tests

### `docs/` - Documentation
- `MCP_CONFIGURATION.md` - MCP setup guide
- `MCP_TROUBLESHOOTING.md` - Troubleshooting guide
- `PIPELINE_SETUP.md` - CI/CD setup guide
- `SETUP_COMPLETE.md` - Post-deployment guide
- `GIT_MULTI_REPO_GUIDE.md` - Git workflow guide

### `scripts/` - Utility Scripts
- `get-function-keys.sh` - Extract Azure function keys
- `push-both.sh` - Git multi-repo push
- `test-functions.sh` - Test function endpoints
- `verify-mcp-server.sh` - Verify MCP functionality

### `local-server/` - Local MCP Development
- `mcp-bridge-server.js` - Local MCP bridge server
- `package.json` - Node.js dependencies
- `package-lock.json` - Lock file
- `node_modules/` - Node.js packages
- `test-mcp-client.py` - Python MCP test client
- `test-mcp-tools.py` - MCP tool tests

### `.azure-pipelines/` - CI/CD Pipeline
- Azure DevOps pipeline configuration

## File Cleanup Status

✅ **Organized**: All files properly categorized and moved to appropriate directories
✅ **Documentation**: All docs moved to `docs/` folder  
✅ **Scripts**: All utility scripts moved to `scripts/` folder and made executable
✅ **Local Development**: MCP server files moved to `local-server/` folder
✅ **Configuration**: Updated paths in config files
✅ **Deployment**: Created `.funcignore` for clean Azure deployment

## Next Steps

1. **Test the reorganization**: Run scripts from new locations
2. **Update CI/CD**: Ensure pipeline works with new structure
3. **Validate deployment**: Confirm .funcignore excludes correct files
4. **Documentation**: All documentation now centralized in `docs/` folder