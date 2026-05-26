# Configuration Guide

The current SmartClinics AI prototype does not require configuration to run locally. It is a static front-end demo.

Production configuration is documented here so teams know what must be added before connecting the prototype to real services.

## Local Prototype Configuration

No `.env` file is required for the checked-in static demo.

The app currently depends on public external assets:

- Google Fonts
- Font Awesome
- Chart.js where used by analytics screens
- Unsplash images

If previewing offline, replace CDN references and remote images with local assets.

## Query Parameters

The translation and patient lobby screens use query string parameters:

| Parameter | Example | Used By |
|---|---|---|
| `lang` | `Spanish` | Translation target language |
| `patient` | `Maria Gonzalez` | Displayed patient context |

Example:

```text
app/translator.html?lang=Spanish&patient=Maria%20Gonzalez
```

## Production Environment Variables

Use backend environment variables for secrets. Do not place API keys in client-side HTML or JavaScript.

Recommended production variables:

```text
APP_ENV=production
APP_BASE_URL=https://app.example.com
API_BASE_URL=https://api.example.com

OPENAI_API_KEY=
OPENAI_MODEL=
GOOGLE_TRANSLATE_KEY=
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

ZOOM_API_KEY=
ZOOM_API_SECRET=
ZOOM_SDK_KEY=
ZOOM_SDK_SECRET=

DATABASE_URL=
REDIS_URL=
SESSION_SECRET=
ENCRYPTION_KEY=
AUDIT_LOG_BUCKET=
```

## Integration Setup

### AI Translation

For a production translation service:

1. Build a backend translation endpoint.
2. Send text/audio transcripts from the browser to the backend.
3. Call the selected AI provider from the backend only.
4. Return translated text, confidence, language, model metadata, and safety flags.
5. Log only approved audit metadata.

See `Spec/04_api_integration_guide.md` for sample OpenAI and Google Translate patterns.

### EHR/FHIR

Production EHR integration should use SMART on FHIR OAuth:

1. Register the app with Epic, Cerner/Oracle Health, or another EHR vendor.
2. Configure redirect URIs.
3. Request the minimum required scopes.
4. Store access tokens securely.
5. Export translated summaries as FHIR resources only after user confirmation.

### Twilio SMS

Use Twilio from a backend service:

1. Verify or purchase a sender number.
2. Store credentials in backend environment variables.
3. Generate short-lived patient session links.
4. Avoid sending PHI in SMS body text.
5. Log message delivery status without exposing message content unnecessarily.

### Zoom Or WebRTC

For video sessions:

1. Use a HIPAA-eligible account and signed BAA when required.
2. Generate meeting signatures from the backend.
3. Disable recording unless explicit consent and retention controls are in place.
4. Keep access links short-lived.

## Client Configuration Pattern

If the static app needs non-secret runtime settings, add a separate file such as:

```javascript
window.SMARTCLINICS_CONFIG = {
  apiBaseUrl: "https://api.example.com",
  environment: "production",
  supportEmail: "support@example.com"
};
```

Load it before app scripts. Never put private keys, OAuth secrets, database passwords, or signing keys in this client file.

## Required Before Real Clinical Use

- Backend API with authentication and authorization
- Encrypted persistence where data must be stored
- Audit logging
- PHI minimization
- Vendor BAAs
- Translation quality validation
- Incident response and disaster recovery plans
- Accessibility and security testing
