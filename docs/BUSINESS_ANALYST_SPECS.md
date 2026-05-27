# Business Analyst Specs

## Product Summary

SmartClinics AI is a clinic workflow application that helps providers and front-desk teams conduct multilingual patient interactions. The current release is a local demo with authentication, tenant scoping, persisted patient data, persisted appointment data, and simulated translation workflows.

## Business Goals

- Reduce language barriers during outpatient visits.
- Help clinic staff prepare translation sessions from schedule, patient registry, or receptionist queue.
- Demonstrate a multitenant foundation for future clinic organizations.
- Provide a realistic local demo before cloud deployment.
- Establish documentation for product, technical, clinical, and deployment stakeholders.

## Stakeholders

| Stakeholder | Need |
|---|---|
| Clinic owner | Understand value, security posture, and deployment path |
| Doctor/provider | Start and conduct translation sessions quickly |
| Receptionist | Check in patients and launch language support |
| Patient | Join a session in preferred language |
| Administrator | Manage team, tenant settings, and integrations |
| Developer | Extend backend, UI, and integrations |
| Cloud architect | Move the local demo to AWS or Azure |

## In-Scope For Current Release

- Local login with seeded user `Shash`.
- Local tenant named `SmartClinic Local`.
- Tenant-scoped patient registry.
- Tenant-scoped appointment list.
- Local SQL persistence using SQLite.
- Simulated translation session flow.
- Simulated emergency keyword detection.
- Simulated EHR, SMS, video, and billing states.
- Documentation for local demo and cloud migration.

## Out Of Scope For Current Release

- Real PHI production storage.
- Live AI model translation.
- Live speech-to-text.
- Live EHR/FHIR writes.
- Live SMS delivery.
- Live video meetings.
- Payment processing.
- Full HIPAA compliance certification.

## Personas

### Provider

The provider needs a fast way to start a translation session from the daily schedule or a patient record. The provider should see patient context, target language, and transcript output.

### Receptionist

The receptionist needs to find patients in the queue, confirm preferred language, and initiate a handoff to the provider or patient lobby.

### Administrator

The administrator needs account, team, settings, and integration visibility. In the local release, these screens are demo-ready but not connected to external services.

## Core User Stories

| ID | User Story | Acceptance Criteria |
|---|---|---|
| BA-001 | As a user, I can sign in before seeing app screens. | Login succeeds with `Shash / 12345`; unauthenticated API calls return `401`. |
| BA-002 | As a clinic user, I only see my tenant data. | Patients and appointments are filtered by session tenant. |
| BA-003 | As a provider, I can start a translation session from dashboard. | Session is recorded locally and translator screen opens. |
| BA-004 | As a provider, I can manage patients. | Patient list loads from backend and new patients persist locally. |
| BA-005 | As a scheduler, I can create appointments. | Appointment list loads from backend and new appointments persist locally. |
| BA-006 | As a doctor, I can simulate translated conversation. | Translator displays provider/patient messages and simulated translations. |
| BA-007 | As clinic staff, I can demo emergency detection. | Emergency keywords trigger visible alert banner. |
| BA-008 | As an evaluator, I can navigate all major screens. | Dashboard, Patients, Appointments, Translator, Lobby, History, Analytics, Settings, Receptionist return `200`. |

## Functional Requirements

- The app shall require login for protected app screens.
- The backend shall store users, tenants, sessions, patients, appointments, translation sessions, and audit logs.
- The backend shall seed one initial tenant and one initial admin user.
- The browser shall display tenant context after login.
- The patient registry shall support search, filtering, details, and session launch.
- The appointment screen shall support today's appointment list and creation.
- The dashboard shall create a translation session before navigation.
- The app shall run locally without external cloud credentials.

## Nonfunctional Requirements

- Local startup should require one command: `python server.py`.
- The demo should run on `localhost:3456`.
- Passwords must not be stored in plain text.
- Session tokens must be random and stored as hashes.
- Clinical data access must be tenant-scoped.
- Local database files and logs must not be committed.

## Demo Acceptance Checklist

- Server starts successfully.
- Login page opens.
- `Shash / 12345` signs in.
- Dashboard displays tenant/user context.
- Patient registry loads seeded data.
- Adding a patient works.
- Appointments load today's seeded data.
- Adding an appointment works.
- Starting a translation session opens translator.
- Settings team list renders real rows, not template text.
- All app pages return HTTP 200.
