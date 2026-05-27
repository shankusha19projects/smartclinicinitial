# Installation Guide

## Prerequisites

- Windows, macOS, or Linux
- Python 3.10 or newer
- Git
- A browser such as Chrome, Edge, Firefox, or Safari

No npm packages or Python packages are required for the current local demo.

## Clone The Repository

```powershell
git clone https://github.com/shankusha19projects/smartclinicinitial.git
cd smartclinicinitial
```

## Start Locally

```powershell
python server.py
```

Open:

```text
http://localhost:3456/app/login.html
```

## Login

```text
Username: Shash
Password: 12345
```

## Database Initialization

On startup, `server.py` creates:

```text
data/smarclinicai.db
```

It applies:

```text
data/schema.sql
```

It seeds:

- Tenant: `SmartClinic Local`
- User: `Shash`
- Patients
- Appointments

## Verify The Install

Open PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:3456/api/health
```

Expected result:

```text
ok: True
databaseName: smarclinicai
```

## Reset Local Data

Stop the server and remove:

```text
data/smarclinicai.db
```

Start again:

```powershell
python server.py
```

The database will be recreated and reseeded.

## Troubleshooting

### Port Already In Use

Set a different port:

```powershell
$env:PORT=4567
python server.py
```

Then open:

```text
http://localhost:4567/app/login.html
```

### Login Fails

Confirm you are using:

```text
Shash / 12345
```

If the database was manually changed, reset local data.

### MySQL Note

This machine had a running MySQL service named `MySQLTest`, but root access without a password was denied. The current release uses SQLite locally until MySQL credentials are available.
