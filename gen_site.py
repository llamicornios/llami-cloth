#!/usr/bin/env python3
"""Generador estático idempotente para Llami Cloth 👑.

Lee el historial JSON de briefs y regenera index.html, ediciones/*.html,
assets/style.css y manifest.json. No usa dependencias externas.
"""
from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
HISTORY_DIR = Path("/home/llamiclaw/briefs/historial")
EDITIONS_DIR = ROOT / "ediciones"
ASSETS_DIR = ROOT / "assets"

BRAND = "Llami Cloth 👑"
TAGLINE = "Brief de Tendencias Moda+IA · Edición diaria"
CONTACT_EMAIL = "kioshishimabuku@gmail.com"
CONTACT_PHONE = "+51 992-670-102"
CONTACT_PHONE_HREF = "tel:+51992670102"
INSTAGRAM = "@kioshishimabuku"
INSTAGRAM_URL = "https://instagram.com/kioshishimabuku"

STYLE_CSS = r"""
:root {
  --bg: #000000;
  --ink: #333333;
  --ink-soft: #6B645A;
  --card: #FFFFFF;
  --border: #0E9F83;
  --menta: #0E9F83;
  --menta-deep: #0B7E68;
  --menta-soft: #DFF7F1;
  --fucsia: #E11D8E;
  --fucsia-deep: #B3126F;
  --fucsia-soft: #FDE4F1;
  --hero-text: #F5F1E8;
  --link: #B3126F;
  --max: 1120px;
  --radius: 22px;
  --shadow: 0 18px 48px rgba(0, 0, 0, 0.18);
}

* { box-sizing: border-box; }

html {
  color-scheme: light dark;
  font-family: Roboto, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--hero-text);
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at top right, rgba(225, 29, 142, 0.16), transparent 34rem),
    radial-gradient(circle at bottom left, rgba(14, 159, 131, 0.14), transparent 30rem),
    var(--bg);
  font-size: 16px;
  line-height: 1.6;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image: linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(to bottom, rgba(0,0,0,0.75), transparent 70%);
}

img, svg { max-width: 100%; }

a {
  color: inherit;
  text-decoration-thickness: 0.12em;
  text-underline-offset: 0.2em;
}

a:hover { color: var(--fucsia); }

a:focus-visible,
button:focus-visible {
  outline: 3px solid var(--menta);
  outline-offset: 4px;
  border-radius: 10px;
}

.skip-link {
  position: absolute;
  left: 1rem;
  top: -5rem;
  z-index: 10;
  background: var(--card);
  color: var(--ink);
  padding: 0.65rem 0.9rem;
  border: 2px solid var(--menta);
  border-radius: 999px;
}

.skip-link:focus { top: 1rem; }

.site-header {
  border-bottom: 1px solid rgba(223, 247, 241, 0.26);
  background: rgba(0, 0, 0, 0.86);
  position: sticky;
  top: 0;
  z-index: 4;
  backdrop-filter: blur(8px);
}

.header-inner,
.hero,
main,
.footer-inner {
  width: min(var(--max), calc(100% - 2rem));
  margin-inline: auto;
}

.header-inner {
  min-height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.brand-link {
  color: var(--hero-text);
  font-weight: 900;
  letter-spacing: 0.02em;
  text-decoration: none;
}

.header-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.35rem 0.8rem;
  color: rgba(245, 241, 232, 0.84);
  font-size: 0.92rem;
  font-weight: 700;
}

.header-nav a { text-decoration: none; }

.hero {
  padding: clamp(3rem, 9vw, 7rem) 0 clamp(2rem, 5vw, 4rem);
}

.eyebrow,
.edition-kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  margin: 0 0 1rem;
  color: var(--menta-soft);
  font-size: 0.82rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1, h2, h3 { line-height: 1.08; }

h1 {
  max-width: 780px;
  margin: 0;
  color: var(--hero-text);
  font-size: clamp(3rem, 11vw, 7.6rem);
  font-weight: 900;
  letter-spacing: -0.07em;
}

.hero-tagline {
  max-width: 620px;
  margin: 1.25rem 0 0;
  color: rgba(245, 241, 232, 0.86);
  font-size: clamp(1.05rem, 2.5vw, 1.45rem);
  font-weight: 500;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.pill {
  display: inline-flex;
  align-items: center;
  border: 1px solid rgba(223, 247, 241, 0.35);
  border-radius: 999px;
  padding: 0.5rem 0.8rem;
  color: var(--hero-text);
  background: rgba(255,255,255,0.06);
  font-size: 0.92rem;
  font-weight: 700;
}

main { padding-bottom: 3rem; }

.section {
  margin: 0 0 clamp(2rem, 6vw, 4rem);
}

.section-header {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.section h2 {
  margin: 0;
  color: var(--hero-text);
  font-size: clamp(1.75rem, 4vw, 3rem);
  font-weight: 900;
  letter-spacing: -0.045em;
}

.section-note {
  margin: 0;
  color: rgba(245, 241, 232, 0.72);
  font-weight: 500;
}

.feature-card,
.edition-card,
.trend-card,
.empty-card {
  background: var(--card);
  color: var(--ink);
  border: 2px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.feature-card {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.2rem;
  padding: clamp(1.15rem, 4vw, 2rem);
}

.feature-meta,
.card-meta,
.trend-label {
  color: var(--menta-deep);
  font-size: 0.84rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.feature-title,
.card-title,
.trend-card h3 {
  margin: 0.3rem 0 0.7rem;
  color: var(--fucsia);
  font-weight: 900;
  letter-spacing: -0.035em;
}

.feature-title { font-size: clamp(1.8rem, 5vw, 3.4rem); }
.card-title { font-size: clamp(1.28rem, 3vw, 2rem); }
.trend-card h3 { font-size: clamp(1.25rem, 3vw, 1.85rem); }

.feature-date,
.card-date,
.edition-date {
  margin: 0;
  color: var(--ink-soft);
  font-weight: 700;
}

.preview-list,
.trend-list {
  padding-left: 1.15rem;
  margin: 0.9rem 0 0;
  color: var(--ink);
}

.preview-list li,
.trend-list li { margin: 0.35rem 0; }

.actions,
.edition-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.1rem;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0.62rem 0.95rem;
  border: 2px solid var(--fucsia-deep);
  border-radius: 999px;
  background: var(--fucsia-deep);
  color: #FFFFFF;
  font-weight: 900;
  text-decoration: none;
}

.button:hover {
  background: var(--menta-deep);
  border-color: var(--menta-deep);
  color: #FFFFFF;
}

.button.secondary {
  background: var(--card);
  color: var(--link);
}

.button.secondary:hover {
  color: #FFFFFF;
  background: var(--link);
}

.editions-list {
  display: grid;
  gap: 1rem;
}

.edition-card {
  padding: clamp(1rem, 3vw, 1.45rem);
}

.edition-card a.card-title-link {
  color: inherit;
  text-decoration: none;
}

.edition-card a.card-title-link:hover .card-title { color: var(--menta-deep); }

.edition-hero {
  padding-bottom: clamp(1.75rem, 5vw, 3rem);
}

.edition-title {
  max-width: 900px;
  font-size: clamp(2.4rem, 7vw, 5.8rem);
}

.trends-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.trend-card {
  padding: clamp(1rem, 3vw, 1.45rem);
}

.trend-card p { margin: 0.45rem 0 0; }

.trend-card strong {
  color: var(--ink);
  font-weight: 900;
}

.source-link {
  color: var(--link);
  font-weight: 900;
  overflow-wrap: anywhere;
}

.empty-card {
  padding: 1.4rem;
  color: var(--ink);
}

.site-footer {
  border-top: 1px solid rgba(223, 247, 241, 0.26);
  padding: 2rem 0;
  color: rgba(245, 241, 232, 0.82);
}

.footer-inner {
  display: grid;
  gap: 1rem;
}

.footer-inner h2 {
  margin: 0;
  color: var(--hero-text);
  font-size: 1.25rem;
}

.footer-inner p { margin: 0; }

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 1rem;
}

.footer-links a { color: var(--hero-text); font-weight: 700; }
.footer-links a:hover { color: var(--fucsia); }

@media (min-width: 720px) {
  .feature-card { grid-template-columns: minmax(0, 1.12fr) minmax(280px, 0.88fr); align-items: center; }
  .editions-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .trends-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (min-width: 1040px) {
  .trends-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .trend-card:nth-child(1), .trend-card:nth-child(4) { grid-column: span 2; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
}
""".strip() + "\n"


