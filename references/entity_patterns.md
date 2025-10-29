# Moqui Entity Patterns Reference

This document provides common Moqui entity patterns and examples for reference when creating entities.

## Entity Hierarchies and Relationships

### Shipment Entity Hierarchy
Understanding Moqui's shipment entity relationships is crucial for proper tracking:

```
ShipmentHeader (overall shipment)
├── ShipmentRouteSegment (shipping leg/carrier)
│   ├── masterTrackingCode (overall tracking number)
│   └── masterTrackingUrl (overall tracking URL)
└── ShipmentPackageRouteSeg (individual packages)
    ├── trackingCode (package tracking number)
    └── trackingUrl (package tracking URL)
```

### Key Relationship Patterns
| Parent Entity | Child Entity | Relationship Type | Common Fields |
|--------------|--------------|------------------|----------------|
| OrderHeader | OrderPart | one-to-many | orderId, orderPartSeqId |
| ShipmentHeader | ShipmentRouteSegment | one-to-many | shipmentId |
| ShipmentRouteSegment | ShipmentPackageRouteSeg | one-to-many | shipmentId, shipmentRouteSegmentSeqId |
| OrderPart | ShipmentItemSourceOrderItem | one-to-many | orderId, orderPartSeqId |

### Tracking Field Patterns
Different entities use different field names for tracking:

| Entity | Tracking Number Field | Tracking URL Field | Usage |
|--------|-------------------|------------------|--------|
| ShipmentRouteSegment | masterTrackingCode | masterTrackingUrl | Overall shipment tracking |
| ShipmentPackageRouteSeg | trackingCode | trackingUrl | Individual package tracking |
| OrderPart | otherPartyOrderId | - | External system reference |

### Relationship Definition Examples
```xml
<!-- One-to-Many: Order to Order Parts -->
<relationship type="many" related="com.example.OrderPart" short-alias="parts">
    <key-map field-name="orderId"/></relationship>

<!-- Many-to-One: Order Part to Order -->
<relationship type="one" related="com.example.OrderHeader" short-alias="order">
    <key-map field-name="orderId"/></relationship>

<!-- One-to-Many with Composite Key: Route Segment to Packages -->
<relationship type="many" related="com.example.ShipmentPackageRouteSeg" short-alias="packages">
    <key-map field-name="shipmentId"/>
    <key-map field-name="shipmentRouteSegmentSeqId"/>
</relationship>
```

### Query Patterns for Hierarchies
```xml
<!-- Find all packages for a shipment -->
<entity-find entity-name="mantle.shipment.ShipmentPackageRouteSeg" list="packageList">
    <econdition field-name="shipmentId" from="shipmentId"/>
</entity-find>

<!-- Find route segment for packages -->
<entity-find entity-name="mantle.shipment.ShipmentRouteSegment" list="routeList">
    <econdition field-name="shipmentId" from="shipmentId"/>
</entity-find>

<!-- Join shipment with order parts -->
<entity-find entity-name="mantle.order.OrderPart" list="orderParts">
    <econdition field-name="orderId" from="orderId"/>
    <relationship-join relationship="orderItems"/>
</entity-find>
```

## Entity Structure Template

```xml
<entity entity-name="ExampleEntity" package="com.example" 
        short-alias="examples" cache="true" use="configuration">
    <!-- Primary key -->
    <field name="exampleEntityId" type="id" is-pk="true"/>
    
    <!-- Common fields -->
    <field name="description" type="text-medium" enable-localization="true"/>
    <field name="sequenceNum" type="number-integer"/>
    <field name="statusId" type="id" enable-audit-log="true"/>
    
    <!-- Audit fields -->
    <field name="createdDate" type="date-time"/>
    <field name="createdByUserAccountId" type="id" enable-audit-log="true"/>
    <field name="lastUpdatedStamp" type="date-time"/>
    
    <!-- Relationships -->
    <relationship type="one" related="moqui.basic.StatusItem" short-alias="status">
        <key-map field-name="statusId"/></relationship>
</entity>
```

## Field Types Reference

### Primary Keys
```xml
<field name="entityId" type="id" is-pk="true"/>
<field name="longEntityId" type="id-long" is-pk="true"/>
```

### Text Fields
```xml
<field name="textShort" type="text-short"/>      <!-- ~50 chars -->
<field name="textMedium" type="text-medium"/>    <!-- ~255 chars -->
<field name="textLong" type="text-long"/>        <!-- ~4000 chars -->
<field name="textVeryLong" type="text-very-long"/> <!-- CLOB -->
```

### Numeric Fields
```xml
<field name="numberInteger" type="number-integer"/>
<field name="numberFloat" type="number-float"/>
<field name="numberDecimal" type="number-decimal"/>
<field name="currencyAmount" type="currency-amount"/>
```

