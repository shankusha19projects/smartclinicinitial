# SmartClinics AI Documentation

This folder contains the implementation and handoff documentation for the local multitenant SmartClinics AI demo.

## Primary Guides

- [Business Analyst Specs](BUSINESS_ANALYST_SPECS.md)
- [Doctor Guide](DOCTOR_GUIDE.md)
- [User Guide](USER_GUIDE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [Architect Guide](ARCHITECT_GUIDE.md)
- [Tech Stack Guide](TECHSTACK_GUIDE.md)
- [Installation Guide](INSTALLATION_GUIDE.md)
- [AWS Migration Guide](AWS_DEPLOYMENT_GUIDE.md)
- [Azure Migration Guide](AZURE_DEPLOYMENT_GUIDE.md)
- [Configuration Guide](CONFIGURATION.md)
- [Security and Compliance Guide](SECURITY_AND_COMPLIANCE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Current Demo Status

SmartClinics AI now runs as a local authenticated demo with:

- Tenant-scoped local backend
- Seed tenant: `SmartClinic Local`
- Seed user: `Shash`
- Seed password: `12345`
- Local SQL database: `data/smarclinicai.db`
- Browser screens protected by session authentication
- Patient and appointment persistence through local API endpoints

External healthcare integrations remain simulated:

- AI translation provider calls
- EHR/FHIR writes
- SMS delivery
- Video meetings
- Production billing

## Source Specs

The `Spec/` directory contains earlier product and technical source material. The files in `docs/` are the current operational handoff guides for the locally runnable system.
