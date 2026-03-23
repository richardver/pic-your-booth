# Component Library

## Approach: Shadcn/ui + PYB Theme

We use [shadcn/ui](https://ui.shadcn.com) as the base component library. Components are installed into `src/components/ui/` and themed via Tailwind CSS using PYB design tokens. We do NOT build custom UI components from scratch.

**Why Shadcn:**
- Copy-paste components — no package dependency, full control
- Built on Radix UI primitives — accessible out of the box
- Tailwind CSS native — maps 1:1 to our token system
- Dark mode support via CSS variables — matches our dark cinematic base

---

## PYB Theme Layer

Shadcn uses CSS variables for theming. We override these in `globals.css`:

```css
:root {
  /* PYB Dark Cinematic Base */
  --background: 240 10% 3%;          /* #08080b */
  --foreground: 240 6% 93%;          /* #ededf0 */
  --card: 240 8% 7%;                 /* #111116 */
  --card-foreground: 240 6% 93%;     /* #ededf0 */
  --popover: 240 8% 7%;             /* #111116 */
  --popover-foreground: 240 6% 93%;  /* #ededf0 */
  --muted: 240 6% 10%;              /* #18181e */
  --muted-foreground: 240 6% 93% / 0.6; /* text muted */
  --border: 0 0% 100% / 0.06;       /* subtle border */
  --input: 0 0% 100% / 0.06;        /* input border */
  --ring: 43 62% 57%;               /* gold focus ring */

  /* PYB Accent Colors */
  --primary: 43 62% 57%;            /* gold #f59e42 */
  --primary-foreground: 0 0% 0%;    /* black text on gold */
  --secondary: 240 8% 10%;          /* elevated surface */
  --secondary-foreground: 240 6% 93%;
  --accent: 240 8% 10%;
  --accent-foreground: 240 6% 93%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;

  --radius: 0.5rem;
}
```

### Segment-Specific Accent Overrides

Apply via data attributes or CSS classes on page containers:

```css
/* DJ pages */
[data-segment="dj"] {
  --primary: 258 89% 66%;           /* violet #8b5cf6 */
  --primary-foreground: 0 0% 100%;  /* white text on violet */
}

/* DJ Gianni profile */
[data-segment="gianni"] {
  --primary: 16 89% 61%;            /* coral #f0654a */
  --primary-foreground: 0 0% 100%;
}

/* Milo profile */
[data-segment="milo"] {
  --primary: 187 82% 53%;           /* cyan #0ea5e9 */
  --primary-foreground: 0 0% 0%;
}
```

---

## Shadcn Components to Install

### Core (install immediately)

| Component | Shadcn Name | PYB Usage |
|---|---|---|
| Button | `button` | CTAs, nav "BOEK JE ERVARING", form submit |
| Input | `input` | Proposal form fields |
| Label | `label` | Form labels |
| Select | `select` | Event type dropdown |
| Textarea | `textarea` | Optional message field |
| Card | `card` | Service cards, package cards, testimonial cards |
| Dialog | `dialog` | Upgrade info modals (?) on package builder |
| Switch | `switch` | Package builder upgrade toggles |
| Badge | `badge` | "MEEST GEKOZEN", genre tags, "NIEUW" |
| Separator | `separator` | Gold divider lines |
| Accordion | `accordion` | FAQ sections |

### Navigation

| Component | Shadcn Name | PYB Usage |
|---|---|---|
| Navigation Menu | `navigation-menu` | Desktop nav (Party Booth / Magic Mirror / DJs) |
| Sheet | `sheet` | Mobile hamburger menu |

### Enhancement (install when needed)

| Component | Shadcn Name | PYB Usage |
|---|---|---|
| Carousel | `carousel` | Photo gallery, testimonial slider |
| Tabs | `tabs` | DJ profile tabs (if needed) |
| Tooltip | `tooltip` | Pricing details, upgrade info |
| Skeleton | `skeleton` | Loading states |
| Toast | `sonner` | Form submission feedback |
| Progress | `progress` | Multi-step form progress bar |
| Radio Group | `radio-group` | DJ extra hours selector |
| Slider | `slider` | If needed for interactive elements |

### Not Needed

| Component | Why Skip |
|---|---|
| Table | No data tables on marketing site |
| Data Table | No admin views |
| Calendar | Use native date input for form |
| Command | No command palette needed |
| Menubar | Nav is simple enough without |

---

## PYB Component Variants

### Button

| Variant | Shadcn Base | PYB Override | Usage |
|---|---|---|---|
| **Gold CTA** | `default` | `bg-[#f59e42] text-black hover:bg-[#c9a545]` | Primary CTAs: "BOEK JE ERVARING", "CHECK BESCHIKBAARHEID" |
| **Violet CTA** | `default` | `bg-[#8b5cf6] text-white hover:bg-[#7c4fee]` | DJ CTAs: "BOEK EEN DJ", "PLAN JE FEEST" |
| **Ghost** | `ghost` | Default Shadcn ghost | Secondary actions, "Meer info →" |
| **Outline** | `outline` | `border-white/10 hover:bg-white/5` | Tertiary actions |

### Card

| Variant | Shadcn Base | PYB Override | Usage |
|---|---|---|---|
| **Service Card** | `card` | `bg-[#111116] border-white/6` | Homepage service cards (Party Booth, Magic Mirror, DJs) |
| **Package Card** | `card` | `bg-[#111116] border-[#f59e42]/20` (gold tint for base) | Package builder base package |
| **Upgrade Row** | Custom | `bg-[#18181e] rounded-lg` with Switch | Toggle upgrade in package builder |
| **Testimonial** | `card` | `bg-transparent border-none` with gold dividers | Quote blocks |

### Badge

| Variant | PYB Override | Usage |
|---|---|---|
| **Gold** | `bg-[#f59e42] text-black` | "MEEST GEKOZEN", prices |
| **Violet** | `bg-[#8b5cf6] text-white` | "ALLEEN BIJ PICYOURBOOTH" |
| **Coral** | `bg-[#f0654a] text-white` | DJ Gianni genre tags |
| **Cyan** | `bg-[#0ea5e9] text-black` | Milo genre tags |
| **Muted** | `bg-white/10 text-white/60` | Secondary labels |

### Input (Form)

| State | PYB Override |
|---|---|
| Default | `bg-[#111116] border-white/10 text-[#ededf0]` |
| Focus | `border-[#f59e42] ring-[#f59e42]/20` (gold focus) |
| Error | `border-red-500 ring-red-500/20` |
| Placeholder | `text-white/40` |

---

## Install Command

```bash
npx shadcn@latest init
# Select: New York style, Zinc color, CSS variables: yes

# Core components
npx shadcn@latest add button input label select textarea card dialog switch badge separator accordion

# Navigation
npx shadcn@latest add navigation-menu sheet

# Enhancement (when needed)
npx shadcn@latest add carousel tabs tooltip skeleton sonner progress radio-group
```

After install, override `globals.css` with PYB theme variables above.

---

## Custom PYB Components (built on Shadcn)

These are PYB-specific compositions using Shadcn primitives:

| Component | Built From | Purpose |
|---|---|---|
| `Nav` | NavigationMenu + Sheet + Button | Shared navigation with mobile hamburger |
| `Hero` | Custom (no Shadcn base) | Page hero with configurable headline, visual, CTA |
| `ServiceCard` | Card + Badge + Button | Homepage service card with price pill |
| `ProofBar` | Custom | Social proof numbers bar (237+ Events, 4.9★, etc.) |
| `PackageBuilder` | Card + Switch + Badge + Button | Interactive package configurator |
| `UpgradeRow` | Switch + Dialog + Badge | Single upgrade toggle with info modal |
| `ProposalForm` | Input + Label + Select + Textarea + Button + Sonner | 6-field proposal form with validation |
| `DJProfile` | Card + Badge + Button | DJ profile section with avatar, genres, socials |
| `BookingWizard` | RadioGroup + Card + Badge + Button | DJ hour selector with running total |
| `FAQ` | Accordion | FAQ section with objection-handling content |
| `Testimonial` | Card + Separator | Quote block with gold dividers |

---

## Typography in Components

All Shadcn components inherit from Tailwind config:

```js
// tailwind.config.ts
fontFamily: {
  display: ['Bebas Neue', 'sans-serif'],  // headings, nav, prices
  sans: ['Space Grotesk', 'sans-serif'],   // body, forms, descriptions
}
```

Usage: `font-display` for Bebas Neue, `font-sans` (default) for Space Grotesk.

---

## Rules

1. **Never build from scratch** what Shadcn already provides
2. **Always use PYB theme variables** — never hardcode colors outside the token system
3. **Segment overrides via data attributes** — `data-segment="dj"` swaps accent colors
4. **Gold buttons always have black text** — `text-black`, never `text-white`
5. **Mobile-first** — Shadcn components are responsive by default, but verify touch targets (44px)
6. **Accessibility comes free** — Shadcn/Radix handles ARIA, focus management, keyboard nav
