# Moqui Service Patterns Reference

This document provides common Moqui service patterns and examples for reference when writing services.

## Service Structure Template

```xml
<service verb="verb" noun="Noun" authenticate="true" allow-remote="false">
    <description>Brief description of what the service does</description>
    <implements service="org.moqui.impl.ServiceInterface"/>
    
    <in-parameters>
        <!-- Input parameters -->
    </in-parameters>
    
    <out-parameters>
        <!-- Output parameters -->
    </out-parameters>
    
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

## Common Service Verbs

- **create** - Create new records
- **update** - Modify existing records
- **store** - Create or update (upsert)
- **delete** - Remove records
- **find** - Search/retrieve records
- **get** - Retrieve single record
- **set** - Set/update values
- **increment** - Increment counters
- **enable/disable** - Change status
- **reset** - Reset to initial state
- **calculate** - Perform calculations
- **process** - Process data/workflows
- **send** - Send notifications/emails
- **validate** - Validate data/rules

## Authentication Levels

```xml
<!-- No authentication required -->
<service verb="methodName" noun="ObjectName" authenticate="anonymous-all"/>

<!-- Read-only, no login required -->
<service verb="methodName" noun="ObjectName" authenticate="anonymous-view"/>

<!-- User must be logged in -->
<service verb="methodName" noun="ObjectName" authenticate="true"/>

<!-- Requires specific role -->
<service verb="methodName" noun="ObjectName" authenticate="true" 
         require-all-roles="ADMIN"/>
```

## Parameter Patterns

### Required Parameters
```xml
<parameter name="entityId" type="id" required="true"/>
```

### Optional Parameters with Defaults
```xml
<parameter name="statusId" type="id"/>
<parameter name="orderByField" default-value="description"/>
```

### Type Specifications
```xml
<parameter name="amount" type="BigDecimal"/>
<parameter name="recordList" type="List">
    <parameter name="record" type="Map"/></parameter>
```

### Validation
```xml
<parameter name="emailField"><text-email/></parameter>
<parameter name="codeField">
    <matches regexp="[A-Z]\w*" message="Must start with uppercase"/></parameter>
```

## Entity Auto Services

### Create Service
```xml
<service verb="create" noun="Example" type="entity-auto">
    <in-parameters>
        <auto-parameters entity-name="com.example.Example" include="nonpk"/>
    </in-parameters>
    <out-parameters>
        <parameter name="exampleId"/>
    </out-parameters>
</service>
```

### Update Service
```xml
<service verb="update" noun="Example" type="entity-auto">
    <in-parameters>
        <auto-parameters entity-name="com.example.Example" include="all"/>
    </in-parameters>
</service>
```

## Common Service Patterns

### Find with Filtering
```xml
<service verb="find" noun="Example" allow-remote="true">
    <in-parameters>
        <parameter name="exampleTypeEnumId"/>
        <parameter name="statusId"/>
        <parameter name="orderByField" default-value="description"/>
        <parameter name="pageIndex" type="Integer" default-value="0"/>
        <parameter name="pageSize" type="Integer" default-value="20"/>
    </in-parameters>
    <out-parameters>
        <parameter name="exampleList" type="List"/>
        <parameter name="totalCount" type="Integer"/>
    </out-parameters>
    <actions>
        <entity-find entity-name="com.example.Example" list="exampleList" count="totalCount">
            <econdition field-name="exampleTypeEnumId" ignore-if-empty="true"/>
            <econdition field-name="statusId" ignore-if-empty="true"/>
            <order-by field-name="${orderByField}"/>
        </entity-find>
    </actions>
</service>
```

### Service with Validation
```xml
<service verb="update" noun="Example">
    <in-parameters>
        <parameter name="exampleId" type="id" required="true"/>
        <parameter name="description" type="text-medium"/>
    </in-parameters>
    <actions>
        <entity-find-one entity-name="com.example.Example" value-field="example"/>
        <if condition="example == null">
            <return error="true" message="Example not found with ID: ${exampleId}"/>
        </if>
        <entity-update entity-name="com.example.Example" include-nonpk="true"/>
    </actions>
</service>
```

### Service with Permission Check
```xml
<service verb="delete" noun="Example" authenticate="true">
    <in-parameters>
        <parameter name="exampleId" type="id" required="true"/>
    </in-parameters>
    <actions>
        <set field="hasPermission" from="ec.user.hasPermission('EXAMPLE', 'DELETE')"/>
        <if condition="!hasPermission">
            <return error="true" message="You don't have permission to delete examples"/>
        </if>
        
        <entity-find-one entity-name="com.example.Example" value-field="example"/>
        <if condition="example == null">
            <return error="true" message="Example not found with ID: ${exampleId}"/>
        </if>
        
        <entity-delete entity-name="com.example.Example"/>
    </actions>
