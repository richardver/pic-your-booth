# Fotoshare — Post-Event Photo Delivery

## What is Fotoshare?

Fotoshare.co is the photo sharing platform used after events to deliver photobooth photos to customers. It's integrated with LumaBooth/DSLRBooth software — photos sync automatically after the event.

**Platform:** https://fotoshare.co

## Post-Event Workflow

1. Event happens — photos taken via Party Booth or Magic Mirror XL
2. Photos sync to fotoshare.co via LumaBooth
3. PYB sends customer a branded portal link (see Portal section below)
4. Customer sees branded PYB splash page → clicks through to fotoshare.co to view/download

## Fotoshare Event Links

Each event gets a unique URL:
```
https://fotoshare.co/e/{EVENT_ID}
```

Example: `https://fotoshare.co/e/YhU4oBy5I4nMcbXAwyowM`

## Features

- Photo gallery with download capability
- Video support (MP4)
- Social sharing (WhatsApp, Facebook, Twitter, email)
- High-resolution images

## Branded Photo Portal

Instead of sending raw fotoshare.co links, PYB wraps them in a branded experience.

**Portal page:** `picyourbooth.nl/yourphotos.html`
**File location:** `docs/pyb/website/deployment/yourphotos.html`

### URL Format

```
https://picyourbooth.nl/yourphotos.html?link=https://fotoshare.co/e/{EVENT_ID}&event={Event+Naam}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `link` | Yes | Full fotoshare.co event URL |
| `event` | No | Event name shown on splash (spaces as `+`) |

### Examples

```
picyourbooth.nl/yourphotos.html?link=https://fotoshare.co/e/YhU4oBy5I4nMcbXAwyowM&event=Bruiloft+Hennevelt
picyourbooth.nl/yourphotos.html?link=https://fotoshare.co/e/ABC123&event=Verjaardag+Sophie
picyourbooth.nl/yourphotos.html?link=https://fotoshare.co/e/XYZ789
```

### Customer Experience

1. Branded PYB splash with confetti animation
2. Event name (if provided) + "Jouw Foto's Staan Klaar!"
3. Gold CTA "Bekijk Je Foto's" → navigates to fotoshare.co
4. "Laat een review achter" link → Google Business review page

### Technical Notes

- Only `fotoshare.co` URLs are whitelisted (security)
- fotoshare.co blocks iframe embedding — portal navigates directly
- Page is `noindex, nofollow`
- GA4 events: `portal_view`, `portal_photos_opened`
- Google review link: `https://g.page/r/CTQz7DQBMBoHEAE/review`
