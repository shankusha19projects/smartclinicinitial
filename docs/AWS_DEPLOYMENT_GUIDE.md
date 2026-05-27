# AWS Migration Guide

This guide describes how to move SmartClinics AI from local demo to AWS.

## Target AWS Architecture

```text
Route 53
  |
CloudFront + ACM
  |
S3 static frontend
  |
API Gateway or ALB
  |
ECS Fargate / Elastic Beanstalk / EC2 API service
  |
RDS PostgreSQL or MySQL
```

Supporting services:

- AWS Secrets Manager
- CloudWatch Logs and Metrics
- AWS WAF
- AWS Backup
- S3 for transcript exports if required
- SNS/Pinpoint or Twilio for messaging
- Cognito or external OIDC for identity

## Migration Steps

### 1. Prepare Application

- Split static frontend from API service.
- Move API base URL into environment configuration.
- Replace SQLite with RDS-compatible database access.
- Add database migrations.
- Add structured logging.
- Add environment-specific config.

### 2. Database

Create RDS:

- Engine: PostgreSQL or MySQL
- Multi-AZ for production
- Encryption at rest enabled
- Private subnets only
- Automated backups enabled

Migrate schema from `data/schema.sql` to RDS migration scripts.

### 3. Backend Hosting

Recommended path:

- Containerize backend.
- Push image to ECR.
- Run on ECS Fargate.
- Place service behind ALB.
- Use private subnets for tasks.
- Allow ALB ingress only on HTTPS.

### 4. Frontend Hosting

- Upload static frontend to S3.
- Serve through CloudFront.
- Use ACM certificate.
- Configure cache invalidation during releases.

### 5. Identity

Replace local login with:

- Amazon Cognito, or
- Okta/Auth0/Azure AD through OIDC

Map identity claims to:

- Tenant
- User role
- Provider profile

### 6. Secrets

Store in Secrets Manager:

- Database credentials
- AI provider keys
- EHR OAuth credentials
- SMS provider credentials
- Signing keys

### 7. Observability

Enable:

- CloudWatch application logs
- ALB access logs
- RDS logs
- CloudWatch alarms
- AWS CloudTrail

### 8. Security Checklist

- TLS 1.2+
- WAF enabled
- Least privilege IAM
- Private database subnets
- Encrypted RDS
- Secrets rotation
- Audit logs retained
- Backup restore tested
- HIPAA BAA review completed

## AWS Go-Live Checklist

- Domain resolves through Route 53.
- HTTPS certificate active.
- Frontend loads through CloudFront.
- API health endpoint works.
- Database migrations applied.
- Login works through production identity.
- Tenant isolation verified.
- Backups configured.
- Monitoring alerts configured.
- Security review completed.
