# Tech Stack Guide

## Current Local Stack

| Category | Technology |
|---|---|
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Backend | Python 3 standard library |
| Web server | `http.server.ThreadingHTTPServer` |
| Database | SQLite through Python `sqlite3` |
| Auth | Local username/password, PBKDF2, session cookie |
| Icons | Font Awesome CDN |
| Fonts | Google Fonts Inter |
| Charts | Chart.js where used |
| Source control | Git |

## Why This Stack

The local release is designed for fast demonstration:

- No npm install required.
- No Python package install required.
- No cloud credentials required.
- No database server credentials required.
- Runs with `python server.py`.

## Backend Details

`server.py` provides:

- Static file serving
- JSON API routing
- Database initialization
- Seed data creation
- Login/logout
- Session validation
- Tenant-scoped patient and appointment APIs

## Database Details

The schema is in:

```text
data/schema.sql
```

The generated local database is:

```text
data/smarclinicai.db
```

The database file is ignored by Git because it is a local runtime artifact.

## Frontend Details

`app/app.js` provides:

- API helper
- Login form handling
- Auth guard
- Tenant/user display injection
- Logout handling
- Mobile sidebar behavior
- Simulated translation functions

Page-specific scripts remain inline inside each HTML page.

## Recommended Production Stack

| Category | Recommended Options |
|---|---|
| Frontend | React, Next.js, Vue, or hardened static HTML |
| Backend | FastAPI, Django, Express, NestJS, .NET, or Java Spring |
| Database | PostgreSQL, MySQL, SQL Server |
| Cache/Jobs | Redis, SQS, Azure Service Bus, Celery, Sidekiq |
| Identity | Auth0, Azure AD B2C, Cognito, Okta |
| AI | OpenAI, Azure OpenAI, AWS Bedrock, Google Cloud Translation |
| Speech | Azure Speech, AWS Transcribe, Google Speech-to-Text |
| SMS | Twilio, AWS SNS/Pinpoint, Azure Communication Services |
| EHR | FHIR R4 integrations |
| Observability | CloudWatch, Azure Monitor, Datadog, OpenTelemetry |

## Migration Guidance

The current code is intentionally simple. For production, avoid adding too much complexity to the local demo branch. Instead:

1. Keep this repo as a functional demo baseline.
2. Create a production backend project when cloud deployment starts.
3. Migrate schema and API contracts.
4. Replace page-inline scripts gradually.
