---
name: Placement Analytics System
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#47464f'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#787680'
  outline-variant: '#c8c5d0'
  surface-tint: '#5b598c'
  primary: '#070235'
  on-primary: '#ffffff'
  primary-container: '#1e1b4b'
  on-primary-container: '#8683ba'
  inverse-primary: '#c4c1fb'
  secondary: '#4e45d5'
  on-secondary: '#ffffff'
  secondary-container: '#6860ef'
  on-secondary-container: '#fffbff'
  tertiary: '#000d16'
  on-tertiary: '#ffffff'
  tertiary-container: '#002535'
  on-tertiary-container: '#0093c6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e3dfff'
  primary-fixed-dim: '#c4c1fb'
  on-primary-fixed: '#181445'
  on-primary-fixed-variant: '#444173'
  secondary-fixed: '#e3dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#100069'
  on-secondary-fixed-variant: '#372abf'
  tertiary-fixed: '#c4e7ff'
  tertiary-fixed-dim: '#7bd0ff'
  on-tertiary-fixed: '#001e2c'
  on-tertiary-fixed-variant: '#004c69'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: Hanken Grotesk
    fontSize: 2.25rem
    fontWeight: '700'
    lineHeight: 2.75rem
    letterSpacing: -0.025em
  headline-xl-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 1.75rem
    fontWeight: '700'
    lineHeight: 2.25rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
    letterSpacing: '0'
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: '0'
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
    letterSpacing: '0'
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.03em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 0.75rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system serves academic leaders, department chairs, and corporate relations directors within engineering institutions. It translates high-volume student performance metrics, hiring pipelines, and predictive placement analytics into an authoritative, dense, yet serene operational dashboard. 

The aesthetic marries **Corporate / Modern** precision with high-density data visualization techniques. It rejects juvenile motifs and decorative fluff in favor of institutional gravitas, architectural discipline, and crisp visual ergonomics. The tone is decisive, analytical, and reassuring—instilling confidence during high-stakes campus placement drives and accreditation audits.

## Colors

The palette establishes an institutional foundation with deep indigos and navies, energized by precise violet and sky blue accents for interactive states and analytical focal points.

- **Primary Tones:** `#1E1B4B` (Deep Navy) anchors global topbars, primary action buttons, and dominant metric labels. `#312E81` and `#4338CA` serve as progressive active states, active tab highlights, and key chart series.
- **Accent Tones:** `#4F46E5` and `#6366F1` act as interactive triggers, focus outlines, and dynamic data drivers. `#38BDF8` (Sky) is reserved for predictive trends, model probability gauges, and secondary metric calls.
- **Neutral Canvas:** The background establishes depth with `#F8FAFC` as the workspace canvas, elevated by `#FFFFFF` for primary cards and analytical modules. `#F1F5F9` provides structural fill for table header rows and inactive segment selectors. Divider strokes use `#E2E8F0`.
- **Text Hierarchies:** Content defaults to `#0F172A` (Slate 900) for primary headers, `#334155` (Slate 700) for readable body and tabular data, and `#64748B` (Slate 500) for metadata and muted labels.
- **Semantic Placement Indicators:**
  - Placed / High Match: `#10B981` (Emerald 500) with `#ECFDF5` background tint.
  - In Pipeline / Under Review: `#F59E0B` (Amber 500) with `#FFFBEB` background tint.
  - Critical / Unplaced / At-Risk: `#EF4444` (Rose 500) with `#FEF2F2` background tint.

## Typography

The typography couples the sharp, contemporary proportions of **Hanken Grotesk** for structural communication with **JetBrains Mono** for data density, roll numbers, GPA indices, probabilities, and system tags.

- **Display & Headlines:** Set in Hanken Grotesk with tightened tracking (`-0.02em` to `-0.025em`) to maintain rigidity across dense dashboards.
- **Data & Numeric Display:** JetBrains Mono is strictly enforced for numerical metrics, conversion ratios, salary figures (LPA/CTC), table pagination counters, and student registration codes to ensure zero horizontal jitter during dynamic table updates.
- **Tabular Figures:** Ensure all numerical tabular implementations activate `tnum` (tabular figures) in CSS to align currency and percentage columns predictably.

## Layout & Spacing

The layout is built upon an adaptive 12-column fluid grid system optimized for widescreen enterprise monitors, scaling down gracefully to single-column phone interfaces.

- **Breakpoints:**
  - Desktop (Default): 1200px and up (12 columns, 24px gutters, 32px canvas margins).
  - Tablet / Laptop: 768px – 1199px (8 columns, 16px gutters, 24px canvas margins).
  - Mobile: Under 768px (4 columns, 12px gutters, 16px canvas margins).
