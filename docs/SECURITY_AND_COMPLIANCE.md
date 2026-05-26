# Security And Compliance Guide

SmartClinics AI is a healthcare-oriented prototype. Treat all future production work as high sensitivity.

## Prototype Status

The current repository:

- Uses simulated data.
- Does not authenticate users.
- Does not connect to real EHR systems.
- Does not send SMS messages.
- Does not call live AI translation APIs.
- Does not store PHI in a production database.
- Does not implement a full HIPAA security program.

Do not use this repository as-is with real patients or protected health information.

## Production Requirements

Before real clinical use, implement:

- User authentication
- Role-based access control
- Strong session management
- Audit logging
- Encrypted storage
- Secure backend APIs
- Vendor BAAs
- Incident response process
- Data retention and deletion policies
- Backup and disaster recovery
- Security monitoring
- Clinical quality validation

## PHI Handling

Recommended principles:

- Collect the minimum necessary PHI.
- Avoid sending PHI in SMS messages.
- Keep patient links short-lived.
- Use server-side access checks for every patient/session record.
- Encrypt PHI at rest and in transit.
- Log metadata, not full clinical text, unless retention is explicitly approved.
- Make retention periods configurable by organization policy.

## AI Translation Safety

For production translation:

- Use audited backend model calls.
- Validate language detection and medical terminology.
- Keep a human escalation path for uncertain or high-risk translations.
- Flag emergency phrases and route according to clinical policy.
- Track confidence, model version, and fallback provider.
- Test with representative clinical scenarios and languages.

## Vendor Compliance

Any vendor used for real clinical workflows may require legal and security review:

- AI provider
- Cloud hosting provider
- EHR vendor
- SMS/voice provider
- Video provider
- Logging and monitoring provider

Where required, execute a Business Associate Agreement before transmitting PHI.

## Browser Security

Recommended headers for hosted environments:

```text
Strict-Transport-Security
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
```

If the app remains static, never expose secrets in client-side files. Any privileged operation must be moved to a backend service.

## Accessibility

Healthcare software must be usable by staff and patients with different needs. Verify:

- Keyboard navigation
- Focus states
- Color contrast
- Screen reader labels
- Mobile viewport behavior
- Reduced motion considerations

See `Spec/03_design_system.md` for design-system details.
