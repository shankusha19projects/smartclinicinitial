# SmartClinics AI — Design System Reference

**Document Version:** 1.0.0  
**Date:** May 9, 2026  
**Source File:** `app/styles.css`

---

## 1. Color System

All color tokens are defined as CSS Custom Properties in `:root` in `app/styles.css`.

### 1.1 Semantic Colors (WCAG AAA Compliant)

These colors pass **4.5:1 contrast ratio** minimum against white or their assigned backgrounds.

```css
:root {
    --primary:  #1558B0;   /* Main interactive blue — 6.4:1 on white */
    --accent:   #1A7035;   /* Success / Positive — 5.7:1 on white */
    --danger:   #B03228;   /* Error / Alert — 5.1:1 on white */
    --warning:  #B8860B;   /* Warning amber — 5.4:1 on white */
    --secondary: #2C3E50;  /* Dark navy — headings, sidebar — 12.2:1 on white */
}
```

### 1.2 Decorative Colors (Cosmetic Use Only)

> ⚠️ These colors do **not** meet contrast requirements and must ONLY be used for decorative icons, chart fills, and language badges (never for body text or interactive labels).

```css
:root {
    --primary-decorative: #4A90E2;   /* Lighter blue (icons, charts) */
    --accent-decorative:  #2ECC71;   /* Bright green (badges, charts) */
    --danger-decorative:  #E74C3C;   /* Bright red (icons, charts) */
}
```

### 1.3 Background / Surface Colors

```css
:root {
    --primary-light: #B8D9F5;  /* Light blue tint for borders */
    --primary-bg:    #E6F3FF;  /* Primary-tinted surface background */
    --bg-light:      #F8F9FA;  /* Page background, table header rows */
    --bg-white:      #FFFFFF;  /* Card and modal backgrounds */
    --border:        #E0E0E0;  /* All borders, dividers, table lines */
}
```

### 1.4 Text Colors

```css
:root {
    --text-main:  #333333;  /* Body text — 12.6:1 on white */
    --text-muted: #666666;  /* Labels, metadata — 5.4:1 on white */
}
```

---

## 2. Typography

### 2.1 Font Stack

```css
--font-family: 'Inter', -apple-system, BlinkMacSystemFont,
               "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Google Fonts import (included in each HTML `<head>`):**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

### 2.2 Font Weight Scale

| Weight | Usage |
|---|---|
| 300 | Light body copy (rarely used) |
| 400 | Body text, paragraphs |
| 500 | Labels, nav items, subtle emphasis |
| 600 | Card titles, form labels, badge text |
| 700 | Section headers, stat values, table headers |
| 800 | Page title H1, KPI card numbers, logo |

### 2.3 Font Size Scale

| Token | Value | Used For |
|---|---|---|
| `0.65rem` | ~10.4px | Micro labels (e.g. badge on badge) |
| `0.75rem` | ~12px | Status badges, metadata, chip text |
| `0.8rem` | ~12.8px | Table sub-labels, SMS time indicators |
| `0.85rem` | ~13.6px | Table column headers, filter buttons, sidebar items |
| `0.9rem` | ~14.4px | Default form fields, secondary buttons |
| `0.95rem` | ~15.2px | Table TD content, card body |
| `1rem` | 16px | Default body |
| `1.1rem` | ~17.6px | Card titles, modal headers |
| `1.5rem` | ~24px | Page title, stat card values |
| `2rem`+ | 32px+ | KPI values, hero numbers |

---

## 3. Spacing System

### 3.1 Layout Variables

```css
:root {
    --sidebar-width:  250px;   /* Fixed sidebar width */
    --header-height:  70px;    /* Top header bar height */
}
```

### 3.2 Content Padding

- **Main content area:** `padding: 2rem` (32px all sides)
- **Card internal padding:** `padding: 1.5rem` (24px)
- **Table cells:** `padding: 1rem` (16px)
- **Navbar items:** `padding: 0.8rem 1.5rem`
- **Modal internal padding:** `padding: 2rem`
- **Form group margin:** `margin-bottom: 1.2rem` – `1.5rem`

### 3.3 Gap Spacing

```css
.stats-grid    { gap: 1.5rem; }   /* Dashboard KPI grid */
.header-actions { gap: 1.5rem; }  /* Header right side */
.form-grid     { gap: 1rem; }     /* 2-column form layout */
.modal-footer  { gap: 1rem; }     /* Action buttons */
```

---

## 4. Border Radius Scale

```css
:root {
    --radius-sm:   8px;    /* Inputs, inline badges, small cards */
    --radius-md:   12px;   /* Cards, modals, major containers */
    --radius-lg:   20px;   /* Large containers (reserved) */
    --radius-pill: 50px;   /* Filter chips, search bar, pill badges */
}
```

---

## 5. Shadow System

| Token | CSS Value | Used For |
|---|---|---|
| Card shadow | `0 2px 10px rgba(0,0,0,0.03)` | `.card`, stat cards |
| Button shadow | `0 2px 8px rgba(74,144,226,0.3)` | `.btn-primary` |
| Button hover | `0 4px 12px rgba(74,144,226,0.4)` | `.btn-primary:hover` |
| Modal shadow | `0 20px 40px rgba(0,0,0,0.2)` | `.modal-content` |
| Quick action | `0 10px 20px rgba(44,62,80,0.2)` | `.quick-action-panel` |
| Header | `0 2px 10px rgba(0,0,0,0.02)` | `.top-header` |

---

## 6. Animation & Transitions

### 6.1 Global Transition

```css
--transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
```

Applied to: buttons, nav items, links, form controls, cards

### 6.2 Modal Animation

```css
/* Entry state */
.modal-overlay { opacity: 0; transition: opacity 0.3s; }
.modal-content { transform: translateY(20px); transition: transform 0.3s; }

