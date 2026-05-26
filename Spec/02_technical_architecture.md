# SmartClinics AI — Technical Architecture & Configuration

**Document Version:** 1.0.0  
**Date:** May 9, 2026

---

## 1. Current Stack (Prototype / Demo)

```
Frontend Only — No Backend Required for Prototype
├── HTML5 (semantic, WCAG AAA)
├── Vanilla CSS (custom design system, no Tailwind)
├── Vanilla JavaScript (ES6+, no framework)
└── Chart.js 4.4.0 (analytics charts only)
```

---

## 2. File Architecture

```
SmartclinicAI/
│
├── index.html                        # Marketing landing page
│
├── app/
│   ├── styles.css                    # Shared design system (all pages import)
│   ├── app.js                        # Core simulation logic (translator + patient)
│   │
│   ├── dashboard.html                # Provider: Command center, session initiation
│   ├── patients.html                 # Provider: Patient registry CRUD
│   ├── appointments.html             # Provider: Calendar & scheduling
│   ├── history.html                  # Provider: Translation transcripts + EHR export
│   ├── analytics.html                # Provider: Charts, KPIs, ROI (uses Chart.js)
│   ├── settings.html                 # Provider: All settings tabs
│   │
│   ├── receptionist.html             # Receptionist: Queue management station
│   │
│   ├── translator.html               # Active session: Doctor's live workspace
│   └── patient_lobby.html            # Active session: Patient mobile view
│
└── Spec/                             # This documentation folder
    ├── 01_product_requirements.md
    ├── 02_technical_architecture.md  ← This file
    ├── 03_design_system.md
    ├── 04_api_integration_guide.md
    └── 05_deployment_guide.md
```

---

## 3. External Dependencies

### CDN-Loaded Libraries

| Library | Version | URL | Used By |
|---|---|---|---|
| Google Fonts — Inter | latest | `fonts.googleapis.com` | All pages |
| Font Awesome | 6.4.0 | `cdnjs.cloudflare.com` | All pages |
| Chart.js | 4.4.0 | `cdn.jsdelivr.net` | `analytics.html` only |

### No NPM / Node Dependencies
The prototype runs entirely as static files — no build step, bundler, or server required.

---

## 4. URL Parameter Convention

Pages communicate state via query string parameters. These are the defined parameters:

| Parameter | Used By | Type | Example |
|---|---|---|---|
| `lang` | `translator.html`, `patient_lobby.html`, `appointments.html` | String | `?lang=Spanish` |
| `patient` | `translator.html`, `patient_lobby.html` | String (URL-encoded) | `?patient=Maria+Gonzalez` |
| `sessionId` | (future) `translator.html` | String | `?sessionId=SX-9X4V` |
| `mode` | (future) `translator.html` | String | `?mode=telehealth` |

**Reading Parameters (standard pattern used throughout app):**
```javascript
const params = new URLSearchParams(window.location.search);
const lang = params.get('lang') || 'Spanish';
const patient = params.get('patient') || 'Unknown Patient';
```

---

## 5. Data Models

### 5.1 Patient Object

```javascript
{
  id:         "PT-8421",          // Format: PT-{4-digit number}
  firstName:  "Maria",
  lastName:   "Gonzalez",
  dob:        "1954-05-12",       // ISO 8601 date string
  language:   "Spanish",          // Preferred language (display name)
  phone:      "(973) 555-0112",
  email:      "maria.g@email.com",
  insurance:  "Medicaid",
  lastVisit:  "2026-05-08",       // ISO 8601 or null
  status:     "scheduled",        // "active" | "scheduled" | "completed"
  notes:      "Post-op orthopedic followup. Hypertensive.",
  visits: [
    {
      date:     "2026-05-08",
      type:     "Post-op Followup",
      duration: "18 min",
      provider: "Dr. Chen"
    }
  ]
}
```

### 5.2 Appointment Object

