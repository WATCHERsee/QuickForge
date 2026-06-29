---
name: Ethereal Forge
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#4cd7f6'
  on-tertiary: '#003640'
  tertiary-container: '#009eb9'
  on-tertiary-container: '#002f38'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#acedff'
  tertiary-fixed-dim: '#4cd7f6'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '450'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 2rem
  element-gap: 1rem
  section-margin: 4rem
  glass-padding: 1.5rem
---

## Brand & Style

The design system is engineered for the high-velocity world of web scaffolding, targeting developers who value precision, speed, and a futuristic aesthetic. The brand personality is "Technical Elegance"—merging the raw power of a CLI with the sophisticated visual depth of modern glassmorphism.

The visual style is characterized by an **Edgeless Glassmorphism** approach. It moves away from traditional containerization in favor of depth created through background blurs, multi-layered translucency, and vibrant, soft-focus gradients. The UI should feel like a holographic interface floating over a deep space void, evoking a sense of limitless potential and high-performance engineering.

## Colors

This design system utilizes a deep, immersive dark palette to maximize the impact of translucent glass effects. 

- **Primary (Indigo):** Used for primary actions, active states, and focus rings.
- **Secondary (Violet):** Used for secondary accents, progress indicators, and gradient stops.
- **Tertiary (Cyan):** Reserved for success states, terminal prompts, and highlights.
- **Background:** A deep midnight navy (`#020617`) serves as the base layer, providing the necessary contrast for the glass components.

Surface colors are never opaque. They are derived from white or primary tints at low opacities (2% to 10%) combined with a high-saturation background blur (20px to 40px).

## Typography

The typography system leverages **Geist** for its precision and neutral, technical character. It is designed to look crisp against blurred backgrounds. 

- **Headlines:** Use tight tracking and heavy weights to anchor the "floating" UI.
- **Body:** Standardized at 16px for readability, using a slightly lighter "Regular" weight to maintain the airy feel of the glass aesthetic.
- **Terminal/Code:** **JetBrains Mono** is utilized for all CLI-related content, input fields, and technical metadata, providing a necessary rhythmic contrast to the sans-serif UI.

## Elevation & Depth

Elevation in this design system is achieved through **Optical Stackability** rather than traditional Y-axis shadows.

- **Surface 1 (Base):** Deep dark background with subtle mesh gradients in indigo/violet.
- **Surface 2 (Standard Glass):** Background blur (32px), 5% white overlay, and a 1px border at 10% white opacity.
- **Surface 3 (Floating/Active):** Background blur (40px), 10% white overlay, and a subtle "inner glow" border (1px primary color at 20% opacity).

Shadows are used sparingly and are "Ambient"—very large, very soft, and tinted with the primary indigo color to simulate a light-emitting surface.

## Shapes

The shape language is sophisticated and modern. All glass panels and containers use a consistent **1rem (16px)** corner radius to soften the technical nature of the CLI data. 

Interactive elements like buttons use a slightly more aggressive rounding (12px) to distinguish them from structural containers. Icons should follow a "linear-duotone" style with rounded caps to match the geometry of the typeface.

## Components

### Buttons
- **Primary:** Solid indigo to violet gradient, no border, white text. Subtle outer glow on hover.
- **Glass (Secondary):** 10% white fill, 32px backdrop blur, 1px white border (10% opacity).

### Glass Cards
High-fidelity containers for project stats. They should feature a "top-light" effect—a subtle 1px white line at the very top edge to simulate light hitting the thickness of the glass.

### Terminal Containers
These are the most critical components. They use a darker, less transparent glass (20% opacity) to ensure code readability. The header of the terminal should feature the "traffic light" window controls and the current directory path in JetBrains Mono.

### Input Fields
Minimalist styling. Only a bottom border (1px white, 10% opacity) in resting state. On focus, the border becomes the primary indigo color with a subtle neon glow underneath the text.

### Chips/Badges
Small, pill-shaped elements with a secondary violet tint and 15% opacity backgrounds. Used for dependency tags and version numbers.