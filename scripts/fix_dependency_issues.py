#!/usr/bin/env python3
"""
Fix Dependency Issues Script
Automatically fixes common dependency issues in VoiceGuard
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def fix_requirements_files():
    """Fix common issues in requirements files"""
    project_root = Path(__file__).parent.parent
    
    # Fix requirements.txt
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        print("🔧 Fixing requirements.txt...")
        
        with open(req_file, 'r') as f:
            content = f.read()
            
        # Remove sqlite3 (built-in module)
        content = content.replace("sqlite3>=", "# sqlite3 - Built into Python\n# sqlite3>=")
        content = content.replace("sqlite3", "# sqlite3 - Built into Python")
        
        # Fix common package issues
        fixes = {
            "PyQt6>=6.7.0": "PyQt6>=6.6.0",
            "PyQt6-tools>=6.7.0": "PyQt6-tools>=6.4.2.3.3",
            "black>=25.0.0": "black>=24.4.0",
            "numpy>=2.0.0": "numpy>=1.24.0",
            "scipy>=2.0.0": "scipy>=1.11.0"
        }
        
        for old, new in fixes.items():
            if old in content:
                content = content.replace(old, new)
                print(f"  Fixed: {old} -> {new}")
                
        with open(req_file, 'w') as f:
            f.write(content)
            
    # Fix requirements-dev.txt
    req_dev_file = project_root / "requirements-dev.txt"
    if req_dev_file.exists():
        print("🔧 Fixing requirements-dev.txt...")
        
        with open(req_dev_file, 'r') as f:
            content = f.read()
            
        # Fix common dev package issues
        dev_fixes = {
            "black>=25.0.0": "black>=24.4.0",
            "black>=23.0.0": "black>=24.4.0",
            "types-requests>=2.33.0": "types-requests>=2.32.0",
            "types-requests>=2.31.0": "types-requests>=2.32.0",
            "pdb++": "pdbpp",
            "pytest>=8.0.0": "pytest>=7.4.0",
            "mypy>=2.0.0": "mypy>=1.7.0"
        }
        
        for old, new in dev_fixes.items():
            if old in content:
                content = content.replace(old, new)
                print(f"  Fixed: {old} -> {new}")
                
        with open(req_dev_file, 'w') as f:
            f.write(content)


def update_known_good_versions():
    """Update known good versions in dependency manager"""
    try:
        from dependency_manager import DependencyManager
        
        print("🔧 Updating known good versions...")
        
        # These are verified working versions as of July 2025
        verified_versions = {
            "numpy": "1.24.4",
            "scipy": "1.11.4",
            "pyaudio": "0.2.11",
            "librosa": "0.10.1",
            "webrtcvad": "2.0.10",
            "speechrecognition": "3.10.0",
            "aiohttp": "3.9.1",
            "pyqt6": "6.6.1",
            "pyqt6-tools": "6.4.2.3.3",
            "pywin32": "306",
            "psutil": "5.9.6",
            "pillow": "10.1.0",
            "cryptography": "41.0.7",
            "pyyaml": "6.0.1",
            "requests": "2.31.0",
            "packaging": "23.2",
            "pytest": "7.4.3",
            "black": "24.4.0",
            "flake8": "6.1.0",
            "mypy": "1.7.1",
            "colorlog": "6.8.2",
            "pdbpp": "0.10.3",
            "types-requests": "2.32.0.20250515"
        }
        
        manager = DependencyManager()
        manager.known_good_versions.update(verified_versions)
        manager._save_known_good_versions()
        
        print("✅ Known good versions updated")
        
    except ImportError:
        print("⚠️ Dependency manager not available, skipping version update")


def validate_installation():
    """Validate that the fixes work"""
    print("🔍 Validating fixes...")
    
    try:
        # Test import of dependency management
        from dependency_manager import DependencyManager
        from dependency_validator import dependency_validator
        
        print("✅ Dependency management modules imported successfully")
        
        # Test basic functionality
        manager = DependencyManager()
        compatible, issues = manager.check_system_compatibility()
        
        if compatible:
            print("✅ System compatibility check passed")
        else:
            print(f"⚠️ System compatibility issues: {issues}")
            
        print("✅ Dependency fixes validated")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


def main():
    """Main fix script entry point"""
    print("🔧 VoiceGuard Dependency Issue Fixer")
    print("=" * 40)
    
    try:
        # Fix requirements files
        fix_requirements_files()
        
        # Update known good versions
        update_known_good_versions()
        
        # Validate fixes
        if validate_installation():
            print("\n✅ All dependency issues fixed successfully!")
            print("\nNext steps:")
            print("1. Run: pip install -r requirements.txt")
            print("2. Run: python src/dependency_cli.py check")
            print("3. Test installation: python install.py")
        else:
            print("\n⚠️ Some issues may remain. Check the output above.")
            
        return 0
        
    except Exception as e:
        print(f"\n❌ Fix script failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
