# User Guide

This guide explains how to use the SmartClinics AI prototype from the perspective of a provider, receptionist, patient, and evaluator.

## Running The Demo

From the project root, either open `index.html` directly or run:

```powershell
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Main Entry Points

| Area | File | Purpose |
|---|---|---|
| Landing page | `index.html` | Product overview, portal links, pricing, FAQ, and value proposition |
| Provider dashboard | `app/dashboard.html` | Start sessions, view schedule, monitor translation work |
| Patient registry | `app/patients.html` | Browse patients, filter by language/status, start sessions |
| Appointments | `app/appointments.html` | View schedule and launch translation from appointments |
| Active translation | `app/translator.html` | Simulated live video and translated conversation |
| Patient lobby | `app/patient_lobby.html` | Mobile-first patient-side session experience |
| History | `app/history.html` | Review simulated translated session transcripts |
| Analytics | `app/analytics.html` | Review usage, accuracy, latency, and provider metrics |
| Settings | `app/settings.html` | Configure profile, translation, integrations, security, billing, team |
| Receptionist | `app/receptionist.html` | Manage queue, send patient links, launch sessions |

## Provider Workflow

1. Open `app/dashboard.html`.
2. Review the upcoming patient banner and today's schedule.
3. Click `New Translation Session` or `Start Translation`.
4. Choose the patient and target language.
5. The app opens `app/translator.html` with query string parameters:

```text
translator.html?lang=Spanish&patient=Maria%20Gonzalez
```

6. Enter provider text in the session composer.
7. The app shows a simulated translated message and a simulated patient response.
8. Emergency phrases such as `chest pain` trigger the emergency banner.

## Receptionist Workflow

1. Open `app/receptionist.html`.
2. Select a patient from the queue.
3. Review the patient's preferred language and status.
4. Use the available actions to simulate sending an SMS link, starting a translation session, or marking workflow status.
5. The patient link points to `app/patient_lobby.html` with the selected language and patient context.

## Patient Workflow

1. Open a patient lobby link such as:

```text
app/patient_lobby.html?lang=Spanish&patient=Demo+Patient
```

2. Review the patient-side session screen.
3. Use the simulated message flow to verify how patient text appears in the translated workflow.

## Evaluator Workflow

Use the included screens to test product completeness:

- Landing page narrative and CTA flow
- Provider session start
- Patient list filtering
- Appointment launch
- Receptionist queue handoff
- Emergency detection behavior
- Translation history modal
- Analytics charts
- Settings tabs
- Responsive behavior on mobile widths

## Demo Data

The app includes hardcoded demo patients, visits, appointments, transcripts, and analytics. These are sample records only. Do not treat them as real patient data.

## Known Prototype Limits

- Translation is simulated in `app/app.js`.
- Patient records are in-memory JavaScript arrays.
- Settings controls are visual/demo-only.
- SMS, EHR, video, and AI provider integrations are not connected.
- Refreshing a page resets most unsaved demo changes.
