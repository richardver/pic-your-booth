# YouTube Shorts Strategie

Platform-specifieke kennis voor YouTube Shorts. Gericht op DJ release clips en event content — dezelfde 9:16 assets als TikTok/Reels.

---

## Waarom YouTube Shorts

| Voordeel | Detail |
|---|---|
| **Zelfde asset** | TikTok/Reels content (9:16, <60s) werkt 1:1 als Short |
| **Zero extra productie** | Remotion rendert exact hetzelfde formaat |
| **Discovery engine** | Shorts worden algoritmisch gepusht naar nieuwe kijkers |
| **SEO** | YouTube is de #2 zoekmachine — "DJ Gianni" begint te ranken |
| **Link in description** | Directe traffic naar SoundCloud/Spotify/website |
| **YouTube API** | Uploads zijn automatiseerbaar (in tegenstelling tot SoundCloud) |

---

## Platform Specs

| Element | Spec |
|---|---|
| Aspect ratio | 9:16 (vertical) |
| Resolutie | 1080x1920 |
| Max lengte | 3 minuten (sinds 2024) |
| Ideale lengte | 30-60 seconden |
| Bestandsformaat | MP4, MOV |
| Max bestandsgrootte | 256 GB |
| Thumbnail | Automatisch geselecteerd (geen custom thumbnail voor Shorts) |
| Titel max | 100 tekens |

---

## YouTube Shorts Algoritme

### Ranking Signalen

| # | Signaal | Toelichting |
|---|---------|------------|
| 1 | **Watch time / completion** | Volledig bekeken Shorts ranken hoger. Loop-watch telt ook. |
| 2 | **Engagement** | Likes, comments, shares — in die volgorde van belang |
| 3 | **Subscribe clicks** | Shorts die volgers opleveren worden meer gepusht |
| 4 | **Swipe-away rate** | Laag = goed. Hoe sneller iemand swipt, hoe slechter het signaal |
| 5 | **Relevance** | Titel, beschrijving, hashtags matchen met kijkgedrag |

### Verschil met TikTok

| Aspect | TikTok | YouTube Shorts |
|---|---|---|
| Ontdekking | For You Page, geluid-gebaseerd | Shorts shelf, zoekresultaten, suggesties |
| Levensduur | Kort (48-72 uur piek) | Lang (Shorts blijven maanden ontdekt worden) |
| Audio | Trending sounds essentieel | Eigen audio werkt goed, minder sound-afhankelijk |
| SEO | Minimaal | Sterk — titel, beschrijving, tags worden geïndexeerd |
| Publiek | Jonger (16-24) | Breder (18-45) |
| Muziek/DJ content | Goed voor clips | Uitstekend — YouTube is #1 voor muziekontdekking |

---

## Upload Optimalisatie

### Titel Format

```
DJ Gianni - [Genre] Mix [Clip Type] | [Mood] #Shorts
```

Voorbeelden:
- `DJ Gianni - Afro Beats Mix Drop 🔥 | Summer Vibes #Shorts`
- `DJ Gianni - Caribbean Party Set | Live at Rotterdam #Shorts`
- `DJ Gianni - Nederlands Urban Mix Teaser | Vol. 1 #Shorts`

### Beschrijving Template

```
[1-2 zinnen over de vibe/clip]

Volledige mix op SoundCloud: [link]
Spotify playlist: [link]

Boekingen: picyourbooth.nl
Instagram: @djgianni
TikTok: @djgianni

#DJGianni #AfroBeats #DJMix #Party #Rotterdam #Nederland
```

### Tags & Hashtags

**Altijd gebruiken:** `#Shorts` `#DJGianni` `#DJMix`

**+ Afro Beats:** `#AfroBeats` `#Amapiano` `#AfroHouse` `#AfroVibes`
**+ Caribbean:** `#Caribbean` `#Dancehall` `#Soca` `#Reggaeton`
**+ Nederlands:** `#DutchDJ` `#NederlandseDJ` `#UrbanNL` `#DutchHipHop`
**+ Event:** `#Bruiloft` `#Feest` `#Party` `#Rotterdam` `#DJHuren`

---

## YouTube Data API v3

### Mogelijkheden

| Actie | API Endpoint | Status |
|---|---|---|
| **Video uploaden** | `videos.insert` | Beschikbaar, quota-gelimiteerd |
| **Metadata updaten** | `videos.update` | Beschikbaar |
| **Analytics ophalen** | YouTube Analytics API | Beschikbaar |
| **Playlists beheren** | `playlists.insert/update` | Beschikbaar |
| **Comments lezen** | `commentThreads.list` | Beschikbaar |

### API Quota

- **10.000 units per dag** (gratis)
- Video upload kost **1.600 units** = max ~6 uploads per dag
- Analytics query kost **1 unit** = vrijwel onbeperkt
- Quota is per project, niet per kanaal

### Authenticatie

- **OAuth 2.0** voor uploads (vereist eenmalige browser-login)
- **API key** voor publieke data (analytics van eigen kanaal vereist OAuth)
- Google Cloud Console project nodig
- YouTube Data API v3 + YouTube Analytics API inschakelen

### Beschikbare Analytics