```javascript
{
  time:     "9:30 AM",
  patient:  "Maria Gonzalez",
  lang:     "Spanish",
  type:     "Post-op Followup",
  duration: 45,             // minutes (integer)
  status:   "scheduled"     // "scheduled" | "completed" | "no-show"
}
```

### 5.3 Translation Session Object

```javascript
{
  id:         "SX-9X4V",          // Format: SX-{4 alphanumeric}
  patient:    "Amir Al-Fayed",
  lang:       "Arabic",
  date:       "2026-05-09",
  time:       "8:15 AM",
  duration:   18,                 // minutes
  accuracy:   97.4,               // percentage (float)
  ehr:        "pending",          // "pending" | "exported"
  emergency:  false,              // boolean — emergency keywords detected
  transcript: [
    {
      role:        "doc",         // "doc" | "patient"
      text:        "Good morning Amir...",
      translation: "صباح الخير عامر..."
    }
  ]
}
```

### 5.4 Queue Entry Object (Receptionist)

```javascript
{
  id:          "PT-8421",
  name:        "Maria Gonzalez",
  time:        "9:30 AM",
  lang:        "Spanish",
  type:        "Post-op Followup",
  status:      "here",            // "here" | "called" | "waiting" | "done"
  insurance:   "Medicaid",
  phone:       "(973) 555-0112",
  room:        "—",               // "Room N" or "—" if unassigned
  copay:       "$20.00",
  checkinTime: "9:12 AM",         // "—" if not yet checked in
  color:       "#c0392b"          // hex color for avatar background
}
```

---

## 6. Simulation Engine (app.js)

### 6.1 Translation Dictionary

```javascript
const translationDictionary = {
  // English → Spanish phrase pairs
  "Hello, I'm Dr. Chen. How are you feeling today?":
    "Hola, soy la Dra. Chen. ¿Cómo se siente hoy?",
  "Are you currently taking any medications?":
    "¿Está tomando algún medicamento actualmente?",
  "Take this twice a day after meals.":
    "Tome esto dos veces al día después de las comidas.",

  // Per-language patient response banks
  "Spanish": {
    "Me duele mucho el pecho al respirar.": "I am having a lot of chest pain when I breathe deeply.",
    "No, no tomo medicinas.": "No, I am not taking any medications.",
    "Gracias, doctora.": "Thank you, doctor."
  },
  "Mandarin": {
    "default": "I've been feeling very dizzy since yesterday morning."
  },

  // Emergency trigger keywords (English)
  "emergency_triggers": [
    "chest pain",
    "can't breathe",
    "heart attack",
    "suicide",
    "bleeding heavily"
  ]
};
```

### 6.2 Latency Simulation

```javascript
// Simulated API response time: 400–800ms
const latency = Math.random() * 400 + 400;
```

- Represents realistic AI translation API round-trip time
- In production: replace with actual API call + `await` pattern

### 6.3 Emergency Detection

```javascript
function checkForEmergency(englishText) {
  const textLower = englishText.toLowerCase();
  const hasEmergency = translationDictionary.emergency_triggers
    .some(trigger => textLower.includes(trigger));
  if (hasEmergency) {
    // Shows #emergencyBanner element
    // Auto-hides after 10,000ms
  }
}
```

**Trigger Check Logic:**
- Runs on every message added to chat
- Checks both doctor's English text AND translated patient responses
- Text must include any trigger substring (case-insensitive)

### 6.4 Message Animation Pattern

```javascript
msgDiv.style.opacity = '0';
msgDiv.style.transform = role === 'doc' ? 'translateX(20px)' : 'translateX(-20px)';
msgDiv.style.transition = 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)';
// After append, toggle to final state:
msgDiv.style.opacity = '1';
msgDiv.style.transform = 'translateX(0)';
```

---

## 7. Language Color System

Consistent language-to-color mapping used across all pages:

