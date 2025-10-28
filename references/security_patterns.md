# Moqui Security Patterns Reference

This document provides common Moqui security patterns and examples for implementing authentication, authorization, and access control.

## Authentication Levels

### No Authentication Required
```xml
<!-- Public service, no login needed -->
<service verb="get" noun="PublicData" authenticate="anonymous-all">
    <description>Publicly accessible data</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

### Read-Only Access
```xml
<!-- Read-only, no login required -->
<service verb="find" noun="PublicInfo" authenticate="anonymous-view">
    <description>Public information that can be read without login</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

### User Authentication Required
```xml
<!-- User must be logged in -->
<service verb="create" noun="Example" authenticate="true">
    <description>Create example record (requires login)</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

### Specific Role Required
```xml
<!-- Requires specific role -->
<service verb="admin" noun="Example" authenticate="true" 
         require-all-roles="ADMIN">
    <description>Admin only example management</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

### Multiple Roles Required
```xml
<!-- Requires all specified roles -->
<service verb="approve" noun="Example" authenticate="true" 
         require-all-roles="MANAGER,APPROVER">
    <description>Approve examples (requires both manager and approver roles)</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

### Any of Multiple Roles
```xml
<!-- Requires any of the specified roles -->
<service verb="review" noun="Example" authenticate="true" 
         require-any-roles="MANAGER,REVIEWER">
    <description>Review examples (manager or reviewer can access)</description>
    <actions>
        <!-- Service logic -->
    </actions>
</service>
```

## Permission Checking

### Basic Permission Check
```xml
<service verb="delete" noun="Example" authenticate="true">
    <description>Delete example record</description>
    <actions>
        <set field="hasPermission" from="ec.user.hasPermission('EXAMPLE', 'DELETE')"/>
        <if condition="!hasPermission">
            <return error="true" message="You don't have permission to delete examples"/>
        </if>
        
        <!-- Service logic -->
    </actions>
</service>
```

### Permission with Resource Check
```xml
<service verb="update" noun="Example" authenticate="true">
    <description>Update example record</description>
    <actions>
        <set field="hasPermission" from="ec.user.hasPermission('EXAMPLE', 'UPDATE', exampleId)"/>
        <if condition="!hasPermission">
            <return error="true" message="You don't have permission to update this example"/>
        </if>
        
        <!-- Service logic -->
    </actions>
</service>
```

### Complex Permission Logic
```xml
<service verb="process" noun="Example" authenticate="true">
    <description>Process example with complex permissions</description>
    <actions>
        <!-- Check basic permission -->
        <set field="hasBasicPermission" from="ec.user.hasPermission('EXAMPLE', 'PROCESS')"/>
        
        <!-- Check ownership or admin override -->
        <set field="isOwner" from="example.createdByUserAccountId == ec.user.userId"/>
        <set field="isAdmin" from="ec.user.isUserInRole('ADMIN')"/>
        
        <if condition="!hasBasicPermission &amp;&amp; !isOwner &amp;&amp; !isAdmin">
            <return error="true" message="Permission denied"/>
        </if>
        
        <!-- Service logic -->
    </actions>
</service>
```

## User Context Access

### Current User Information
```xml
<service verb="get" noun="UserInfo" authenticate="true">
    <description>Get current user information</description>
    <actions>
        <!-- Basic user info -->
        <set field="userId" from="ec.user.userId"/>
        <set field="username" from="ec.user.username"/>
        <set field="partyId" from="ec.user.partyId"/>
        
        <!-- User preferences -->
        <set field="theme" from="ec.user.getPreference('theme')"/>
        <set field="language" from="ec.user.getPreference('language')"/>
        
        <!-- Current timestamp -->
        <set field="nowTimestamp" from="ec.user.nowTimestamp"/>
        
        <return message="User information retrieved successfully"/>
    </actions>