- **Rhythm & Structure:** Base spacing conforms to a rigid 4px/8px incremental scale. Internal card padding is standardized at `space-lg` (24px) for analytical summary widgets and `space-md` (16px) for compact data tables and filter bars. Section blocks maintain `space-xl` separation to preserve structural breathing room amidst dense numerical tables.

## Elevation & Depth

Visual hierarchy uses low-contrast physical tiers, relying primarily on subtle border outlines supplemented by soft, multi-layered diffuse shadows.

- **Canvas Base (Tier 0):** `#F8FAFC` flat surface.
- **Surface Elevation (Tier 1 - Metric Cards, Panels):** Pure white background (`#FFFFFF`), bounded by a 1px solid hairline border in `#E2E8F0`. Layered shadow: `0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 6px -2px rgba(15, 23, 42, 0.02)`.
- **Hover & Focused State (Tier 2):** Applied when interacting with row items, selectable cards, and open dropdowns. Hairline border brightens to `#CBD5E1`. Layered shadow: `0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 10px 15px -3px rgba(15, 23, 42, 0.04)`.
- **Floating Modals & Flyouts (Tier 3):** `#FFFFFF` surface with a delicate border (`#CBD5E1`), lifted by `0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04)`.

## Shapes

The design system enforces a **Soft** shape archetype (`roundedness: 1`), creating an architectural, instrument-like feel.

- **Micro Components (Chips, Buttons, Inputs, Tooltips):** `0.25rem` (4px) corner radius, signaling crisp, sharp utility without harsh, zero-radius brutality.
- **Mid Components (Data Cards, Modal Dialogs, Table Shells):** `0.5rem` (8px) corner radius (`rounded-lg`), providing enough curvature to contain content logically without consuming valuable data real estate.
- **Containers & Drawers:** `0.75rem` (12px) maximum corner radius (`rounded-xl`).
- **Interactive Toggles & Avatars:** Fully rounded circular geometry (`9999px`) is limited solely to student profile avatars and small semantic status beacon dots.

## Components

### Buttons
- **Primary:** Background `#1E1B4B`, label in white, height 36px, horizontal padding 14px. Hover state shifts to `#312E81`. Focus state reveals a 2px offset ring in `#4F46E5`.
- **Secondary:** White background with a 1px border in `#E2E8F0`, text in `#334155`. Hover shifts background to `#F8FAFC` and border to `#CBD5E1`.
- **Destructive:** Background `#FEF2F2`, text `#EF4444`, border 1px `#FCA5A5`. Hover deepens to `#EF4444` background with white text.

### Metric Cards & Key Performance Indicators
- Encapsulated within Tier 1 surfaces. Features an uppercase category label (`label-sm`, `#64748B`), an oversized metric value in Hanken Grotesk (`headline-lg`, `#0F172A`), followed by an inline trend indicator badge:
  - Positive: `#ECFDF5` pill containing an emerald icon and percentage in JetBrains Mono (`label-sm`).
  - Negative: `#FEF2F2` pill containing a rose icon and percentage.

### Data Tables
- Table header row uses `#F1F5F9` background, `0.75rem` uppercase label styling, `#475569` text color, and a 1px bottom border in `#E2E8F0`.
- Data rows alternate pure white and `#FCFDFE` (subtle banding) with a hover overlay of `#F8FAFC`. Vertical cell padding is locked to `10px` for high row density.
- Cell alignment: Left-aligned for student names and engineering disciplines; right-aligned with JetBrains Mono for CGPA, test scores, and packages.

### Status Chips & Badges
- Strict layout: 22px height, 8px padding, 4px corner radius.
- **Placed:** Background `#ECFDF5`, text `#065F46`, 1px border `#A7F3D0`. Includes a 6px solid emerald dot.
- **In Review:** Background `#FFFBEB`, text `#92400E`, 1px border `#FDE68A`. Includes a 6px solid amber dot.
- **At Risk:** Background `#FEF2F2`, text `#991B1B`, 1px border `#FECACA`. Includes a 6px solid rose dot.

### Model Probability Gauges & Progress Bars
- Linear bars have a 6px height, track background in `#E2E8F0`, and fill gradient from `#4338CA` to `#38BDF8`.
- Model prediction scores (e.g., "Placement Likelihood: 87%") show numerical probabilities in `label-md` accompanied by a segmented likelihood meter.

### Inputs & Filters
- Form controls use a 36px height, pure white surface, 1px `#CBD5E1` border, and 12px horizontal inset.
- Active state transitions border to `#4F46E5` with a `0 0 0 3px rgba(99, 102, 241, 0.15)` focus ring.
- Filter chips feature a removable `X` icon, using `#F1F5F9` surface with `#334155` typography.

### Iconography (Lucide Icons)
- Stroke width is fixed strictly to `1.75px` across all sizes to preserve crisp geometric harmony. Standard icon size is 16px inside controls and table actions, scaling up to 20px within main navigation sidebars.