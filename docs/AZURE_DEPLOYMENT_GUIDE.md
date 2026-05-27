# Azure Migration Guide

This guide describes how to move SmartClinics AI from local demo to Azure.

## Target Azure Architecture

```text
Azure DNS
  |
Azure Front Door + managed certificate
  |
Azure Static Web Apps or Storage Static Website
  |
Azure App Service / Container Apps
  |
Azure Database for PostgreSQL or MySQL
```

Supporting services:

- Azure Key Vault
- Azure Monitor and Application Insights
- Azure Web Application Firewall
- Azure Backup
- Azure Communication Services or Twilio
- Microsoft Entra ID / Azure AD B2C

## Migration Steps

### 1. Prepare Application

- Split static frontend and API runtime.
- Move local constants into environment settings.
- Replace SQLite access with managed database connection.
- Add database migration scripts.
- Add structured logs and correlation IDs.

### 2. Database

Create one of:

- Azure Database for PostgreSQL Flexible Server
- Azure Database for MySQL Flexible Server
- Azure SQL Database if SQL Server is preferred

Recommended settings:

- Private endpoint
- Encrypted storage
- Automated backups
- Zone redundancy for production
- Firewall restricted to app subnet

### 3. Backend Hosting

Recommended options:

- Azure App Service for simple API hosting
- Azure Container Apps for containerized workloads
- AKS only if orchestration complexity is justified

Set environment variables for:

- Database URL
- Identity provider settings
- Secrets references
- Allowed origins

### 4. Frontend Hosting

Use either:

- Azure Static Web Apps, or
- Azure Storage static website behind Azure Front Door

Configure:

- Custom domain
- HTTPS
- API base URL
- Cache rules

### 5. Identity

Replace local login with:

- Microsoft Entra ID
- Azure AD B2C
- External OIDC provider

Map claims to tenant and role records in the backend.

### 6. Secrets

Store in Azure Key Vault:

- Database credentials
- AI provider keys
- EHR OAuth credentials
- SMS credentials
- Signing keys

Use managed identity from App Service or Container Apps to read secrets.

### 7. Observability

Enable:

- Application Insights
- Azure Monitor alerts
- Log Analytics workspace
- Diagnostic settings for database and app services
- Activity logs

### 8. Security Checklist

- HTTPS only
- WAF enabled in Front Door
- Private database access
- Managed identity for secrets
- No secrets in static files
- Audit logging
- Backup restore tested
- HIPAA and organizational compliance review completed

## Azure Go-Live Checklist

- Frontend deployed and reachable.
- API deployed and healthy.
- Database migrations applied.
- Key Vault references working.
- Login integrated with Entra/Azure AD B2C.
- Tenant isolation verified.
- Logs visible in Application Insights.
- Alerts configured.
- Backup and restore tested.
