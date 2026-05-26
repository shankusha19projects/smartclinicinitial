# Documentation Index

Use these guides to understand, run, configure, deploy, and extend SmartClinics AI.

## Start Here

- [User Guide](USER_GUIDE.md): how each portal works and how to run the demo workflow.
- [Configuration Guide](CONFIGURATION.md): local settings, production environment variables, and integration setup.
- [Deployment Guide](DEPLOYMENT.md): static hosting, GitHub Pages, and production deployment path.
- [Developer Guide](DEVELOPER_GUIDE.md): file structure, code conventions, testing, and extension points.
- [Security and Compliance Guide](SECURITY_AND_COMPLIANCE.md): prototype limitations and production safeguards.
- [Troubleshooting Guide](TROUBLESHOOTING.md): common local preview and GitHub Pages issues.

## Full Specification Set

The `Spec/` directory contains the detailed product and implementation references:

- `Spec/01_product_requirements.md`
- `Spec/02_technical_architecture.md`
- `Spec/03_design_system.md`
- `Spec/04_api_integration_guide.md`
- `Spec/05_deployment_guide.md`

## Current Prototype Status

The checked-in app is a static, browser-based prototype. It simulates:

- Real-time medical translation
- Patient queue and receptionist handoff
- Translation history
- Analytics
- EHR, SMS, and video integrations
- Settings, billing, security, and team workflows

It does not perform real API calls, store PHI, send SMS messages, join video meetings, or write to EHR systems.