@dataclass(frozen=True)
class Edition:
    slug: str
    source_file: str
    edicion: int
    number: str
    fecha_larga: str
    fecha_corta: str
    generado: str
    tendencias: list[dict[str, str]]

    @property
    def sort_key(self) -> tuple[str, int, str]:
        # El slug YYYY-MM-DD_NNN viene del nombre de archivo: estable, cronológico e idempotente.
        date_part = self.slug.split("_", 1)[0]
        return (date_part, self.edicion, self.slug)


def h(value: Any) -> str:
    return escape(str(value), quote=True)


def clean_slug(path: Path) -> str:
    slug = path.stem
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{3,}", slug):
        # Fallback estable para historiales futuros con nombres raros.
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-").lower() or "edicion"
    return slug


def load_editions() -> list[Edition]:
    editions: list[Edition] = []
    for path in sorted(HISTORY_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        tendencias = data.get("tendencias", [])
        if not isinstance(tendencias, list):
            tendencias = []
        edicion = int(data.get("edicion", 0) or 0)
        editions.append(
            Edition(
                slug=clean_slug(path),
                source_file=str(path),
                edicion=edicion,
                number=f"#{edicion:03d}" if edicion else "#000",
                fecha_larga=str(data.get("fecha_larga", "")),
                fecha_corta=str(data.get("fecha_corta", "")),
                generado=str(data.get("generado", "")),
                tendencias=[{str(k): str(v) for k, v in t.items()} for t in tendencias if isinstance(t, dict)],
            )
        )
    return sorted(editions, key=lambda e: e.sort_key, reverse=True)


def page_shell(title: str, description: str, body: str, current: str = "") -> str:
    nav_ediciones = ' aria-current="page"' if current == "ediciones" else ""
    nav_inicio = ' aria-current="page"' if current == "inicio" else ""
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{h(description)}">
  <title>{h(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a class="brand-link" href="index.html"{nav_inicio}>{BRAND}</a>
      <nav class="header-nav" aria-label="Navegación principal">
        <a href="index.html"{nav_inicio}>Inicio</a>
        <a href="index.html#ediciones"{nav_ediciones}>Ediciones</a>
        <a href="#contacto">Contacto</a>
      </nav>
    </div>
  </header>
{body}
</body>
</html>
"""


def page_shell_edition(title: str, description: str, body: str) -> str:
    # Variante con rutas relativas desde ediciones/.
    return page_shell(title, description, body, current="ediciones").replace('href="assets/style.css"', 'href="../assets/style.css"').replace('href="index.html"', 'href="../index.html"').replace('href="index.html#ediciones"', 'href="../index.html#ediciones"')


def preview_items(edition: Edition, limit: int = 3) -> str:
    items = edition.tendencias[:limit]
    if not items:
        return '<p class="card-date">Sin tendencias registradas en el JSON.</p>'
    return "<ol class=\"preview-list\">" + "".join(f"<li>{h(t.get('titulo', 'Sin título'))}</li>" for t in items) + "</ol>"


def render_index(editions: list[Edition]) -> str:
    if not editions:
        body = f"""
  <section class="hero" aria-labelledby="hero-title">
    <p class="eyebrow">Repositorio de briefs</p>
    <h1 id="hero-title">{BRAND}</h1>
    <p class="hero-tagline">{TAGLINE}</p>
  </section>
  <main id="contenido">
    <section class="section" aria-labelledby="ultima-edicion">
      <h2 id="ultima-edicion">Última edición</h2>
      <article class="empty-card"><p>No hay ediciones todavía.</p></article>
    </section>
  </main>
{footer_html('../' if False else '')}
"""
        return page_shell(f"{BRAND} · Repositorio", TAGLINE, body, current="inicio")

    latest = editions[0]
    edition_cards = []
    for ed in editions[1:]:
        edition_cards.append(f"""
        <article class="edition-card">
          <p class="card-meta">Edición {h(ed.number)}</p>
          <a class="card-title-link" href="ediciones/{h(ed.slug)}.html"><h3 class="card-title">{h(ed.fecha_corta)}</h3></a>
          <p class="card-date">{h(ed.fecha_larga)}</p>
          {preview_items(ed)}
          <div class="actions"><a class="button secondary" href="ediciones/{h(ed.slug)}.html">Leer edición</a></div>
        </article>
""")
    previous_html = "".join(edition_cards) if edition_cards else '<article class="empty-card"><p>No hay ediciones anteriores todavía.</p></article>'
    latest_titles = preview_items(latest, limit=4)
    body = f"""
  <section class="hero" aria-labelledby="hero-title">
    <p class="eyebrow">Repositorio de briefs</p>
    <h1 id="hero-title">{BRAND}</h1>
    <p class="hero-tagline">{TAGLINE}</p>
    <div class="hero-meta" aria-label="Pilares del proyecto">
      <span class="pill">Veracidad &gt; cantidad</span>
      <span class="pill">Fuente citada</span>
      <span class="pill">Ángulo diseñador + docente</span>
    </div>
  </section>
  <main id="contenido">
    <section class="section" aria-labelledby="ultima-edicion">
      <div class="section-header">
        <h2 id="ultima-edicion">Última edición</h2>
        <p class="section-note">Deducida del historial: {h(latest.fecha_corta)}</p>
      </div>
      <article class="feature-card">
        <div>
          <p class="feature-meta">Edición {h(latest.number)}</p>
          <h3 class="feature-title">{h(latest.fecha_corta)}</h3>
          <p class="feature-date">{h(latest.fecha_larga)}</p>
          <div class="actions"><a class="button" href="ediciones/{h(latest.slug)}.html">Leer la edición completa</a></div>
        </div>
        <div aria-label="Preview de tendencias de la última edición">
          {latest_titles}
        </div>
      </article>
    </section>
    <section class="section" id="ediciones" aria-labelledby="ediciones-title">
      <div class="section-header">
        <h2 id="ediciones-title">Ediciones anteriores</h2>
        <p class="section-note">Archivo jerárquico por fecha + edición.</p>
      </div>
      <div class="editions-list">
{previous_html}
      </div>
    </section>
  </main>
{footer_html('')}
"""
    return page_shell(f"{BRAND} · Repositorio", f"{TAGLINE}: archivo de {len(editions)} ediciones.", body, current="inicio")


def footer_html(prefix: str) -> str:
    return f"""
  <footer class="site-footer" id="contacto" role="contentinfo">
    <div class="footer-inner">
      <h2>{BRAND}</h2>
      <p>Veracidad &gt; cantidad · fuente citada con URL real · corto y kawaii · ángulo diseñador + docente.</p>
      <div class="footer-links" aria-label="Contacto">
        <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
        <a href="{CONTACT_PHONE_HREF}">{CONTACT_PHONE}</a>
        <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer">{INSTAGRAM}</a>
      </div>
      <p>Hecho para Kioshi desde el archivo de briefs. 🦙</p>
    </div>
  </footer>
"""


def trend_card(t: dict[str, str], idx: int) -> str:
    title = t.get("titulo", "Sin título")
    que = t.get("que", "")
    por_que = t.get("por_que", "")
    fuente = t.get("fuente", "")
    url = t.get("url", "")
    source = h(fuente)
    if url:
        source = f'<a class="source-link" href="{h(url)}" target="_blank" rel="noopener noreferrer">{h(fuente or url)}</a>'
    return f"""
        <article class="trend-card">
          <p class="trend-label">Tendencia {idx:02d}</p>
          <h3>{h(title)}</h3>
          <p><strong>Qué:</strong> {h(que)}</p>
          <p><strong>Por qué:</strong> {h(por_que)}</p>
          <p><strong>Fuente:</strong> {source}</p>
        </article>
"""


def render_edition(editions: list[Edition], index: int) -> str:
    ed = editions[index]
    newer = editions[index - 1] if index > 0 else None
    older = editions[index + 1] if index + 1 < len(editions) else None
    cards = "".join(trend_card(t, i) for i, t in enumerate(ed.tendencias, start=1))
    if not cards:
        cards = '<article class="empty-card"><p>Esta edición no tiene tendencias registradas en el JSON.</p></article>'
    older_link = f'<a class="button secondary" href="{h(older.slug)}.html">Edición anterior {h(older.number)}</a>' if older else ''
    newer_link = f'<a class="button secondary" href="{h(newer.slug)}.html">Edición siguiente {h(newer.number)}</a>' if newer else ''
    body = f"""
  <section class="hero edition-hero" aria-labelledby="edition-title">
    <p class="edition-kicker">Edición {h(ed.number)}</p>
    <h1 class="edition-title" id="edition-title">{h(ed.fecha_corta)}</h1>
    <p class="hero-tagline">{h(ed.fecha_larga)}</p>
    <div class="actions"><a class="button secondary" href="../index.html">Volver al inicio</a></div>
  </section>
  <main id="contenido">
    <section class="section" aria-labelledby="tendencias-title">
      <div class="section-header">
        <h2 id="tendencias-title">Tendencias</h2>
        <p class="section-note">Textos copiados tal cual del historial JSON.</p>
      </div>
      <div class="trends-grid">
{cards}
      </div>
      <nav class="edition-nav" aria-label="Navegación entre ediciones">
        {older_link}
        <a class="button" href="../index.html#ediciones">Archivo</a>
        {newer_link}
      </nav>
    </section>
  </main>
{footer_html('../')}
"""
    return page_shell_edition(f"{BRAND} · Edición {ed.number} · {ed.fecha_corta}", f"Brief Moda+IA {ed.number} del {ed.fecha_corta}.", body)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build_manifest(editions: list[Edition]) -> dict[str, Any]:
    return {
        "brand": BRAND,
        "source_dir": str(HISTORY_DIR),
        "total_ediciones": len(editions),
        "total_tendencias": sum(len(e.tendencias) for e in editions),
        "ediciones": [
            {
                "slug": e.slug,
                "edicion": e.edicion,
                "numero": e.number,
                "fecha_larga": e.fecha_larga,
                "fecha_corta": e.fecha_corta,
                "generado": e.generado,
                "source_file": e.source_file,
                "html": f"ediciones/{e.slug}.html",
                "tendencias": len(e.tendencias),
            }
            for e in editions
        ],
    }


def main() -> None:
    editions = load_editions()
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Regeneración limpia de páginas de edición para no dejar slugs obsoletos.
    for old in EDITIONS_DIR.glob("*.html"):
        old.unlink()

    write_text(ASSETS_DIR / "style.css", STYLE_CSS)
    write_text(ROOT / "index.html", render_index(editions))
    for i, _ in enumerate(editions):
        write_text(EDITIONS_DIR / f"{editions[i].slug}.html", render_edition(editions, i))
    manifest = build_manifest(editions)
    write_text(ROOT / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    total_tendencias = manifest["total_tendencias"]
    print(f"Procesadas {len(editions)} ediciones y {total_tendencias} tendencias.")


if __name__ == "__main__":
    main()
