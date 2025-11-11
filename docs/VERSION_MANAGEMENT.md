# Version Management Guide

## Overview

The Financi project uses **automatic version management** to ensure consistency across all deployments. The version is maintained in a single source of truth and automatically propagated during the CI/CD pipeline.

---

## Version Sources

### Single Source of Truth: `VERSION` File

The `VERSION` file at the project root contains the current version:

```
1.2.0
```

This file is:
- ✅ **Automatically read** by the Azure DevOps pipeline
- ✅ **Validated** for semantic versioning format (X.Y.Z)
- ✅ **Propagated** to all deployment configurations

### Secondary Source: `function_app.py`

The version is also embedded in the code for runtime access:

```python
"version": "1.2.0"
```

---

## How It Works

### During CI/CD Pipeline

The Azure DevOps pipeline automatically:

1. **Extracts** version from `VERSION` file (or falls back to `function_app.py`)
2. **Validates** the version format
3. **Sets** environment variable `MCP_SERVER_VERSION` in Azure Functions
4. **Deploys** the application with the correct version

**No manual intervention required!** 🎉

### Version Extraction Script

In `.azure-pipelines/azure-pipelines.yml`:

```yaml
- script: |
    # Extract version from VERSION file (single source of truth)
    if [ -f "VERSION" ]; then
      VERSION=$(cat VERSION | tr -d '[:space:]')
      echo "✅ Version from VERSION file: $VERSION"
    else
      # Fallback to function_app.py
      VERSION=$(grep -oP '"version":\s*"\K[^"]+' src/function_app.py | head -1)
      echo "✅ Version from function_app.py: $VERSION"
    fi
    
    # Validate version format (semver: X.Y.Z)
    if [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo "✅ Valid version format: $VERSION"
      echo "##vso[task.setvariable variable=appVersion;isOutput=true]$VERSION"
    else
      echo "❌ Invalid version format: $VERSION"
      exit 1
    fi
  displayName: 'Extract Application Version'
```

---

## Version Management Script

We provide a Python script to help manage versions: `scripts/version.py`

### Usage

#### Show Current Version
```bash
python scripts/version.py show
```

Output:
```
Current version: 1.2.0
✅ function_app.py: 1.2.0 (synced)
```

#### Bump Version

**Patch version** (1.2.0 → 1.2.1):
```bash
python scripts/version.py bump patch
```

**Minor version** (1.2.0 → 1.3.0):
```bash
python scripts/version.py bump minor
```

**Major version** (1.2.0 → 2.0.0):
```bash
python scripts/version.py bump major
```

#### Set Specific Version
```bash
python scripts/version.py set 2.5.3
```

#### Sync Versions
If `VERSION` and `function_app.py` get out of sync:
```bash
python scripts/version.py sync
```

---

## Workflow for Releasing a New Version

### Option 1: Using the Script (Recommended)

```bash
# 1. Bump version
python scripts/version.py bump minor

# 2. Review changes
git diff

# 3. Commit and push
git add VERSION src/function_app.py
git commit -m "Bump version to 1.3.0"
./scripts/push-both.sh

# 4. Pipeline automatically deploys with new version! 🚀
```

### Option 2: Manual

```bash
# 1. Edit VERSION file
echo "1.3.0" > VERSION

# 2. Sync to other files
python scripts/version.py sync

# 3. Commit and push
git add VERSION src/function_app.py
git commit -m "Bump version to 1.3.0"
./scripts/push-both.sh
```

---

## Benefits

### ✅ Automatic
- No need to manually update pipeline YAML
- Version automatically extracted and validated
- Consistent across all environments

### ✅ Single Source of Truth
- `VERSION` file is the authoritative source
- Script ensures all files stay in sync
- No version mismatches

### ✅ Semantic Versioning
- Enforces X.Y.Z format
- Clear meaning: MAJOR.MINOR.PATCH
- Pipeline validates format

### ✅ Git-Friendly
- Version tracked in source control
- Easy to see version history
- Revert-friendly

---

## Version Scheme

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (1.X.0): New features, backward-compatible
- **PATCH** (1.2.X): Bug fixes, backward-compatible

### Examples

- `1.0.0` → `1.0.1`: Fixed a bug in stock price endpoint
- `1.0.0` → `1.1.0`: Added HTTP wrapper endpoints
- `1.0.0` → `2.0.0`: Changed API authentication method (breaking)

---

## Troubleshooting

### Version Mismatch

If `VERSION` and `function_app.py` show different versions:

```bash
python scripts/version.py show
```

Output:
```
Current version: 1.2.0
⚠️  function_app.py: 1.1.0 (out of sync!)
   Run: python scripts/version.py sync
```

**Solution:**
```bash
python scripts/version.py sync
```

### Pipeline Fails on Version Validation

**Error:**
```
❌ Invalid version format: 1.2
Version must follow semantic versioning (e.g., 1.2.0)
```

**Solution:**
Update `VERSION` file to use X.Y.Z format:
```bash
echo "1.2.0" > VERSION
```

### Checking Deployed Version

```bash
curl -s https://financi.azurewebsites.net/api/health | python3 -m json.tool | grep version
```

Output:
```json
"version": "1.2.0"
```

---

## Migration from Manual Version

### Before (Manual - ❌ BAD)
```yaml
# Hardcoded in pipeline YAML
"MCP_SERVER_VERSION=1.0.0"
```

**Problems:**
- Had to edit pipeline for every version bump
- Easy to forget to update
- Version in code vs. deployment could mismatch

### After (Automatic - ✅ GOOD)
```yaml
# Dynamically extracted
"MCP_SERVER_VERSION=$(appVersion)"
```

**Benefits:**
- Update `VERSION` file only
- Pipeline automatically uses it
- Always in sync

---

## Summary

| Task | Command |
|------|---------|
| Show current version | `python scripts/version.py show` |
| Bump patch (1.2.0 → 1.2.1) | `python scripts/version.py bump patch` |
| Bump minor (1.2.0 → 1.3.0) | `python scripts/version.py bump minor` |
| Bump major (1.2.0 → 2.0.0) | `python scripts/version.py bump major` |
| Set specific version | `python scripts/version.py set X.Y.Z` |
| Sync versions | `python scripts/version.py sync` |
| Check deployed version | `curl https://financi.azurewebsites.net/api/health` |

---

## Next Steps

1. **Use the script** to bump versions when releasing
2. **Never manually edit** the pipeline version anymore
3. **Always commit** `VERSION` file changes
4. **Let the pipeline** handle the rest automatically

🎉 Version management is now fully automated!
