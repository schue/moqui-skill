# Moqui Entity Query Examples

This document provides common entity query patterns and examples for reference when writing Moqui services and screen actions.

## Basic Query Patterns

### Find Single Record
```xml
<entity-find-one entity-name="com.example.Example" value-field="example">
    <field-map field-name="exampleId" from="exampleId"/>
</entity-find-one>
```

### Find Multiple Records
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" value="EsActive"/>
    <order-by field-name="description"/>
</entity-find>
```

### Find with Count
```xml
<entity-find entity-name="com.example.Example" list="exampleList" count="totalCount">
    <econdition field-name="statusId" value="EsActive"/>
</entity-find>
```

## Filtering Patterns

### Simple Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" value="EsActive"/>
    <econdition field-name="exampleTypeEnumId" value="EtTypeA"/>
    <order-by field-name="description"/>
</entity-find>
```

### Ignore Empty Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" from="statusId" ignore-if-empty="true"/>
    <econdition field-name="exampleTypeEnumId" from="exampleTypeEnumId" ignore-if-empty="true"/>
    <order-by field-name="description"/>
</entity-find>
```

### Like/Contains Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="description" operator="like" value="${description}%"/>
    <order-by field-name="description"/>
</entity-find>
```

### In List Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" in="statusIdList"/>
    <order-by field-name="description"/>
</entity-find>
```

### Between Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="createdDate" operator="greater-equals" from="fromDate"/>
    <econdition field-name="createdDate" operator="less" from="thruDate"/>
    <order-by field-name="createdDate"/>
</entity-find>
```

## Date Filtering

### Date Range Filter
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <date-filter valid-date="effectiveDate"/>
    <order-by field-name="description"/>
</entity-find>
```

### Custom Date Range
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="fromDate" operator="less-equals" from="effectiveDate"/>
    <econdition field-name="thruDate" operator="greater" from="effectiveDate" 
                ignore-if-empty="true"/>
    <order-by field-name="description"/>
</entity-find>
```

### Recent Records
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="createdDate" operator="greater-equals" 
                from="${ec.user.nowTimestamp - 7}"/>
    <order-by field-name="createdDate" descending="true"/>
</entity-find>
```

## Ordering and Pagination

### Single Field Ordering
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <order-by field-name="description"/>
</entity-find>
```

### Multiple Field Ordering
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <order-by field-name="sequenceNum"/>
    <order-by field-name="description"/>
</entity-find>
```

### Descending Order
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <order-by field-name="createdDate" descending="true"/>
</entity-find>
```

### Pagination
```xml
<entity-find entity-name="com.example.Example" list="exampleList" count="totalCount">
    <econdition field-name="statusId" value="EsActive"/>
    <order-by field-name="description"/>
</entity-find>

<!-- Manual pagination in script -->
<script>
def startIdx = pageIndex * pageSize
def endIdx = startIdx + pageSize
exampleList = exampleList.subList(startIdx, Math.min(endIdx, exampleList.size()))
</script>
```

## Complex Queries

### Subquery Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="exampleId" 
                in="select exampleId from com.example.ExampleDetail where statusId = 'EdActive'"/>
    <order-by field-name="description"/>
</entity-find>
```

### Join Conditions
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" value="EsActive"/>
    <econdition entity-alias="ST" field-name="description" operator="like" value="${statusFilter}%"/>
    <relationship-join relationship="status"/>
    <order-by field-name="description"/>
</entity-find>
```

### View Entity Queries
```xml
<entity-find entity-name="com.example.ExampleAndStatus" list="exampleList">
    <econdition field-name="statusId" value="EsActive"/>
    <econdition field-name="statusDescription" operator="like" value="${statusFilter}%"/>
    <order-by field-name="description"/>
</entity-find>
```

## Query with Relationships

### Using Relationship Short Alias
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="status.description" operator="like" value="${statusFilter}%"/>
    <relationship-join relationship="status"/>
    <order-by field-name="description"/>
</entity-find>
```

### Multiple Relationship Joins
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="status.description" operator="like" value="${statusFilter}%"/>
    <econdition field-name="type.description" operator="like" value="${typeFilter}%"/>
    <relationship-join relationship="status"/>
    <relationship-join relationship="type"/>
    <order-by field-name="description"/>
</entity-find>
```

## Conditional Queries

