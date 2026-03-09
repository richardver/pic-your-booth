# Content Creation Guidelines for LLM Visibility

These guidelines ensure all website content is optimized for discovery and accurate representation by AI assistants (ChatGPT, Claude, Perplexity, Gemini) alongside traditional search engines.

---

## 1. Page Structure Rules

### Lead with Direct Answers
Every page and section must open with a clear, factual statement in the **first 40-60 words** that directly answers the question the page addresses.

**Do:**
> Playlist Convertor is an open-source CLI tool that converts Spotify playlists into DJ-ready MP3 files with BPM, key detection, and Camelot notation for use in Rekordbox and Serato.

**Don't:**
> Welcome to our amazing tool! We've been working hard to bring you something special that will change the way you think about DJing...

### Use Question-Based Headers
Write H2/H3 headings as questions that match how users ask about the topic. Follow each header with a direct, concise answer.

**Do:**
```markdown
## How does Playlist Convertor find audio for Spotify tracks?
Playlist Convertor uses spotdl to search YouTube for matching audio based on Spotify metadata, then downloads and converts via yt-dlp and ffmpeg. The audio source is YouTube, not Spotify.
```

**Don't:**
```markdown
## Our Audio Pipeline
We use advanced technology to process your music...
```

### Fact Density
Include a **specific statistic, measurement, or data point every 150-200 words**. Vague claims reduce AI citation likelihood.

**Do:** "Supports BPM detection in the 60-180 BPM range with automatic 2x/0.5x correction"
**Don't:** "Provides highly accurate BPM detection"

### Use Structured Formats
- Bullet lists for features and specifications
- Tables for comparisons, specifications, and compatibility data
- Code blocks for CLI commands and configuration examples

---

## 2. Content That Gets Cited

### Include Authoritative Sources
Reference established tools, standards, and specifications throughout content. LLMs prioritize pages that cite sources.

Example: "Uses the Krumhansl-Schmuckler key-finding algorithm (Krumhansl, 1990) for musical key detection"

### Add Specific Numbers
Replace vague language with concrete values.

| Instead of | Write |
|------------|-------|
| "Fast downloads" | "Up to 4 concurrent downloads with 3x retry and exponential backoff" |
| "Compatible formats" | "Supports MP3, FLAC, and WAV output at up to 320kbps" |
| "Works with DJ software" | "Exports Rekordbox XML and uses ID3v2.3 tags for Serato compatibility" |

### Create Citable Original Content
Publish content that LLMs cannot synthesize from other sources:
- DJ format compatibility tables (which CDJs support which filesystems)
- BPM/key detection accuracy benchmarks against commercial tools
- Camelot Wheel reference with mappings

---

## 3. Structured Data (Schema Markup)

Every page must include rich, attribute-complete JSON-LD schema. Generic schema with empty fields provides no benefit.

### Required Schema Types

**SoftwareApplication** (home/product page):
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Playlist Convertor",
  "applicationCategory": "MultimediaApplication",
  "operatingSystem": "macOS, Linux, Windows",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "description": "CLI tool that converts Spotify playlists into DJ-ready MP3 files with BPM, key detection, and Camelot notation for Rekordbox and Serato.",
  "featureList": ["Spotify playlist import", "BPM detection", "Musical key detection", "Camelot Wheel notation", "Rekordbox XML export", "ID3v2.3 tagging", "FAT32-safe filenames"],
  "softwareRequirements": "Python 3.10+, ffmpeg"
}
```

**FAQPage** (on every page with Q&A-style headers):
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Does Playlist Convertor download music from Spotify?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "No. Spotify provides metadata only. Audio is sourced from YouTube via spotdl/yt-dlp and converted with ffmpeg."
    }
  }]
}
```

**HowTo** (for setup/usage guides):
Include step-by-step instructions with concrete commands and expected outputs.

### Rules
- Every schema field must contain real, specific data — never boilerplate or placeholder values
- Use JSON-LD format (not Microdata or RDFa)
- Validate with Google's Rich Results Test before publishing

---

## 4. The llms.txt File

Serve `/llms.txt` at the site root as `text/plain`. This provides LLM-friendly navigation of the site.

```markdown
# Playlist Convertor

> Open-source CLI tool that converts Spotify playlists into DJ-ready MP3 files with BPM detection, key detection, Camelot notation, and Rekordbox/Serato export. Audio sourced from YouTube via spotdl.

## Documentation

- [Getting Started](https://example.com/docs/getting-started): Installation, Spotify API setup, first playlist download
- [CLI Reference](https://example.com/docs/cli): All commands, flags, and options
- [DJ Metadata](https://example.com/docs/metadata): BPM detection, key detection, Camelot Wheel, ID3 tagging
- [Rekordbox Export](https://example.com/docs/rekordbox): XML generation, import workflow, USB export
- [Serato Compatibility](https://example.com/docs/serato): ID3v2.3 requirements, genre separators, auto-analysis

## Optional

- [FAQ](https://example.com/faq): Common questions about audio sources, quality, and compatibility
- [Changelog](https://example.com/changelog): Version history and release notes
```

