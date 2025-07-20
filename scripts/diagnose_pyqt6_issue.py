#!/usr/bin/env python3
"""
Diagnose PyQt6-tools Installation Issues
Comprehensive diagnostic to find where the 6.5.0 version requirement is coming from
"""

import os
import sys
import subprocess
from pathlib import Path


def find_all_requirement_files():
    """Find all files that might contain package requirements"""
    project_root = Path(__file__).parent.parent
    
    print("🔍 Searching for all requirement files...")
    
    # File patterns to search
    patterns = [
        "requirements*.txt",
        "setup.py",
        "setup.cfg", 
        "pyproject.toml",
        "Pipfile",
        "environment.yml",
        "conda.yml",
        "*.requirements",
        "pip-requirements.txt"
    ]
    
    found_files = []
    
    for pattern in patterns:
        for file_path in project_root.rglob(pattern):
            if file_path.is_file():
                found_files.append(file_path)
                
    return found_files


def search_for_pyqt6_versions(files):
    """Search for PyQt6-tools version requirements in files"""
    print("\n🔍 Searching for PyQt6-tools version requirements...")
    
    problematic_files = []
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Search for PyQt6-tools requirements
            if 'PyQt6-tools' in content:
                print(f"\n📄 Found PyQt6-tools in: {file_path}")
                
                # Extract lines containing PyQt6-tools
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'PyQt6-tools' in line:
                        print(f"  Line {i}: {line.strip()}")
                        
                        # Check for problematic versions
                        if '>=6.5.0' in line or '>=6.7.0' in line:
                            problematic_files.append((file_path, i, line.strip()))
                            print(f"  ❌ PROBLEMATIC VERSION FOUND!")
                            
        except Exception as e:
            print(f"  ⚠️ Could not read {file_path}: {e}")
            
    return problematic_files


def check_pip_cache():
    """Check pip cache for cached requirements"""
    print("\n🗂️ Checking pip cache...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "cache", "list"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            cache_lines = result.stdout.split('\n')
            pyqt_cache = [line for line in cache_lines if 'pyqt6' in line.lower()]
            
            if pyqt_cache:
                print("Found PyQt6 related cache entries:")
                for line in pyqt_cache[:10]:  # Show first 10
                    print(f"  {line}")
            else:
                print("No PyQt6 related cache entries found")
        else:
            print(f"Could not list cache: {result.stderr}")
            
    except Exception as e:
        print(f"Error checking cache: {e}")


def check_virtual_environment():
    """Check virtual environment status"""
    print("\n🐍 Checking virtual environment...")
    
    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    print(f"In virtual environment: {in_venv}")
    print(f"Python executable: {sys.executable}")
    print(f"Python prefix: {sys.prefix}")
    
    if in_venv:
        print(f"Base prefix: {sys.base_prefix}")
        
    # Check pip freeze for current packages
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "freeze"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            installed_packages = result.stdout.split('\n')
            pyqt_packages = [pkg for pkg in installed_packages if 'pyqt6' in pkg.lower()]
            
            if pyqt_packages:
                print("Currently installed PyQt6 packages:")
                for pkg in pyqt_packages:
                    print(f"  {pkg}")
            else:
                print("No PyQt6 packages currently installed")
        else:
            print(f"Could not get installed packages: {result.stderr}")
            
    except Exception as e:
        print(f"Error checking installed packages: {e}")


def test_installation_command():
    """Test the exact installation command that's failing"""
    print("\n🧪 Testing installation commands...")
    
    commands_to_test = [
        ["pip", "install", "-r", "requirements.txt", "--dry-run"],
        ["pip", "install", "PyQt6-tools>=6.4.2.3.3", "--dry-run"],
        ["pip", "install", "PyQt6-tools==6.4.2.3.3", "--dry-run"]
    ]
    
    for cmd in commands_to_test:
        try:
            print(f"\nTesting: {' '.join(cmd)}")
            
            # Remove --dry-run if not supported
            if '--dry-run' in cmd:
                test_cmd = [c for c in cmd if c != '--dry-run']
                test_cmd.extend(['--no-deps', '--no-install'])
            else:
                test_cmd = cmd
                
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("  ✅ Command would succeed")
            else:
                print(f"  ❌ Command would fail: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("  ⏱️ Command timed out")
        except Exception as e:
            print(f"  ❌ Error testing command: {e}")


def provide_solutions(problematic_files):
    """Provide solutions based on findings"""
    print("\n💡 Solutions:")
    
    if problematic_files:
        print("❌ Found problematic version requirements:")
        for file_path, line_num, line_content in problematic_files:
            print(f"  {file_path}:{line_num} - {line_content}")
            
        print("\n🔧 To fix:")
        print("1. Edit the problematic files above")
        print("2. Replace PyQt6-tools>=6.5.0 with PyQt6-tools>=6.4.2.3.3")
        print("3. Replace PyQt6-tools>=6.7.0 with PyQt6-tools>=6.4.2.3.3")
        print("4. Clear pip cache: pip cache purge")
        print("5. Try installation again")
        
    else:
        print("✅ No problematic version requirements found in files")
        print("\n🔧 If you're still getting the error, try:")
        print("1. Clear pip cache: pip cache purge")
        print("2. Deactivate and recreate virtual environment")
        print("3. Check if you're running pip install from a different directory")
        print("4. Make sure you're using the correct requirements.txt file")
        
    print("\n📋 Quick fix commands:")
    print("pip cache purge")
    print("pip install PyQt6-tools==6.4.2.3.3")
    print("pip install -r requirements.txt")


def main():
    """Main diagnostic function"""
    print("🔍 PyQt6-tools Installation Issue Diagnostic")
    print("=" * 50)
    
    try:
        # Find all requirement files
        requirement_files = find_all_requirement_files()
        print(f"Found {len(requirement_files)} potential requirement files")
        
        # Search for PyQt6-tools versions
        problematic_files = search_for_pyqt6_versions(requirement_files)
        
        # Check pip cache
        check_pip_cache()
        
        # Check virtual environment
        check_virtual_environment()
        
        # Test installation commands
        test_installation_command()
        
        # Provide solutions
        provide_solutions(problematic_files)
        
        print(f"\n🎯 Diagnostic Summary:")
        print(f"  Requirement files found: {len(requirement_files)}")
        print(f"  Problematic files: {len(problematic_files)}")
        
        if problematic_files:
            print(f"  ❌ Issues found - see solutions above")
            return 1
        else:
            print(f"  ✅ No obvious issues found")
            return 0
            
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