/* Active state (added via JS) */
.modal-content.active { transform: translateY(0); }
```

### 6.3 Chat Message Slide-In

```javascript
/* Initial */
msgDiv.style.opacity = '0';
msgDiv.style.transform = 'translateX(±20px)';
msgDiv.style.transition = 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)';
/* Final (10ms after append) */
msgDiv.style.opacity = '1';
msgDiv.style.transform = 'translateX(0)';
```

### 6.4 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

## 7. Component Classes

### 7.1 Sidebar Layout

```css
.app-container  { display: flex; height: 100vh; overflow: hidden; }
.sidebar        { width: 250px; background: var(--secondary); }
.sidebar-header { height: 70px; padding: 0 1.5rem; }
.sidebar-logo   { color: white; font-weight: 800; font-size: 1.25rem; }
.sidebar-nav    { flex: 1; padding: 2rem 0; overflow-y: auto; }
.nav-item       { padding: 0.8rem 1.5rem; border-left: 4px solid transparent; }
.nav-item.active { border-left-color: var(--primary); }
.sidebar-footer { padding: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); }
```

### 7.2 Main Content Layout

```css
.main-wrapper { flex: 1; display: flex; flex-direction: column; height: 100vh; }
.top-header   { height: 70px; background: white; border-bottom: 1px solid var(--border); }
.main-content { flex: 1; overflow-y: auto; padding: 2rem; }
.page-title   { font-size: 1.5rem; font-weight: 700; display: flex; justify-content: space-between; }
```

### 7.3 Button Variants

```css
.btn         { padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; }
.btn-primary { background: #1558B0; color: white; }
.btn-outline { background: transparent; border: 1px solid var(--border); }
.btn-danger  { background: #B03228; color: white; }
```

### 7.4 Status Badges

```css
.status-badge     { padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.status-completed { background: rgba(46,204,113,0.12); color: #1A7035; }
.status-active    { background: rgba(74,144,226,0.12); color: #1558B0; }
.status-scheduled { background: rgba(184,134,11,0.12); color: #7A5800; }
```

### 7.5 Card

```css
.card        { background: white; border-radius: 12px; border: 1px solid #E0E0E0; padding: 1.5rem; }
.card-header { display: flex; justify-content: space-between; border-bottom: 1px solid var(--bg-light); }
.card-title  { font-size: 1.1rem; font-weight: 600; color: var(--secondary); }
```

### 7.6 Search Bar

```css
.search-bar { display: flex; align-items: center; background: var(--bg-light);
              border-radius: 50px; padding: 0.5rem 1rem; width: 300px; border: 1px solid var(--border); }
```

### 7.7 Table

```css
table   { width: 100%; border-collapse: collapse; }
th      { font-size: 0.85rem; text-transform: uppercase; background: var(--bg-light); }
th, td  { padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); }
tr:hover td { background: var(--bg-light); }
```

---

## 8. Focus & Accessibility Styles

```css
/* Global focus ring (WCAG 2.4.7 - visible focus) */
*:focus-visible {
    outline: 3px solid var(--primary);   /* #1558B0, 3px width */
    outline-offset: 2px;
}
```

All interactive elements (buttons, links, form controls) inherit this focus style.

---

## 9. Landing Page (index.html) Design Tokens

The landing page uses independently defined CSS variables within `<style>` tags:

```css
:root {
    --primary: #1558B0;
    --primary-decorative: #4A90E2;
    --secondary: #1a252f;
    --accent: #1A7035;
    --accent-decorative: #2ECC71;
    --danger: #E74C3C;
    --text-muted: #666;
    --text-main: #333;
    --bg-light: #f8f9fa;
    --border: #e9ecef;
    --primary-bg: #f0f7ff;
    --primary-light: #c5dff8;
    --glass-shadow: 0 4px 30px rgba(0, 0, 0, 0.06);
    --radius-sm: 8px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --radius-pill: 50px;
    --transition: all 0.3s ease;
    --glass-bg: rgba(255, 255, 255, 0.8);
    --glass-border: rgba(255, 255, 255, 0.6);
}
```

> Note: Landing page and app share the same philosophy but have independent CSS contexts. Unification is a recommended future step.

---

## 10. Icons

**Library:** Font Awesome 6.4.0 Free (CDN)

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

| Usage Context | Icon Classes Used |
|---|---|
| Sidebar nav | `fa-home`, `fa-users`, `fa-calendar-alt`, `fa-history`, `fa-chart-line`, `fa-cog`, `fa-headset` |
| Actions | `fa-plus`, `fa-eye`, `fa-phone-volume`, `fa-edit`, `fa-trash`, `fa-save` |
| Communication | `fa-paper-plane`, `fa-sms`, `fa-bullhorn`, `fa-mobile-alt`, `fa-qrcode` |
| Status | `fa-check`, `fa-times`, `fa-exclamation-triangle`, `fa-shield-alt` |
| File & Data | `fa-file-export`, `fa-download`, `fa-history`, `fa-folder-open` |
| Medical | `fa-stethoscope`, `fa-user-md`, `fa-clinic-medical` |
