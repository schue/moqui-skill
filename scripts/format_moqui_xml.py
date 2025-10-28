#!/usr/bin/env python3
"""
Moqui XML Formatter

Formats and pretty-prints Moqui XML files (entities, services, etc.)
This script helps maintain consistent XML formatting across Moqui projects.

Usage:
    format_moqui_xml.py <file.xml>
    format_moqui_xml.py --directory <path/to/xml/files>
"""

import sys
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def format_xml_file(file_path, backup=True):
    """Format a single XML file."""
    try:
        # Read original file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Convert to string with proper indentation
        rough_string = ET.tostring(root, encoding='unicode')
        
        # Pretty print using minidom
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")
        
        # Clean up minidom output
        # Remove XML declaration if present (we'll add our own)
        pretty_xml = re.sub(r'<\?xml[^>]*\?>\s*', '', pretty_xml)
        
        # Add proper XML declaration
        lines = pretty_xml.split('\n')
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
        
        # Reconstruct with proper formatting
        formatted_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        
        for i, line in enumerate(lines):
            if i == 0:  # Skip the first line (it's the root element)
                continue
            
            # Ensure proper indentation
            if line.strip():
                formatted_lines.append(line.rstrip())
        
        formatted_content = '\n'.join(formatted_lines)
        
        # Add final newline
        if not formatted_content.endswith('\n'):
            formatted_content += '\n'
        
        # Check if content changed
        if original_content == formatted_content:
            print(f"✅ {file_path} - already formatted")
            return True
        
        # Create backup if requested
        if backup:
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"💾 Backup created: {backup_path}")
        
        # Write formatted content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"✅ {file_path} - formatted successfully")
        return True
        
    except ET.ParseError as e:
        print(f"❌ {file_path} - XML parse error: {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path} - formatting error: {e}")
        return False

def format_directory(directory_path, backup=True):
    """Format all XML files in a directory."""
    xml_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    if not xml_files:
        print("❌ No XML files found in directory")
        return False
    
    print(f"📁 Found {len(xml_files)} XML files")
    
    all_success = True
    for xml_file in xml_files:
        if not format_xml_file(xml_file, backup):
            all_success = False
    
    return all_success

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  format_moqui_xml.py <file.xml>")
        print("  format_moqui_xml.py --directory <path/to/xml/files>")
        print("  format_moqui_xml.py --directory <path> --no-backup")
        sys.exit(1)
    
    backup = True
    if '--no-backup' in sys.argv:
        backup = False
    
    if sys.argv[1] == '--directory':
        if len(sys.argv) < 3:
            print("❌ Directory path required")
            sys.exit(1)
        directory = sys.argv[2]
        if not os.path.isdir(directory):
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        success = format_directory(directory, backup)
    else:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        success = format_xml_file(file_path, backup)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()