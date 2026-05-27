# User Guide

This guide explains how to use SmartClinics AI during a local demo.

## Login

Open:

```text
http://localhost:3456/app/login.html
```

Use:

```text
Username: Shash
Password: 12345
```

After login, the app opens the provider dashboard. All app screens use the same local session cookie and tenant context.

## Main Screens

| Screen | URL | Purpose |
|---|---|---|
| Login | `/app/login.html` | Authenticates the demo user |
| Dashboard | `/app/dashboard.html` | Provider home, schedule snapshot, new translation session |
| Patients | `/app/patients.html` | Tenant-scoped patient registry |
| Appointments | `/app/appointments.html` | Daily schedule and appointment creation |
| Translator | `/app/translator.html` | Simulated live translation session |
| Patient Lobby | `/app/patient_lobby.html` | Patient-side session view |
| History | `/app/history.html` | Demo translation history |
| Analytics | `/app/analytics.html` | Usage and performance dashboards |
| Settings | `/app/settings.html` | Profile, translation, integrations, security, billing, team |
| Receptionist | `/app/receptionist.html` | Front-desk queue workflow |

## Provider Workflow

1. Sign in as `Shash`.
2. Review the dashboard tenant pill and sidebar user profile.
3. Click `New Translation Session`.
4. Choose a patient name and target language.
5. Click `Create Link & Start`.
6. The backend creates a local translation session record.
7. The browser opens the active translator screen.
8. Type a phrase in the composer to simulate translated provider speech.
9. Use phrases like `chest pain` to show emergency detection.

## Patient Registry Workflow

1. Open Patients from the sidebar.
2. Search by name, patient ID, language, or email.
3. Use filters such as `Scheduled Today`, `Spanish`, or `Mandarin`.
4. Click the eye icon to inspect patient details.
5. Click `Session` to start a translation session for that patient.
6. Click `Add Patient` to create a new tenant-scoped patient.

Patient creation is persisted locally through `/api/patients`.

## Appointment Workflow

1. Open Appointments from the sidebar.
2. Review today's queue.
3. Click `New Appointment`.
4. Enter patient, time, type, language, and notes.
5. Click `Schedule`.

Appointment creation is persisted locally through `/api/appointments`.

## Receptionist Workflow

1. Open Receptionist View.
2. Select a patient from the queue.
3. Review language, visit reason, and queue status.
4. Use actions to simulate session launch and communication handoff.

SMS delivery is still simulated in local mode.

## Settings Workflow

Use Settings to demo:

- Profile information
- Translation preferences
- Notification toggles
- EHR and communication integration states
- Security settings
- Billing plan display
- Team member list

External integration buttons intentionally show local-mode messages until live credentials are configured.

## Logout

Use the sign-out icon in the sidebar profile area. The backend clears the local session cookie.
