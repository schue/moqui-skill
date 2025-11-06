#!/usr/bin/env python3
"""
Moqui Service Generator

Generates Moqui service templates based on common patterns.
This script helps create boilerplate service definitions quickly.

Usage:
    generate_service.py --verb <verb> --noun <noun> --type <type>
    generate_service.py --interactive

Types:
    create - Create new record service
    update - Update existing record service  
    find - Find/search records service
    get - Get single record service
    delete - Delete record service
    custom - Custom service with actions
"""

import sys
import os
from datetime import datetime

def generate_create_service(verb, noun, entity_name=None):
    """Generate a create service template."""
    if not entity_name:
        entity_name = f"com.example.{noun}"
    
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true">
        <description>Create a new {noun.lower()} record</description>
        <implements service="org.moqui.impl.ServiceInterface"/>
        
        <in-parameters>
            <parameter name="description" type="text-medium" required="true"/>
            <parameter name="statusId" type="id"/>
            <parameter name="{{noun.lower()}}TypeEnumId" type="id"/>
        </in-parameters>
        
        <out-parameters>
            <parameter name="{{noun.lower()}}Id" type="id"/>
            <parameter name="{noun.lower()}" type="Map"/>
        </out-parameters>
        
        <actions>
            <entity-create entity-name="{entity_name}" include-nonpk="true"/>
            <set field="{{noun.lower()}}" from="ec.entity.get({entity_name}.class, {{noun.lower()}}Id)"/>
        </actions>
    </service>
    
</services>'''
    
    return service_template.replace('{{noun.lower()}}', noun.lower())

def generate_update_service(verb, noun, entity_name=None):
    """Generate an update service template."""
    if not entity_name:
        entity_name = f"com.example.{noun}"
    
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true">
        <description>Update an existing {noun.lower()} record</description>
        <implements service="org.moqui.impl.ServiceInterface"/>
        
        <in-parameters>
            <parameter name="{{noun.lower()}}Id" type="id" required="true"/>
            <parameter name="description" type="text-medium"/>
            <parameter name="statusId" type="id"/>
            <parameter name="{{noun.lower()}}TypeEnumId" type="id"/>
        </in-parameters>
        
        <out-parameters>
            <parameter name="{noun.lower()}" type="Map"/>
        </out-parameters>
        
        <actions>
            <entity-find-one entity-name="{entity_name}" value-field="{{noun.lower()}}"/>
            <if condition="{{noun.lower()}} == null">
                <return error="true" message="{noun} not found with ID: ${{{{noun.lower()}}}}Id"/>
            </if>
            <entity-update entity-name="{entity_name}" include-nonpk="true"/>
        </actions>
    </service>
    
</services>'''
    
    return service_template.replace('{{noun.lower()}}', noun.lower())

def generate_find_service(verb, noun, entity_name=None):
    """Generate a find service template."""
    if not entity_name:
        entity_name = f"com.example.{noun}"
    
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true" allow-remote="true">
        <description>Find {noun.lower()} records with optional filtering</description>
        
        <in-parameters>
            <parameter name="{{noun.lower()}}TypeEnumId"/>
            <parameter name="statusId"/>
            <parameter name="orderByField" default-value="description"/>
            <parameter name="pageIndex" type="Integer" default-value="0"/>
            <parameter name="pageSize" type="Integer" default-value="20"/>
        </in-parameters>
        
        <out-parameters>
            <parameter name="{noun.lower()}List" type="List"/>
            <parameter name="totalCount" type="Integer"/>
            <parameter name="pageIndex" type="Integer"/>
            <parameter name="pageSize" type="Integer"/>
        </out-parameters>
        
        <actions>
            <entity-find entity-name="{entity_name}" list="{noun.lower()}List" count="totalCount">
                <econdition field-name="{{noun.lower()}}TypeEnumId" ignore-if-empty="true"/>
                <econdition field-name="statusId" ignore-if-empty="true"/>
                <order-by field-name="${{orderByField}}"/>
            </entity-find>
            
            <if condition="pageIndex &amp;&amp; pageSize">
                <script>
                    def startIdx = pageIndex * pageSize
                    def endIdx = startIdx + pageSize
                    {noun.lower()}List = {noun.lower()}List.subList(startIdx, Math.min(endIdx, {noun.lower()}List.size()))
                </script>
            </if>
        </actions>
    </service>
    
</services>'''
    
    return service_template.replace('{{noun.lower()}}', noun.lower())

def generate_get_service(verb, noun, entity_name=None):
    """Generate a get service template."""
    if not entity_name:
        entity_name = f"com.example.{noun}"
    
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true" allow-remote="true">
        <description>Get a single {noun.lower()} record by ID</description>
        
        <in-parameters>
            <parameter name="{{noun.lower()}}Id" type="id" required="true"/>
        </in-parameters>
        
        <out-parameters>
            <parameter name="{noun.lower()}" type="Map"/>
        </out-parameters>
        
        <actions>
            <entity-find-one entity-name="{entity_name}" value-field="{{noun.lower()}}"/>
            <if condition="{{noun.lower()}} == null">
                <return error="true" message="{noun} not found with ID: ${{{{noun.lower()}}}}Id"/>
            </if>
        </actions>
    </service>
    
</services>'''
    
    return service_template.replace('{{noun.lower()}}', noun.lower())