```javascript
const langColors = {
  'Spanish':    '#e74c3c',   // Red
  'Mandarin':   '#e67e22',   // Orange
  'Arabic':     '#16a085',   // Teal
  'Hindi':      '#8e44ad',   // Purple
  'Russian':    '#2980b9',   // Blue
  'Tagalog':    '#d35400',   // Dark orange
  'Vietnamese': '#27ae60',   // Green
  'Portuguese': '#c0392b',   // Dark Red
  'French':     '#2c3e50',   // Dark navy
  'Korean':     '#1abc9c'    // Cyan
};

// Background version (10% opacity):
// background: `${langColors[lang]}18`   (18 = 0.09 alpha in hex)
```

---

## 8. Modal Pattern (Reused Across Pages)

### HTML Structure
```html
<div class="modal-overlay" id="myModal">
  <div class="modal-content" id="myModalContent">
    <div class="modal-header">...</div>
    <!-- body -->
    <div class="modal-footer">...</div>
  </div>
</div>
```

### Open/Close Pattern
```javascript
function openModal(overlayId, contentId) {
  const overlay = document.getElementById(overlayId);
  const content = document.getElementById(contentId);
  overlay.style.display = 'flex';
  setTimeout(() => {
    overlay.style.opacity = '1';
    content.classList.add('active');   // triggers translateY(0)
  }, 10);
}

function closeModal(overlayId) {
  const overlay = document.getElementById(overlayId);
  overlay.style.opacity = '0';
  overlay.querySelector('.modal-content').classList.remove('active');
  setTimeout(() => { overlay.style.display = 'none'; }, 300);
}
```

### Overlay-Click-to-Close
```javascript
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeModal(overlay.id);
  });
});
```

---

## 9. Session ID Generation

```javascript
// Current (client-side, demo only)
const sessionId = 'SX-' + Math.random().toString(36).substr(2, 4).toUpperCase();

// Production: Server should generate collision-resistant UUIDs
// Format: SX-{UUID4-short} or full UUID stored in DB
```

---

## 10. Navigation Architecture

```
index.html
└── Links to:
    ├── app/dashboard.html     (Provider entry)
    ├── app/receptionist.html  (Receptionist entry)
    └── app/patient_lobby.html (Patient entry)

app/dashboard.html (base sidebar)
├── app/patients.html
├── app/appointments.html
├── app/history.html
├── app/analytics.html
├── app/settings.html
├── app/receptionist.html
└── app/translator.html  (via modal → URL params)

app/translator.html
└── app/patient_lobby.html  (link generated for patient)

app/receptionist.html
├── app/translator.html  (Start Session button)
├── app/patients.html    (View Records)
└── app/appointments.html (Book Follow-Up)
```

---

## 11. Production Migration Path

To convert this prototype into a production application, the following changes are required:

### 11.1 Backend (Recommended: Node.js / Python FastAPI)
```
POST /api/sessions/create       → Create session, return sessionId
POST /api/translate             → Call translation API, return translated text
POST /api/sessions/{id}/export  → Export to EHR via FHIR
GET  /api/patients              → Paginated patient list from DB
GET  /api/analytics             → Real aggregated usage data
WebSocket /ws/session/{id}      → Real-time bidirectional translation
```

### 11.2 Replace Simulation With Real APIs
| Simulation Code | Production Replacement |
|---|---|
| `generateMockTranslation()` | OpenAI `gpt-4o` / Google Cloud Translation API |
| `simulatePatientReply()` | WebSocket message from patient's browser |
| `latency = Math.random() * 400` | Actual API response time |
| `patients[]` array | Database query (PostgreSQL / DynamoDB) |

### 11.3 Authentication Layer
- Provider login: OAuth 2.0 + MFA
- Patient join: Token-based link (no account required)
- Session tokens: short-lived JWTs (15-minute expiry for patient)

### 11.4 Database Schema
Key tables needed:
- `providers` — credentials, NPI, specialty
- `patients` — demographics, language, consent
- `sessions` — session metadata, timestamps
- `transcripts` — message-level records (with access logs for HIPAA)
- `ehr_exports` — export log with FHIR transaction records
