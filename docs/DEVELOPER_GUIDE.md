# Developer Guide

This guide explains how the current codebase works and how to extend it safely.

## Runtime Overview

The app is a local Python-backed HTML/CSS/JavaScript application.

```text
Browser
  |
  | HTTP on localhost:3456
  v
server.py
  |
  | sqlite3
  v
data/smarclinicai.db
```

No build step is required.

## Important Files

| File | Purpose |
|---|---|
| `server.py` | Local backend, static file server, auth, API, SQLite access |
| `data/schema.sql` | SQL schema for tenants, users, sessions, patients, appointments |
| `app/login.html` | Local login screen |
| `app/app.js` | Shared auth guard, API client, sidebar behavior, translation demo |
| `app/styles.css` | Shared app styling and responsive behavior |
| `app/dashboard.html` | Provider dashboard and session creation |
| `app/patients.html` | Patient registry, filters, add patient modal |
| `app/appointments.html` | Daily appointment workflow |
| `app/translator.html` | Simulated translation session |
| `app/settings.html` | Profile, tenant/team, settings, local-mode integrations |

## Running Locally

```powershell
python server.py
```

Open:

```text
http://localhost:3456/app/login.html
```

## Seed Data

Database initialization happens automatically when `server.py` starts.

Seed tenant:

```text
SmartClinic Local
```

Seed user:

```text
Username: Shash
Password: 12345
Role: Admin
```

Seed clinical demo data:

- 6 patients
- 6 appointments

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/health` | Backend and database health |
| `POST` | `/api/login` | Login with username/password |
| `POST` | `/api/logout` | Clear current session |
| `GET` | `/api/me` | Current user and tenant |
| `GET` | `/api/bootstrap` | Current user, tenant, and counts |
| `GET` | `/api/patients` | Tenant-scoped patient list |
| `POST` | `/api/patients` | Create tenant-scoped patient |
| `GET` | `/api/appointments?date=YYYY-MM-DD` | Tenant-scoped appointment list |
| `POST` | `/api/appointments` | Create appointment |
| `POST` | `/api/sessions/create` | Create translation session record |

## Authentication Flow

1. Login posts to `/api/login`.
2. Backend verifies PBKDF2 password hash.
3. Backend creates a random session token.
4. Browser receives `scai_session` as an HttpOnly cookie.
5. `app/app.js` calls `/api/me` on protected screens.
6. Unauthenticated users are redirected to `/app/login.html`.

## Multitenancy Pattern

Every persisted clinical table includes `tenant_id`.

The API never accepts `tenant_id` from the browser for clinical operations. It derives tenant scope from the authenticated session.

When adding new tables:

1. Include `tenant_id`.
2. Add a foreign key to `tenants(id)`.
3. Filter all reads and writes by the session tenant.
4. Avoid exposing cross-tenant IDs in the UI.

## Adding A New Backend Endpoint

1. Add a route branch in `Handler.handle_api`.
2. Call `require_session()` unless the endpoint is public.
3. Read JSON with `self.json_body()`.
4. Use parameterized SQL only.
5. Return JSON with `self.send_json()`.
6. Add local smoke checks before committing.

## Validation Commands

```powershell
python -m py_compile server.py
node --check app\app.js
Invoke-RestMethod http://127.0.0.1:3456/api/health
```

## Production Notes

Before real clinical use, replace local SQLite and simulated workflows with production-grade services:

- Managed relational database
- Strong password and MFA policy
- Secrets manager
- HTTPS everywhere
- Centralized logging and auditing
- HIPAA security review
- Live AI translation provider integration
- EHR/FHIR integration
- SMS provider integration
