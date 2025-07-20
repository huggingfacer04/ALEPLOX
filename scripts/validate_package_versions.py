#!/usr/bin/env python3
"""
Package Version Validator
Validates that all package versions in requirements files actually exist on PyPI
"""

import sys
import requests
import json
from pathlib import Path
from packaging import version
from typing import Dict, List, Tuple, Optional


def check_package_version(package_name: str, version_spec: str = None) -> Tuple[bool, str, List[str]]:
    """
    Check if a package version exists on PyPI
    Returns: (exists, latest_version, available_versions)
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        
        if response.status_code != 200:
            return False, "", []
            
        data = response.json()
        latest_version = data['info']['version']
        available_versions = list(data['releases'].keys())
        
        # Filter out versions with no files
        valid_versions = []
        for ver in available_versions:
            version_files = data['releases'][ver]
            if version_files:  # Has files
                valid_versions.append(ver)
                
        # Sort versions
        try:
            valid_versions = sorted(valid_versions, key=lambda v: version.parse(v), reverse=True)
        except:
            pass  # Keep original order if parsing fails
            
        if version_spec:
            # Check if specific version exists
            if version_spec in valid_versions:
                return True, version_spec, valid_versions
            else:
                return False, latest_version, valid_versions
        else:
            return True, latest_version, valid_versions
            
    except Exception as e:
        print(f"Error checking {package_name}: {e}")
        return False, "", []


def parse_requirements_file(file_path: Path) -> List[Tuple[str, str]]:
    """Parse requirements file and return list of (package, version_spec) tuples"""
    packages = []
    
    if not file_path.exists():
        return packages
        
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-r'):
                # Parse package name and version
                if '>=' in line:
                    package, version_spec = line.split('>=', 1)
                    packages.append((package.strip(), version_spec.strip()))
                elif '==' in line:
                    package, version_spec = line.split('==', 1)
                    packages.append((package.strip(), version_spec.strip()))
                elif '<' in line:
                    package = line.split('<')[0].strip()
                    packages.append((package, None))
                else:
                    packages.append((line.strip(), None))
                    
    return packages


def validate_requirements_files():
    """Validate all requirements files"""
    project_root = Path(__file__).parent.parent
    requirements_files = [
        project_root / "requirements.txt",
        project_root / "requirements-dev.txt"
    ]
    
    all_issues = []
    all_suggestions = {}
    
    for req_file in requirements_files:
        if not req_file.exists():
            continue
            
        print(f"\n🔍 Checking {req_file.name}...")
        packages = parse_requirements_file(req_file)
        
        for package_name, version_spec in packages:
            print(f"  Checking {package_name}...", end=" ")
            
            exists, latest_version, available_versions = check_package_version(package_name, version_spec)
            
            if not exists:
                if available_versions:
                    print(f"❌ Version {version_spec} not found")
                    print(f"    Available versions: {', '.join(available_versions[:5])}...")
                    
                    # Suggest closest version
                    if version_spec:
                        try:
                            target_version = version.parse(version_spec)
                            closest_version = None
                            min_diff = float('inf')
                            
                            for av in available_versions:
                                try:
                                    av_parsed = version.parse(av)
                                    if av_parsed <= target_version:
                                        diff = abs((target_version - av_parsed).total_seconds() if hasattr(target_version - av_parsed, 'total_seconds') else 0)
                                        if diff < min_diff:
                                            min_diff = diff
                                            closest_version = av
                                except:
                                    continue
                                    
                            if not closest_version and available_versions:
                                closest_version = available_versions[0]  # Latest
                                
                            if closest_version:
                                all_suggestions[package_name] = closest_version
                                print(f"    💡 Suggested: {closest_version}")
                        except:
                            if available_versions:
                                all_suggestions[package_name] = available_versions[0]
                                print(f"    💡 Suggested: {available_versions[0]}")
                    
                    all_issues.append(f"{package_name}: {version_spec} not found")
                else:
                    print(f"❌ Package not found on PyPI")
                    all_issues.append(f"{package_name}: Package not found")
            else:
                print("✅")
                
    return all_issues, all_suggestions


def update_requirements_with_suggestions(suggestions: Dict[str, str]):
    """Update requirements files with suggested versions"""
    project_root = Path(__file__).parent.parent
    requirements_files = [
        project_root / "requirements.txt",
        project_root / "requirements-dev.txt"
    ]
    
    for req_file in requirements_files:
        if not req_file.exists():
            continue
            
        print(f"\n📝 Updating {req_file.name}...")
        
        # Read current content
        with open(req_file, 'r') as f:
            lines = f.readlines()
            
        # Update lines
        updated_lines = []
        for line in lines:
            original_line = line.strip()
            
            if original_line and not original_line.startswith('#') and not original_line.startswith('-r'):
                # Extract package name
                package_name = original_line.split('>=')[0].split('==')[0].split('<')[0].strip()
                
                if package_name in suggestions:
                    new_version = suggestions[package_name]
                    new_line = f"{package_name}>={new_version}\n"
                    updated_lines.append(new_line)
                    print(f"  Updated {package_name}: {original_line} -> {package_name}>={new_version}")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
                
        # Write updated content
        with open(req_file, 'w') as f:
            f.writelines(updated_lines)


def main():
    """Main validation entry point"""
    print("🔍 VoiceGuard Package Version Validator")
    print("=" * 50)
    
    # Validate requirements files
    issues, suggestions = validate_requirements_files()
    
    # Summary
    print(f"\n📊 Validation Summary:")
    print(f"  Issues found: {len(issues)}")
    print(f"  Suggestions available: {len(suggestions)}")
    
    if issues:
        print(f"\n❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
            
    if suggestions:
        print(f"\n💡 Suggested fixes:")
        for package, suggested_version in suggestions.items():
            print(f"  - {package}: use version {suggested_version}")
            
        # Ask if user wants to apply suggestions
        response = input(f"\nApply suggested fixes? [y/N]: ")
        if response.lower() in ['y', 'yes']:
            update_requirements_with_suggestions(suggestions)
            print("✅ Requirements files updated!")
        else:
            print("ℹ️ No changes made")
    else:
        print("✅ All package versions are valid!")
        
    return 0 if not issues else 1


if __name__ == '__main__':
    sys.exit(main())
