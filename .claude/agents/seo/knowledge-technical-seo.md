# Technische SEO

Meta tags, structured data, sitemap, performance en technische vereisten.

---

## Meta Tags per Pagina

| Pagina | Title (max 60) | Meta Description (max 155) |
|---|---|---|
| Homepage | Photobooth Huren \| Premium Entertainment \| PicYourBooth | Photobooth en DJ huren in de Randstad. Magic Mirror XL vanaf €599, Party Booth vanaf €199. Vraag vrijblijvend een voorstel aan. |
| Magic Mirror | Fotospiegel Huren \| AI Photobooth \| Magic Mirror XL | Premium fotospiegel met professionele camera. Tot 5 uur, bezorging inbegrepen. Vanaf €599 per event. |
| Party Booth | Photobooth Huren Goedkoop \| Party Booth vanaf €199 | Digitale photobooth voor elk feest. Zelf ophalen, 5 minuten opzetten. AI achtergrond beschikbaar. Vanaf €199 per dag. |
| DJs | DJ Huren \| DJ Gianni & DJ Milø \| Vanaf €149 | DJ huren met Spotify playlist-optimalisatie. Speakers, licht en rookmachine inbegrepen. Vanaf €149 per avond. |
| Offerte | Photobooth Offerte Aanvragen \| PicYourBooth | Ontvang binnen 24 uur een vrijblijvend voorstel. Party Booth, Magic Mirror XL of DJ. Geen verplichtingen. |

## Structured Data (JSON-LD)

### Elke Pagina: LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "PicYourBooth",
  "description": "Premium photobooth en DJ entertainment in de Randstad",
  "url": "https://picyourbooth.nl",
  "email": "info@picyourbooth.nl",
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": { "@type": "GeoCoordinates", "latitude": 52.0, "longitude": 4.5 },
    "geoRadius": "50000"
  },
  "priceRange": "€149 - €2000",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "237"
  }
}
```

### Product Pagina's: Product Schema

```json
{
  "@type": "Product",
  "name": "Magic Mirror XL",
  "description": "Premium fotospiegel met professionele camera, tot 5 uur inclusief, bezorging inbegrepen",
  "offers": {
    "@type": "Offer",
    "price": "599",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  }
}
```

### FAQ Schema (voor LLM zichtbaarheid)

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Wat kost een photobooth huren?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bij PicYourBooth huur je een Party Booth vanaf €199 per dag of een Magic Mirror XL vanaf €599 per event."
      }
    }
  ]
}
```

## Technische Checklist

- [ ] `<html lang="nl">` op elke pagina
- [ ] `<link rel="canonical">` op elke pagina
- [ ] `sitemap.xml` automatisch gegenereerd (Next.js)
- [ ] `robots.txt` correct geconfigureerd
- [ ] Open Graph tags (og:title, og:description, og:image)
- [ ] Twitter Card tags
- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] Images: WebP/AVIF, lazy loading, alt text met keyword
- [ ] HTTPS (Vercel default)
- [ ] Mobile-first responsive

## URL Structuur

```
picyourbooth.nl/                    → Homepage
picyourbooth.nl/magic-mirror        → Magic Mirror XL
picyourbooth.nl/party-booth         → Party Booth
picyourbooth.nl/djs                 → DJs
picyourbooth.nl/offerte             → Proposal Form
picyourbooth.nl/rotterdam (Fase 2)  → Stadspagina
picyourbooth.nl/amsterdam (Fase 2)  → Stadspagina
```

Geen trailing slashes. Geen /nl/ prefix (single language site).
