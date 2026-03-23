# UI/UX Design Principles

## 10 Priority-Ranked Design Rule Categories

### 1. Accessibility (Highest Priority)
- Color contrast: 4.5:1 for text, 3:1 for UI components (WCAG AA)
- Touch targets: 44x44px minimum on mobile
- Focus indicators: visible 2px ring on all interactive elements
- Screen reader: semantic HTML, ARIA labels for icon-only buttons
- Keyboard navigation: all functions accessible without mouse
- Don't rely on color alone - use icons, text, patterns
- Respect `prefers-reduced-motion` - disable animations for those who need it
- Minimum text size: 16px body, 14px small, 12px caption (sparingly)

### 2. Touch & Interaction
- Touch targets: 44x44px minimum (Apple HIG & Material Design)
- 8px minimum spacing between touch targets
- Thumb zone design: primary actions in bottom 40% of mobile screen
- Sticky CTA button on long mobile pages
- Swipe gestures: only as supplement to visible buttons
- Hover effects: don't depend on hover for essential info (mobile has no hover)

### 3. Performance
- Largest Contentful Paint (LCP): under 2.5 seconds
- Cumulative Layout Shift (CLS): under 0.1
- Images: compressed WebP/AVIF, lazy-loaded below fold
- Fonts: preconnect to Google Fonts, `font-display: swap`
- Third-party scripts: defer or async
- Critical CSS: inline above-fold styles

### 4. Style Selection
- Match visual style to segment (premium vs accessible vs energy)
- Consistency across all pages - same tokens, same spacing, same components
- Dark mode support when targeting premium segment
- Avoid mixing more than 2 visual styles

### 5. Layout & Responsive
- Mobile-first: design for mobile, enhance for desktop
- Use CSS Grid for page layouts, Flexbox for components
- Max content width: 1280px with responsive padding
- Consistent spacing scale (4px base unit)
- 12-column grid for complex layouts
- Avoid horizontal scrolling on any viewport

### 6. Typography & Color
- One heading font + one body font maximum
- Type scale: Major Third (1.25) ratio
- Line height: 1.1-1.3 for headings, 1.5-1.6 for body
- Max line length: 65-75 characters
- Color: 60/30/10 rule (primary/secondary/accent)
- Don't use pure black (#000) - use #111 or darker gray

### 7. Animation
- Micro-interactions: 150-200ms (hover, toggle, focus)
- Transitions: 200-300ms (page transitions, reveals)
- Complex animations: 300-400ms max (modals, accordions)
- Exit faster than enter (feels snappier)
- Use transform + opacity only (GPU-accelerated)
- Stagger sequences: 50-100ms delay between items
- Spring physics for natural feel (no linear easing)

### 8. Forms & Feedback
- Labels above inputs (not placeholder-only)
- Inline validation (real-time feedback)
- Specific error messages near the field ("Vul een geldig e-mailadres in")
- Success states (green check, confirmation message)
- Loading states on submit buttons (spinner, disable button)
- Progress indicators for multi-step flows

### 9. Navigation Patterns
- Maximum 7±2 items in primary navigation
- Current page indicator (active state)
- Breadcrumbs for deep pages
- Mobile: hamburger menu OR bottom tab bar
- Search: prominent on content-heavy sites
- Footer: secondary navigation, contact info, legal

### 10. Charts & Data Visualization
- Use appropriate chart type for data relationship
- Label all axes and data points
- Ensure colorblind-safe palettes
- Provide data tables as accessible alternative
- Animate chart entry for engagement (respect reduced-motion)

---

## Visual Hierarchy Principles

### Size Creates Hierarchy
Larger elements = more important. Headlines > subheads > body > captions.

### Contrast Creates Focus
High contrast draws the eye. Use for CTAs and key messages.

### Spacing Creates Grouping
Related items close together, unrelated items separated. Gestalt proximity principle.

### Color Creates Meaning
Consistent semantic colors. Accent color reserved for actions.

### Position Creates Flow
F-pattern (text-heavy) or Z-pattern (minimal) scanning. Place CTAs in natural eye flow.

---

## UX Best Practices Summary (Top 25)

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | Progressive disclosure | Show only what's needed at each step |
| 2 | Error prevention > error messages | Validate inputs, confirm destructive actions |
| 3 | Recognition over recall | Show options, don't make users remember |
| 4 | Consistency | Same patterns, same components throughout |
| 5 | Feedback for every action | Visual response within 100ms |
| 6 | Clear visual hierarchy | Size, contrast, spacing guide the eye |
| 7 | Minimize cognitive load | Max 3-5 options, clear grouping |
| 8 | Forgiving design | Undo, back buttons, easy correction |
| 9 | Loading states | Never leave users wondering what's happening |
| 10 | Mobile-first | Start simple, enhance for larger screens |
| 11 | Whitespace is design | Don't fill every pixel - breathing room |
| 12 | One primary action per screen | Clear single CTA, de-emphasize secondary |
| 13 | Content-first design | Real content before visual design decisions |
| 14 | Test with real users | 5 users catch 85% of usability issues |
| 15 | F-pattern for text pages | Key info on left, important at top |
| 16 | Thumb-zone design on mobile | Primary actions in easy reach |
| 17 | Skeleton screens > spinners | Show content structure while loading |
| 18 | Proper empty states | Guide users when no data/content exists |
| 19 | Infinite scroll vs pagination | Pagination for goal-oriented, infinite for browsing |
| 20 | Toast notifications for feedback | Brief, non-blocking, auto-dismiss (4-6s) |
| 21 | Sticky elements sparingly | Only for critical CTAs and navigation |
| 22 | Image alt text always | Descriptive for content, empty for decorative |
| 23 | Link text descriptive | "Bekijk onze pakketten" not "Klik hier" |
| 24 | Form labels visible | Always visible, not just placeholder text |
| 25 | Scroll indicators | Show there's more content below the fold |

---

## Accessibility Testing Checklist

### Keyboard
- [ ] Tab through all interactive elements in logical order
- [ ] Enter/Space activates buttons and links
- [ ] Escape closes modals and dropdowns
- [ ] Arrow keys navigate within menus, tabs, selects
- [ ] Focus never gets trapped (except in modals intentionally)
- [ ] Skip-to-content link present

### Screen Reader
- [ ] All images have alt text (or aria-hidden for decorative)
- [ ] Form inputs have labels (htmlFor/id linked)
- [ ] Error messages linked to inputs (aria-describedby)
- [ ] Dynamic content uses aria-live regions
- [ ] Headings in correct hierarchy (h1 > h2 > h3)
- [ ] Landmarks used (nav, main, footer, aside)

### Visual
- [ ] Text contrast 4.5:1 (check with WebAIM)
- [ ] UI component contrast 3:1
- [ ] Focus indicators visible (2px ring)
- [ ] Works at 200% browser zoom
- [ ] Information not conveyed by color alone
- [ ] Animations respect prefers-reduced-motion

### Forms
- [ ] Labels visible (not placeholder-only)
- [ ] Required fields indicated (with sr-only text)
- [ ] Error messages specific and linked to field
- [ ] Fieldset/legend for grouped inputs
- [ ] Submit button has descriptive text
