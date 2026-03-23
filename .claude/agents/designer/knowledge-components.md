# Component Library

Shadcn/ui base + PYB theme. Full reference in `.claude/agents/designer/knowledge-components-full.md`.

---

## Approach

- **Shadcn/ui** as base — copy-paste components, Radix primitives, Tailwind native
- **PYB theme layer** — CSS variables in `globals.css` override Shadcn defaults
- **Segment overrides** — `data-segment="dj"` / `data-segment="gianni"` / `data-segment="milo"` swap accent colors
- **Never build from scratch** what Shadcn provides

## Core Components

Button, Input, Label, Select, Textarea, Card, Dialog, Switch, Badge, Separator, Accordion, NavigationMenu, Sheet

## PYB Button Variants

| Variant | Classes | Usage |
|---|---|---|
| Gold CTA | `bg-[#d4b14e] text-black` | Photobooth CTAs |
| Violet CTA | `bg-[#8b5cf6] text-white` | DJ CTAs |
| Ghost | Shadcn default | Secondary actions |

## PYB Custom Components (Shadcn compositions)

Nav, Hero, ServiceCard, ProofBar, PackageBuilder, UpgradeRow, ProposalForm, DJProfile, BookingWizard, FAQ, Testimonial

## Typography

- `font-display` = Bebas Neue (headings, nav, prices)
- `font-sans` = Space Grotesk (body, forms)

For full specs, variants, install commands: `.claude/agents/designer/knowledge-components-full.md`
