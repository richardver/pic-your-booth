# Milo Brand Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build out Milo's complete brand assets and knowledge files to match DJ Gianni's level of completeness — profile, playbooks, voice tags, mixtape prompts, component CSS, and website updates.

**Architecture:** Mirror DJ Gianni's file structure for Milo. Each deliverable is a standalone file in `.claude/agents/dj-promoter/` (knowledge/playbooks) or `.claude/agents/designer/` (visual/CSS). All content follows the approved design at `docs/plans/2026-03-29-milo-brand-design.md`.

**Tech Stack:** Markdown (knowledge files), HTML/CSS (playbooks, brand guide, component reference), Gemini prompt templates

**Design doc:** `docs/plans/2026-03-29-milo-brand-design.md`

---

## Task 1: Update knowledge-dj-milo.md with full brand content

**Files:**
- Modify: `.claude/agents/dj-promoter/knowledge-dj-milo.md`

**Reference:** `.claude/agents/dj-promoter/knowledge-dj-gianni.md` (mirror this structure)

**Step 1: Read current file and design doc**

Read both files to understand the gap.

**Step 2: Rewrite knowledge-dj-milo.md**

Update to include all approved brand content from the design doc:
- Profile table: add Age (16), Sound references (Franky Rizardo, Max Dean, Josh Baker), Sound description, Sub-tagline (Next Wave), Personality, Starting scene (GetFunky), Aspirational target (ADE)
- Tagline: change to "Deep in the groove"
- Genres: already updated to Tech House, House, Deep
- Visual Identity: add Genre Accent Colors table (Tech House cyan, House blue, Deep violet) with rules
- Photo Direction: keep as-is (already good)
- Social Bios: update to English-first versions from design doc
- Content Angles: rewrite to match design doc's 6 content pillars
- Platform Notes: update with design doc platform strategy
- Voice Tags: add full section (primary tags, set-specific, transition, outro, production guidelines)
- Mixtape Cover Art: add section mirroring Gianni's
- Strategy Playbooks: add section pointing to new playbook files (created in later tasks)
- Brand Assets Index: update with all new file paths

**Step 3: Verify consistency**

Grep for "House, Techno" or "Je voelt de bass" to ensure no old references remain.

**Step 4: Commit**

```bash
git add .claude/agents/dj-promoter/knowledge-dj-milo.md
git commit -m "feat: complete Milo brand knowledge with full positioning and strategy"
```

---

## Task 2: Update dj-milo-profile.md

**Files:**
- Modify: `.claude/agents/dj-promoter/dj-milo-profile.md`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-profile.md`

**Step 1: Read current file**

**Step 2: Update profile**

- Tagline: "Deep in the groove"
- Sub-tagline: Next Wave
- Add: Age, Sound references, Personality, Starting scene, PYB role
- Social Bios: update to English-first versions from design doc

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-profile.md
git commit -m "feat: update Milo profile with approved brand positioning"
```

---

## Task 3: Create Milo social bios file

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-social-bios.md`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-social-bios.md` (mirror structure)

**Step 1: Read Gianni's social bios for structure**

**Step 2: Create Milo social bios**

English-first. Content from design doc Section 6:

```markdown
# Milo - Social Bios

Platform-specific bios. Keep consistent across all channels. Contact always via info@picyourbooth.nl.

---

## Instagram

Milo
Tech House . House
Deep in the groove
Bookings via link in bio

## TikTok

Milo
Tech House . House . Deep
Deep in the groove
Bookings: info@picyourbooth.nl

## SoundCloud

Milo — Next wave Dutch house. Groovy tech house with depth. Seamless transitions, every track strategic. Bookings: info@picyourbooth.nl
```

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-social-bios.md
git commit -m "feat: add Milo social bios (English-first)"
```

---

## Task 4: Create Milo voice tags file

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-voice-tags.md`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-voice-tags.md` (mirror structure)

**Step 1: Read Gianni's voice tags for structure**

**Step 2: Create Milo voice tags**

Follow design doc Section 7. Tone: deeper, calmer, more minimal than Gianni.

```markdown
# Milo - Voice Tags