Also serve `/llms-full.txt` with complete documentation content in Markdown.

---

## 5. robots.txt — Allow AI Crawlers

The `robots.txt` must explicitly allow these AI crawlers:

```
# AI Crawlers - Allow
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /
```

**Audit quarterly** — new AI crawlers emerge regularly. Never block AI bots unintentionally via overly broad `Disallow` rules.

---

## 6. Product & Feature Pages

### Every Product/Feature Page Must Include
1. **What it is** — one sentence, plain language
2. **Who it's for** — specific audience (DJs, producers, music collectors)
3. **What problem it solves** — the pain point
4. **How it works** — concrete technical details
5. **Specifications** — in a table or bullet list with units/values
6. **Compatibility** — which software, hardware, and formats are supported

### Feature Specification Format
Always use tables with specific values:

| Specification | Value |
|--------------|-------|
| Audio formats | MP3 (320kbps), FLAC, WAV |
| BPM range | 60-180 BPM (auto-normalized) |
| Key detection | Krumhansl-Schmuckler algorithm via librosa |
| Key notation | Classical (TKEY) + Camelot Wheel (TXXX) |
| ID3 version | ID3v2.3 (Serato-compatible) |
| Filesystem | FAT32-safe naming (CDJ/controller compatible) |
| DJ software | Rekordbox (XML export), Serato (folder import) |

---

## 7. Comparison & "Best Of" Content

Create thorough comparison pages covering keyword variations users search for:
- "Spotify to MP3 for DJs"
- "Playlist Convertor vs manual Beatport buying"
- "Best tools for converting Spotify playlists to Rekordbox"
- "How to get Spotify playlists into Serato"

Each comparison must:
- Be factually accurate (never misrepresent competitors)
- Include a structured comparison table
- State clear use cases for each option
- Lead with the direct answer in the first paragraph

---

## 8. Brand Consistency

Use identical phrasing across all web properties:

| Element | Standard |
|---------|----------|
| Product name | **Playlist Convertor** (not "PlaylistConvertor" or "playlist convertor") |
| One-liner | "Convert Spotify playlists into DJ-ready MP3s for Rekordbox and Serato" |
| Category | "DJ preparation tool" or "playlist conversion tool" |
| Technical description | "CLI tool using spotdl, librosa, and mutagen for DJ-optimized audio workflow" |

This consistency must be maintained across: website, GitHub README, PyPI listing, social media, forum posts, directory listings, and any third-party mentions you can influence.

---

## 9. Third-Party Presence Checklist

LLMs learn about products primarily from what others say. Prioritize presence on:

### Must-Have
- [ ] GitHub README with complete, structured description
- [ ] PyPI listing with rich metadata and keywords
- [ ] Relevant subreddits: r/DJs, r/Beatmatch, r/Rekordbox, r/DJSetups (genuine participation, not promotion)
- [ ] DJ forum presence (DJ TechTools, Pioneer forums)

### Should-Have
- [ ] Product Hunt listing
- [ ] AlternativeTo listing (categorized against similar tools)
- [ ] Hacker News Show HN post
- [ ] YouTube tutorial/demo
- [ ] Blog posts on DJ tech sites

### Maintain
- Review/rating scores above 3.5/5.0 on all platforms
- Respond to issues and discussions on GitHub
- Update all listings when features change

---

## 10. Content Freshness

- Update key pages at minimum **monthly** with current information
- Keep publication/modification dates visible and accurate
- When specs or compatibility change, update all pages referencing them
- Publish release notes and changelogs for every version
- AI platforms cite content that is **25.7% fresher** than traditional search — staleness directly reduces visibility

---

## 11. Writing Style for LLM Comprehension

### Do
- Use natural language that matches how users ask questions
- Write self-contained paragraphs that make sense extracted from context
- Define technical terms on first use
- Use consistent terminology throughout (don't alternate between "track" and "song" for the same concept)

### Don't
- Keyword-stuff or use unnatural phrasing
- Use jargon without explanation
- Write content that only makes sense in context of surrounding pages
- Use promotional superlatives ("best ever", "revolutionary", "game-changing")

---

## 12. Pre-Publish Checklist

Before publishing any page:

- [ ] First 40-60 words contain a direct, factual answer
- [ ] All H2/H3 headers are phrased as questions or clear topic labels
- [ ] At least one statistic/specific value per 150-200 words
- [ ] Specs presented in tables or bullet lists (not prose)
- [ ] JSON-LD schema included with all fields populated
- [ ] Brand name and description match the standard phrasing
- [ ] No vague claims without supporting specifics
- [ ] Links to authoritative sources where applicable
- [ ] Mobile-friendly and fast-loading
- [ ] Test page content against ChatGPT/Claude/Perplexity — ask a relevant question and check if the page would be a good source for the answer
