# Developer Guide

This guide explains how the current prototype is organized and where to make changes.

## Technology Stack

- HTML
- CSS
- JavaScript
- Font Awesome icons via CDN
- Google Fonts via CDN
- Chart.js where used by analytics

There is currently no package manager, bundler, build step, backend server, or database in this repository.

## File Structure

```text
index.html                 Public product page
app/styles.css             Shared portal styling
app/app.js                 Shared translation simulation logic
app/dashboard.html         Provider dashboard
app/patients.html          Patient registry
app/appointments.html      Appointment calendar/list
app/translator.html        Active translation session
app/patient_lobby.html     Patient-side session view
app/history.html           Translation transcript history
app/analytics.html         Usage analytics
app/settings.html          Settings and integrations
app/receptionist.html      Front desk workflow
Spec/                      Product and technical specifications
docs/                      GitHub-facing user and developer docs
```

## Running Locally

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

## Main JavaScript Behavior

`app/app.js` contains shared demo behavior for translation sessions:

- Mock translation dictionary
- Simulated patient replies
- Emergency keyword detection
- Chat message rendering
- Typing indicators
- Latency simulation

Several HTML files also include page-specific inline JavaScript for demo data and UI behavior.

## Adding A New Portal Page

1. Create a new HTML file under `app/`.
2. Link `styles.css`.
3. Reuse the existing sidebar and top header pattern.
4. Add the page to the sidebar navigation in each portal page if it should be globally reachable.
5. Keep demo data local unless a shared module is introduced.
6. Test at desktop and mobile widths.

## Adding A New Language

For the prototype:

1. Add the language option in relevant selects.
2. Add display colors where language color maps exist.
3. Add mock translation responses in `app/app.js` if needed.
4. Add sample patient or appointment records using the language.
5. Verify filters, badges, and session routes.

For production, language support should come from the backend translation provider and a centrally managed language registry.

## Replacing Simulated Translation

Do not call AI provider APIs directly from browser code. Instead:

1. Add a backend endpoint such as `POST /api/translate`.
2. Authenticate the user.
3. Validate and sanitize input.
4. Call the AI provider from the backend.
5. Return translated text and metadata.
6. Update `app/app.js` to call the backend endpoint.

Suggested response shape:

```json
{
  "sourceLanguage": "en",
  "targetLanguage": "Spanish",
  "sourceText": "Take this twice a day after meals.",
  "translatedText": "Tome esto dos veces al dia despues de las comidas.",
  "confidence": 0.98,
  "model": "configured-model-name",
  "safetyFlags": []
}
```

## Testing Checklist

- Landing page loads.
- Navigation links work.
- New session modal opens.
- Translation session starts with query parameters.
- Emergency phrase banner appears.
- Patient registry filters work.
- Appointment launch works.
- History modal opens and export button behaves.
- Analytics charts render.
- Settings tabs switch correctly.
- Receptionist queue actions work.
- Mobile layout remains usable.

## Code Style

- Keep CSS variables aligned with the existing design system.
- Prefer accessible text contrast and semantic markup.
- Keep demo data clearly separated from real integration code.
- Avoid placing secrets or real PHI in the repository.
- Use clear file names and direct links between portal pages.

For deeper architecture details, see `Spec/02_technical_architecture.md`.
