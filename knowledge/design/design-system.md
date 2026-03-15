# Design System - Tokens, Colors, Typography, Components

## Token Architecture

Three-layer system: Primitive → Semantic → Component

### Layer 1: Primitive Tokens (Raw Values)

```css
:root {
  /* Spacing (4px base) */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-24: 6rem;     /* 96px */

  /* Typography */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */
  --font-size-5xl: 3rem;      /* 48px */
  --font-size-6xl: 3.815rem;  /* 61px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;

  /* Border Radius */
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-2xl: 1rem;     /* 16px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);

  /* Z-Index Scale */
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;

  /* Duration */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 400ms;
}
```

### Layer 2: Semantic Tokens (Purpose-Based)

```css
:root {
  /* Backgrounds */
  --color-background: 0 0% 100%;          /* White */
  --color-foreground: 222.2 84% 4.9%;     /* Near-black */
  --color-card: 0 0% 100%;
  --color-card-foreground: 222.2 84% 4.9%;
  --color-muted: 210 40% 96.1%;
  --color-muted-foreground: 215.4 16.3% 46.9%;

  /* Brand */
  --color-primary: 222.2 47.4% 11.2%;
  --color-primary-foreground: 210 40% 98%;
  --color-secondary: 210 40% 96.1%;
  --color-secondary-foreground: 222.2 47.4% 11.2%;
  --color-accent: 210 40% 96.1%;
  --color-accent-foreground: 222.2 47.4% 11.2%;

  /* Status */
  --color-success: 142 76% 36%;
  --color-success-foreground: 0 0% 100%;
  --color-warning: 38 92% 50%;
  --color-warning-foreground: 0 0% 0%;
  --color-destructive: 0 84.2% 60.2%;
  --color-destructive-foreground: 210 40% 98%;
  --color-info: 217 91% 60%;
  --color-info-foreground: 0 0% 100%;

  /* UI */
  --color-border: 214.3 31.8% 91.4%;
  --color-input: 214.3 31.8% 91.4%;
  --color-ring: 222.2 84% 4.9%;
}

/* Dark Mode */
.dark {
  --color-background: 222.2 84% 4.9%;
  --color-foreground: 210 40% 98%;
  --color-card: 222.2 84% 4.9%;
  --color-card-foreground: 210 40% 98%;
  --color-muted: 217.2 32.6% 17.5%;
  --color-muted-foreground: 215 20.2% 65.1%;
  --color-primary: 210 40% 98%;
  --color-primary-foreground: 222.2 47.4% 11.2%;
  --color-border: 217.2 32.6% 17.5%;
}
```

### Layer 3: Component Tokens

```css
/* Button */
--button-height-sm: 32px;
--button-height-md: 40px;
--button-height-lg: 48px;
--button-padding-sm: 12px;
--button-padding-md: 16px;
--button-padding-lg: 24px;
--button-font-size: var(--font-size-sm);
--button-radius: var(--radius-md);

/* Input */
--input-height-sm: 32px;
--input-height-md: 40px;
--input-height-lg: 48px;
--input-padding: 8px 12px;
--input-radius: var(--radius-md);

/* Card */
--card-padding: var(--space-6);
--card-radius: var(--radius-xl);
--card-shadow: var(--shadow-sm);
--card-gap: var(--space-4);
```

---

## Typography System

### Type Scale (Major Third 1.25)

| Element | Size (rem) | Size (px) | Weight | Line Height | Letter Spacing |
|---------|------------|-----------|--------|-------------|----------------|
| Display | 3.815 | 61 | 700 | 1.1 | -0.02em |
| H1 | 3.052 | 49 | 700 | 1.2 | 0 |
| H2 | 2.441 | 39 | 600 | 1.25 | 0 |
| H3 | 1.953 | 31 | 600 | 1.3 | 0 |
| H4 | 1.563 | 25 | 600 | 1.35 | 0 |
| H5 | 1.25 | 20 | 600 | 1.4 | 0 |
| Body Large | 1.125 | 18 | 400 | 1.6 | 0 |
| Body | 1 | 16 | 400 | 1.5 | 0 |
| Small | 0.875 | 14 | 400 | 1.5 | 0 |
| Caption | 0.75 | 12 | 400 | 1.4 | 0 |

### Responsive Typography

```css
/* Mobile (< 768px) */
h1 { font-size: 2rem; }     /* 32px */
h2 { font-size: 1.5rem; }   /* 24px */
h3 { font-size: 1.25rem; }  /* 20px */

/* Desktop (>= 768px) */
h1 { font-size: 3rem; }     /* 48px */
h2 { font-size: 2.25rem; }  /* 36px */
h3 { font-size: 1.75rem; }  /* 28px */
```

