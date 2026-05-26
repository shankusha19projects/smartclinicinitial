# SmartClinics AI — API Integration Guide

**Document Version:** 1.0.0  
**Date:** May 9, 2026  
**Scope:** Production integration roadmap for translation, EHR, communication, and video APIs

---

## 1. Translation APIs

### 1.1 OpenAI GPT-4o (Primary Recommended)

**Use Case:** Real-time clinical translation with context awareness and term consistency

```javascript
// Production replacement for generateMockTranslation()
async function translateWithOpenAI(text, targetLanguage, clinicalContext = '') {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a certified medical interpreter. Translate the following clinical text 
                    from English to ${targetLanguage} with precision, preserving all medical 
                    terminology. Maintain tone appropriate for patient communication.
                    ${clinicalContext ? 'Context: ' + clinicalContext : ''}`
        },
        {
          role: 'user',
          content: text
        }
      ],
      max_tokens: 500,
      temperature: 0.1   // Low temperature for medical accuracy
    })
  });
  const data = await response.json();
  return data.choices[0].message.content;
}
```

**Configuration:**
| Parameter | Value | Notes |
|---|---|---|
| Model | `gpt-4o` | Best accuracy; use `gpt-4o-mini` for cost reduction |
| Temperature | `0.1` | Low randomness for clinical precision |
| Max Tokens | `500` | Sufficient for typical clinical utterances |
| API Key Header | `Authorization: Bearer` | Must be server-side only (never client) |

---

### 1.2 Google Cloud Translation API (Fallback)

**Use Case:** High-volume batch translation, language detection

```javascript
// Google Cloud Translation
async function translateWithGoogle(text, targetLanguage) {
  const response = await fetch(
    `https://translation.googleapis.com/language/translate/v2?key=${process.env.GOOGLE_TRANSLATE_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        q: text,
        target: languageCodeMap[targetLanguage],  // e.g. 'es', 'zh', 'ar'
        format: 'text'
      })
    }
  );
  const data = await response.json();
  return data.data.translations[0].translatedText;
}
```

**Language Code Mapping:**
```javascript
const languageCodeMap = {
  'Spanish':    'es',
  'Mandarin':   'zh',
  'Arabic':     'ar',
  'Hindi':      'hi',
  'Russian':    'ru',
  'Tagalog':    'tl',
  'Vietnamese': 'vi',
  'Portuguese': 'pt',
  'French':     'fr',
  'Korean':     'ko',
  'Haitian Creole': 'ht',
  'Polish':     'pl',
  'Italian':    'it',
  'German':     'de',
  'Japanese':   'ja',
  'Somali':     'so',
  'Amharic':    'am',
  'Punjabi':    'pa',
  'Bengali':    'bn',
  'Urdu':       'ur'
};
```

---

### 1.3 AWS Transcribe + Translate (Bedrock)

**Use Case:** Real-time streaming speech-to-text + translation pipeline

```javascript
// AWS Transcribe WebSocket stream (server-side)
const { TranscribeStreamingClient, StartStreamTranscriptionCommand } = require("@aws-sdk/client-transcribe-streaming");

const client = new TranscribeStreamingClient({ region: "us-east-1" });

const command = new StartStreamTranscriptionCommand({
  LanguageCode: "en-US",
  MediaEncoding: "pcm",
  MediaSampleRateHertz: 16000,
  AudioStream: audioStream,
  VocabularyName: "MedicalVocabulary"  // Custom medical term vocabulary
});
```

**Configuration:**
| Parameter | Value |
|---|---|
| Region | `us-east-1` |
| Media Encoding | `pcm` |
| Sample Rate | `16000` Hz |
| Vocabulary | Custom medical vocabulary file |
| Specialty | `PRIMARYCARE` or `CARDIOLOGY` |

---

## 2. EHR Integrations (FHIR R4)

### 2.1 Epic Systems

**FHIR Base URLs:**
```
Production:  https://{epic-instance}.epic.com/api/FHIR/R4/
Sandbox:     https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/
```

**Authentication:** OAuth 2.0 SMART on FHIR

```javascript
// Epic SMART on FHIR Auth
const epicAuthConfig = {
  clientId:    process.env.EPIC_CLIENT_ID,
  clientSecret: process.env.EPIC_CLIENT_SECRET,
  tokenUrl:    'https://{epic-instance}.epic.com/oauth2/token',
  scope:       'patient/*.read patient/*.write launch'
};
```

**Exporting Translation Session as FHIR DocumentReference:**
```javascript
async function exportSessionToEpic(session, accessToken) {
  const fhirDocument = {
    resourceType: "DocumentReference",
    status: "current",
    type: {
      coding: [{
        system: "http://loinc.org",
        code:   "34118-4",
        display: "Medical interpreter note"
      }]
    },
    subject: { reference: `Patient/${session.epicPatientId}` },
    date: new Date().toISOString(),
    content: [{
      attachment: {
        contentType: "text/plain",
        title: `Translation Session ${session.id} — ${session.lang}`,
        data: btoa(formatTranscriptText(session.transcript))
      }
    }],
    extension: [{
      url: "https://smartclinics.ai/fhir/StructureDefinition/translation-accuracy",
      valueDecimal: session.accuracy
    }]
  };

  return fetch(`${EPIC_FHIR_BASE}/DocumentReference`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/fhir+json'
    },
    body: JSON.stringify(fhirDocument)
  });
}
```

---

### 2.2 Cerner / Oracle Health

**FHIR Millennium Base URL:**
```
https://fhir-open.cerner.com/r4/{tenant-id}/
```

**Note:** Cerner uses the same FHIR R4 standard; swap the base URL and auth credentials.

---

### 2.3 athenahealth

**API Base:**
```
https://api.athenahealth.com/v1/{practice-id}/
```

athenahealth uses a proprietary REST API (not FHIR). Clinical notes are posted via the `/documents/clinicaldocument` endpoint.

---

## 3. Communication APIs

### 3.1 Twilio (SMS / Patient Link Delivery)

**SMS Sending Configuration:**
```javascript
const twilio = require('twilio');
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

async function sendPatientSessionLink(toPhone, patientName, sessionLink, language) {
  const messages = {
    'Spanish':  `Hola ${patientName}. Su médico está listo. Haga clic aquí para unirse: ${sessionLink}`,
    'Mandarin': `您好 ${patientName}。您的医生已准备好。点击加入: ${sessionLink}`,
    'Arabic':   `مرحبا ${patientName}. طبيبك جاهز. انقر للانضمام: ${sessionLink}`,
    'English':  `Hello ${patientName}. Your doctor is ready. Click to join: ${sessionLink}`
  };

  return client.messages.create({
    body: messages[language] || messages['English'],
    from: process.env.TWILIO_PHONE_NUMBER,   // e.g. '+18445550100'
    to: toPhone
  });
}
```

**Environment Variables Required:**
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+18445550100
```

---

### 3.2 Zoom (HIPAA-Compliant Video)

**Zoom Meeting SDK Config:**
```javascript
const ZoomMtg = require('@zoom/meetingsdk');

ZoomMtg.init({
  leaveUrl: `${window.location.origin}/app/dashboard.html`,
  isSupportAV: true,
  isSupportChat: false,    // Disable chat for HIPAA
  isSupportQA: false,
  success: () => {
    ZoomMtg.join({
      signature: generateZoomSignature(meetingId, role),
      meetingNumber: meetingId,
      userName: 'Dr. ' + providerName,
      apiKey: process.env.ZOOM_API_KEY,
      userEmail: providerEmail,
      passWord: meetingPassword
    });
  }
});
```

**Zoom HIPAA Requirements:**
- Must use HIPAA-eligible Zoom account
- Enable end-to-end encryption in account settings
- Disable cloud recording unless explicitly needed + consented
- Sign Business Associate Agreement with Zoom

---

## 4. WebRTC (Alternative to Zoom — Direct P2P)

For lower-latency or no-third-party video integration:

```javascript
// WebRTC Peer Connection Config
const rtcConfig = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    {
      urls: 'turn:your-turn-server.com:3478',
      username: process.env.TURN_USERNAME,
      credential: process.env.TURN_CREDENTIAL
    }
  ]
};

