# Configuration Guide

SmartClinics AI runs locally with no required environment variables.

## Local Defaults

| Setting | Default |
|---|---|
| Host | `localhost` |
| Port | `3456` |
| Database | `data/smarclinicai.db` |
| Login user | `Shash` |
| Login password | `12345` |
| Tenant | `SmartClinic Local` |

## Optional Local Port

To run on another port:

```powershell
$env:PORT=4567
python server.py
```

Open:

```text
http://localhost:4567/app/login.html
```

## Local Database

The database is created automatically from:

```text
data/schema.sql
```

The runtime database file is:

```text
data/smarclinicai.db
```

This file is intentionally ignored by Git.

## External Assets

The app uses public CDNs for:

- Google Fonts
- Font Awesome
- Chart.js where used
- Unsplash demo images

For offline demos, replace those references with local assets.

## Production Environment Variables

When moving to production, configure secrets only on the backend:

```text
APP_ENV=production
APP_BASE_URL=https://app.example.com
API_BASE_URL=https://api.example.com
DATABASE_URL=
SESSION_SECRET=
ENCRYPTION_KEY=

OPENAI_API_KEY=
OPENAI_MODEL=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AWS_REGION=
AWS_BEDROCK_MODEL_ID=

EPIC_FHIR_BASE_URL=
EPIC_CLIENT_ID=
EPIC_CLIENT_SECRET=
CERNER_FHIR_BASE_URL=
CERNER_CLIENT_ID=
CERNER_CLIENT_SECRET=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
```

## Integration Configuration

### AI Translation

The current local demo uses simulated translation. Production translation should be called from the backend only.

### EHR/FHIR

Production EHR integration should use SMART on FHIR OAuth, minimum scopes, token encryption, and audit logging.

### SMS

Production SMS should send short-lived links and avoid PHI in message bodies.

### Video

Production video should use a HIPAA-eligible account and signed BAA where required.
