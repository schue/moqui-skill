# Moqui Field Types Reference

This document provides a comprehensive reference of all available Moqui field types with usage examples and best practices.

## Primary Key Types

### id
**Description**: Standard primary key field type (32-character string)
**Usage**: Primary keys for most entities
**Format**: 32-character alphanumeric string
**Example**:
```xml
<field name="exampleId" type="id" is-pk="true"/>
```

### id-long
**Description**: Long primary key field type (64-character string)
**Usage**: Primary keys for entities with very large datasets
**Format**: 64-character alphanumeric string
**Example**:
```xml
<field name="longExampleId" type="id-long" is-pk="true"/>
```

## Text Field Types

### text-short
**Description**: Short text field
**Length**: Up to 50 characters
**Usage**: Short codes, abbreviations, short names
**Example**:
```xml
<field name="code" type="text-short"/>
<field name="abbreviation" type="text-short"/>
```

### text-medium
**Description**: Medium text field
**Length**: Up to 255 characters
**Usage**: Names, descriptions, titles, standard text fields
**Example**:
```xml
<field name="description" type="text-medium" enable-localization="true"/>
<field name="title" type="text-medium"/>
<field name="email" type="text-medium"/>
```

### text-long
**Description**: Long text field
**Length**: Up to 4000 characters
**Usage**: Long descriptions, notes, comments
**Example**:
```xml
<field name="longDescription" type="text-long" enable-localization="true"/>
<field name="notes" type="text-long"/>
```

### text-very-long
**Description**: Very long text field (CLOB)
**Length**: Unlimited (stored as CLOB)
**Usage**: Documents, large content, HTML, JSON data
**Example**:
```xml
<field name="content" type="text-very-long"/>
<field name="documentBody" type="text-very-long"/>
<field name="jsonData" type="text-very-long"/>
```

## Numeric Field Types

### number-integer
**Description**: Integer numbers
**Range**: -2,147,483,648 to 2,147,483,647 (32-bit signed integer)
**Usage**: Counts, sequence numbers, IDs, quantities
**Example**:
```xml
<field name="sequenceNum" type="number-integer"/>
<field name="quantity" type="number-integer"/>
<field name="count" type="number-integer"/>
```

### number-float
**Description**: Floating point numbers
**Precision**: Single-precision (32-bit)
**Usage**: Measurements, percentages, approximate values
**Example**:
```xml
<field name="percentage" type="number-float"/>
<field name="temperature" type="number-float"/>
<field name="weight" type="number-float"/>
```

### number-decimal
**Description**: Decimal numbers with exact precision
**Precision**: 18 digits total, 6 decimal places
**Usage**: Monetary values, precise measurements, calculations
**Example**:
```xml
<field name="amount" type="number-decimal"/>
<field name="price" type="number-decimal"/>
<field name="taxRate" type="number-decimal"/>
```

### currency-amount
**Description**: Currency amounts (specialized decimal)
**Precision**: 18 digits total, 6 decimal places
**Usage**: Monetary values, financial calculations
**Features**: Automatic currency formatting and conversion
**Example**:
```xml
<field name="totalAmount" type="currency-amount"/>
<field name="unitPrice" type="currency-amount"/>
<field name="taxAmount" type="currency-amount"/>
```

## Date and Time Types

### date
**Description**: Date only (no time)
**Format**: YYYY-MM-DD
**Usage**: Birth dates, event dates, effective dates
**Example**:
```xml
<field name="birthDate" type="date"/>
<field name="effectiveDate" type="date"/>
<field name="expiryDate" type="date"/>
```

### time
**Description**: Time only (no date)
**Format**: HH:MM:SS
**Usage**: Opening hours, scheduled times
**Example**:
```xml
<field name="openingTime" type="time"/>
<field name="closingTime" type="time"/>
```

