# Troubleshooting Guide

## Server Does Not Start

Run from the repository root:

```powershell
python server.py
```

If port `3456` is busy:

```powershell
$env:PORT=4567
python server.py
```

## Health Check Fails

Open:

```text
http://127.0.0.1:3456/api/health
```

Expected:

```text
ok: true
databaseName: smarclinicai
```

## Login Fails

Use:

```text
Username: Shash
Password: 12345
```

If data was modified, stop the server, delete `data/smarclinicai.db`, and restart.

## App Redirects Back To Login

The session cookie may be missing or expired. Sign in again at:

```text
http://localhost:3456/app/login.html
```

## Patients Or Appointments Are Empty

Confirm the database seeded correctly:

```powershell
sqlite3 data\smarclinicai.db "SELECT COUNT(*) FROM patients; SELECT COUNT(*) FROM appointments;"
```

If needed, reset the database file.

## Icons, Fonts, Or Images Do Not Load

The demo uses public CDNs and Unsplash images. Confirm internet access or replace those assets with local files.

## Translation Does Not Call Real AI

That is expected. Translation is simulated in the local demo. Production should call an AI provider through the backend.

## EHR, SMS, Or Video Buttons Do Not Perform Real Actions

That is expected in local mode. Those integrations require production credentials, BAAs where required, secure secrets, and backend integration work.

## Git Shows Dubious Ownership

On Windows, Git may warn that the repository is owned by another user. If you trust the folder:

```powershell
git config --global --add safe.directory "C:/Partitions1/Ateequr Projects Healthcare/SmartclinicAI"
```

Or use the existing per-command `safe.directory` override.

## GitHub Push Fails

Check:

```powershell
git status --short --branch
git remote -v
git branch --show-current
```

Make sure the remote is:

```text
https://github.com/shankusha19projects/smartclinicinitial.git
```