Voice tags for mixtapes, sets, and videos. Short, minimal, recognizable. Deeper and calmer than DJ Gianni's tags — the music speaks.

## Primary Tags (use in every set)

**Opener:**
- "Milo... Deep in the groove"
- "This is Milo"
- "Milo in the mix"

**Drop tag (before the drop):**
- "Milo"
- "Next wave"
- "Deep in the groove"

## Set-Specific Tags

**Tech House set:**
- "Milo... Tech House edition"
- "Groovy... Milo"

**House set:**
- "Milo... House session"
- "Feel the groove... Milo"

**Deep set:**
- "Milo... going deep"
- "Deep in the groove... Milo"

## Transition Tags
- "Milo" / "Next wave" / "Deep" / "Clean"

## Outro Tags
- "Milo... deep in the groove"
- "This was Milo... next wave"
- "Bookings via PicYourBooth punt nl"

## Production Guidelines
- **Voice:** Confident, low, calm — even calmer than Gianni. Almost whispered.
- **Effect:** Clean reverb/delay, subtle. No autotune.
- **Length:** Max 2-3 seconds per tag
- **Timing:** Just before the drop or during transitions
- **Frequency:** Max 1 tag per 3-4 minutes. Less is more.
- **Recording:** Quiet space, phone mic or USB mic, mono
```

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-voice-tags.md
git commit -m "feat: add Milo voice tags library"
```

---

## Task 5: Create Milo photo direction file

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-photo-direction.md`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-photo-direction.md` (mirror structure)

**Step 1: Read Gianni's photo direction for structure**

**Step 2: Create Milo photo direction**

Content from design doc Section 5 visual guidance + existing knowledge-dj-milo.md photo direction:

```markdown
# Milo - Profile Photo Direction

Guidance for Milo profile photography across all platforms and brand materials.

---

## Style

- Moody, blue-tinted studio portrait
- Cool single light source with subtle cyan/blue glow
- Dark background with depth
- Underwater/immersive feel — not harsh, but deep
- Cinematic, not commercial
- B&W base with cyan color grade overlay acceptable

## Wardrobe

- Headphones on or around neck
- Dark clothing — black or very dark
- Clean, minimal styling

## Crop & Usage

- Clean crop for profile picture use across all platforms
- Square-safe composition (1:1)
- Works at small sizes (profile avatars) and large (banners, covers)
- Minimum 800x800px
- Border-radius: 24px in UI context

## Mood Keywords

Deep — Underwater — Immersive — Architectural — Late-night — Groove

## Video/Content Photography

- Color grade: dark, desaturated base + cyan/teal. Never warm.
- Lighting: single source. Club lighting, LED strips, cyan/blue glow. No flash.
- Composition: clean, minimal. Negative space.
- POV: behind-the-decks for set clips. Low angle for authority. Close-ups on hands/mixer.
- Grain: subtle film grain for moody shots. Clean for transition clips.

## Source Photos

- `docs/images/dj-milo/profile/milo-portrait.jpg`
- `docs/images/dj-milo/profile/dj-milo-1.jpg`
```

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-photo-direction.md
git commit -m "feat: add Milo photo direction guide"
```

---

## Task 6: Create Milo mixtape cover Gemini prompt

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-mixtape-gemini-prompt.md`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-mixtape-gemini-prompt.md` (adapt for Milo)

**Step 1: Read Gianni's Gemini prompt template**

Read full file for structure and prompt pattern.

**Step 2: Create Milo version**

Adapt the prompt for Milo's brand:
- Name: "MILO" (Bebas Neue, uppercase)
- "Deep in the groove" as tagline in italic Space Grotesk
- Genre tags: Tech House, House, Deep — pill-shaped, cyan
- Background: #050508 with cyan (#34d399) gradient glow
- Diamond mark (M) instead of hexagon (G)
- Sine wave motif instead of EQ bars
- Genre accent colors table: Tech House (cyan #34d399), House (blue #38bdf8), Deep (violet #8b5cf6)
- Do NOT include: warm tones, coral, golden amber
- Mood: Deep, immersive, groove-driven — dark club aesthetic

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-mixtape-gemini-prompt.md
git commit -m "feat: add Milo mixtape cover Gemini prompt template"
```