| Metric | API | Detail |
|---|---|---|
| Views | Analytics API | Per video, per dag, cumulatief |
| Watch time | Analytics API | Minuten, completion rate |
| Impressions | Analytics API | Hoe vaak getoond in Shorts shelf |
| CTR | Analytics API | Impressions → views ratio |
| Subscriber gain | Analytics API | Per video subscriber conversie |
| Traffic sources | Analytics API | Shorts shelf, zoekresultaten, extern |
| Demographics | Analytics API | Leeftijd, geslacht, land, stad |
| Top videos | Analytics API | Ranking op views, watch time, engagement |

---

## Content Strategie voor DJ Gianni

### Wat Posten als Shorts

| Content Type | Bron | Frequentie |
|---|---|---|
| **Release clip** (Remotion) | Nieuwe mix → teaser clip | Bij elke SoundCloud release |
| **Live set clip** | Beste 30-60s van een gig | Na elk event |
| **Behind the decks** | POV camera tijdens draai | 1-2x/week |
| **Transition showcase** | Smooth mix transition | Wekelijks |
| **Crowd reaction** | Beste reactie van een set | Na events |
| **Studio session** | Mixing/prep footage | 1x/week |

### Cross-Platform Distributie

```
Remotion rendert 1 video (9:16, 1080x1920)
├─→ TikTok (primair, eerst posten)
├─→ Instagram Reels (binnen 24 uur)
├─→ YouTube Shorts (binnen 24-48 uur)
└─→ SoundCloud (full mix link in alle beschrijvingen)
```

**Timing:** Post NIET gelijktijdig op alle platformen. Stagger:
1. TikTok eerst (snelste ontdekking, test de hook)
2. Instagram Reels 12-24 uur later
3. YouTube Shorts 24-48 uur later (langere levensduur, hoeft niet snel)

### Publicatietijden (NL markt)

| Dag | Beste tijd | Waarom |
|---|---|---|
| Vrijdag | 17:00-19:00 | Weekend-modus, party-content zoeken |
| Zaterdag | 11:00-14:00 | Vrije tijd, browsing |
| Zondag | 10:00-13:00 | Relax-modus |
| Doordeweeks | 12:00-13:00 of 18:00-20:00 | Lunch/na werk |

---

## Kanaal Setup (DJ Gianni)

### Kanaal Branding

| Element | Spec |
|---|---|
| Kanaal naam | DJ Gianni |
| Handle | @djgianni (of @djgianni.nl als bezet) |
| Banner | 2048x1152px — coral accent, "Pure Vibes" tagline |
| Profielfoto | Zelfde als Instagram — consistente branding |
| Beschrijving | NL + EN, genres, boekingsinfo, links |

### Kanaal Beschrijving Template

```
DJ Gianni - Pure Vibes 🔥

Afro Beats • Caribbean • Nederlands Urban
Rotterdam, Nederland

Mixes, live sets en behind the decks.
Stuur je Spotify playlist, ik bouw er een professionele set van.

Volledige mixes: soundcloud.com/djgianni
Boekingen: picyourbooth.nl
Instagram: @djgianni
TikTok: @djgianni
```

---

## Metrics & Benchmarks

### Wat Te Meten

| Metric | Benchmark (startend kanaal) | Goed |
|---|---|---|
| Views per Short | 100-500 eerste maand | 1.000+ |
| Completion rate | 60%+ | 80%+ |
| Subscriber conversie | 1-3% per Short | 5%+ |
| Likes-to-views ratio | 3-5% | 8%+ |
| Shorts shelf impressions | Groeiend week-over-week | Consistent groei |

### Doelen

| Periode | Views/Short | Subscribers | Shorts |
|---|---|---|---|
| Maand 1-3 | 200-1.000 | 50-200 | 2-3x/week |
| Maand 3-6 | 1.000-5.000 | 200-500 | 3-5x/week |
| Maand 6-12 | 5.000+ | 500-1.000 | Dagelijks |

---

## Veelgemaakte Fouten

1. **Geen #Shorts in titel** — Niet altijd nodig, maar helpt YouTube categoriseren
2. **Horizontale video uploaden** — Moet 9:16 zijn, anders geen Short
3. **Langer dan 3 minuten** — Wordt gewone video, niet Short
4. **Geen beschrijving/links** — Gemiste traffic naar SoundCloud
5. **Watermark van TikTok** — YouTube deprioritiseert video's met TikTok logo. Altijd origineel uploaden
6. **Alles tegelijk posten** — Stagger over platformen voor maximaal bereik
7. **Geen consistentie** — Algoritme beloont regelmatige uploads
8. **Copyright claims** — YouTube's Content ID is strenger dan TikTok. Gebruik eigen mixes/audio.

---

## Copyright op YouTube

YouTube's **Content ID** systeem is agressiever dan TikTok of SoundCloud:

- DJ mixes met mainstream tracks krijgen bijna gegarandeerd een **Content ID claim**
- Claim = niet per se een takedown, maar:
  - Monetisatie gaat naar de rechthebbende
  - Video kan geblokkeerd worden in bepaalde landen
  - Meerdere claims = risico op copyright strike
- **3 strikes = kanaal verwijderd**

### Strategie voor DJ content:
- **Originele mixes/edits** — Gebruik bootlegs, mashups, eigen edits
- **Korte clips** — <30 sec clips van tracks zijn veiliger (fair use territory)
- **Focus op performance** — POV, crowd shots, behind the decks met muziek op achtergrond
- **Instrumentals/beats** — Minder Content ID detectie dan volledige tracks
- **Eigen Remotion audio** — Release clips met rechtenvrije audio of eigen stems