</service>
```

### User Role Checking
```xml
<service verb="check" noun="UserRoles" authenticate="true">
    <description>Check user roles and permissions</description>
    <actions>
        <!-- Check specific role -->
        <set field="isManager" from="ec.user.isUserInRole('MANAGER')"/>
        <set field="isAdmin" from="ec.user.isUserInRole('ADMIN')"/>
        
        <!-- Get all user roles -->
        <set field="userRoles" from="ec.user.getUserRoles()"/>
        
        <!-- Check permission directly -->
        <set field="canCreate" from="ec.user.hasPermission('EXAMPLE', 'CREATE')"/>
        <set field="canUpdate" from="ec.user.hasPermission('EXAMPLE', 'UPDATE')"/>
        <set field="canDelete" from="ec.user.hasPermission('EXAMPLE', 'DELETE')"/>
        
        <return message="Role check completed"/>
    </actions>
</service>
```

## Data Security Patterns

### Row-Level Security
```xml
<service verb="find" noun="Example" authenticate="true">
    <description>Find examples with row-level security</description>
    <actions>
        <!-- Base query -->
        <entity-find entity-name="com.example.Example" list="exampleList">
            <econdition field-name="statusId" value="EsActive"/>
        </entity-find>
        
        <!-- Apply row-level security based on user role -->
        <if condition="!ec.user.isUserInRole('ADMIN')">
            <!-- Non-admin users can only see their own records -->
            <script>
                exampleList = exampleList.findAll { it.createdByUserAccountId == ec.user.userId }
            </script>
        </if>
        
        <return message="Examples retrieved with security applied"/>
    </actions>
</service>
```

### Tenant Isolation
```xml
<service verb="find" noun="Example" authenticate="true">
    <description>Find examples with tenant isolation</description>
    <actions>
        <!-- Get current tenant ID -->
        <set field="tenantId" from="ec.tenantId"/>
        
        <!-- Query with tenant filter -->
        <entity-find entity-name="com.example.Example" list="exampleList">
            <econdition field-name="tenantId" from="tenantId"/>
            <econdition field-name="statusId" value="EsActive"/>
        </entity-find>
        
        <return message="Examples retrieved for current tenant"/>
    </actions>
</service>
```

### Field-Level Security
```xml
<service verb="get" noun="Example" authenticate="true">
    <description>Get example with field-level security</description>
    <actions>
        <entity-find-one entity-name="com.example.Example" value-field="example"/>
        
        <!-- Remove sensitive fields for non-admin users -->
        <if condition="!ec.user.isUserInRole('ADMIN')">
            <set field="example.sensitiveField" from="null"/>
            <set field="example.internalNotes" from="null"/>
        </if>
        
        <return message="Example retrieved with field-level security"/>
    </actions>
</service>
```

## Audit and Logging

### Audit Trail
```xml
<service verb="update" noun="Example" authenticate="true">
    <description>Update example with audit trail</description>
    <actions>
        <!-- Get original record for audit -->
        <entity-find-one entity-name="com.example.Example" value-field="originalExample"/>
        
        <!-- Perform update -->
        <entity-update entity-name="com.example.Example" include-nonpk="true"/>
        
        <!-- Create audit record -->
        <service-call name="create#ExampleAudit" in-map="[exampleId: exampleId,
                        userId: ec.user.userId,
                        changeDate: ec.user.nowTimestamp,
                        fieldName: 'status',
                        oldValue: originalExample.statusId,
                        newValue: example.statusId]"/>
        
        <return message="Example updated with audit trail"/>
    </actions>
</service>
```

### Security Event Logging
```xml
<service verb="delete" noun="Example" authenticate="true">
    <description>Delete example with security logging</description>
    <actions>
        <!-- Log security event before deletion -->
        <service-call name="create#SecurityEventLog" in-map="[userId: ec.user.userId,
                        eventType: 'EXAMPLE_DELETE',
                        resourceId: exampleId,
                        ipAddress: ec.context.ipAddress,
                        userAgent: ec.context.userAgent,
                        eventDate: ec.user.nowTimestamp]"/>
        
        <!-- Perform deletion -->
        <entity-delete entity-name="com.example.Example"/>
        
        <return message="Example deleted and logged"/>
    </actions>
