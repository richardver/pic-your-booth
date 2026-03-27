# HubSpot & Sales Pipeline

## HubSpot Account

- **Portal ID:** 148115666
- **Region:** EU (eu1)
- **Plan:** Free tier (no workflows)
- **Form GUID:** db651e47-c976-c50d-3a00-befbb16823ba (offerte form)

## Funnel

Meta Ads → Website → Offerte Form → HubSpot Contact + Deal → Follow-up → Booked

## Deal Pipeline

### Sales Stages (open)

| Stage | Probability | Purpose |
|---|---|---|
| Nieuw | 10% | Fresh lead from form submission |
| Offerte | 20% | Proposal sent to client |
| Klant Nabellen (SMS) | 20% | Follow-up call/SMS to client |
| Wachten op Klant | 10% | Waiting for client response |
| In Gesprek | 40% | Active conversation, negotiating |

### Won Stages (100%, operational checklist)

| Stage | Purpose |
|---|---|
| Akkoord | Deal confirmed by client |
| Voorbereiden | Prep equipment and logistics |
| Fotostrip Akkoord | Confirm photo strip design with client |
| Agenda bijwerken | Update team calendar |
| Fotoshare + Review | Share photos with client, request review |
| Klant Afsluiten (SMS) | Final close, thank you message |

### Lost

| Stage | Purpose |
|---|---|
| Verloren | Deal lost |

## Data Model

Contact (person) → has many Deals (bookings)

### Contact Properties

| Property | Type | Notes |
|---|---|---|
| firstname | Built-in | From form |
| email | Built-in | From form |
| phone | Built-in | From form |
| last_service_type | Custom dropdown | Temp, moved to Deal by n8n |
| last_event_type | Custom dropdown | Temp, moved to Deal by n8n |
| last_event_date | Custom date | Temp, moved to Deal by n8n |
| last_message | Custom text | Temp, moved to Deal by n8n |

### Deal Properties

| Property | Type | Values |
|---|---|---|
| service_type | Dropdown | party-booth, magic-mirror, dj |
| event_type | Dropdown | bruiloft, bedrijfsfeest, verjaardag, festival-club, anders |
| event_date | Date | Event date |

### Deal Naming Convention

`[Service] - [Contact Name] - [Event Date]`
Example: `Magic Mirror XL - Lisa de Vries - 2026-06-15`

## Automation (n8n)

Form submit → Contact created with temp fields → n8n trigger → Create Deal in "Nieuw" stage → Copy event fields → Clear temp contact fields.

Free-tier workaround for HubSpot's paid workflow feature.

## Form Fields → HubSpot Mapping

| Website Form | HubSpot Property | Object |
|---|---|---|
| naam | firstname | Contact |
| email | email | Contact |
| telefoon | phone | Contact |
| service | last_service_type | Contact (temp) |
| type-event | last_event_type | Contact (temp) |
| datum | last_event_date | Contact (temp) |
| bericht | last_message | Contact (temp) |
