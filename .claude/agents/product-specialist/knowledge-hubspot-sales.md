# HubSpot & Sales Pipeline

## HubSpot Account

- **Portal ID:** 148115666
- **Region:** EU (eu1)
- **Plan:** Free tier (no workflows)
- **Form GUID:** d94791f2-5db1-434e-802f-beec5a08ee94 (offerte form)

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

### Contact Properties (on HubSpot Form)

| HubSpot Internal Name | Type | Notes |
|---|---|---|
| `lastname` | Built-in | "Naam" field from website form |
| `email` | Built-in | From form |
| `phone` | Built-in | From form |
| `service_type` | Custom dropdown | party-booth, magic-mirror, dj |
| `evenement_type` | Custom dropdown | bruiloft, bedrijfsfeest, verjaardag, festival-club, anders |
| `evenement_date` | Custom date | Event date (dd-mm-yyyy format) |
| `evenement_upgrades` | Custom multiple checkboxes | vip, keychain, host, ai_photobooth, live_dj, premium_design, levering, ai_background+filters |
| `message` | Custom text | Optional message from visitor |

| `evenement_starttime` | Custom text | Start time of event — not collected on offerte form, filled in later during sales process |

### Upgrade Values (for `evenement_upgrades` checkboxes)

**Magic Mirror XL:**
| Label | CRM Value | Price |
|---|---|---|
| VIP Upgrade | `vip` | +€ 149 |
| Wedding Keychain Station | `keychain` | +€ 499 |
| Photobooth Host | `host` | +€ 149 |
| AI Photo Experience | `ai_photobooth` | +€ 499 |
| Live DJ Set | `live_dj` | +€ 149 |

**Party Booth:**
| Label | CRM Value | Price |
|---|---|---|
| Premium Ontwerp | `premium_design` | +€ 25 |
| Levering & Ophalen | `levering` | +€ 49 |
| AI Foto's + Filters | `ai_background+filters` | +€ 49 |
| Live DJ Set | `live_dj` | +€ 149 |

**DJ:**
| Label | CRM Value | Price |
|---|---|---|
| Extra uur (4 uur totaal) | `dj_extra_uur_1` | +€ 49 |
| Extra uur (5 uur totaal) | `dj_extra_uur_2` | +€ 98 |
| Extra uur (6 uur totaal) | `dj_extra_uur_3` | +€ 147 |

### Deal Properties

**Built-in:**

| Property | Type | Notes |
|---|---|---|
| Deal name | Text | `[Service] - [Contact Name] - [Event Date]` |
| Amount | Number | Deal value |
| Close date | Date | Maps to `event_date` |
| Deal owner | User | HubSpot user |

**Custom (5 properties, filled during sales/planning):**

| Property | Type | Notes |
|---|---|---|
| `venue_location` | Text | Venue name + address |
| `evenement_starttime` | Text | Start time of event (e.g. "20:00") |
| `evenement_delivery_time` | Text | Time equipment arrives at venue (e.g. "18:00") |
| `evenement_pickup_time` | Text | Time equipment gets picked up (e.g. "01:00") |
| `assigned_operator` | Dropdown | luca, milo, richard — DJ bookings only |

**Form data (stays on Contact + form submission, not duplicated on Deal):**
- `service_type`, `event_type`, `event_date`, `evenement_upgrades`, `message` — available via Contact association and form submission record

### Deal Naming Convention

`[Service] - [Contact Name] - [Event Date]`
Example: `Magic Mirror XL - Lisa de Vries - 2026-06-15`

## Automation (n8n)

Form submit → Contact created with fields → n8n trigger → Create Deal in "Nieuw" stage → Copy event fields to Deal.

Free-tier workaround for HubSpot's paid workflow feature.

## Form Fields → HubSpot Mapping

| Website Form Field | HubSpot Property | Notes |
|---|---|---|
| naam | `lastname` | Built-in Last Name property |
| email | `email` | Built-in |
| telefoon | `phone` | Built-in |
| service | `service_type` | Custom dropdown |
| type-event | `evenement_type` | Custom dropdown |
| datum | `evenement_date` | Custom date |
| upgrades (from URL) | `evenement_upgrades` | Semicolon-separated checkbox values |
| bericht | `message` | Custom text |