</service>
```

## Input Validation and Sanitization

### Parameter Validation
```xml
<service verb="create" noun="Example" authenticate="true">
    <description>Create example with input validation</description>
    <in-parameters>
        <parameter name="description" type="text-medium" required="true">
            <text-length min="1" max="255"/>
        </parameter>
        <parameter name="email" type="text-medium">
            <text-email/>
        </parameter>
        <parameter name="phoneNumber" type="text-medium">
            <matches regexp="^\+?[\d\s\-\(\)]+$" message="Invalid phone number format"/>
        </parameter>
    </in-parameters>
    <actions>
        <!-- Additional validation in actions -->
        <if condition="description.contains('script')">
            <return error="true" message="Invalid content detected"/>
        </if>
        
        <!-- Sanitize input -->
        <set field="cleanDescription" from="description.replaceAll('<[^>]*>', '')"/>
        <set field="example.description" from="cleanDescription"/>
        
        <entity-create entity-name="com.example.Example" include-nonpk="true"/>
        <return message="Example created with validated input"/>
    </actions>
</service>
```

### SQL Injection Prevention
```xml
<service verb="find" noun="Example" authenticate="true">
    <description>Find examples safely</description>
    <in-parameters>
        <parameter name="searchText" type="text-medium"/>
    </in-parameters>
    <actions>
        <!-- SAFE: Use parameterized queries -->
        <entity-find entity-name="com.example.Example" list="exampleList">
            <econdition field-name="description" operator="like" value="${searchText}%"/>
        </entity-find>
        
        <!-- AVOID: Never do this -->
        <!-- <script>def sql = "SELECT * FROM example WHERE description LIKE '" + searchText + "%'"</script> -->
        
        <return message="Examples found safely"/>
    </actions>
</service>
```

## Rate Limiting

### Basic Rate Limiting
```xml
<service verb="send" noun="Notification" authenticate="true">
    <description>Send notification with rate limiting</description>
    <actions>
        <!-- Check rate limit -->
        <set field="rateLimitKey" from="ec.user.userId + '_notification'"/>
        <set field="currentCount" from="ec.cache.get(rateLimitKey, 0)"/>
        
        <if condition="currentCount >= 10">
            <return error="true" message="Rate limit exceeded. Please try again later."/>
        </if>
        
        <!-- Increment counter -->
        <set field="newCount" from="currentCount + 1"/>
        <ec.cache.put(rateLimitKey, newCount, 3600) <!-- 1 hour expiry -->
        
        <!-- Send notification -->
        <service-call name="send#EmailNotification" in-map="[userId: ec.user.userId, message: message]"/>
        
        <return message="Notification sent"/>
    </actions>
</service>
```

## Session Security

### Session Validation
```xml
<service verb="validate" noun="Session" authenticate="true">
    <description>Validate current session</description>
    <actions>
        <!-- Check session validity -->
        <set field="sessionValid" from="ec.user.sessionValid"/>
        <if condition="!sessionValid">
            <return error="true" message="Session has expired"/>
        </if>
        
        <!-- Check session age -->
        <set field="sessionAge" from="ec.user.nowTimestamp - ec.user.sessionCreatedTime"/>
        <if condition="sessionAge > 28800"> <!-- 8 hours -->
            <return error="true" message="Session too old"/>
        </if>
        
        <return message="Session is valid"/>
    </actions>
</service>
```

## Best Practices

### Security Checklist
1. **Always authenticate** sensitive services
2. **Use principle of least privilege** for permissions
3. **Validate all input** parameters
4. **Implement audit logging** for important operations
5. **Use parameterized queries** to prevent SQL injection
6. **Apply row-level security** for multi-tenant data
7. **Implement rate limiting** for public APIs
8. **Log security events** for monitoring
9. **Use HTTPS** for all authenticated requests
10. **Regular security reviews** of permissions and access

### Common Security Mistakes to Avoid
1. **Hardcoded credentials** in service code
2. **Missing authentication** on sensitive operations
3. **Overly permissive permissions** 
4. **SQL injection vulnerabilities**
5. **Missing audit trails**
6. **Insufficient input validation**
7. **Cross-tenant data access**
8. **Session fixation vulnerabilities**
9. **Missing rate limiting**
10. **Inadequate error handling** that leaks information

### Security Testing
1. **Test with different user roles**
2. **Verify row-level security**
3. **Test input validation**
4. **Check for SQL injection**
5. **Verify audit logging**
6. **Test rate limiting**
7. **Check session security**
8. **Test cross-tenant isolation**
9. **Verify HTTPS enforcement**
10. **Test error handling**