#!/usr/bin/env python3
"""
Moqui Entity Validator

Validates Moqui entity XML files for common patterns and structure.
This script helps ensure entity definitions follow correct Moqui framework patterns.

Usage:
    validate_entity.py <entity-file.xml>
    validate_entity.py --directory <path/to/entities>
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Common Moqui field types
VALID_FIELD_TYPES = {
    'id', 'id-long', 'text-short', 'text-medium', 'text-long', 'text-very-long',
    'number-integer', 'number-float', 'number-decimal', 'currency-amount',
    'date', 'time', 'date-time', 'timestamp', 'boolean', 'text-indicator'
}

def check_entity_patterns(xml_file):
    """Check for common Moqui entity pattern compliance."""
    issues = []
    suggestions = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Check root element
        if root.tag != 'entities':
            issues.append("Root element should be 'entities'")
        
        # Check namespace
        if 'http://moqui.org/xsd/entity-definition-3.xsd' not in str(root.attrib):
            suggestions.append("Consider adding XSD namespace: xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='http://moqui.org/xsd/entity-definition-3.xsd'")
        
        # Check each entity
        for entity in root.findall('entity'):
            entity_name = entity.get('entity-name', 'unnamed entity')
            package_name = entity.get('package', 'no package')
            
            # Check required attributes
            if not entity.get('entity-name'):
                issues.append(f"Entity missing entity-name attribute")
            if not entity.get('package'):
                issues.append(f"Entity '{entity_name}': missing package attribute")
            
            # Check naming conventions
            if entity_name and not entity_name.replace('_', '').isalnum():
                suggestions.append(f"Entity '{entity_name}': consider using alphanumeric with underscores")
            
            # Check fields
            fields = entity.findall('field')
            if not fields:
                issues.append(f"Entity '{entity_name}': no fields defined")
            
            primary_keys = []
            for field in fields:
                field_name = field.get('name')
                field_type = field.get('type')
                is_pk = field.get('is-pk') == 'true'
                
                if not field_name:
                    issues.append(f"Entity '{entity_name}': field missing name")
                    continue
                
                if not field_type:
                    issues.append(f"Entity '{entity_name}': field '{field_name}' missing type")
                elif field_type not in VALID_FIELD_TYPES:
                    suggestions.append(f"Entity '{entity_name}': field '{field_name}' has unknown type '{field_type}'")
                
                # Check primary key naming
                if is_pk:
                    primary_keys.append(field_name)
                    expected_pk_name = f"{entity_name.lower()}Id"
                    if field_name != expected_pk_name:
                        suggestions.append(f"Entity '{entity_name}': primary key '{field_name}' should probably be '{expected_pk_name}'")
                
                # Check common field patterns
                if field_name.endswith('Id') and field_type != 'id':
                    suggestions.append(f"Entity '{entity_name}': field '{field_name}' ending with 'Id' should probably be type 'id'")
                
                if field_name.endswith('Date') and field_type and 'date' not in field_type:
                    suggestions.append(f"Entity '{entity_name}': field '{field_name}' ending with 'Date' should probably be a date type")
            
            # Check if entity has primary key
            if not primary_keys:
                issues.append(f"Entity '{entity_name}': no primary key fields defined")
            
            # Check relationships
            for relationship in entity.findall('relationship'):
                rel_type = relationship.get('type')
                related = relationship.get('related')
                short_alias = relationship.get('short-alias')
                
                if not rel_type:
                    issues.append(f"Entity '{entity_name}': relationship missing type")
                elif rel_type not in ['one', 'many', 'one-nofk']:
                    suggestions.append(f"Entity '{entity_name}': relationship type '{rel_type}' should be 'one', 'many', or 'one-nofk'")
                
                if not related:
                    issues.append(f"Entity '{entity_name}': relationship missing related entity")
                
                if not short_alias:
                    suggestions.append(f"Entity '{entity_name}': relationship should have short-alias for easier access")
                
                # Check key-maps
                key_maps = relationship.findall('key-map')
                if not key_maps:
                    issues.append(f"Entity '{entity_name}': relationship missing key-map elements")
                
                for key_map in key_maps:
                    if not key_map.get('field-name'):
                        issues.append(f"Entity '{entity_name}': key-map missing field-name")
                
    except ET.ParseError as e:
        issues.append(f"XML Parse Error: {e}")
    except Exception as e:
        issues.append(f"Pattern check error: {e}")
    
    return issues, suggestions

def validate_entity_file(file_path):
    """Validate a single entity file."""
    print(f"\n🔍 Validating: {file_path}")
    
    try:
        # Basic XML validation
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        print("✅ XML is well-formed")
        
        # Pattern checks
        issues, suggestions = check_entity_patterns(file_path)
        
        if issues:
            print("\n⚠️  Issues found:")
            for issue in issues:
                print(f"  • {issue}")
        
        if suggestions:
            print("\n💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        
        if not issues and not suggestions:
            print("✅ No issues found - entity follows Moqui patterns")
        
        return len(issues) == 0
        
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return False

def validate_directory(directory_path):
    """Validate all entity files in a directory."""
    entity_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                # Quick check if it's an entity file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        if '<entity' in content:
                            entity_files.append(file_path)
                except:
                    pass
    
    if not entity_files:
        print("❌ No entity XML files found in directory")
        return False
    
    print(f"📁 Found {len(entity_files)} entity files")
    
    all_valid = True
    for entity_file in entity_files:
        if not validate_entity_file(entity_file):
            all_valid = False
    
    return all_valid

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  validate_entity.py <entity-file.xml>")
        print("  validate_entity.py --directory <path/to/entities>")
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
        
        success = validate_entity_file(file_path)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()