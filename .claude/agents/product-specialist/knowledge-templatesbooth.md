# TemplatesBooth — Template Selection Portal

## What is TemplatesBooth?

TemplatesBooth.com is a partner platform providing photo strip template galleries. Customers browse and select a design for their photobooth event. Templates work with DSLRBooth/LumaBooth software.

**Platform:** https://templatesbooth.com
**Widget key:** `NDcxNg%3D%3D`

## Customer Workflow

1. PYB sends customer the branded design link
2. Customer sees PYB splash "Kies Jouw Design!" with confetti
3. Clicks "Bekijk Templates" → TemplatesBooth widget loads in iframe
4. Customer browses templates, selects one, fills in details, submits
5. Redirected to "Bedankt" confirmation on PYB site
6. PYB receives email notification with submission details

## Branded Design Portal

**Page:** `picyourbooth.nl/yourdesign.html`
**File:** `docs/website/deployment/yourdesign.html`

### URL Format

```
https://picyourbooth.nl/yourdesign.html?event={Event+Naam}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `event` | No | Event name shown on splash (spaces as `+`) |

### Examples

```
picyourbooth.nl/yourdesign.html?event=Bruiloft+Lisa
picyourbooth.nl/yourdesign.html
```

### Submission Redirect

After submitting, TemplatesBooth redirects to:
```
picyourbooth.nl/yourdesign.html?submitted=true
```
This shows a branded "Bedankt" confirmation with confetti.

**Important:** Set the redirect URL in TemplatesBooth widget settings to:
```
https://picyourbooth.nl/yourdesign.html?submitted=true
```

## Widget Configuration (on templatesbooth.com)

- **Language:** Dutch
- **Background color:** `#08080b`
- **Custom CSS:** Full PYB branded theme at `docs/website/deployment/assets/css/templatesbooth-widget.css`
- **Layout sizes:** 2x6 Strip (default), plus other options enabled
- **Form fields:** First Name, Last Name, Email, Event Date, Personalized text lines
- **Notification emails:** Set to PYB email for submissions
- **Redirect URL:** `https://picyourbooth.nl/yourdesign.html?submitted=true`
- **CheckCherry API key:** `NDcxNg%3D%3D` (for future CRM integration)

### Custom CSS

The widget CSS applies PYB dark luxury theme: `--bg: #08080b`, `--surface: #111116`, gold accents `#f59e42`, Bebas Neue + Space Grotesk fonts. Copy the full contents of `assets/css/templatesbooth-widget.css` into the TemplatesBooth Custom CSS field.

## Technical Notes

- TemplatesBooth allows iframe embedding (unlike fotoshare.co)
- Widget embedded via: `https://templatesbooth.com/widget-embed/?key=NDcxNg%3D%3D`
- Custom CSS can be injected via TemplatesBooth widget settings
- Page is `noindex, nofollow`
- GA4 events: `design_portal_view`, `design_widget_opened`, `design_submitted`