const peerConnection = new RTCPeerConnection(rtcConfig);
```

**Signaling Server:** Required (Node.js WebSocket, Socket.io recommended)

---

## 5. Environment Variables Reference

Create a `.env` file at project root for production:

```env
# Application
NODE_ENV=production
APP_URL=https://app.smartclinics.ai
PORT=3000

# Translation APIs
OPENAI_API_KEY=sk-...
GOOGLE_TRANSLATE_KEY=AIza...
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# EHR Integrations
EPIC_CLIENT_ID=...
EPIC_CLIENT_SECRET=...
EPIC_FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4
CERNER_TENANT_ID=...
CERNER_CLIENT_ID=...
ATHENA_PRACTICE_ID=...
ATHENA_CLIENT_KEY=...
ATHENA_CLIENT_SECRET=...

# Communication
TWILIO_ACCOUNT_SID=ACxxx...
TWILIO_AUTH_TOKEN=xxx...
TWILIO_PHONE_NUMBER=+18445550100

# Video
ZOOM_API_KEY=...
ZOOM_API_SECRET=...

# Database
DATABASE_URL=postgresql://user:password@host:5432/smartclinics_prod
REDIS_URL=redis://localhost:6379

# Auth / Encryption
JWT_SECRET=...        # min 64 chars, cryptographically random
ENCRYPTION_KEY=...    # 32-byte AES-256 key for PHI at rest

# WebSocket
WS_PORT=3001
TURN_USERNAME=...
TURN_CREDENTIAL=...
```

> 🔒 **CRITICAL:** Never commit `.env` to version control. Add to `.gitignore` immediately.

---

## 6. HIPAA Technical Safeguards Config

### 6.1 Data Encryption

```javascript
// PHI encryption at rest (AES-256-GCM)
const crypto = require('crypto');

function encryptPHI(plaintext) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm',
    Buffer.from(process.env.ENCRYPTION_KEY, 'hex'), iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return {
    iv: iv.toString('hex'),
    tag: tag.toString('hex'),
    data: encrypted.toString('hex')
  };
}
```

### 6.2 Audit Log Schema

```sql
CREATE TABLE audit_logs (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id      UUID NOT NULL,
  patient_id   UUID,
  session_id   VARCHAR(20),
  action       VARCHAR(100) NOT NULL,  -- 'view_transcript', 'export_ehr', 'start_session'
  resource     VARCHAR(200),
  ip_address   INET,
  user_agent   TEXT,
  timestamp    TIMESTAMPTZ DEFAULT NOW(),
  status       VARCHAR(20)             -- 'success' | 'denied'
);
```

### 6.3 Session Timeout

```javascript
// Auto-logout after 30 minutes of inactivity
let inactivityTimer;
const TIMEOUT_MINUTES = 30;

function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(() => {
    // Clear session, redirect to login
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = '/login?reason=timeout';
  }, TIMEOUT_MINUTES * 60 * 1000);
}

['mousemove', 'keydown', 'click', 'touchstart'].forEach(event => {
  document.addEventListener(event, resetInactivityTimer);
});
```