### Date/Time Fields
```xml
<field name="dateField" type="date"/>
<field name="timeField" type="time"/>
<field name="dateTimeField" type="date-time"/>
<field name="timestampField" type="timestamp"/>
```

### Indicator Fields
```xml
<field name="indicatorField" type="text-indicator" default="'N'"/>
<field name="booleanField" type="boolean"/>
```

### Date Range Fields
```xml
<field name="fromDate" type="date-time"/>
<field name="thruDate" type="date-time"/>
```

## Field Naming Conventions

### Primary Keys
- `{entityName}Id` (e.g., `userId`, `statusId`, `enumId`)
- Use `id-long` for very large datasets

### Foreign Keys
- `{relatedEntity}Id` (e.g., `userGroupId`, `statusTypeId`)
- Match the related entity's primary key name

### Type Fields
- `{field}TypeEnumId` (e.g., `statusTypeId`, `artifactTypeEnumId`)
- Reference enumeration type IDs

### Date Ranges
- `fromDate`/`thruDate` for validity periods
- Use `date-time` type for precision

### Audit Fields
- `createdDate`, `lastUpdatedStamp`, `createdByUserLogin`
- Enable audit logging with `enable-audit-log="true"`

## Common Field Attributes

```xml
<field name="fieldName" type="text-medium" 
        enable-audit-log="true"     <!-- Track changes -->
        enable-localization="true"    <!-- Translatable -->
        encrypt="true"              <!-- Encrypt sensitive data -->
        not-null="true"             <!-- Required field -->
        default="'N'"               <!-- Default value -->
        is-pk="true"                <!-- Primary key -->
/>
```

## Relationship Patterns

### One-to-Many (Parent to Children)
```xml
<!-- In parent entity -->
<relationship type="many" related="com.example.ChildEntity" short-alias="children">
    <key-map field-name="parentEntityId" related="childEntityId"/></relationship>

<!-- In child entity -->
<relationship type="one" related="com.example.ParentEntity" short-alias="parent">
    <key-map field-name="parentEntityId"/></relationship>
```

### Many-to-One (Child to Parent)
```xml
<relationship type="one" related="moqui.basic.StatusItem" short-alias="status">
    <key-map field-name="statusId"/></relationship>
```

### Self-Referencing (Hierarchical)
```xml
<relationship type="one-nofk" title="Parent" related="com.example.ExampleEntity" short-alias="parent">
    <key-map field-name="parentEntityId" related="exampleEntityId"/></relationship>

<relationship type="many" title="Children" related="com.example.ExampleEntity" short-alias="children">
    <key-map field-name="exampleEntityId" related="parentEntityId"/></relationship>
```

### Many-to-Many through Join Entity
```xml
<!-- In main entity -->
<relationship type="many" related="com.example.ExampleCategoryMember" short-alias="categories">
    <key-map field-name="exampleEntityId"/></relationship>

<!-- Join entity structure -->
<entity entity-name="ExampleCategoryMember" package="com.example">
    <field name="exampleEntityId" type="id" is-pk="true"/>
    <field name="categoryId" type="id" is-pk="true"/>
    <field name="fromDate" type="date-time" is-pk="true"/>
    <field name="thruDate" type="date-time"/>
    
    <relationship type="one" related="com.example.ExampleEntity" short-alias="example">
        <key-map field-name="exampleEntityId"/></relationship>
    <relationship type="one" related="com.example.Category" short-alias="category">
        <key-map field-name="categoryId"/></relationship>
</entity>
```

### Relationship with Title
```xml
<relationship type="one" title="Currency" related="moqui.basic.Uom" short-alias="currencyUom">
    <key-map field-name="currencyUomId"/></relationship>
```

## Entity Use Types

### Configuration Entities
```xml
<entity entity-name="ConfigEntity" package="com.example" use="configuration" cache="true">
    <!-- Cached configuration data -->
</entity>
```

### Transactional Entities
```xml
<entity entity-name="TransactionalEntity" package="com.example" use="transactional">
    <!-- Business transaction data with full audit -->
</entity>
```

### Non-transactional Entities
```xml
<entity entity-name="LogEntity" package="com.example" use="nontransactional" cache="never">
    <!-- Log data, no audit needed -->
</entity>
```

## Common Entity Attributes

```xml
<entity entity-name="ExampleEntity" package="com.example" 
        short-alias="examples"           <!-- Short alias for queries -->
        cache="true"                     <!-- Enable caching -->
        use="configuration"              <!-- Entity use type -->
        sequence-bank-size="10">         <!-- Sequence bank size for PKs -->
```

## View Entity Patterns

