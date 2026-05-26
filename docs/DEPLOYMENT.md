# Deployment Guide

This guide covers deployment options for the current static prototype and the recommended path for a production system.

## Static Prototype Deployment

Because the current app is static HTML/CSS/JavaScript, it can be hosted on:

- GitHub Pages
- Netlify
- Vercel static hosting
- AWS S3 plus CloudFront
- Azure Static Web Apps
- Any standard web server

## GitHub Pages

To publish the current prototype with GitHub Pages:

1. Open the repository on GitHub.
2. Go to `Settings` -> `Pages`.
3. Set source to `Deploy from a branch`.
4. Choose branch `master`.
5. Choose folder `/root`.
6. Save.

After GitHub builds the site, open the generated Pages URL. The landing page should load from `index.html`, and portal links should resolve under `/app/`.

## Local Verification Before Deploy

Run:

```powershell
python -m http.server 8000
```

Verify:

```text
http://localhost:8000
http://localhost:8000/app/dashboard.html
http://localhost:8000/app/translator.html?lang=Spanish&patient=Demo+Patient
```

## Static Hosting Notes

- Use HTTPS.
- Make sure `index.html`, `app/`, `Spec/`, and `docs/` are included.
- Do not add real secrets to the static files.
- If using a custom domain, configure DNS and HTTPS certificates.
- If assets fail to load, check CDN restrictions and Content Security Policy.

## Production Architecture

For real clinical use, the static front end should be backed by production services:

```text
Browser
  |
  | HTTPS
  v
Frontend Static Hosting
  |
  | API calls
  v
Backend API
  |-- Auth and RBAC
  |-- Translation orchestration
  |-- EHR/FHIR integration
  |-- SMS link delivery
  |-- Video session service
  |-- Audit logging
  |-- Database and encrypted storage
```

## Recommended Production Controls

- TLS 1.2 or higher
- Strong authentication and role-based access
- Server-side secret management
- PHI encryption at rest and in transit
- Audit trail for access and exports
- Configurable retention windows
- Rate limiting and abuse prevention
- Monitoring and alerting
- Backup and recovery strategy
- Vendor BAAs where required

## Deployment Checklist

- [ ] Static app builds and loads without console errors.
- [ ] All portal links resolve correctly.
- [ ] External assets are approved or self-hosted.
- [ ] No secrets are present in client code.
- [ ] Backend API is deployed behind HTTPS.
- [ ] Environment variables are configured.
- [ ] EHR OAuth redirect URLs are registered.
- [ ] SMS and video vendors are configured.
- [ ] Security headers are configured.
- [ ] HIPAA and organization compliance reviews are complete.

For a deeper infrastructure plan, see `Spec/05_deployment_guide.md`.