### date-time
**Description**: Date and time
**Format**: YYYY-MM-DD HH:MM:SS.SSS
**Usage**: Timestamps, creation dates, event times
**Example**:
```xml
<field name="createdDate" type="date-time"/>
<field name="lastUpdatedStamp" type="date-time"/>
<field name="eventDateTime" type="date-time"/>
```

### timestamp
**Description**: Timestamp (same as date-time)
**Format**: YYYY-MM-DD HH:MM:SS.SSS
**Usage**: Alternative to date-time
**Example**:
```xml
<field name="timestamp" type="timestamp"/>
```

## Boolean and Indicator Types

### boolean
**Description**: Boolean true/false values
**Values**: true/false
**Usage**: Boolean flags, switches
**Example**:
```xml
<field name="isActive" type="boolean"/>
<field name="hasPermission" type="boolean"/>
<field name="isDeleted" type="boolean"/>
```

### text-indicator
**Description**: Indicator field (Y/N values)
**Values**: 'Y'/'N' (single character)
**Usage**: Status indicators, flags
**Default**: Usually defaults to 'N'
**Example**:
```xml
<field name="enabled" type="text-indicator" default="'N'"/>
<field name="isPrimary" type="text-indicator" default="'N'"/>
<field name="hasAttachment" type="text-indicator" default="'N'"/>
```

## Special Field Types

### binary-very-long
**Description**: Binary data (BLOB)
**Usage**: File attachments, images, binary content
**Example**:
```xml
<field name="attachment" type="binary-very-long"/>
<field name="imageData" type="binary-very-long"/>
```

## Field Attributes

### Common Attributes

#### is-pk
**Description**: Marks field as primary key
**Values**: true/false
**Example**:
```xml
<field name="exampleId" type="id" is-pk="true"/>
```

#### enable-audit-log
**Description**: Track changes to this field
**Values**: true/false
**Example**:
```xml
<field name="statusId" type="id" enable-audit-log="true"/>
<field name="amount" type="currency-amount" enable-audit-log="true"/>
```

#### enable-localization
**Description**: Field supports multiple languages
**Values**: true/false
**Example**:
```xml
<field name="description" type="text-medium" enable-localization="true"/>
<field name="name" type="text-medium" enable-localization="true"/>
```

#### encrypt
**Description**: Encrypt field data
**Values**: true/false
**Example**:
```xml
<field name="creditCardNumber" type="text-medium" encrypt="true"/>
<field name="ssn" type="text-medium" encrypt="true"/>
```

#### not-null
**Description**: Field cannot be null
**Values**: true/false
**Example**:
```xml
<field name="requiredField" type="text-medium" not-null="true"/>
```

#### default
**Description**: Default value for field
**Example**:
```xml
<field name="enabled" type="text-indicator" default="'N'"/>
<field name="sequenceNum" type="number-integer" default="0"/>
<field name="createdDate" type="date-time" default="ec.user.nowTimestamp"/>
```

## Field Naming Conventions

### Primary Keys
- `{entityName}Id` - Standard primary key
- `{entityName}Id` - Use `id-long` for very large datasets

**Examples**:
```xml
<field name="userId" type="id" is-pk="true"/>
<field name="productId" type="id" is-pk="true"/>
<field name="transactionId" type="id-long" is-pk="true"/>
```

### Foreign Keys
- `{relatedEntity}Id` - Foreign key reference
- Match the related entity's primary key name

**Examples**:
```xml
<field name="userId" type="id"/> <!-- References User.userId -->
<field name="productId" type="id"/> <!-- References Product.productId -->
<field name="statusId" type="id"/> <!-- References StatusItem.statusId -->
```

### Type Fields
- `{field}TypeEnumId` - Enumeration type reference
- `{field}TypeId` - Type reference

**Examples**:
```xml
<field name="productTypeEnumId" type="id"/>
<field name="statusTypeId" type="id"/>
<field name="paymentMethodTypeEnumId" type="id"/>
```

### Date Range Fields
- `fromDate` - Start date/time
- `thruDate` - End date/time