</service>
```

### Service with Transaction (Framework Default)
```xml
<service verb="process" noun="Example" authenticate="true">
    <in-parameters>
        <parameter name="exampleId" type="id" required="true"/>
    </in-parameters>
    <actions>
        <!-- All operations in this service will be in a single transaction -->
        <entity-find-one entity-name="com.example.Example" value-field="example"/>
        <entity-update entity-name="com.example.Example" include-nonpk="true"/>
        
        <!-- Call other services in same transaction -->
        <service-call name="create#ExampleHistory" in-map="[exampleId: exampleId, 
                        statusId: example.statusId, changeDate: ec.user.nowTimestamp]"/>
    </actions>
</service>
```

### Critical Financial Operation (Explicit Transaction)
```xml
<service verb="close" noun="FinancialPeriod" authenticate="true" 
         transaction="force-new" transaction-timeout="600">
    <in-parameters>
        <parameter name="financialPeriodId" type="id" required="true"/>
    </in-parameters>
    <actions>
        <!-- Critical financial closing - requires isolation -->
        <script>ec.transaction.commitBeginOnly();</script>
        <!-- Financial closing operations -->
    </actions>
</service>
```

**Note**: 98.5% of Moqui framework services use default transaction behavior (no attribute). Only add explicit transaction attributes for critical financial operations or long-running tasks (>5 minutes).

## Error Handling Patterns

### Return Error with Message
```xml
<return error="true" message="Error description here"/>
```

### Return Error with Public Message
```xml
<return error="true" message="Internal error" public="true" type="danger"/>
```

### Success Messages
```xml
<message public="true" type="success">Operation completed successfully</message>
<message public="true" type="warning">Warning message</message>
```

## User Context Access

```xml
<!-- Current user information -->
<set field="currentUserId" from="ec.user.userId"/>
<set field="currentUsername" from="ec.user.username"/>
<set field="currentPartyId" from="ec.user.partyId"/>

<!-- Current timestamp -->
<set field="nowTimestamp" from="ec.user.nowTimestamp"/>

<!-- User preferences -->
<set field="preference" from="ec.user.getPreference('key')"/>

<!-- Check user role -->
<set field="isAdmin" from="ec.user.isUserInRole('ADMIN')"/>
```

## Service Call Patterns

### Simple Service Call
```xml
<service-call name="create#Example" in-map="[description: 'New Example']"/>
```

### With Output
```xml
<service-call name="find#Example" out-parameter="exampleList" 
              in-map="[statusId: 'EsActive']"/>
```

### Async Service Call
```xml
<service-call name="process#Example" async="true" 
              in-map="[exampleId: exampleId]"/>
```

## Date Operations

```xml
<!-- Current timestamp -->
<set field="now" from="ec.user.nowTimestamp"/>

<!-- Date arithmetic -->
<set field="futureDate" from="ec.user.nowTimestamp + 30"/>

<!-- Date formatting -->
<set field="formattedDate" from="ec.l10n.format(date, 'yyyy-MM-dd')"/>

<!-- Date filtering in entity-find -->
<entity-find entity-name="com.example.Example" list="exampleList">
    <date-filter valid-date="effectiveDate"/>
</entity-find>
```

## Collection Operations

```xml
<!-- Initialize list -->
<set field="resultList" from="[]"/>

<!-- Add to list -->
<script>resultList.add([field1:value1, field2:value2])</script>

<!-- Iterate list -->
<iterate list="recordList" entry="record">
    <!-- Process each record -->
</iterate>

<!-- Filter list -->
<set field="activeRecords" from="recordList.findAll { it.statusId == 'EsActive' }"/>
```

## String Operations

```xml
<!-- Convert to camel case -->
<set field="camelCase" from="prettyToCamelCase(inputString, false)"/>

<!-- Generate random string -->
<set field="randomString" from="getRandomString(12)"/>

<!-- Hash/encrypt -->
<set field="hashedValue" from="ec.ecfi.getSimpleHash(inputValue, salt)"/>
```

## Best Practices

1. **Always include descriptions** for services and parameters
2. **Use proper authentication levels** based on service sensitivity
3. **Validate input parameters** before processing
4. **Return meaningful error messages** for debugging
5. **Use entity-auto services** for simple CRUD operations
6. **Implement permission checks** for sensitive operations
7. **Use transactions** for multi-step operations
8. **Follow verb-noun naming convention** consistently
9. **Include localization support** for user-facing text
10. **Add audit logging** for important operations