---

## Task 7: Create Milo SoundCloud strategy playbook (HTML)

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-soundcloud-strategie.html`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-soundcloud-strategie.html` (adapt for Milo)

**Step 1: Read Gianni's SoundCloud strategy for structure**

Read full HTML to understand the sections and design system used.

**Step 2: Create Milo version**

Same HTML structure and design tokens, but:
- Swap coral tokens for cyan tokens (--mi: #34d399)
- Content adapted for Milo's brand:
  - Mix series: "Deep in the Groove Vol. X" (monthly)
  - Genre series: Tech House Sessions, House Grooves, Deep Cuts
  - Optimize titles for English (international house scene)
  - Cover art specs from Task 6
  - Voice tags from Task 4
  - Upload specs same as Gianni
  - Release cadence: 1x/month minimum

**Step 3: Verify HTML renders correctly**

Open in browser, check all sections load and tokens display correctly.

**Step 4: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-soundcloud-strategie.html
git commit -m "feat: add Milo SoundCloud strategy playbook"
```

---

## Task 8: Create Milo TikTok promotion playbook (HTML)

**Files:**
- Create: `.claude/agents/dj-promoter/dj-milo-tiktok-promotie.html`

**Reference:** `.claude/agents/dj-promoter/dj-gianni-tiktok-promotie.html` (adapt for Milo)

**Step 1: Read Gianni's TikTok playbook for structure**

Read full HTML to understand sections, phone-frame mockups, script cards.

**Step 2: Create Milo version**

Same HTML structure, swap to cyan tokens. Content adapted:
- 7-day promotion cycle per mix release
- Content hooks from design doc (English-first):
  - "clean." (transition clips)
  - "deep in the groove" (set clips)
  - "soundcheck at [venue]" (BTS)
  - "this track. every time." (track reveals)
  - "16 and already on the decks at [venue]" (journey)
  - "friday nights at getfunky" (venue-specific)
- Caption templates: minimal, lowercase, English
- Hashtag strategy: #techhouse #house #deep #deepinthegroove #nextwave #getfunky #ade
- Filming guide: dark/moody, cyan lighting, behind-the-decks POV
- Post templates from design doc Section 5

**Step 3: Verify HTML renders correctly**

**Step 4: Commit**

```bash
git add .claude/agents/dj-promoter/dj-milo-tiktok-promotie.html
git commit -m "feat: add Milo TikTok promotion playbook"
```

---

## Task 9: Create Milo component CSS reference (HTML)

**Files:**
- Create: `.claude/agents/designer/dj-milo-component-css-reference.html`

**Reference:** `.claude/agents/designer/dj-gianni-component-css-reference.html` (adapt for Milo)

**Step 1: Read Gianni's component CSS reference for structure**

Read full HTML to understand what components are documented.

**Step 2: Create Milo version**

Same component library structure, swap to cyan tokens. Components:
- DJ card (cyan accent, diamond mark, sine wave motif)
- Genre tags (Tech House, House, Deep + genre-accented variants)
- Profile layout
- Set list
- Buttons (BOEK MILO, ghost variant)
- Social icons
- Play button
- Bio cards
- Mixtape cover template
- All CSS custom properties documented

**Step 3: Verify HTML renders correctly**

**Step 4: Commit**

```bash
git add .claude/agents/designer/dj-milo-component-css-reference.html
git commit -m "feat: add Milo component CSS reference"
```

---

## Task 10: Update growth strategy with Milo-specific positioning

**Files:**
- Modify: `.claude/agents/dj-promoter/knowledge-growth-strategy.md`

**Step 1: Read current file**

**Step 2: Update Milo sections**

- Differentiation table: update tagline to "Deep in the groove", update audience to "electro scene, house heads, students"
- Add Milo-specific growth milestones:
  - GetFunky regular slot
  - First SoundCloud mix release
  - 500 followers on TikTok/Instagram
  - First booking outside PYB
  - ADE appearance (stretch goal)
- Update mix series reference to "Deep in the Groove Vol. X"

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/knowledge-growth-strategy.md
git commit -m "feat: update growth strategy with Milo brand positioning"
```

---

## Task 11: Update website djs.html with new Milo positioning

**Files:**
- Modify: `docs/pyb/website/deployment/djs.html`
- Modify: `docs/pyb/website/deployment/llms.txt`
- Modify: `docs/pyb/website/deployment/llms-full.txt`

**Step 1: Read current Milo sections in all three files**

Search for "Milo" in each file to find all sections that reference him.

**Step 2: Update djs.html**

- Profile card: update tagline to "Deep in the groove", add "Next Wave" sub-tagline if appropriate
- Bio text: update to groove-driven positioning from design doc
- Genre tags: verify "Tech House, House, Deep" (should already be correct)
- FAQ: verify genre references are consistent

**Step 3: Update llms.txt and llms-full.txt**

- Update Milo description and tagline references
- Verify genre consistency

**Step 4: Commit**

```bash
git add docs/pyb/website/deployment/djs.html docs/pyb/website/deployment/llms.txt docs/pyb/website/deployment/llms-full.txt
git commit -m "feat: update website with Milo brand positioning"
```

---

## Task 12: Update Brand Assets Index in knowledge-dj-milo.md

**Files:**
- Modify: `.claude/agents/dj-promoter/knowledge-dj-milo.md`

**Step 1: Read current Brand Assets Index**

**Step 2: Add all new file paths**

After all previous tasks are complete, update the Brand Assets Index table:

| Asset | Path |
|---|---|
| Brand guide (HTML) | `.claude/agents/designer/dj-milo-brand-guide.html` |
| CSS reference | `.claude/agents/designer/dj-milo-component-css-reference.html` |
| Component library | `.claude/agents/designer/dj-milo-component-css-reference.html` |
| Profile | `.claude/agents/dj-promoter/dj-milo-profile.md` |
| Voice tags | `.claude/agents/dj-promoter/dj-milo-voice-tags.md` |
| Social bios | `.claude/agents/dj-promoter/dj-milo-social-bios.md` |
| Photo direction | `.claude/agents/dj-promoter/dj-milo-photo-direction.md` |
| Mixtape Gemini prompt | `.claude/agents/dj-promoter/dj-milo-mixtape-gemini-prompt.md` |
| SoundCloud strategie | `.claude/agents/dj-promoter/dj-milo-soundcloud-strategie.html` |
| TikTok promotie playbook | `.claude/agents/dj-promoter/dj-milo-tiktok-promotie.html` |

**Step 3: Commit**

```bash
git add .claude/agents/dj-promoter/knowledge-dj-milo.md
git commit -m "feat: complete Milo brand assets index"
```

---

## Task 13: Final consistency check and memory update

**Step 1: Grep for stale references**

```bash
# Should return only docs/plans/ (historical, leave as-is)
grep -r "House, Techno" --include="*.md" --include="*.html" --include="*.txt"
grep -r "Je voelt de bass" --include="*.md" --include="*.html" --include="*.txt"
grep -r "DJ Milø" --include="*.md" --include="*.html" --include="*.txt"
```

Fix any remaining stale references found outside `docs/plans/`.

**Step 2: Update memory**

Save project memory for Milo brand decisions:
- DJ name: Milo (no "DJ" prefix)
- Genres: Tech House, House, Deep
- Tagline: "Deep in the groove" / Sub-tagline: "Next Wave"
- English-first brand
- Sound refs: Franky Rizardo, Max Dean, Josh Baker
- Scene: GetFunky (The Hague), aspirational ADE

**Step 3: Final commit**

```bash
git add -A
git commit -m "chore: final Milo brand consistency check"
```