**Examples**:
```xml
<field name="fromDate" type="date-time"/>
<field name="thruDate" type="date-time"/>
```

### Audit Fields
- `createdDate` - Creation timestamp
- `createdByUserAccountId` - Creator user ID
- `lastUpdatedStamp` - Last update timestamp
- `lastUpdatedByUserAccountId` - Last updater user ID

**Examples**:
```xml
<field name="createdDate" type="date-time"/>
<field name="createdByUserAccountId" type="id" enable-audit-log="true"/>
<field name="lastUpdatedStamp" type="date-time"/>
<field name="lastUpdatedByUserAccountId" type="id" enable-audit-log="true"/>
```

### Status Fields
- `statusId` - Status reference
- `{entity}StatusId` - Entity-specific status

**Examples**:
```xml
<field name="statusId" type="id" enable-audit-log="true"/>
<field name="orderStatusId" type="id" enable-audit-log="true"/>
```

## Common Field Patterns

### Standard Entity Pattern
```xml
<entity entity-name="Example" package="com.example">
    <!-- Primary Key -->
    <field name="exampleId" type="id" is-pk="true"/>
    
    <!-- Basic Fields -->
    <field name="name" type="text-medium" enable-localization="true"/>
    <field name="description" type="text-long" enable-localization="true"/>
    <field name="sequenceNum" type="number-integer"/>
    
    <!-- Status -->
    <field name="statusId" type="id" enable-audit-log="true"/>
    
    <!-- Audit Fields -->
    <field name="createdDate" type="date-time"/>
    <field name="createdByUserAccountId" type="id" enable-audit-log="true"/>
    <field name="lastUpdatedStamp" type="date-time"/>
    <field name="lastUpdatedByUserAccountId" type="id" enable-audit-log="true"/>
</entity>
```

### Configuration Entity Pattern
```xml
<entity entity-name="ConfigExample" package="com.example" use="configuration" cache="true">
    <field name="configExampleId" type="id" is-pk="true"/>
    <field name="configKey" type="text-medium" not-null="true"/>
    <field name="configValue" type="text-very-long"/>
    <field name="description" type="text-medium" enable-localization="true"/>
    <field name="enabled" type="text-indicator" default="'Y'"/>
</entity>
```

### Transactional Entity Pattern
```xml
<entity entity-name="TransactionExample" package="com.example" use="transactional">
    <field name="transactionExampleId" type="id" is-pk="true"/>
    <field name="transactionDate" type="date-time" not-null="true"/>
    <field name="amount" type="currency-amount" not-null="true"/>
    <field name="description" type="text-medium"/>
    <field name="statusId" type="id" enable-audit-log="true"/>
    <field name="createdDate" type="date-time"/>
    <field name="createdByUserAccountId" type="id" enable-audit-log="true"/>
</entity>
```

## Best Practices

### Choosing Field Types
1. **Use appropriate length** - Don't use text-very-long for short strings
2. **Use numeric types correctly** - number-decimal for money, number-integer for counts
3. **Use date-time for timestamps** - Not separate date and time fields
4. **Use text-indicator for Y/N flags** - Not boolean for database compatibility
5. **Use currency-amount for money** - Not number-decimal

### Field Attributes
1. **Enable audit logging** for important fields
2. **Enable localization** for user-facing text
3. **Encrypt sensitive data** like SSN, credit cards
4. **Set appropriate defaults** for indicators and booleans
5. **Use not-null** for required fields

### Performance Considerations
1. **Avoid text-very-long** when possible (use separate attachment table)
2. **Use appropriate indexes** for foreign keys and query fields
3. **Consider field size** for large datasets
4. **Use caching** for configuration entities
5. **Optimize date queries** with proper indexing

### Data Integrity
1. **Use proper field types** for data validation
2. **Set constraints** for business rules
3. **Use audit fields** for tracking changes
4. **Implement referential integrity** with relationships
5. **Validate input** at service level