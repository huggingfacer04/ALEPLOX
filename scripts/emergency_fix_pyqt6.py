#!/usr/bin/env python3
"""
Emergency PyQt6-tools Version Fix
Completely fixes all PyQt6-tools version issues across the entire project
"""

import os
import sys
import subprocess
from pathlib import Path


def fix_all_files():
    """Fix PyQt6-tools version in all files"""
    project_root = Path(__file__).parent.parent
    
    print("🔧 Emergency PyQt6-tools Version Fix")
    print("=" * 40)
    
    # Files to check and fix
    files_to_fix = [
        "requirements.txt",
        "requirements-dev.txt", 
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "config/dependency_config.json",
        "src/dependency_manager.py"
    ]
    
    # Version replacements
    replacements = {
        "PyQt6-tools>=6.5.0": "PyQt6-tools>=6.4.2.3.3",
        "PyQt6-tools>=6.7.0": "PyQt6-tools>=6.4.2.3.3", 
        "PyQt6>=6.7.0": "PyQt6>=6.6.0",
        "PyQt6>=6.5.0": "PyQt6>=6.6.0",
        '"pyqt6": "6.7.1"': '"pyqt6": "6.6.1"',
        '"pyqt6-tools": "6.5.0"': '"pyqt6-tools": "6.4.2.3.3"'
    }
    
    fixed_files = []
    
    for file_path in files_to_fix:
        full_path = project_root / file_path
        
        if not full_path.exists():
            continue
            
        print(f"Checking {file_path}...")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Apply all replacements
            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    print(f"  Fixed: {old} -> {new}")
                    
            # Write back if changed
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"  ✅ Updated {file_path}")
            else:
                print(f"  ✅ {file_path} already correct")
                
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
            
    return fixed_files


def clear_pip_cache():
    """Clear pip cache to avoid cached version issues"""
    print("\n🧹 Clearing pip cache...")
    
    try:
        # Clear pip cache
        result = subprocess.run([
            sys.executable, "-m", "pip", "cache", "purge"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Pip cache cleared")
        else:
            print(f"⚠️ Could not clear pip cache: {result.stderr}")
            
    except Exception as e:
        print(f"⚠️ Error clearing pip cache: {e}")


def create_fixed_requirements():
    """Create a completely fixed requirements.txt"""
    project_root = Path(__file__).parent.parent
    req_file = project_root / "requirements.txt"
    
    print("\n📝 Creating fixed requirements.txt...")
    
    # Known working requirements
    fixed_requirements = """# VoiceGuard Emergency Shutdown Service - Production Dependencies
# Updated with verified available package versions

# Core scientific computing
numpy>=1.24.0
scipy>=1.11.0

# Audio processing
PyAudio>=0.2.11
librosa>=0.10.1
webrtcvad>=2.0.10
SpeechRecognition>=3.10.0

# Web and networking
aiohttp>=3.9.0
requests>=2.31.0

# GUI framework - FIXED VERSIONS
PyQt6>=6.6.0
PyQt6-tools>=6.4.2.3.3

# Windows integration
pywin32>=306
psutil>=5.9.0

# Image processing
Pillow>=10.1.0

# Security and encryption
cryptography>=41.0.0

# Configuration and data
PyYAML>=6.0.0
packaging>=23.2

# Development and formatting
black>=24.4.0

# Logging
colorlog>=6.8.0

# Note: sqlite3 is built into Python and doesn't need installation
"""
    
    try:
        with open(req_file, 'w') as f:
            f.write(fixed_requirements)
        print("✅ Fixed requirements.txt created")
        return True
    except Exception as e:
        print(f"❌ Error creating fixed requirements: {e}")
        return False


def test_installation():
    """Test that the fixed versions can be installed"""
    print("\n🧪 Testing PyQt6-tools installation...")
    
    try:
        # Test if we can get info about the package
        result = subprocess.run([
            sys.executable, "-m", "pip", "index", "versions", "PyQt6-tools"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyQt6-tools package information retrieved")
            print("Available versions:")
            for line in result.stdout.split('\n'):
                if 'Available versions:' in line or line.strip().startswith('6.'):
                    print(f"  {line.strip()}")
        else:
            print(f"⚠️ Could not get package info: {result.stderr}")
            
        # Test specific version
        print("\nTesting specific version 6.4.2.3.3...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--dry-run", "PyQt6-tools==6.4.2.3.3"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Version 6.4.2.3.3 is installable")
        else:
            print(f"❌ Version 6.4.2.3.3 test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Installation test error: {e}")


def main():
    """Main emergency fix function"""
    try:
        # Fix all files
        fixed_files = fix_all_files()
        
        # Clear pip cache
        clear_pip_cache()
        
        # Create completely fixed requirements
        create_fixed_requirements()
        
        # Test installation
        test_installation()
        
        print(f"\n🎯 Emergency Fix Summary:")
        print(f"  Files fixed: {len(fixed_files)}")
        print(f"  Fixed files: {', '.join(fixed_files) if fixed_files else 'None needed fixing'}")
        
        print(f"\n✅ Emergency fix completed!")
        print(f"\nNext steps:")
        print(f"1. Try installing again: pip install -r requirements.txt")
        print(f"2. If still failing, try: pip install PyQt6-tools==6.4.2.3.3")
        print(f"3. Check available versions: pip index versions PyQt6-tools")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Emergency fix failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
