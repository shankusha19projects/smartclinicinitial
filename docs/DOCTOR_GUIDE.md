# Doctor Guide

This guide explains how a provider should demonstrate and use SmartClinics AI in the local version.

## Sign In

Open:

```text
http://localhost:3456/app/login.html
```

Use:

```text
Shash / 12345
```

## Daily Dashboard

After login, the dashboard shows:

- Current tenant context
- Provider profile area
- Upcoming translation need
- Today schedule and recent sessions
- Quick action to start a new translation session

## Start A Translation Session

1. Click `New Translation Session`.
2. Enter a patient name or use the default patient context.
3. Select the patient target language.
4. Keep live subtitles enabled for the demo.
5. Click `Create Link & Start`.

The local backend creates a translation session record and opens the translator.

## During A Session

Use the message composer to simulate provider speech.

Suggested demo prompts:

```text
Hello, I'm Dr. Chen. How are you feeling today?
Are you currently taking any medications?
Take this twice a day after meals.
```

The screen shows:

- Provider original text
- Simulated translated output
- Simulated patient response
- Conversation-style transcript

## Emergency Alert Demo

Type:

```text
I have chest pain and can't breathe.
```

The emergency banner should appear briefly. This is a demo keyword detector, not a clinical safety system.

## From Patient Registry

1. Open Patients.
2. Search or filter the registry.
3. Click the eye icon for patient details.
4. Click `Start Translation Session`.

## From Appointments

1. Open Appointments.
2. Find a scheduled patient.
3. Click `Start`.

## Clinical Safety Notes

The local version is for demonstration only.

Do not use it for:

- Real diagnosis
- Emergency response
- Production patient care
- Real PHI storage
- Medical decision-making

Before clinical use, the product must be connected to audited translation, EHR, SMS, identity, monitoring, and compliance systems.
