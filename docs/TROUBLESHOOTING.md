# Troubleshooting Guide

Use this guide when the local preview or GitHub-hosted version does not behave as expected.

## Page Opens But Looks Unstyled

Check that the app is opened from the repository root and that relative paths resolve correctly.

Preferred local preview:

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Icons Or Fonts Do Not Load

The prototype uses external CDNs. Confirm the browser has internet access and that the network does not block:

- Google Fonts
- Cloudflare CDN for Font Awesome
- Chart.js CDN if analytics charts are used

For offline demos, replace CDN links with local files.

## Images Do Not Load

Some images are loaded from Unsplash URLs. If images are blocked or unavailable, replace the remote URLs with files under `assets/` or another local asset folder.

## Portal Links Return 404 On GitHub Pages

Confirm GitHub Pages is publishing from:

```text
branch: master
folder: /root
```

Open routes with the repository path included if GitHub Pages is project-scoped:

```text
https://<user>.github.io/<repo>/app/dashboard.html
```

## Translation Does Not Call Real APIs

That is expected. The checked-in demo uses simulated translation in `app/app.js`. To connect real translation, add a backend API and update the browser code to call it.

## Changes Disappear After Refresh

That is expected for many demo interactions. The prototype keeps most data in JavaScript memory and does not persist to a database.

## Emergency Banner Does Not Appear

Use a phrase that includes one of the configured trigger terms in English:

```text
chest pain
can't breathe
heart attack
suicide
bleeding heavily
```

The current trigger list lives in `app/app.js`.

## Git Shows Dubious Ownership

On Windows, Git may warn that the repository is owned by another user. If you trust the folder, run:

```powershell
git config --global --add safe.directory "C:/Partitions1/Ateequr Projects Healthcare/SmartclinicAI"
```

Or use Git's per-command safe directory override.

## GitHub Push Fails

Check:

- You are authenticated to GitHub.
- The remote URL is correct.
- The branch is `master`.
- You have permission to push to the repository.

Useful commands:

```powershell
git status --short --branch
git remote -v
git branch --show-current
```
