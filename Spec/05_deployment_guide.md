# SmartClinics AI — Deployment Guide

**Document Version:** 1.0.0  
**Date:** May 9, 2026

---

## 1. Current State: Static Prototype

The current build is a **pure frontend prototype** — no server, no database, no authentication.

### Running Locally (Prototype)

```bash
# Option 1: VS Code Live Server
# Install the "Live Server" extension, right-click index.html → Open with Live Server

# Option 2: Python built-in server
python -m http.server 8000
# → Open http://localhost:8000

# Option 3: Node http-server
npx http-server . -p 8000
# → Open http://localhost:8000

# Option 4: Double-click index.html (some features may be limited due to CORS)
```

**Direct page access while running locally:**
```
http://localhost:8000/                             → Landing page
http://localhost:8000/app/dashboard.html           → Provider portal
http://localhost:8000/app/patients.html            → Patient registry
http://localhost:8000/app/appointments.html        → Calendar
http://localhost:8000/app/history.html             → Translation history
http://localhost:8000/app/analytics.html           → Analytics
http://localhost:8000/app/settings.html            → Settings
http://localhost:8000/app/receptionist.html        → Receptionist portal
http://localhost:8000/app/translator.html?lang=Spanish&patient=Demo+Patient
http://localhost:8000/app/patient_lobby.html?lang=Spanish&patient=Demo+Patient
```

---

## 2. Production Deployment Architecture

### 2.1 Recommended Stack (SaaS Production)

```
┌─────────────────────────────────────────────────────────────┐
│                     CloudFront CDN / Cloudflare              │
│           (SSL termination, DDoS protection, caching)        │
└────────────────────────────┬────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼──────────┐      ┌──────────▼──────────┐
    │   Static Frontend  │      │   Node.js API Server │
    │  (S3 + CloudFront) │      │   (ECS / EC2 / EKS)  │
    └────────────────────┘      └──────────┬──────────┘
                                           │
                         ┌─────────────────┼────────────────────┐
                         │                 │                    │
              ┌──────────▼──────┐  ┌───────▼───────┐  ┌────────▼──────┐
              │   PostgreSQL    │  │     Redis      │  │  WebSocket    │
              │  (RDS/Aurora)   │  │  (ElastiCache) │  │  Server       │
              └─────────────────┘  └───────────────┘  └───────────────┘
```

---

### 2.2 AWS Deployment (Recommended for HIPAA)

AWS offers a **HIPAA Eligible Services** list. Use only these for PHI:

| Service | Usage |
|---|---|
| S3 | Static frontend hosting |
| CloudFront | CDN with HTTPS enforcement |
| EC2 / ECS / Fargate | API server |
| RDS (PostgreSQL) | Patient records, sessions, transcripts |
| ElastiCache (Redis) | Session state, real-time pub/sub |
| Cognito | Authentication (MFA, SSO) |
| KMS | Encryption key management for PHI |
| WAF | Web Application Firewall |
| CloudTrail | Audit logging |
| Secrets Manager | API keys, credentials |
| Certificate Manager | SSL/TLS certificates |

**Sign AWS Business Associate Agreement (BAA) before storing any PHI.**

---

### 2.3 Environment Setup

**Step 1 — Server provisioning**
```bash
# Minimum specs for production pod
CPU:    2 vCPUs
RAM:    4 GB
Disk:   20 GB SSD
OS:     Ubuntu 22.04 LTS
```

**Step 2 — Install runtime**
```bash
# Node.js 20 LTS (recommended)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version   # v20.x.x
npm --version    # 10.x.x
```

**Step 3 — Clone and install**
```bash
git clone https://github.com/your-org/smartclinics-ai.git
cd smartclinics-ai
npm install
cp .env.example .env
# → Fill in all environment variables (see 04_api_integration_guide.md)
```

**Step 4 — Database setup**
```bash
# PostgreSQL 15+
sudo apt install postgresql postgresql-contrib

psql -U postgres -c "CREATE DATABASE smartclinics_prod;"
psql -U postgres -c "CREATE USER sc_api WITH ENCRYPTED PASSWORD 'yourpassword';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE smartclinics_prod TO sc_api;"

# Run migrations
npm run migrate
```

**Step 5 — Build and start**
```bash
# Development
npm run dev

# Production
npm run build
npm start

# With PM2 (process manager)
npm install pm2 -g
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

### 2.4 PM2 Ecosystem Config

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name:         'smartclinics-api',
      script:       './server/index.js',
      instances:    'max',            // Cluster mode
      exec_mode:    'cluster',
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    },
    {
      name:         'smartclinics-ws',
      script:       './server/websocket.js',
      instances:    1,
      env_production: {
        NODE_ENV: 'production',
        WS_PORT: 3001
      }
    }
  ]
};
```

---

### 2.5 Nginx Reverse Proxy Config

