# SmartClinics AI

SmartClinics AI is a production-ready prototype for real-time medical translation workflows in outpatient and virtual care settings. It demonstrates how providers, reception teams, and patients can use AI-assisted translation to reduce language barriers during appointments, intake, follow-up, and documentation.

This repository now includes a local-only Python backend for authentication, tenant scoping, and SQL persistence. Translation, EHR, SMS, AI model calls, and video meetings remain simulated until production integrations are added.

## What Is Included

- Public marketing and product page: `index.html`
- Provider dashboard: `app/dashboard.html`
- Patient registry: `app/patients.html`
- Appointment schedule: `app/appointments.html`
- Active translation session: `app/translator.html`
- Patient lobby/session view: `app/patient_lobby.html`
- Translation history: `app/history.html`
- Analytics: `app/analytics.html`
- Settings and integrations screen: `app/settings.html`
- Receptionist workflow: `app/receptionist.html`
- Shared app styles and demo logic: `app/styles.css`, `app/app.js`
- Product, architecture, design, API, and deployment specs: `Spec/`
- UAT report generator and sample UAT workbook: `generate_uat.py`, `SmartClinics_AI_UAT_Report.xlsx`

## Quick Start

Run the local backend from the project root:

```powershell
python server.py
```

Then open:

```text
http://localhost:3456/app/login.html
```

Seeded local login:

```text
Username: Shash
Password: 12345
Tenant: SmartClinic Local
Database: data/smarclinicai.db
```

The app screens are protected by the local session cookie and redirect to login when unauthenticated.

## Demo Workflow

1. Open `index.html` to review the product overview.
2. Sign in at `app/login.html`.
3. Start a new translation session from the dashboard.
4. Choose a patient name and target language.
5. Use the active session screen to simulate translated provider and patient messages.
6. Review history, analytics, settings, and receptionist workflows from the sidebar.

## Configuration Overview

The local backend requires no environment variables. External assets are loaded from public CDNs for fonts, icons, images, and charts.

Local SQL discovery: this machine has a running MySQL service named `MySQLTest` on port `3306`, but root access without a password is denied. The current local backend therefore uses the SQLite SQL database `data/smarclinicai.db` until MySQL credentials are available.

For production, the documented configuration includes:

- AI translation provider keys
- EHR/FHIR endpoints and OAuth credentials
- Twilio SMS settings
- Zoom or WebRTC settings
- Database connection strings
- HIPAA retention, audit, and encryption controls

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) and [Spec/04_api_integration_guide.md](Spec/04_api_integration_guide.md).

## Documentation

- [Documentation Index](docs/README.md)
- [Business Analyst Specs](docs/BUSINESS_ANALYST_SPECS.md)
- [Doctor Guide](docs/DOCTOR_GUIDE.md)
- [User Guide](docs/USER_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Architect Guide](docs/ARCHITECT_GUIDE.md)
- [Tech Stack Guide](docs/TECHSTACK_GUIDE.md)
- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [AWS Migration Guide](docs/AWS_DEPLOYMENT_GUIDE.md)
- [Azure Migration Guide](docs/AZURE_DEPLOYMENT_GUIDE.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Security and Compliance Guide](docs/SECURITY_AND_COMPLIANCE.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Full Product Specs](Spec/README.md)

## Important Safety Note

This repository is a prototype and should not be used as-is for real patient care, medical decision-making, emergency response, protected health information, or live clinical workflows. Before production use, replace simulated behavior with audited backend services, execute security review, sign required BAAs, validate clinical translation quality, complete HIPAA controls, and obtain organization approval.

## Repository Structure

```text
.
|-- index.html
|-- server.py
|-- data/
|   |-- schema.sql
|   `-- smarclinicai.db
|-- app/
|   |-- login.html
|   |-- dashboard.html
|   |-- patients.html
|   |-- appointments.html
|   |-- translator.html
|   |-- patient_lobby.html
|   |-- history.html
|   |-- analytics.html
|   |-- settings.html
|   |-- receptionist.html
|   |-- styles.css
|   `-- app.js
|-- docs/
|-- Spec/
|-- generate_uat.py
|-- SmartClinics_AI_UAT_Report.xlsx
|-- screenshot_hero.png
`-- screenshot_pricing.png
```

## License

No license file is currently included. Add a license before distributing, reusing, or accepting external contributions.
