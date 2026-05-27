# Architect Guide

## Current Architecture

SmartClinics AI currently runs as a local monolith:

```text
Browser
  |
  | HTTP
  v
Python ThreadingHTTPServer
  |
  | sqlite3
  v
SQLite database
```

This design is intentionally simple for local demo and handoff.

## Application Layers

| Layer | Current Implementation | Future Production Direction |
|---|---|---|
| Presentation | Static HTML/CSS/JS under `app/` | React/Vue/Next.js or hardened static frontend |
| API | `server.py` route handler | FastAPI, Django, Express, or .NET API |
| Auth | Local username/password/session cookie | SSO/OIDC, MFA, RBAC |
| Database | SQLite file | PostgreSQL, MySQL, SQL Server, or managed cloud database |
| Translation | Simulated JS dictionary | AI translation and speech services |
| EHR | Simulated state | FHIR R4 integrations |
| SMS | Simulated state | Twilio or cloud communication service |
| Video | Simulated state | Zoom, WebRTC, or ACS |

## Multitenancy

The local schema uses shared-table multitenancy:

- `tenants`
- `users.tenant_id`
- `patients.tenant_id`
- `appointments.tenant_id`
- `translation_sessions.tenant_id`
- `audit_logs.tenant_id`

The authenticated session determines tenant scope. Browser requests do not supply tenant IDs for clinical data.

## Data Model

Key entities:

- Tenant: clinic organization boundary
- User: authenticated staff member
- Session: local web session
- Patient: tenant-scoped patient record
- Appointment: tenant-scoped scheduled interaction
- Translation Session: session metadata for translation encounters
- Audit Log: security and operational event trail

## Security Architecture

Current local controls:

- PBKDF2 password hashing
- Random session tokens
- Hashed session token storage
- HttpOnly session cookie
- SameSite cookie
- Tenant-scoped queries
- Parameterized SQL

Production controls still required:

- HTTPS/TLS termination
- MFA
- Central identity provider
- Secrets manager
- Database encryption at rest
- Field-level PHI encryption where required
- Audit log retention
- WAF and rate limiting
- Backup and disaster recovery
- HIPAA security risk assessment

## Recommended Production Architecture

```text
User Browser
  |
  v
CDN / Static Frontend Hosting
  |
  v
API Gateway / Load Balancer
  |
  v
Backend API Service
  |-- Auth / RBAC
  |-- Tenant context
  |-- Translation orchestration
  |-- EHR integration
  |-- SMS integration
  |-- Audit logging
  v
Managed Database
```

## Scalability Path

1. Keep current schema shape.
2. Move SQLite to managed relational database.
3. Split static frontend hosting from backend API hosting.
4. Add service-level observability.
5. Add background jobs for EHR export, SMS delivery, and transcript processing.
6. Add tenant administration and onboarding flows.

## Architecture Decision Records To Add Later

- API framework selection
- Database selection
- Identity provider selection
- Translation provider selection
- EHR integration pattern
- Audit and retention model
- Cloud hosting target