```nginx
# /etc/nginx/sites-available/smartclinics
server {
    listen 443 ssl http2;
    server_name app.smartclinics.ai;

    ssl_certificate     /etc/ssl/certs/smartclinics.crt;
    ssl_certificate_key /etc/ssl/private/smartclinics.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' cdn.jsdelivr.net cdnjs.cloudflare.com fonts.googleapis.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com; font-src fonts.gstatic.com; img-src 'self' data: images.unsplash.com;";

    # Static files (frontend)
    location / {
        root /var/www/smartclinics/dist;
        try_files $uri $uri/ /index.html;
        gzip on;
        gzip_types text/plain text/css application/json application/javascript;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket proxy
    location /ws/ {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_read_timeout 3600;
    }
}

# HTTP redirect
server {
    listen 80;
    server_name app.smartclinics.ai;
    return 301 https://$server_name$request_uri;
}
```

---

## 3. HIPAA Compliance Checklist

### Administrative Safeguards
- [ ] Assign Security Officer responsible for HIPAA compliance
- [ ] Conduct annual workforce security training
- [ ] Sign Business Associate Agreements (BAAs) with all vendors
  - [ ] AWS BAA
  - [ ] OpenAI BAA (or use Azure OpenAI with existing Azure BAA)
  - [ ] Zoom Business BAA
  - [ ] Twilio BAA
- [ ] Document incident response plan
- [ ] Conduct annual risk assessment

### Physical Safeguards
- [ ] Use HIPAA-covered data centers (AWS us-east-1, us-west-2)
- [ ] Restrict physical access to servers
- [ ] Workstation security policy (screen lock, encryption)

### Technical Safeguards
- [ ] TLS 1.2+ for all data in transit (enforced by Nginx config)
- [ ] AES-256 encryption for all PHI at rest
- [ ] Unique user authentication (no shared logins)
- [ ] Automatic session timeout (30 minutes — configured in settings)
- [ ] Audit logs for all PHI access (CloudTrail + application logs)
- [ ] Emergency access procedure (break-glass account)
- [ ] PHI deletion capability (Right to erasure workflow)
- [ ] Minimum necessary access (role-based permissions)

---

## 4. CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy SmartClinics AI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci && npm run build

      - name: Deploy to S3
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            us-east-1

      - run: aws s3 sync ./dist s3://smartclinics-frontend-prod --delete

      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} --paths "/*"
```

---

## 5. Monitoring & Alerting

### Recommended Tools

| Tool | Purpose |
|---|---|
| **AWS CloudWatch** | Server metrics, API latency, error rates |
| **Sentry** | Frontend / API error tracking |
| **Datadog / New Relic** | Full-stack APM |
| **PagerDuty** | On-call alerting |
| **Uptime Robot** | External uptime monitoring |

### Key Metrics to Alert On

```yaml
alerts:
  - name: "API Error Rate > 1%"
    threshold: "5xx errors > 1% of requests over 5 min"
    severity: critical

  - name: "Translation Latency > 2s"
    threshold: "p95 translation response > 2000ms"
    severity: warning

  - name: "Database Connection Failure"
    threshold: "DB connection refused"
    severity: critical

  - name: "Emergency Detection Failure"
    threshold: "Emergency keyword false negative rate > 0.1%"
    severity: critical
```

---

## 6. Disaster Recovery

| Scenario | RTO | RPO | Recovery Procedure |
|---|---|---|---|
| API server down | 5 min | 0 | Auto-restart via PM2 / ECS service replacement |
| Database failure | 30 min | 5 min | Failover to RDS Multi-AZ standby |
| Region outage | 4 hours | 15 min | Route53 failover to us-west-2 replica |
| Data corruption | 24 hours | 24 hours | Restore from daily automated snapshot |

**Backup Schedule:**
- Database: Continuous with 5-minute point-in-time recovery (RDS)
- Transcripts: Daily S3 backup with 7-year retention (HIPAA requirement)
- Audit logs: Immutable S3 Object Lock, 7-year retention

---

## 7. Domain & DNS Configuration

```
# DNS Records
A     app.smartclinics.ai       → CloudFront distribution IP
A     www.smartclinics.ai       → CloudFront distribution IP  
A     api.smartclinics.ai       → Load balancer IP
CNAME ws.smartclinics.ai        → api.smartclinics.ai
TXT   smartclinics.ai           → "v=spf1 include:sendgrid.net ~all"
MX    smartclinics.ai           → mail.smartclinics.ai (10)
```

**SSL Certificate:** AWS Certificate Manager (ACM) — free, auto-renewing

---

## 8. Scaling Strategy

### Vertical Scaling Thresholds
| Metric | Scale Up Trigger |
|---|---|
| CPU | > 70% for 5 minutes |
| Memory | > 80% |
| Concurrent WebSockets | > 500 per instance |

### Horizontal Scaling
- API: ECS Auto Scaling, min 2 / max 10 tasks
- WebSocket: Sticky sessions via ALB, Redis pub/sub for cross-instance messaging
- Database: Read replicas for analytics queries

### Translation Cost Optimization
- Cache repeated phrases (Redis, 24-hour TTL): reduces OpenAI calls by ~40%
- Use `gpt-4o-mini` for non-clinical exchanges; `gpt-4o` for clinical
- Batch translate if multiple patients share same phrases in same session
