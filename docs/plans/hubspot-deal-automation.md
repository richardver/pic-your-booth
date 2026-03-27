# HubSpot Deal Automation Plan

## Goal
Form submission on offerte page → Contact created in HubSpot → Deal auto-created via n8n with event fields.

## Architecture
```
Website Form → HubSpot Forms API → Contact (with temp event fields)
                                        ↓
                                   n8n Workflow
                                        ↓
                                   Create Deal (with event fields)
                                        ↓
                                   Clear temp fields on Contact
```

## Step 1: HubSpot Custom Properties (Contact level, temporary)
Create these contact properties in HubSpot (Settings > Properties):
- [ ] `last_service_type` — Dropdown: party-booth, magic-mirror, dj
- [ ] `last_event_type` — Dropdown: bruiloft, bedrijfsfeest, verjaardag, festival-club, anders
- [ ] `last_event_date` — Date picker
- [ ] `last_message` — Single-line text

Prefixed with "last_" to signal these are temporary and get moved to Deal.

## Step 2: HubSpot Form Configuration
- [ ] Add the 4 custom properties to the HubSpot form (db651e47-c976-c50d-3a00-befbb16823ba)
- [ ] Update offerte.html JS field mapping to use `last_service_type`, `last_event_type`, `last_event_date`, `last_message`
- [ ] Test form submission creates contact with all fields populated

## Step 3: HubSpot Deal Properties (Deal level, permanent)
Create these deal properties in HubSpot:
- [ ] `service_type` — Dropdown: party-booth, magic-mirror, dj
- [ ] `event_type` — Dropdown: bruiloft, bedrijfsfeest, verjaardag, festival-club, anders
- [ ] `event_date` — Date picker

## Step 4: n8n Workflow
Build workflow:
- [ ] Trigger: HubSpot webhook on contact creation/update (when last_service_type is not empty)
- [ ] Action 1: Create Deal in HubSpot linked to Contact
  - Deal name: "[service_type] - [contact name] - [event_date]"
  - Pipeline stage: "Nieuw voorstel"
  - Copy service_type, event_type, event_date from contact
  - Add message to deal notes
- [ ] Action 2: Clear temp contact fields (last_service_type, last_event_type, last_event_date, last_message)
- [ ] Test full flow end to end

## Step 5: Deal Pipeline Setup (already configured in HubSpot)

### Sales stages (open)
| Stage | Weighted |
|---|---|
| Nieuw | 10% |
| Offerte | 20% |
| Klant Nabellen (SMS) | 20% |
| Wachten op Klant | 10% |
| In Gesprek | 40% |

### Won stages (100%)
| Stage | Purpose |
|---|---|
| Akkoord | Deal confirmed |
| Voorbereiden | Prep equipment/logistics |
| Fotostrip Akkoord | Confirm photo strip design |
| Agenda bijwerken | Update calendar |
| Fotoshare + Review | Share photos, request review |
| Klant Afsluiten (SMS) | Final close, thank you |

### Lost
| Stage | |
|---|---|
| Verloren | Deal lost |

n8n workflow should create new deals in stage "Nieuw".

## Status
- [x] Portal ID connected (148115666)
- [x] Form GUID connected (db651e47-c976-c50d-3a00-befbb16823ba)
- [ ] Step 1: Custom contact properties
- [ ] Step 2: Form configuration
- [ ] Step 3: Custom deal properties
- [ ] Step 4: n8n workflow
- [ ] Step 5: Deal pipeline