### Font Pairing Recommendations for PYB

| Segment | Heading Font | Body Font | Vibe |
|---------|-------------|-----------|------|
| Premium (Magic Mirror) | Playfair Display | Source Sans Pro | Elegant, refined |
| Accessible (iPad) | Poppins | Open Sans | Friendly, modern |
| DJ / Energy | Inter | Inter | Clean, bold |
| Brand default | Inter | Inter | Professional, versatile |

### Paragraph Rules
- Max line length: 65-75 characters (`max-width: 65ch`)
- Paragraph spacing: 1rem bottom margin
- Left-align text (never justify)
- Don't use thin weights (<400) at small sizes
- All caps: only for short labels, add 0.05em letter-spacing

---

## Color Palette Management

### Color Distribution Rule
- **Primary**: 60-70% of design (backgrounds, main elements)
- **Secondary**: 20-30% (supporting elements, cards)
- **Accent**: 5-10% (CTAs, highlights, interactive elements)

### WCAG Contrast Requirements

| Element | Level AA | Level AAA |
|---------|----------|-----------|
| Normal text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | 4.5:1 |

### Color Usage Rules
- Don't use more than 2-3 colors in single component
- Don't use pure black (#000) for text - use #111 or similar
- Don't rely solely on color for meaning (add icons/text)
- Test all combinations for accessibility
- Use semantic colors consistently (red = error, green = success)

---

## Component Specifications

### Button

| Variant | Background | Text | Use Case |
|---------|------------|------|----------|
| default | primary | white | Primary actions (CTA) |
| secondary | gray-100 | gray-900 | Secondary actions |
| outline | transparent | foreground | Tertiary actions |
| ghost | transparent | foreground | Subtle actions |
| destructive | red-600 | white | Dangerous actions |

| Size | Height | Padding X | Font Size |
|------|--------|-----------|-----------|
| sm | 32px | 12px | 14px |
| default | 40px | 16px | 14px |
| lg | 48px | 24px | 16px |

### Input

| State | Border | Background | Ring |
|-------|--------|------------|------|
| default | gray-300 | white | none |
| hover | gray-400 | white | none |
| focus | primary | white | primary/20% |
| error | red-500 | white | red/20% |
| disabled | gray-200 | gray-100 | none |

### Card

| Variant | Shadow | Border | Use Case |
|---------|--------|--------|----------|
| default | sm | 1px | Standard content |
| elevated | lg | none | Featured content |
| outline | none | 1px | Subtle container |
| interactive | sm→md on hover | 1px | Clickable card |

Spacing: Header 24px, Content 24px, Footer 24px, Gap 16px.

### Interactive States (All Components)

| State | Trigger | Transition | Visual Change |
|-------|---------|------------|---------------|
| default | None | - | Base appearance |
| hover | Mouse over | 150ms ease-in-out | Slight color shift |
| focus | Tab/click | - | 2px focus ring |
| active | Mouse down | - | Darkest shade |
| disabled | disabled attr | - | 50% opacity, no pointer |
| loading | Async action | - | Spinner + 70% opacity |

Priority (highest to lowest): disabled > loading > active > focus > hover > default.

---

## Responsive Design

### Breakpoints (Mobile-First)

| Prefix | Width | Target |
|--------|-------|--------|
| (base) | 0px | Mobile phones |
| sm: | 640px | Large phones |
| md: | 768px | Tablets |
| lg: | 1024px | Laptops |
| xl: | 1280px | Desktops |
| 2xl: | 1536px | Large screens |

### Common Responsive Patterns

**Card Grid:**
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
```

**Hero Section:**
```html
<section class="py-12 md:py-20 lg:py-32">
  <div class="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
```

**Navigation:**
```html
<div class="hidden md:flex gap-6">Desktop nav</div>
<button class="md:hidden">Mobile menu</button>
```

**Sidebar Layout:**
```html
<div class="flex flex-col lg:flex-row min-h-screen">
  <aside class="w-full lg:w-64">Sidebar</aside>
  <main class="flex-1">Content</main>
</div>
```

### Mobile Testing Checklist
- [ ] Test at 320px (small mobile)
- [ ] Test at 640px (phone breakpoint)
- [ ] Test at 768px (tablet)
- [ ] Test at 1024px (desktop)
- [ ] Touch targets 44x44px minimum
- [ ] Verify sticky CTA on mobile
- [ ] Check text readability at all sizes
- [ ] Test landscape orientation
