# Moqui Service Writer Skill

An Anthropic-style skill for creating, validating, and modifying Moqui framework services, entities, and queries.

## Overview

This skill provides comprehensive guidance for writing correct Moqui XML definitions, following framework patterns and conventions. It includes validation tools, reference documentation, and templates to help developers avoid common pitfalls when working with the Moqui enterprise framework.

## Features

### 🛠️ Validation Tools
- **Service Validator** (`scripts/validate_service.py`) - Validates service XML files for patterns and structure
- **Entity Validator** (`scripts/validate_entity.py`) - Validates entity XML files for patterns and conventions
- **XML Formatter** (`scripts/format_moqui_xml.py`) - Formats and pretty-prints Moqui XML files

### 📝 Generation Tools
- **Service Generator** (`scripts/generate_service.py`) - Interactive service template generator for common patterns

### 📚 Reference Documentation
- **Service Patterns** (`references/service_patterns.md`) - Common service patterns and examples
- **Entity Patterns** (`references/entity_patterns.md`) - Entity design patterns and relationships
- **Query Examples** (`references/query_examples.md`) - Entity-find query patterns and examples
- **Security Patterns** (`references/security_patterns.md`) - Authentication, authorization, and security patterns
- **Field Types** (`references/field_types.md`) - Complete field type reference with usage examples

### 📋 Templates
- **Service Template** (`assets/service_template.xml`) - Empty service template with proper structure
- **Entity Template** (`assets/entity_template.xml`) - Complete entity template with common patterns
- **Component Template** (`assets/component_template.xml`) - Component configuration template

## Quick Start

### For New Moqui Development
1. Generate service templates: `python3 scripts/generate_service.py --interactive`
2. Create entity definitions using `assets/entity_template.xml` as a starting point
3. Validate XML files with `scripts/validate_service.py` and `scripts/validate_entity.py`
4. Format XML consistently using `scripts/format_moqui_xml.py`

### For Existing Moqui Projects
1. Validate current files to identify issues and improvements
2. Reference patterns in `references/` for best practices
3. Use templates in `assets/` for new components
4. Apply consistent formatting across all XML files

## Usage Examples

### Generate a Service
```bash
# Interactive mode
python3 scripts/generate_service.py --interactive

# Direct generation
python3 scripts/generate_service.py --verb create --noun Product --type create
```

### Validate Files
```bash
# Validate single service file
python3 scripts/validate_service.py service/ExampleServices.xml

# Validate entire directory
python3 scripts/validate_service.py --directory service/

# Validate entities
python3 scripts/validate_entity.py entity/ExampleEntities.xml
```

### Format XML
```bash
# Format single file with backup
python3 scripts/format_moqui_xml.py service/ExampleServices.xml

# Format directory without backup
python3 scripts/format_moqui_xml.py --directory entity/ --no-backup
```

## Skill Structure

```
moqui-service-writer/
├── SKILL.md                    # Main skill documentation
├── README.md                    # This file
├── scripts/                     # Executable tools
│   ├── validate_service.py       # Service validation
│   ├── validate_entity.py        # Entity validation
│   ├── generate_service.py       # Service generation
│   └── format_moqui_xml.py     # XML formatting
├── references/                  # Reference documentation
│   ├── service_patterns.md       # Service patterns
│   ├── entity_patterns.md        # Entity patterns
│   ├── query_examples.md        # Query examples
│   ├── security_patterns.md      # Security patterns
│   └── field_types.md          # Field type reference
└── assets/                      # Template files
    ├── service_template.xml      # Service template
    ├── entity_template.xml       # Entity template
    └── component_template.xml   # Component template
```

## Compatibility

This skill is designed for use with:
- **Moqui Framework** 2.1+
- **Python** 3.6+
- **Anthropic Claude** with skill support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly with Moqui projects
5. Submit a pull request

## License

This skill is provided under the same terms as specified in the LICENSE.txt file.

## Support

For issues and questions:
1. Check the comprehensive documentation in `SKILL.md`
2. Review the reference materials in `references/`
3. Test with the validation tools provided
4. Check common issues in the troubleshooting section of `SKILL.md`

---

**Note**: This skill is designed to complement the existing Moqui framework documentation by providing practical, hands-on assistance for common development tasks.