def generate_delete_service(verb, noun, entity_name=None):
    """Generate a delete service template."""
    if not entity_name:
        entity_name = f"com.example.{noun}"
    
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true">
        <description>Delete a {noun.lower()} record</description>
        
        <in-parameters>
            <parameter name="{{noun.lower()}}Id" type="id" required="true"/>
        </in-parameters>
        
        <actions>
            <entity-find-one entity-name="{entity_name}" value-field="{{noun.lower()}}"/>
            <if condition="{{noun.lower()}} == null">
                <return error="true" message="{noun} not found with ID: ${{{{noun.lower()}}}}Id"/>
            </if>
            <entity-delete entity-name="{entity_name}"/>
        </actions>
    </service>
    
</services>'''
    
    return service_template.replace('{{noun.lower()}}', noun.lower())

def generate_custom_service(verb, noun):
    """Generate a custom service template."""
    service_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-3.xsd">
    
    <service verb="{verb}" noun="{noun}" authenticate="true">
        <description>Custom {verb} {noun.lower()} service</description>
        
        <in-parameters>
            <parameter name="inputParameter" type="text-medium" required="true"/>
            <!-- Add more parameters as needed -->
        </in-parameters>
        
        <out-parameters>
            <parameter name="result" type="Map"/>
            <parameter name="message" type="String"/>
        </out-parameters>
        
        <actions>
            <!-- Add your custom logic here -->
            <set field="result" from="[:]"/>
            <set field="result.processed" from="true"/>
            <set field="result.timestamp" from="ec.user.nowTimestamp"/>
            <set field="message" from="Custom {verb} {noun.lower()} completed successfully"/>
        </actions>
    </service>
    
</services>'''
    
    return service_template

def interactive_mode():
    """Run in interactive mode."""
    print("🚀 Moqui Service Generator - Interactive Mode")
    print("=" * 50)
    
    # Get service type
    print("\nAvailable service types:")
    print("1. create - Create new record")
    print("2. update - Update existing record")
    print("3. find - Find/search records")
    print("4. get - Get single record")
    print("5. delete - Delete record")
    print("6. custom - Custom service")
    
    while True:
        try:
            choice = input("\nSelect service type (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                break
            print("Please enter a number between 1 and 6")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
    
    type_map = {
        '1': 'create',
        '2': 'update', 
        '3': 'find',
        '4': 'get',
        '5': 'delete',
        '6': 'custom'
    }
    
    service_type = type_map[choice]
    
    # Get verb and noun
    if service_type == 'custom':
        verb = input("Enter verb (e.g., process, calculate): ").strip()
        noun = input("Enter noun (e.g., Order, Report): ").strip()
    else:
        verb = service_type
        noun = input(f"Enter noun (e.g., Product, User): ").strip()
    
    # Get entity name (optional)
    entity_name = input(f"Enter entity name (optional, default: com.example.{noun}): ").strip()
    if not entity_name:
        entity_name = None
    
    # Generate service
    if service_type == 'create':
        content = generate_create_service(verb, noun, entity_name)
    elif service_type == 'update':
        content = generate_update_service(verb, noun, entity_name)
    elif service_type == 'find':
        content = generate_find_service(verb, noun, entity_name)
    elif service_type == 'get':
        content = generate_get_service(verb, noun, entity_name)
    elif service_type == 'delete':
        content = generate_delete_service(verb, noun, entity_name)
    else:
        content = generate_custom_service(verb, noun)
    
    # Output file
    filename = f"{verb}{noun}.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Service generated: {filename}")
    print(f"📝 Service: {verb}#{noun}")
    print(f"📂 Entity: {entity_name or f'com.example.{noun}'}")
    print(f"\nNext steps:")
    print(f"1. Review and customize the generated service")
    print(f"2. Update parameter types and validation")
    print(f"3. Add business logic to the actions section")
    print(f"4. Test the service")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  generate_service.py --verb <verb> --noun <noun> --type <type> [--entity <entity>]")
        print("  generate_service.py --interactive")
        print("\nTypes: create, update, find, get, delete, custom")
        sys.exit(1)
    
    if sys.argv[1] == '--interactive':
        interactive_mode()
        return
    
    # Parse command line arguments
    verb = noun = service_type = entity_name = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--verb' and i + 1 < len(sys.argv):
            verb = sys.argv[i + 1]
            i += 2
        elif arg == '--noun' and i + 1 < len(sys.argv):
            noun = sys.argv[i + 1]
            i += 2
        elif arg == '--type' and i + 1 < len(sys.argv):
            service_type = sys.argv[i + 1]
            i += 2
        elif arg == '--entity' and i + 1 < len(sys.argv):
            entity_name = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not verb or not noun or not service_type:
        print("❌ Missing required arguments: --verb, --noun, --type")
        sys.exit(1)
    
    if service_type not in ['create', 'update', 'find', 'get', 'delete', 'custom']:
        print("❌ Invalid type. Use: create, update, find, get, delete, custom")
        sys.exit(1)
    
    # Generate service
    if service_type == 'create':
        content = generate_create_service(verb, noun, entity_name)
    elif service_type == 'update':
        content = generate_update_service(verb, noun, entity_name)
    elif service_type == 'find':
        content = generate_find_service(verb, noun, entity_name)
    elif service_type == 'get':
        content = generate_get_service(verb, noun, entity_name)
    elif service_type == 'delete':
        content = generate_delete_service(verb, noun, entity_name)
    else:
        content = generate_custom_service(verb, noun)
    
    # Output file
    filename = f"{verb}{noun}.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Service generated: {filename}")

if __name__ == "__main__":
    main()