### Basic View Entity
```xml
<view-entity entity-name="ExampleAndStatus" package="com.example">
    <member-entity entity-alias="EX" entity-name="com.example.ExampleEntity"/>
    <member-relationship entity-alias="ST" join-from-alias="EX" relationship="status"/>
    <alias-all entity-alias="EX"/>
    <alias entity-alias="ST" name="statusDescription" field="description"/>
</view-entity>
```

### Complex View with Custom Joins
```xml
<view-entity entity-name="ExampleWithTypeAndStatus" package="com.example">
    <member-entity entity-alias="EX" entity-name="com.example.ExampleEntity"/>
    <member-entity entity-alias="TYPE" entity-name="moqui.basic.Enumeration" 
                 join-from-alias="EX">
        <key-map field-name="exampleTypeEnumId" related="enumId"/>
    </member-entity>
    <member-entity entity-alias="STATUS" entity-name="moqui.basic.StatusItem" 
                 join-from-alias="EX">
        <key-map field-name="statusId" related="statusId"/>
    </member-entity>
    
    <alias-all entity-alias="EX"/>
    <alias entity-alias="TYPE" name="typeDescription" field="description"/>
    <alias entity-alias="STATUS" name="statusDescription" field="description"/>
    
    <entity-condition>
        <econdition field-name="EX.statusId" value="EsActive"/>
        <order-by field-name="EX.description"/>
    </entity-condition>
</view-entity>
```

## Seed Data Patterns

### Enumeration Type and Values
```xml
<entity entity-name="ExampleEntity" package="com.example">
    <!-- ... fields ... -->
    <seed-data>
        <!-- Enumeration Type -->
        <moqui.basic.EnumerationType description="Example Type" enumTypeId="ExampleType"/>
        
        <!-- Enumeration Values -->
        <moqui.basic.Enumeration description="Type A" enumId="EtTypeA" 
                                 enumTypeId="ExampleType" sequenceNum="1"/>
        <moqui.basic.Enumeration description="Type B" enumId="EtTypeB" 
                                 enumTypeId="ExampleType" sequenceNum="2"/>
        
        <!-- Status Type -->
        <moqui.basic.StatusType description="Example Status" statusTypeId="ExampleStatus"/>
        
        <!-- Status Items -->
        <moqui.basic.StatusItem description="Draft" sequenceNum="1" 
                                statusId="EsDraft" statusTypeId="ExampleStatus"/>
        <moqui.basic.StatusItem description="Active" sequenceNum="10" 
                                statusId="EsActive" statusTypeId="ExampleStatus"/>
        <moqui.basic.StatusItem description="Inactive" sequenceNum="99" 
                                statusId="EsInactive" statusTypeId="ExampleStatus"/>
    </seed-data>
</entity>
```

### Default Data
```xml
<entity entity-name="ExampleEntity" package="com.example">
    <!-- ... fields ... -->
    <seed-data>
        <!-- Default records -->
        <com.example.ExampleEntity exampleEntityId="DEFAULT" description="Default Example"
                                  statusId="EsActive" sequenceNum="1"/>
    </seed-data>
</entity>
```

## Best Practices

### Entity Design
1. **Include audit fields** on transactional entities
2. **Use appropriate field types** for data
3. **Define relationships** with meaningful short-aliases
4. **Use view entities** for complex queries
5. **Add seed data** for enumerations and reference data

### Field Design
1. **Use consistent naming** conventions
2. **Add localization** for user-facing text
3. **Enable audit logging** for important fields
4. **Use proper defaults** for indicators
5. **Validate data types** match usage patterns

### Relationship Design
1. **Always define both sides** of relationships
2. **Use meaningful short-aliases** for easy access
3. **Consider performance** for large datasets
4. **Use join entities** for many-to-many relationships
5. **Add title attributes** for clarity

### Performance Considerations
1. **Enable caching** for configuration entities
2. **Use appropriate use types** (configuration vs transactional)
3. **Optimize view entities** for common queries
4. **Consider sequence bank size** for high-volume entities
5. **Index foreign keys** appropriately

## Common Pitfalls to Avoid

1. **Missing Dependencies** - Always declare component dependencies
2. **Incorrect Field Types** - Use appropriate field types
3. **Missing Relationships** - Define relationships for foreign keys
4. **No Authentication** - Set proper authentication on services
5. **Hardcoded Values** - Use enumerations instead
6. **SQL Injection** - Use entity-find with econdition
7. **Transaction Issues** - Set proper transaction attributes
8. **Missing Localization** - Use enable-localization for text
9. **Missing Audit Fields** - Include createdDate, lastUpdatedStamp
10. **Incorrect Naming** - Follow conventions consistently