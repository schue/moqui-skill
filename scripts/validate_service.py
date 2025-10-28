#!/usr/bin/env python3
"""
Moqui Service Validator

Validates Moqui service XML files for common patterns and structure.
This script helps ensure service definitions follow correct Moqui framework patterns.

Usage:
    validate_service.py <service-file.xml>
    validate_service.py --directory <path/to/services>
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def check_service_patterns(xml_file):
    """Check for common Moqui service pattern compliance."""
    issues = []
    suggestions = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Check root element
        if root.tag != 'services':
            issues.append("Root element should be 'services'")
        
        # Check namespace
        if 'http://moqui.org/xsd/service-definition-3.xsd' not in str(root.attrib):
            suggestions.append("Consider adding XSD namespace: xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='http://moqui.org/xsd/service-definition-3.xsd'")
        
        # Check each service
        for service in root.findall('service'):
            verb = service.get('verb')
            noun = service.get('noun')
            service_name = f"{verb}#{noun}" if verb and noun else "unnamed service"
            
            # Check verb-noun naming
            if verb and noun:
                if not verb.islower():
                    issues.append(f"Service '{service_name}': verb should be lowercase")
                if not noun[0].isupper():
                    suggestions.append(f"Service '{service_name}': consider PascalCase for noun")
            elif not verb or not noun:
                issues.append(f"Service missing verb or noun attributes")
            
            # Check authentication
            auth = service.get('authenticate', 'true')
            if auth == 'true' and not service.get('require-all-roles'):
                suggestions.append(f"Service '{service_name}': consider adding require-all-roles for security")
            
            # Check parameters
            in_params = service.find('in-parameters')
            out_params = service.find('out-parameters')
            
            if in_params is not None:
                for param in in_params.findall('parameter'):
                    param_name = param.get('name')
                    if not param_name:
                        issues.append(f"Service '{service_name}': parameter missing name")
                    elif not param.get('type') and not param.get('required'):
                        suggestions.append(f"Parameter '{param_name}': consider adding type specification")
            
            # Check actions
            actions = service.find('actions')
            if actions is None:
                issues.append(f"Service '{service_name}': missing actions section")
            elif actions.text is None or not actions.text.strip():
                issues.append(f"Service '{service_name}': empty actions section")
                
    except ET.ParseError as e:
        issues.append(f"XML Parse Error: {e}")
    except Exception as e:
        issues.append(f"Pattern check error: {e}")
    
    return issues, suggestions

def validate_service_file(file_path):
    """Validate a single service file."""
    print(f"\n🔍 Validating: {file_path}")
    
    try:
        # Basic XML validation
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        print("✅ XML is well-formed")
        
        # Pattern checks
        issues, suggestions = check_service_patterns(file_path)
        
        if issues:
            print("\n⚠️  Issues found:")
            for issue in issues:
                print(f"  • {issue}")
        
        if suggestions:
            print("\n💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        
        if not issues and not suggestions:
            print("✅ No issues found - service follows Moqui patterns")
        
        return len(issues) == 0
        
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return False

def validate_directory(directory_path):
    """Validate all service files in a directory."""
    service_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                # Quick check if it's a service file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        if '<service' in content:
                            service_files.append(file_path)
                except:
                    pass
    
    if not service_files:
        print("❌ No service XML files found in directory")
        return False
    
    print(f"📁 Found {len(service_files)} service files")
    
    all_valid = True
    for service_file in service_files:
        if not validate_service_file(service_file):
            all_valid = False
    
    return all_valid

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  validate_service.py <service-file.xml>")
        print("  validate_service.py --directory <path/to/services>")
        sys.exit(1)
    
    if sys.argv[1] == '--directory':
        if len(sys.argv) < 3:
            print("❌ Directory path required")
            sys.exit(1)
        directory = sys.argv[2]
        if not os.path.isdir(directory):
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        success = validate_directory(directory)
    else:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        success = validate_service_file(file_path)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()