# SmartClinics AI — Product Specification & Requirements Document

**Document Version:** 1.0.0  
**Date:** May 9, 2026  
**Status:** ✅ Production-Ready Prototype  
**Prepared By:** SmartClinics AI Engineering Team  
**Company:** DOT STAR INC

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Portals & User Roles](#3-portals--user-roles)
4. [Functional Requirements](#4-functional-requirements)
5. [Technical Architecture](#5-technical-architecture)
6. [Design System & UI](#6-design-system--ui)
7. [Security & Compliance](#7-security--compliance)
8. [Integration Requirements](#8-integration-requirements)
9. [Performance Requirements](#9-performance-requirements)
10. [Accessibility Requirements](#10-accessibility-requirements)
11. [Translation Engine Specification](#11-translation-engine-specification)
12. [Deployment Requirements](#12-deployment-requirements)
13. [Future Roadmap](#13-future-roadmap)

---

## 1. Executive Summary

SmartClinics AI is a **HIPAA-compliant, real-time AI medical translation platform** designed to eliminate language barriers in clinical settings. The platform reduces interpreter costs by up to 96.8% while improving patient outcomes through 24/7 multilingual healthcare communication.

### Key Metrics (Prototype Simulation)
| Metric | Value |
|---|---|
| AI Translation Accuracy | 98.7% (BLEU > 45) |
| Latency Target | < 800ms per translation |
| Languages Supported | 20+ languages |
| Cost Per Minute | $0.05 (vs $1.00–$2.00 for human interpreters) |
| EHR Integrations | Epic, Cerner/Oracle, athenahealth |
| Compliance | HIPAA, HITRUST, WCAG AAA |

---

## 2. Product Overview

### 2.1 Problem Statement
- Approximately **67 million people** in the US speak a language other than English at home
- Federal law (Title VI, Affordable Care Act Section 1557) requires language access in federally funded healthcare
- Human medical interpreters cost **$1.00–$2.00/minute** with 15–45 minute scheduling delays
- Language barriers cause: misdiagnoses, avoidable readmissions, informed consent failures

### 2.2 Solution
SmartClinics AI provides real-time AI-powered translation integrated directly into the clinical workflow — no scheduling, no delay, no separate app needed for patients.

### 2.3 Business Model
| Plan | Price | Minutes | Languages |
|---|---|---|---|
| Starter | $99/mo | 500 min | 10 languages |
| Professional | $199/mo | 2,000 min | 20 languages |
| Enterprise | Custom | Unlimited | All 100+ languages |

---

## 3. Portals & User Roles

SmartClinics AI consists of three functional portals, each scoped to a distinct user role.

### 3.1 Provider Portal (Doctor/Clinician)
**Entry:** `app/dashboard.html`  
**Primary Users:** Physicians, Nurse Practitioners, PAs, Specialists

Includes:
- Main dashboard with today's schedule and KPIs
- Patient Registry management
- Appointment Calendar (Day/Week/Month views)
- Active Translation Session workspace
- Translation History & transcript review
- Analytics & ROI dashboard
- Settings (profile, translation preferences, integrations, security, billing, team)

### 3.2 Receptionist Portal
**Entry:** `app/receptionist.html`  
**Primary Users:** Front desk staff, MA, patient coordinators

Includes:
- Live patient arrival queue
- Walk-in check-in workflow
- Room and copay management
- SMS communication to patients
- Patient link generation and delivery

### 3.3 Patient Portal
**Entry:** `app/patient_lobby.html`  
**Primary Users:** Patients (any language background)

Includes:
- No-app-required mobile web interface
- Real-time translated conversation view
- Microphone input (tap-and-hold)
- Language-first design (text in patient's native language)

---

## 4. Functional Requirements

### 4.1 Landing Page (`index.html`)

#### Navigation Bar
- Logo with SVG icon and company name
- Links: Features, How It Works, Pricing, Portals, About
- "Launch App" CTA button → `app/dashboard.html`
- Mobile hamburger menu with accessible toggle

#### Sections Required
| Section | Description |
|---|---|
| Hero | H1, subhead, 2 CTA buttons, stats bar |
| Problem | Language barrier statistics and impact |
| How It Works | 4-step workflow with icons |
| Features | Grid of core capabilities |
| Security | HIPAA, encryption, retention badges |
| Pricing | 3-tier cards (Starter, Professional, Enterprise) |
| Testimonials | 3 customer quotes |
| ROI Calculator | Dual-range slider with live savings calculation |
| FAQ | Accordion with 4 items |
| Comparison Table | SmartClinics vs competitors |
| Portal Access | 3 portal entry cards |
| Press | Forbes, TechCrunch, Healthcare IT News |
| Final CTA | Trial signup |
| Footer | Company info, links, legal |

---

### 4.2 Provider Dashboard (`app/dashboard.html`)

#### KPI Stats Bar
- Total Translations Today
- Average Latency (ms)
- Time Saved (minutes)
- EHR Exports Completed

#### Today's Patient Schedule Table
- Columns: Time, Patient Name, Language Tag, Appointment Type, Status Badge, Action Button
- "Prepare Session" → opens `New Translation Session` modal
- Status values: `Scheduled`, `In Progress`, `Completed`

#### "New Translation Session" Modal
**Required Fields:**
- Patient Name (text input)
- Patient Language (dropdown, 10 language options)
- Session Type (dropdown: In-Person / Telehealth)
- Notes (textarea, optional)

**Behavior on Submit:**
- Validates required fields
- Generates unique Session ID (format: `SX-XXXX`)
- Generates Patient Link URL: `patient_lobby.html?lang={lang}&patient={name}`
- Displays copyable link for SMS/sharing
- "Start Session" button → navigates to `translator.html?lang={lang}&patient={name}`

---

### 4.3 Patient Registry (`app/patients.html`)

#### Patient Table
- Columns: Patient (avatar + name + ID), DOB/Age, Language Tag, Last Visit, Status Badge, Actions
- Action buttons: View (eye icon), Start Session (phone icon)

#### Filter System
- Filter buttons: All, Active, Scheduled Today, Completed, Spanish, Mandarin, Arabic
- Active filter has `var(--primary)` background
- Search bar: searches name, ID, email, language (live keyup filter)

#### Add Patient Modal
**Fields:**
| Field | Type | Required |
|---|---|---|
| First Name | text | ✅ |
| Last Name | text | ✅ |
| Date of Birth | date | ✅ |
| Patient ID | text (auto-generated) | Read-only |
| Preferred Language | select | ✅ |
| Phone Number | tel | — |
| Email | email | — |
| Insurance Provider | text | — |
| Notes | textarea | — |

**Behavior:**
- Auto-generates `PT-{n}` ID on modal open
- Adds to `patients[]` array on submit
- Re-renders table with new record at top

#### Patient Detail Modal
Sections:
1. **Demographics** — 8-field grid (ID, DOB, Age, Language, Phone, Email, Insurance, Status)
2. **Clinical Notes** — free text
3. **Visit History** — list with date, type, duration, provider

---

### 4.4 Appointments (`app/appointments.html`)

#### View Modes
| Mode | Description |
|---|---|
| Day View | Hour-by-hour slots (7 AM – 4:30 PM), appointment blocks per time |
| Week View | 7-column grid with day headers |
| Month View | Classic calendar grid with appointment dots |

#### Appointment Block (Day View)
- Left border color-coded by language
- Patient name + status badge
- Type, language, duration subtitle
- Click → launches `translator.html?lang={lang}&patient={name}`

#### Today's Queue List
- Rendered below calendar
- Each row: time, patient name, type, duration, language tag, action button
- Completed sessions show `Completed` badge; scheduled show `Start` button

#### Schedule Appointment Modal
**Fields:**
| Field | Type | Values |
|---|---|---|
| Patient Name | text + datalist | Autocomplete from patient names |
| Date | date | Default: today |
| Time | select | 7:00 AM – 4:30 PM in 30-min slots |
| Appointment Type | select | Follow-up, Initial Consult, Routine Checkup, Urgent Care, Telehealth, Lab, Prescription Review |
| Patient Language | select | 7 language options |
| Notes | textarea | Optional |

---

### 4.5 Translation History (`app/history.html`)

#### History Table
- Columns: Session ID, Patient, Date/Time, Language, Duration, Accuracy, EHR Status, Actions
- Session ID styled in monospace with `var(--primary)` color
- Emergency sessions marked with ⚠ warning icon
- Accuracy shown as numeric value + animated bar

#### Filter Controls
| Filter | Type | Options |
|---|---|---|
| Language | select | All, Spanish, Mandarin, Arabic, Hindi, Russian |
| Date | select | All, Today, This Week, This Month |
| EHR Status | select | All, EHR Exported, Pending Export |

#### Session Transcript Modal
- **Metadata bar** (4 items): Duration, Accuracy, Exchanges, EHR Status
- **Transcript viewer** — bilingual bubble layout, color-coded by role
  - Doctor messages: right-aligned, blue background
  - Patient messages: left-aligned, white with border
  - Each bubble shows original text + italic translation subtitle
- **Actions**: Close, Print, Export to EHR
- EHR Export triggers toast notification and updates table row status

#### CSV Export
- Generates columns: Session ID, Patient, Date, Language, Duration, Accuracy, EHR Status
- File: `translation_history.csv`

---

### 4.6 Analytics (`app/analytics.html`)

#### KPI Cards (4)
| Card | Value | Change |
|---|---|---|
| Total Translations | 342 | +18% |
| Average Accuracy | 98.2% | +0.4% |
| Interpreter Time Saved | 143h | +22h |
| Cost Savings | $4,290 | vs traditional |

#### Charts (Chart.js 4.x)
| Chart | Type | Data |
|---|---|---|
| Translation Volume | Line (filled) | 30 data points, last 30 days |
| Language Distribution | Doughnut | 6 languages |
| AI Model Usage | Bar | 3 models (OpenAI, Gemini, Bedrock) |

#### Language Breakdown
- Animated bar chart (CSS-only)
- Spanish 48%, Mandarin 22%, Arabic 15%, Hindi 9%, Russian 6%

#### Patient Satisfaction
- Star rating display (4.8/5)
- Individual star breakdown bars (5★ 72%, 4★ 20%, 3★ 8%)

#### ROI Summary
- Dark gradient banner
- 4 metrics: Human cost, SmartClinics cost, Net savings, Cost reduction %

---

### 4.7 Settings (`app/settings.html`)

#### Tab: Profile
- Avatar upload (UI only)
- Fields: First/Last Name, Title/Specialty, NPI Number, Email, Phone, Bio

#### Tab: Translation
- Default Provider Language (select)
- AI Translation Model (select: Auto, OpenAI GPT-4o, Gemini, AWS Bedrock)
- Translation Formality (select: Clinical, Conversational, Simple)
- Emergency Detection Sensitivity (select: High, Medium, Low)
- Toggle switches (4): Live Subtitles, Speaker Diarization, Auto Transcription, Emergency SMS
- Medical Glossary editor (dynamic add/remove rows)

#### Tab: Notifications
- Toggle switches (6): Appointment Reminders, Emergency Alerts, Session Summary, EHR Confirmation, Weekly Reports, Marketing

#### Tab: Integrations
- EHR: Epic (connected), Cerner (disconnected), athenahealth (disconnected)
- Communication: Twilio SMS/Voice (connected), Zoom HIPAA (connected)

#### Tab: Security
- Password change (3 fields)
- Toggle switches (3): 2FA, Biometric Login, Auto-Logout
- Danger Zone: Delete Account button

#### Tab: Billing
- Current plan display (Professional, $199/mo)
- Usage progress bars (minutes, sessions)
- Change Plan / Cancel buttons

#### Tab: Team
- Team member list with avatar, name, email, role selector, status badge
- Invite by email (prompt dialog)

---

### 4.8 Receptionist Portal (`app/receptionist.html`)

#### Header Bar (Dark)
- Back link to Provider Portal
- Station label with real-time clock (`HH:MM:SS`)
- Walk-In Check-In button

#### Queue Panel (380px sidebar)
- Patient cards with: color-coded avatar, name, check-in status dot, language, appointment time, visit type
- Status types:
  - 🟢 (green pulse) — Checked In
  - 🔵 (blue) — In Room  
  - 🟡 (yellow) — Scheduled
- Selection highlights card with `var(--primary-bg)` background

#### Patient Workspace (right panel)
Activated on queue item selection:

**Header:** Large avatar, patient name, status badge, appointment summary, action buttons (Start Translation Session, Call to Exam Room)

**Detail Grid (6 items):** Insurance, Phone, Wait Time (live calculated), Check-In Time, Assigned Room, Copay

**Quick Actions (6 cards):**
| Action | Behavior |
|---|---|
| Assign Room | Prompt → updates room field and status to "In Room" |
| Collect Copay | Alert confirmation |
| Send Patient Link | Confirm dialog → SMS simulation alert |
| View Records | Navigate to `patients.html` |
| Book Follow-Up | Navigate to `appointments.html` |
| Mark No-Show | Confirm → removes from queue |

**SMS Composer:**
- 4 quick-select templates: Room Ready, Running Late, Appt Reminder, Lab Results
- Free-text textarea
- Send button with recipient phone display

#### Walk-In Check-In Modal
**Fields:** Patient Name (autocomplete), Appointment Time (select), Language (select), Visit Reason (text)  
**Behavior:** Adds new patient entry to queue list on submit

---

### 4.9 Translator (Active Session) (`app/translator.html`)

**URL Parameters:** `?lang={LANG}&patient={NAME}`

#### Layout
- Left panel: video placeholder (provider/patient feeds)
- Right panel: live bilingual chat transcript

#### Session Header
- Patient name and language badge
- Session ID display
- Live session timer (MM:SS)
- Simulated latency indicator
- End Session button

#### Chat Transcript
- Doctor messages: right-aligned blue bubbles
- Patient messages: left-aligned white bubbles
- Each bubble: original text + italic subtitle translation
- Animated slide-in on append

#### Emergency Banner
- Red/amber alert bar (hidden by default)
- Appears when emergency keywords detected
- Auto-hides after 10 seconds
- Keywords: `chest pain`, `can't breathe`, `heart attack`, `suicide`, `bleeding heavily`

#### Input Form
- Text input with placeholder
- Microphone button (mousedown/touchstart: recording state, mouseup/touchend: submit)
- Submit button

#### Simulation Controls
- "Simulate Patient Reply" button
- "Trigger Emergency" button

---

### 4.10 Patient Lobby (`app/patient_lobby.html`)

**URL Parameters:** `?lang={LANG}&patient={NAME}`

- Language detection from URL parameter
- Welcome message displayed in patient's language
- Provider speaking → patient sees translated text
- Patient speaks → tap-and-hold mic, release to send
- Mobile-optimized layout
- No login or app installation required
