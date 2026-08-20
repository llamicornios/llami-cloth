---
version: alpha
name: Llami Cloth
description: Micro-revista fashion-tech peruana — editorial textil sobre fondo negro, kawaii medido, acentos fucsia/menta accesibles.
colors:
  bg: "#000000"
  ink: "#333333"
  ink-soft: "#6B645A"
  card: "#FFFFFF"
  border: "#0E9F83"
  menta: "#0E9F83"
  menta-deep: "#0B7E68"
  menta-soft: "#DFF7F1"
  fucsia: "#E11D8E"
  fucsia-deep: "#B3126F"
  fucsia-soft: "#FDE4F1"
  hero-text: "#F5F1E8"
  link: "#B3126F"
typography:
  display-h1:
    fontFamily: Space Grotesk
    fontSize: 7.6rem
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.04em"
  display-h2:
    fontFamily: Space Grotesk
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.03em"
  card-title:
    fontFamily: Space Grotesk
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  body:
    fontFamily: Roboto
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  meta:
    fontFamily: Roboto
    fontSize: 0.84rem
    fontWeight: 700
    letterSpacing: "0.08em"
rounded:
  sm: 10px
  lg: 999px
  card: 22px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
components:
  button-primary:
    backgroundColor: "{colors.fucsia-deep}"
    textColor: "#FFFFFF"
    rounded: "{rounded.lg}"
    height: 44px
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.menta-deep}"
    textColor: "#FFFFFF"
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
  card-title:
    textColor: "{colors.fucsia-deep}"
    typography: "{typography.card-title}"
---

# Llami Cloth 👑

## Overview

"llama + tela": la marca de briefs de tendencias moda+IA que Llami Cloth
publica cada mañana. El sitio es su archivo público: fondo negro editorial,
cards tipo ficha textil (pespunte punteado), acentos fucsia/menta y kawaii
medido — cero decoración gratuita.

## Colors

- **bg (#000000):** fondo editorial. Todo el contenido vive sobre negro.
- **hero-text (#F5F1E8):** texto principal sobre negro.
- **fucsia-deep (#B3126F):** el acento que siempre cumple WCAG AA (6.5:1)
  sobre blanco — se usa para títulos e interacción.
- **menta (#0E9F83) / menta-deep (#0B7E68):** acento secundario (textura,
  pisos, hover verde).
- **card (#FFFFFF) + ink (#333333):** superficies de contenido legibles.

## Typography

- **Display (Space Grotesk)** para h1, h2, títulos de card y marca: gesto
  fashion-tech, tracking moderado.
- **Roboto** para el cuerpo: continuidad con el PDF del brief diario.

## Components

- `button-primary`: fucsia-deep, 44px de alto, pill (radio 999px) — el único
  CTA de alta énfasis.
- `card`: blanca, borde menta, radio 22px. Las cards secundarias llevan borde
  **de pespunte (dashed)** como costura; la tendencia principal es sólida
  fucsia-deep.
- Títulos de card en `fucsia-deep` (siempre AA sobre blanco).

## Do's and Don'ts

- **Sí:** fondo negro; fucsia-deep para texto sobre blanco; pespunte/textura
  textil sutil; Space Grotesk en títulos; kawaii medido (una 👑 como máximo).
- **No:** texto fucsia claro (#E11D8E) sobre blanco (falla AA 4.5:1);
  glassmorphism; gradientes agresivos; decoración textil excesiva; emoji
  decorativo.
