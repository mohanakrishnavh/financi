#!/usr/bin/env python3
"""
Version Management Script
Automatically syncs version across all project files.
"""

import re
import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
VERSION_FILE = PROJECT_ROOT / "VERSION"
FUNCTION_APP = PROJECT_ROOT / "src" / "function_app.py"


def get_current_version():
    """Read version from VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return None


def update_function_app_version(version):
    """Update version in function_app.py."""
    content = FUNCTION_APP.read_text()
    
    # Pattern to match: "version": "X.Y.Z"
    pattern = r'"version":\s*"[0-9]+\.[0-9]+\.[0-9]+"'
    replacement = f'"version": "{version}"'
    
    updated_content = re.sub(pattern, replacement, content)
    
    if content != updated_content:
        FUNCTION_APP.write_text(updated_content)
        print(f"✅ Updated version in {FUNCTION_APP.relative_to(PROJECT_ROOT)}")
        return True
    else:
        print(f"ℹ️  Version already correct in {FUNCTION_APP.relative_to(PROJECT_ROOT)}")
        return False


def validate_version(version):
    """Validate semantic version format."""
    pattern = r'^[0-9]+\.[0-9]+\.[0-9]+$'
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}. Must be X.Y.Z (e.g., 1.2.0)")
    return True


def bump_version(bump_type='patch'):
    """
    Bump version number.
    
    Args:
        bump_type: 'major', 'minor', or 'patch'
    """
    current = get_current_version()
    if not current:
        print("❌ No VERSION file found. Creating with version 1.0.0")
        current = "1.0.0"
    
    major, minor, patch = map(int, current.split('.'))
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Use 'major', 'minor', or 'patch'")
    
    new_version = f"{major}.{minor}.{patch}"
    set_version(new_version)
    return new_version


def set_version(version):
    """Set version in all project files."""
    validate_version(version)
    
    # Update VERSION file
    VERSION_FILE.write_text(version + '\n')
    print(f"✅ Updated VERSION file to {version}")
    
    # Update function_app.py
    update_function_app_version(version)
    
    print(f"\n🎉 Version set to {version}")
    print("\n📝 Next steps:")
    print("   1. Review changes: git diff")
    print("   2. Commit: git add VERSION src/function_app.py")
    print(f"   3. Commit: git commit -m 'Bump version to {version}'")
    print("   4. Push: ./scripts/push-both.sh")


def show_version():
    """Display current version."""
    version = get_current_version()
    if version:
        print(f"Current version: {version}")
    else:
        print("❌ VERSION file not found")
    
    # Also check function_app.py
    if FUNCTION_APP.exists():
        content = FUNCTION_APP.read_text()
        match = re.search(r'"version":\s*"([0-9]+\.[0-9]+\.[0-9]+)"', content)
        if match:
            app_version = match.group(1)
            if app_version == version:
                print(f"✅ function_app.py: {app_version} (synced)")
            else:
                print(f"⚠️  function_app.py: {app_version} (out of sync!)")
                print(f"   Run: python scripts/version.py sync")


def sync_versions():
    """Sync version from VERSION file to all other files."""
    version = get_current_version()
    if not version:
        print("❌ VERSION file not found. Create it first.")
        sys.exit(1)
    
    print(f"Syncing version {version} across all files...")
    update_function_app_version(version)
    print("✅ Version sync complete")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/version.py show              # Show current version")
        print("  python scripts/version.py bump [type]       # Bump version (major/minor/patch)")
        print("  python scripts/version.py set <version>     # Set specific version")
        print("  python scripts/version.py sync              # Sync VERSION to all files")
        print()
        print("Examples:")
        print("  python scripts/version.py bump patch        # 1.2.0 -> 1.2.1")
        print("  python scripts/version.py bump minor        # 1.2.0 -> 1.3.0")
        print("  python scripts/version.py bump major        # 1.2.0 -> 2.0.0")
        print("  python scripts/version.py set 2.0.0         # Set to 2.0.0")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'show':
        show_version()
    elif command == 'bump':
        bump_type = sys.argv[2] if len(sys.argv) > 2 else 'patch'
        bump_version(bump_type)
    elif command == 'set':
        if len(sys.argv) < 3:
            print("❌ Please provide a version number")
            sys.exit(1)
        set_version(sys.argv[2])
    elif command == 'sync':
        sync_versions()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
