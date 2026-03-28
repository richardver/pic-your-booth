# TemplatesBooth — Photostrip Templates & Design Selection

## What is TemplatesBooth?

TemplatesBooth.com is a partner platform providing photo strip template galleries for photobooth operators. PYB uses it to let customers choose their photostrip design before an event. Templates are compatible with DSLRBooth and LumaBooth software.

**Platform:** https://templatesbooth.com
**Account:** PYB has an active subscription
**Widget key:** `NDcxNg%3D%3D`
**CheckCherry API key:** `NDcxNg%3D%3D`

## Photostrip Template Basics

### What is a photostrip template?
A design overlay applied to the photos taken in the photobooth. It defines the layout, colors, text placement, and style of the final printed/digital photo output.

### Layout Sizes

| Layout | Dimensions | Use Case |
|--------|-----------|----------|
| **2x6 Strip** (default) | 2" x 6" | Classic photobooth strip, 2-4 photos stacked vertically |
| **2x6 Horizontal** | 6" x 2" | Horizontal strip variant |
| **4x6 Postcard (Portrait)** | 4" x 6" | Single large photo or collage, portrait |
| **4x6 Postcard (Landscape)** | 6" x 4" | Single large photo or collage, landscape |
| **4x6 Half n Half** | 4" x 6" | Split layout |
| **Square** | Various | Square format for social media |

### Image Types
- **Portrait** — vertical orientation photos
- **Landscape** — horizontal orientation photos
- **Square** — 1:1 ratio

### Photo Count Options
Templates support 1, 2, 3, or 4 images per strip.

### Animated Options
- **Animated Overlays** — GIF/video overlays (Portrait, Landscape, Square)
- **Welcome Screens** — Start screens shown before photo session
  - 1080x1920 (Portrait phone)
  - 1920x1080 (Landscape)
  - **1024x1366 (Portrait)** — iPad Pro format, used by PYB
  - 1366x1024 (Landscape)

## Template Categories

Available categories on the widget (selectable in settings):
Birthday, Wedding, Corporate, Christmas, Halloween, New Year's Eve, Nightlife, Graduation, Baby Shower, Minimalist, Retro, Tropical, Casino, Art Deco, Indian Wedding, LGBT, Valentines Day, Sports, Quinceañera, Sweet 16th, and more.

## How Templates Work with PYB Equipment

### Party Booth (LumaBooth / iPad)
- Templates loaded into LumaBooth app
- Customer selects template → LumaBooth applies it to photos
- Output: digital photo strip sent via AirDrop, email, or QR code
- Welcome screen: 1024x1366 (iPad Pro Portrait)

### Magic Mirror XL (DSLRBooth / DSLR Camera)
- Templates loaded into DSLRBooth software
- Higher resolution output (DSLR quality)
- Can print physical strips or share digitally
- Supports animated overlays

## Customer Design Selection Workflow

### Pre-Event Flow
1. Customer books PYB photobooth
2. PYB sends branded design link: `picyourbooth.nl/yourdesign.html?event={naam}`
3. Customer sees PYB splash "Kies Jouw Design!" with confetti
4. Clicks "Bekijk Templates" → TemplatesBooth widget loads in iframe
5. Customer browses templates by category, layout, orientation
6. Selects a template → fills in personalization details
7. Submits → redirected to branded "Bedankt" page
8. PYB receives email notification with submission details

### What the Customer Submits
- **Selected template** (link + preview image)
- **Last name** (required)
- **Email** (required)
- **Event date**
- **Personalized text line 1** (required) — e.g., event name, names
- **Personalized text line 2** — e.g., date, hashtag
- **Personalized text line 3** — e.g., additional text
- **Primary color** (background)
- **Secondary color**
- **Text color**
- **Other color** (if design supports)

### After Submission
1. PYB receives email with template choice + personalization details
2. PYB customizes the template in Canva or Photoshop with customer's text/colors
3. Final design loaded into LumaBooth/DSLRBooth before event
4. Template ready for the event

## Branded Design Portal

**Page:** `picyourbooth.nl/yourdesign.html`
**File:** `docs/pyb/website/deployment/yourdesign.html`

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

### States

| URL | What Shows |
|-----|-----------|
| `yourdesign.html` | Splash → Widget |
| `yourdesign.html?event=Bruiloft+Lisa` | Splash with event name → Widget |
| `yourdesign.html?submitted=true` | Branded "Bedankt" confirmation with confetti |

### Submission Redirect

Set in TemplatesBooth widget settings:
```
https://picyourbooth.nl/yourdesign.html?submitted=true
```

Uses enhanced embed code with `postMessage` listener for parent-page redirect.

## Widget Configuration (on templatesbooth.com)

### Settings
- **Language:** Dutch
- **Background color:** `#08080b`
- **Default layout:** 2x6 Strip
- **Welcome screens:** 1024x1366 (Portrait) — iPad Pro
- **Form fields:** Last Name, Email, Event Date, Personalized text lines 1-3, Colors
- **Notification emails:** Set to PYB email
- **Redirect URL:** `https://picyourbooth.nl/yourdesign.html?submitted=true`
- **Embed type:** Enhanced (parent redirect)

### Custom CSS
Full PYB dark luxury theme stored at: `docs/pyb/website/deployment/assets/css/templatesbooth-widget.css`

Applies: dark background `#08080b`, surface `#111116`, gold accents `#f59e42`, Bebas Neue + Space Grotesk fonts, pill-shaped buttons, rounded cards.

**Known limitation:** Custom CSS only applies to the gallery view (widget-embed), NOT to the form/detail page (widget-embed-form) or lightbox popup. Email sent to TemplatesBooth support requesting fix (2026-03-28).

### Visible Categories
Configurable in widget settings — can show/hide categories and pin a default category.

## Technical Notes

- TemplatesBooth allows iframe embedding (requires `frame-src https://templatesbooth.com` in CSP)
- Widget URL: `https://templatesbooth.com/widget-embed/?key=NDcxNg%3D%3D`
- Form URL: `https://templatesbooth.com/widget-embed-form?key={encoded_key}`
- Custom CSS injected via `<style id="widget_custom_css">` in widget HTML
- Page is `noindex, nofollow`
- GA4 events: `design_portal_view`, `design_widget_opened`, `design_submitted`
- Cloudflare CDN caches widget content (may delay CSS updates)

## Template File Formats

TemplatesBooth provides templates compatible with:
- **Canva** — online editing
- **DSLRBooth** — `.dslrbooth` format
- **LumaBooth** — `.lumabooth` format
- **Darkroom Booth** — `.darkroom` format
- **Adobe Photoshop** — `.psd` format
