# Deployment Guide

This guide covers the current local deployment and the recommended production path. For cloud-specific steps, see:

- [AWS Migration Guide](AWS_DEPLOYMENT_GUIDE.md)
- [Azure Migration Guide](AZURE_DEPLOYMENT_GUIDE.md)

## Local Deployment

Start the app:

```powershell
python server.py
```

Open:

```text
http://localhost:3456/app/login.html
```

Login:

```text
Shash / 12345
```

## Current Runtime

```text
Browser
  |
  v
Python local server on localhost:3456
  |
  v
SQLite database at data/smarclinicai.db
```

## Production Deployment Direction

For a production deployment, split the app into:

- Static frontend hosting
- Backend API service
- Managed relational database
- Managed identity provider
- Secrets manager
- Observability and alerting

## Production Readiness Checklist

- Replace SQLite with managed PostgreSQL, MySQL, or SQL Server.
- Replace local login with OIDC/SSO and MFA.
- Move all secrets to a cloud secrets manager.
- Add HTTPS and secure headers.
- Add database migrations.
- Add centralized audit logging.
- Add monitoring and alerts.
- Add backup and restore procedures.
- Complete HIPAA/security review before clinical use.

## GitHub Hosting Note

The repo can be pushed to GitHub for source control and documentation. GitHub Pages alone is not enough for the current authenticated local app because the backend must run somewhere. Use GitHub for source, then deploy the backend to AWS, Azure, or another server.
