# SmartClinics AI

SmartClinics AI is a production-ready prototype for real-time medical translation workflows in outpatient and virtual care settings. It demonstrates how providers, reception teams, and patients can use AI-assisted translation to reduce language barriers during appointments, intake, follow-up, and documentation.

This repository is currently a static front-end prototype. It uses HTML, CSS, and JavaScript with simulated translation, patient, appointment, analytics, and integration behavior. No real patient data, live AI model calls, EHR writes, SMS delivery, or video meetings are performed by the checked-in demo.

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

You can open the prototype directly in a browser:

```text
index.html
```

For the best local preview, run a small static web server from the project root:

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Useful demo routes:

```text
http://localhost:8000/app/dashboard.html
http://localhost:8000/app/translator.html?lang=Spanish&patient=Demo+Patient
http://localhost:8000/app/patient_lobby.html?lang=Spanish&patient=Demo+Patient
http://localhost:8000/app/receptionist.html
```

## Demo Workflow

1. Open `index.html` to review the product overview.
2. Select a portal from the landing page or open `app/dashboard.html`.
3. Start a new translation session from the dashboard.
4. Choose a patient name and target language.
5. Use the active session screen to simulate translated provider and patient messages.
6. Review history, analytics, settings, and receptionist workflows from the sidebar.

## Configuration Overview

The current prototype is client-only and requires no environment variables to run locally. External assets are loaded from public CDNs for fonts, icons, images, and charts.

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
- [User Guide](docs/USER_GUIDE.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Security and Compliance Guide](docs/SECURITY_AND_COMPLIANCE.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Full Product Specs](Spec/README.md)

## Important Safety Note

This repository is a prototype and should not be used as-is for real patient care, medical decision-making, emergency response, protected health information, or live clinical workflows. Before production use, replace simulated behavior with audited backend services, execute security review, sign required BAAs, validate clinical translation quality, complete HIPAA controls, and obtain organization approval.

## Repository Structure

```text
.
|-- index.html
|-- app/
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