### Dynamic Field Selection
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <select-field field-name="exampleId"/>
    <select-field field-name="description"/>
    <if condition="includeStatus">
        <select-field field-name="statusId"/>
    </if>
    <order-by field-name="description"/>
</entity-find>
```

### Conditional Ordering
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <if condition="orderBy == 'name'">
        <order-by field-name="description"/>
    <else/>
        <order-by field-name="createdDate" descending="true"/>
    </if>
</entity-find>
```

## Performance Optimization

### Limit Results
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <econdition field-name="statusId" value="EsActive"/>
    <order-by field-name="description"/>
    <limit-range start="0" size="100"/>
</entity-find>
```

### Select Specific Fields
```xml
<entity-find entity-name="com.example.Example" list="exampleList">
    <select-field field-name="exampleId"/>
    <select-field field-name="description"/>
    <econdition field-name="statusId" value="EsActive"/>
    <order-by field-name="description"/>
</entity-find>
```

### Use Cache
```xml
<entity-find entity-name="com.example.Example" list="exampleList" cache="true">
    <econdition field-name="statusId" value="EsActive"/>
    <order-by field-name="description"/>
</entity-find>
```

## Data Manipulation Queries

### Create Record
```xml
<entity-create entity-name="com.example.Example" include-nonpk="true"/>
```

### Update Record
```xml
<entity-update entity-name="com.example.Example" include-nonpk="true"/>
```

### Delete Record
```xml
<entity-delete entity-name="com.example.Example"/>
```

### Delete by Condition
```xml
<entity-delete-by-condition entity-name="com.example.Example">
    <econdition field-name="statusId" value="EsDraft"/>
</entity-delete-by-condition>
```

### Bulk Operations
```xml
<entity-find entity-name="com.example.Example" list="examplesToUpdate">
    <econdition field-name="statusId" value="EsDraft"/>
</entity-find>

<iterate list="examplesToUpdate" entry="example">
    <set field="example.statusId" from="'EsActive'"/>
    <entity-update value-field="example"/>
</iterate>
```

## Advanced Patterns

### Hierarchical Queries
```xml
<!-- Find all children of a parent -->
<entity-find entity-name="com.example.Example" list="childList">
    <econdition field-name="parentExampleId" from="parentExampleId"/>
    <order-by field-name="sequenceNum"/>
</entity-find>
```

### Tree Traversal
```xml
<!-- Find all descendants (recursive) -->
<script>
def findDescendants(parentId, result = []) {
    def children = ec.entity.find("com.example.Example").condition("parentExampleId", parentId).list()
    for (child in children) {
        result.add(child)
        findDescendants(child.exampleId, result)
    }
    return result
}

def allDescendants = findDescendants(rootExampleId)
</script>
```

### Aggregation Queries
```xml
<!-- Count by status -->
<entity-find entity-name="com.example.Example" list="statusCounts">
    <select-field field-name="statusId"/>
    <select-field field-name="exampleId" function="count"/>
    <group-by field-name="statusId"/>
</entity-find>
```

### Custom SQL Queries
```xml
<!-- For complex queries not possible with entity-find -->
<script>
def sql = """
    SELECT e.exampleId, e.description, COUNT(d.exampleDetailId) as detailCount
    FROM com.example.Example e
    LEFT JOIN com.example.ExampleDetail d ON e.exampleId = d.exampleId
    WHERE e.statusId = 'EsActive'
    GROUP BY e.exampleId, e.description
    ORDER BY detailCount DESC
"""

def results = ec.entity.sqlFind(sql, [maxRows: 100])
</script>
```

## Error Handling

### Check Record Existence
```xml
<entity-find-one entity-name="com.example.Example" value-field="example"/>
<if condition="example == null">
    <return error="true" message="Example not found with ID: ${exampleId}"/>
</if>
```

### Validate Query Results
```xml
<entity-find entity-name="com.example.Example" list="exampleList"/>
<if condition="exampleList.isEmpty()">
    <message type="warning">No examples found matching criteria</message>
</if>
```

## Best Practices

1. **Use ignore-if-empty** for optional filter conditions
2. **Add proper ordering** for consistent results
3. **Use pagination** for large result sets
4. **Select specific fields** when possible for performance
5. **Use view entities** for complex queries
6. **Add error handling** for missing records
7. **Use date-filter** for time-sensitive data
8. **Cache frequently accessed data**
9. **Limit result size** for performance
10. **Use relationships** instead of joins when possible