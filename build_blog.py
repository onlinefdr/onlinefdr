#!/usr/bin/env python3
"""
onlinefdr.com.au — Blog generator

Builds the blog index, category pages, and individual post pages from
Markdown files in /blog-content/. Reuses the shared shell (nav, footer,
marquee, entity bar, CSS, JS) from build_pages.py so the blog inherits
the exact site design.

USAGE:
    cd site/ && python3 build_blog.py

WORKFLOW:
    1. Place blog post .md file into /site/blog-content/
    2. Run this script. It validates frontmatter, renders all pages,
       writes them to /site/blog/, and updates sitemap.xml.
    3. cp the output files to their served locations (the script does
       this automatically; no manual cp needed).
    4. Commit and push.

FRONTMATTER (YAML, between --- lines, required on every post):
    title: "Post title here, sentence case, no full stop"
    slug: "url-friendly-slug-here"
    date: 2026-05-19            (ISO YYYY-MM-DD)
    category: "Parenting"        (one of CATEGORIES below)
    meta_description: "150-160 character SEO description"
    related_pages: ["/parenting/", "/how-it-works/"]
    reading_time: 7
    hero_image: "filename.jpg"   (OPTIONAL; if absent, placeholder is rendered)

VALIDATION:
    - Em-dashes in body or frontmatter trigger a warning (not fatal).
    - related_pages must come from APPROVED_RELATED_PAGES.
    - category must be in CATEGORIES.
    - slug must match SLUG_PATTERN.
"""

import os
import re
import sys
import json
import yaml
import html
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────

SITE_ROOT = Path(__file__).parent
CONTENT_DIR = SITE_ROOT / "blog-content"
OUT_DIR = SITE_ROOT / "blog"
BASE_CSS_PATH = SITE_ROOT / "base.css"
BUILD_PAGES_PATH = SITE_ROOT / "build_pages.py"
SITEMAP_PATH = SITE_ROOT / "sitemap.xml"

POSTS_PER_PAGE = 12

CATEGORIES = ["Parenting", "Financial Settlement", "Process", "Section 60I", "General"]

# Map display name → URL slug
CATEGORY_SLUGS = {
    "Parenting": "parenting",
    "Financial Settlement": "financial-settlement",
    "Process": "process",
    "Section 60I": "section-60i",
    "General": "general",
}

APPROVED_RELATED_PAGES = {
    "/parenting/", "/financial-settlement/", "/section-60i/",
    "/how-it-works/", "/what-is-fdr/", "/about/", "/book/",
}

# Display labels for the related-pages block
PAGE_LABELS = {
    "/parenting/": "Parenting Matters",
    "/financial-settlement/": "Financial Settlements",
    "/section-60i/": "Section 60I Certificates",
    "/how-it-works/": "How It Works",
    "/what-is-fdr/": "What is FDR?",
    "/about/": "About the Practice",
    "/book/": "Book a Discovery Call",
}

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# ─────────────────────────────────────────────────────────────────
# SHELL IMPORT
# ─────────────────────────────────────────────────────────────────
# Pull NAV_LINKS, MARQUEE_ITEMS, ENTITY_BAR, FOOTER, BASE_JS out of
# build_pages.py without executing it. We read the source and exec only
# the constant-assignment blocks we need.

def load_shell_components():
    """Extract shell constants from build_pages.py by reading source."""
    with open(BUILD_PAGES_PATH) as f:
        src = f.read()

    # Crude but reliable: find each top-level assignment and exec it
    # in an isolated namespace.
    ns = {}

    # NAV_LINKS = """...""" (single-line triple-quoted)
    for name in ["NAV_LINKS", "NAV_CTA", "MARQUEE_ITEMS", "ENTITY_BAR", "FOOTER", "BASE_JS", "SOCIAL_RAIL", "SOCIAL_INLINE"]:
        # Match: NAME = """...""" (multiline)
        pattern = re.compile(
            rf'^{name}\s*=\s*"""(.*?)"""',
            re.MULTILINE | re.DOTALL
        )
        m = pattern.search(src)
        if not m:
            raise RuntimeError(f"Could not find {name} in build_pages.py")
        ns[name] = m.group(1)

    return ns


SHELL = load_shell_components()

GTAG = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18195606042"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'AW-18195606042');
  </script>"""


# ─────────────────────────────────────────────────────────────────
# BASE CSS
# ─────────────────────────────────────────────────────────────────

with open(BASE_CSS_PATH) as f:
    BASE_CSS = f.read()


# ─────────────────────────────────────────────────────────────────
# BLOG-SPECIFIC CSS
# ─────────────────────────────────────────────────────────────────

BLOG_CSS = """
/* ── BLOG: shared ── */
.blog-page-header{background:var(--charcoal);padding:120px 0 56px;position:relative;overflow:hidden}
.blog-page-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.blog-page-header-inner{position:relative;z-index:1;max-width:880px;margin:0 auto}
.blog-page-header .page-label{color:var(--ochre-lt);font-size:0.72rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:18px;display:block}
.blog-page-header h1{font-size:clamp(2.2rem,5vw,4rem);font-weight:800;line-height:1.05;letter-spacing:-0.03em;color:var(--white);margin-bottom:18px;text-wrap:balance}
.blog-page-header h1 .accent{color:var(--ochre)}
.blog-page-header .page-intro{color:rgba(253,250,246,0.65);font-size:clamp(1rem,1.3vw,1.1rem);line-height:1.6;max-width:680px}

/* Category filter pills */
.blog-filters{background:var(--dust);border-bottom:1px solid var(--dust-3);padding:18px 0}
.blog-filters-inner{display:flex;flex-wrap:wrap;gap:8px;align-items:center;max-width:1100px;margin:0 auto;padding:0 var(--pad)}
.blog-filters-label{font-size:0.72rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--mid);margin-right:6px}
.filter-pill{display:inline-flex;align-items:center;font-family:var(--f);font-size:0.82rem;font-weight:600;color:var(--charcoal);background:var(--white);border:1px solid var(--dust-3);border-radius:100px;padding:7px 14px;text-decoration:none;transition:border-color 0.2s,background 0.2s,color 0.2s}
.filter-pill:hover{border-color:var(--ochre);color:var(--terra)}
.filter-pill.active{background:var(--charcoal);color:var(--white);border-color:var(--charcoal)}

/* Blog index grid */
.blog-grid-wrap{padding:56px 0 80px;background:var(--bg)}
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;max-width:1100px;margin:0 auto;padding:0 var(--pad)}
@media(max-width:900px){.blog-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.blog-grid{grid-template-columns:1fr}}

.post-card{display:flex;flex-direction:column;background:var(--white);border:1px solid var(--dust-3);border-radius:12px;overflow:hidden;transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;text-decoration:none;color:inherit}
.post-card:hover{border-color:var(--ochre);transform:translateY(-2px);box-shadow:0 10px 30px rgba(44,40,37,0.06)}
.post-card-image{aspect-ratio:16/10;background:var(--dust-2);position:relative;overflow:hidden;border-bottom:1px solid var(--dust-3)}
.post-card-image img{width:100%;height:100%;object-fit:cover;display:block}
.post-card-image-placeholder{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--dust-3)}
.post-card-image-placeholder svg{width:38px;height:38px}
.post-card-body{padding:22px 22px 24px;display:flex;flex-direction:column;flex:1}
.post-card-meta{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.post-card-cat{display:inline-flex;font-size:0.62rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--terra);background:var(--ochre-pale);padding:4px 10px;border-radius:100px}
.post-card-date{font-size:0.74rem;font-weight:500;color:var(--mid)}
.post-card-pinned{display:inline-flex;align-items:center;gap:5px;font-size:0.62rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#fff;background:var(--terra);padding:4px 10px;border-radius:100px}
.post-card-pinned svg{width:11px;height:11px}
.post-card h2{font-size:1.1rem;font-weight:700;line-height:1.3;color:var(--charcoal);margin-bottom:10px;letter-spacing:-0.01em}
.post-card-excerpt{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.6;margin-bottom:16px;flex:1}
.post-card-read{font-size:0.78rem;font-weight:600;color:var(--terra);display:inline-flex;align-items:center;gap:6px;margin-top:auto}
.post-card-read svg{transition:transform 0.2s}
.post-card:hover .post-card-read svg{transform:translateX(3px)}

/* Pagination */
.blog-pagination{display:flex;justify-content:center;align-items:center;gap:8px;margin:48px auto 0;max-width:1100px;padding:0 var(--pad)}
.page-link{display:inline-flex;align-items:center;justify-content:center;min-width:38px;height:38px;padding:0 12px;font-family:var(--f);font-size:0.88rem;font-weight:600;color:var(--charcoal);background:var(--white);border:1px solid var(--dust-3);border-radius:8px;text-decoration:none;transition:border-color 0.2s,background 0.2s,color 0.2s}
.page-link:hover{border-color:var(--ochre);color:var(--terra)}
.page-link.active{background:var(--charcoal);color:var(--white);border-color:var(--charcoal)}
.page-link.disabled{opacity:0.4;pointer-events:none}

.blog-empty{text-align:center;padding:80px 20px;color:var(--mid)}
.blog-empty h2{font-size:1.4rem;font-weight:700;color:var(--charcoal);margin-bottom:8px}
.blog-empty p{font-size:0.95rem;line-height:1.6}

/* ── POST PAGE ── */
.post-header{background:var(--charcoal);padding:120px 0 56px;position:relative;overflow:hidden}
.post-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.post-header-inner{position:relative;z-index:1;max-width:760px;margin:0 auto;padding:0 var(--pad)}
.post-cat-pill{display:inline-flex;font-size:0.66rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--ochre);background:rgba(196,135,58,0.12);padding:5px 12px;border-radius:100px;margin-bottom:18px;text-decoration:none;transition:background 0.2s}
.post-cat-pill:hover{background:rgba(196,135,58,0.2)}
.post-header h1{font-size:clamp(2rem,4.5vw,3.4rem);font-weight:800;line-height:1.1;letter-spacing:-0.02em;color:var(--white);margin-bottom:20px;text-wrap:balance}
.post-meta{display:flex;align-items:center;gap:16px;flex-wrap:wrap;color:rgba(253,250,246,0.55);font-size:0.84rem;font-weight:500}
.post-meta-sep{opacity:0.4}

.post-hero-image{max-width:880px;margin:0 auto;padding:0 var(--pad);transform:translateY(-32px)}
.post-hero-image-inner{aspect-ratio:21/9;border-radius:12px;overflow:hidden;background:var(--dust-2);border:1px solid var(--dust-3);position:relative}
.post-hero-image-inner img{width:100%;height:100%;object-fit:cover;display:block}
.post-hero-placeholder{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:var(--dust-3)}
.post-hero-placeholder svg{width:42px;height:42px}
.post-hero-placeholder span{font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase}

.post-body-wrap{padding:0 0 80px;background:var(--bg)}
.post-body{max-width:720px;margin:0 auto;padding:0 var(--pad)}

/* TLDR summary block (top of post, AEO-optimised) */
.post-tldr{max-width:720px;margin:0 auto 36px;padding:0 var(--pad)}
.post-tldr-inner{background:var(--dust);border:1px solid var(--dust-3);border-left:3px solid var(--ochre);border-radius:8px;padding:22px 26px}
.post-tldr-label{display:inline-block;font-size:0.66rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--terra);margin-bottom:8px}
.post-tldr-text{font-size:0.98rem;font-weight:500;color:var(--charcoal);line-height:1.65;margin:0}
@media(max-width:768px){.post-tldr-inner{padding:18px 20px}}
.post-body h2{font-size:clamp(1.4rem,2.4vw,1.75rem);font-weight:700;color:var(--charcoal);letter-spacing:-0.01em;line-height:1.25;margin:42px 0 16px}
.post-body h2:first-child{margin-top:8px}
.post-body h3{font-size:clamp(1.1rem,1.6vw,1.25rem);font-weight:700;color:var(--charcoal);line-height:1.3;margin:32px 0 12px}
.post-body p{font-size:1.02rem;font-weight:400;color:var(--mid);line-height:1.8;margin-bottom:18px}
.post-body p strong{color:var(--charcoal);font-weight:700}
.post-body a{color:var(--terra);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;transition:color 0.2s}
.post-body a:hover{color:var(--ochre)}
.post-body ul,.post-body ol{margin:0 0 22px 22px;padding:0}
.post-body ul li,.post-body ol li{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.8;margin-bottom:8px;padding-left:4px}
.post-body ul li::marker{color:var(--terra)}
.post-body ol li::marker{color:var(--terra);font-weight:700}
.post-body blockquote{border-left:3px solid var(--ochre);padding:6px 0 6px 22px;margin:28px 0;color:var(--charcoal);font-style:normal;font-size:1.05rem;font-weight:500;line-height:1.65}
.post-body code{background:var(--dust-2);padding:2px 6px;border-radius:4px;font-size:0.9em;font-family:Menlo,Consolas,monospace}
/* Language grid (multilingual post): 3 columns desktop, responsive down */
.lang-grid{column-count:3;column-gap:24px;margin:24px 0 28px;padding:24px;background:var(--dust);border:1px solid var(--dust-3);border-radius:12px}
.lang-item{display:block;break-inside:avoid;font-size:0.95rem;color:var(--charcoal);line-height:1.9;padding:2px 0;border-bottom:1px solid var(--dust-2)}
@media(max-width:680px){.lang-grid{column-count:2}}
@media(max-width:420px){.lang-grid{column-count:1}}

/* Related pages block */
.post-related{max-width:720px;margin:48px auto 0;padding:0 var(--pad)}
.post-related-inner{background:var(--dust);border:1px solid var(--dust-3);border-radius:12px;padding:28px 30px}
.post-related h3{font-size:0.74rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--mid);margin-bottom:14px}
.post-related-links{display:flex;flex-direction:column;gap:8px}
.post-related-link{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 18px;background:var(--white);border:1px solid var(--dust-3);border-radius:8px;text-decoration:none;color:var(--charcoal);font-weight:600;font-size:0.95rem;transition:border-color 0.2s,transform 0.2s}
.post-related-link:hover{border-color:var(--ochre);transform:translateX(2px)}
.post-related-link svg{color:var(--terra);flex-shrink:0}

/* Post final CTA */
.post-cta{max-width:720px;margin:48px auto 0;padding:0 var(--pad)}
.post-cta-inner{background:var(--charcoal);border-radius:12px;padding:36px 32px;text-align:center;color:var(--white)}
.post-cta-inner h3{font-size:clamp(1.3rem,2.2vw,1.7rem);font-weight:700;color:var(--white);margin-bottom:10px;letter-spacing:-0.01em}
.post-cta-inner p{font-size:0.96rem;color:rgba(253,250,246,0.7);line-height:1.6;margin-bottom:22px;max-width:520px;margin-left:auto;margin-right:auto}
.post-cta-inner .btn{display:inline-flex;align-items:center;gap:8px;background:var(--ochre);color:var(--charcoal);font-family:var(--f);font-size:0.95rem;font-weight:700;padding:14px 26px;border-radius:8px;text-decoration:none;transition:background 0.2s,transform 0.2s}
.post-cta-inner .btn:hover{background:var(--ochre-lt);transform:translateY(-1px)}

@media(max-width:768px){
  .post-related-inner{padding:22px 20px}
  .post-cta-inner{padding:28px 22px}
  .post-hero-image{transform:translateY(-24px)}
  .post-hero-image-inner{aspect-ratio:16/9}
}
"""


# ─────────────────────────────────────────────────────────────────
# MARKDOWN → HTML (minimal, no external deps)
# ─────────────────────────────────────────────────────────────────
# Blog markdown is authored by Claude and placed in /site/blog-content/.
# We need a small, correct converter
# that handles: H2/H3, paragraphs, bold, italic, links, lists,
# blockquotes, inline code. No tables, no images-in-body (we put hero
# above the body via frontmatter), no HTML pass-through.

INLINE_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
INLINE_BOLD = re.compile(r'\*\*([^*]+)\*\*')
INLINE_ITALIC = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')
INLINE_CODE = re.compile(r'`([^`]+)`')


def inline_md(text):
    """Apply inline markdown transformations."""
    # Escape HTML special chars first, then re-allow our inline patterns
    text = html.escape(text, quote=False)
    # Inline code (do first so its contents aren't re-processed)
    text = INLINE_CODE.sub(lambda m: f'<code>{m.group(1)}</code>', text)
    # Bold before italic (avoids ** vs * confusion)
    text = INLINE_BOLD.sub(lambda m: f'<strong>{m.group(1)}</strong>', text)
    text = INLINE_ITALIC.sub(lambda m: f'<em>{m.group(1)}</em>', text)
    # Links — note: bracketed text was already escaped, so &amp;quot; etc
    # would have been mangled. Run links on raw to capture, then escape only
    # the URL safely.
    def link_sub(m):
        text_part = m.group(1)
        url_part = m.group(2)
        # url already escaped by html.escape above; that's fine for our links
        return f'<a href="{url_part}">{text_part}</a>'
    text = INLINE_LINK.sub(link_sub, text)
    return text


def md_to_html(md_text):
    """Convert Markdown body to HTML. Block-level processing."""
    lines = md_text.split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line — skip
        if not stripped:
            i += 1
            continue

        # Raw HTML passthrough block: a line starting with <div ...> captures
        # everything verbatim until the matching closing </div> on its own line.
        # Used for the language table and any other pre-built HTML the renderer
        # does not natively support (renderer has no table support by design).
        if stripped.startswith("<div"):
            html_block = [line]
            i += 1
            depth = stripped.count("<div") - stripped.count("</div>")
            while i < n and depth > 0:
                html_block.append(lines[i])
                depth += lines[i].count("<div") - lines[i].count("</div>")
                i += 1
            out.append("\n".join(html_block))
            continue

        # Headings: ## or ###
            out.append(f"<h3>{inline_md(stripped[4:].strip())}</h3>")
            i += 1
            continue
        if stripped.startswith("## "):
            out.append(f"<h2>{inline_md(stripped[3:].strip())}</h2>")
            i += 1
            continue
        # H1 in body is a mistake (title is in frontmatter) — skip silently
        if stripped.startswith("# "):
            i += 1
            continue

        # Blockquote
        if stripped.startswith("> "):
            quote_lines = []
            while i < n and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = " ".join(quote_lines)
            out.append(f"<blockquote>{inline_md(quote_text)}</blockquote>")
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item_text = re.sub(r"^[-*]\s+", "", lines[i].strip())
                items.append(f"<li>{inline_md(item_text)}</li>")
                i += 1
            out.append(f"<ul>{''.join(items)}</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item_text = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f"<li>{inline_md(item_text)}</li>")
                i += 1
            out.append(f"<ol>{''.join(items)}</ol>")
            continue

        # Paragraph — gather until blank or block boundary
        para_lines = []
        while i < n:
            l = lines[i]
            ls = l.strip()
            if not ls:
                break
            if (ls.startswith("## ") or ls.startswith("### ") or ls.startswith("# ")
                    or ls.startswith("> ") or re.match(r"^[-*]\s+", ls)
                    or re.match(r"^\d+\.\s+", ls)):
                break
            para_lines.append(ls)
            i += 1
        para_text = " ".join(para_lines)
        out.append(f"<p>{inline_md(para_text)}</p>")

    return "\n".join(out)


# ─────────────────────────────────────────────────────────────────
# POST PARSING + VALIDATION
# ─────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


class ValidationError(Exception):
    pass


def parse_post(path):
    """Parse a single markdown file. Returns dict with metadata + body_html."""
    with open(path) as f:
        raw = f.read()

    m = FRONTMATTER_RE.match(raw)
    if not m:
        raise ValidationError(f"{path.name}: no YAML frontmatter block found")

    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise ValidationError(f"{path.name}: invalid YAML: {e}")

    if not isinstance(meta, dict):
        raise ValidationError(f"{path.name}: frontmatter must be a YAML mapping")

    body_md = m.group(2).strip()

    # Validate required fields
    required = ["title", "slug", "date", "category", "meta_description",
                "related_pages", "reading_time"]
    for field in required:
        if field not in meta:
            raise ValidationError(f"{path.name}: missing required frontmatter field: {field}")

    # Validate values
    if not SLUG_PATTERN.match(meta["slug"]):
        raise ValidationError(
            f"{path.name}: slug '{meta['slug']}' invalid. "
            f"Use lowercase letters, digits, hyphens only."
        )

    if meta["category"] not in CATEGORIES:
        raise ValidationError(
            f"{path.name}: category '{meta['category']}' not in {CATEGORIES}"
        )

    # date — accept either YYYY-MM-DD string or a date object from YAML
    if isinstance(meta["date"], str):
        try:
            meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(f"{path.name}: date '{meta['date']}' not ISO YYYY-MM-DD")
    elif hasattr(meta["date"], "isoformat"):
        pass  # YAML parsed it for us
    else:
        raise ValidationError(f"{path.name}: date must be YYYY-MM-DD")

    if not isinstance(meta["related_pages"], list) or not (1 <= len(meta["related_pages"]) <= 2):
        raise ValidationError(f"{path.name}: related_pages must be a list of 1-2 entries")

    for p in meta["related_pages"]:
        if p not in APPROVED_RELATED_PAGES:
            raise ValidationError(
                f"{path.name}: related_pages entry '{p}' not in approved list"
            )

    if not isinstance(meta["reading_time"], int) or meta["reading_time"] < 1:
        raise ValidationError(f"{path.name}: reading_time must be a positive integer")

    # TLDR (optional, but if present must be 200-500 chars for AEO)
    if "tldr" in meta and meta["tldr"]:
        tldr_len = len(meta["tldr"])
        if not (150 <= tldr_len <= 600):
            print(f"  WARN {path.name}: tldr is {tldr_len} chars "
                  f"(target 200-500 for AEO featured snippet). Not fatal.")
        if "—" in meta["tldr"]:
            print(f"  WARN {path.name}: em-dash in tldr.")
    else:
        meta["tldr"] = None

    # pin_order (optional positive int). Hand-ranked pin position on the blog
    # index: 1 = top, 2 = next, etc. Unpinned posts (no pin_order) follow in
    # newest-first order below the pinned block. Display property, not a category.
    if "pin_order" in meta and meta["pin_order"] is not None:
        if not isinstance(meta["pin_order"], int) or meta["pin_order"] < 1:
            raise ValidationError(
                f"{path.name}: pin_order must be a positive integer (1 = top)"
            )
    else:
        meta["pin_order"] = None

    meta_desc = meta["meta_description"]
    if not (100 <= len(meta_desc) <= 200):
        print(f"  WARN {path.name}: meta_description is {len(meta_desc)} chars "
              f"(target 150-160). Not fatal.")

    # Em-dash check (warning, not fatal)
    if "—" in body_md or "—" in meta["title"]:
        print(f"  WARN {path.name}: em-dash found. Locked rule violation, but not "
              f"fatal so build continues. Please review and replace before publishing.")

    # Generate excerpt from first paragraph
    body_for_excerpt = re.sub(r"^#+\s+.*$", "", body_md, flags=re.MULTILINE)
    body_for_excerpt = body_for_excerpt.strip()
    first_para_match = re.search(r"^([^\n#>\-*].+?)(?:\n\n|\Z)", body_for_excerpt, re.DOTALL)
    if first_para_match:
        excerpt = first_para_match.group(1).replace("\n", " ").strip()
        # Strip markdown inline marks for excerpt
        excerpt = re.sub(r"\*\*([^*]+)\*\*", r"\1", excerpt)
        excerpt = re.sub(r"\*([^*]+)\*", r"\1", excerpt)
        excerpt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", excerpt)
        if len(excerpt) > 200:
            excerpt = excerpt[:197].rsplit(" ", 1)[0] + "…"
        meta["excerpt"] = excerpt
    else:
        meta["excerpt"] = meta["meta_description"]

    meta["body_html"] = md_to_html(body_md)
    meta["source_path"] = path

    return meta


def load_all_posts():
    """Load and validate every markdown file in CONTENT_DIR."""
    if not CONTENT_DIR.exists():
        CONTENT_DIR.mkdir(parents=True)
        return []

    posts = []
    for p in sorted(CONTENT_DIR.glob("*.md")):
        try:
            posts.append(parse_post(p))
        except ValidationError as e:
            print(f"  ERROR {e}")
            sys.exit(1)

    # Halt if two posts share the same pin_order (clash must not pass silently)
    seen = {}
    for p in posts:
        po = p["pin_order"]
        if po is not None:
            if po in seen:
                print(f"  ERROR pin_order clash: position {po} used by both "
                      f"'{seen[po]}' and '{p['slug']}'. Renumber one of them.")
                sys.exit(1)
            seen[po] = p["slug"]

    # Pinned posts first by pin_order (1 = top), then unpinned newest-first
    posts.sort(key=lambda x: (
        x["pin_order"] if x["pin_order"] is not None else float("inf"),
        x["date"].toordinal() * -1,
    ))
    return posts


# ─────────────────────────────────────────────────────────────────
# RENDERING
# ─────────────────────────────────────────────────────────────────

def shell(title, meta_desc, canonical, schema_json, page_html, current_page=None,
          extra_css="", robots="index, follow", show_marquee=True):
    """Render a full HTML page using the site shell + blog CSS."""
    nav_links = SHELL["NAV_LINKS"]
    if current_page:
        nav_links = nav_links.replace(
            f'href="{current_page}"',
            f'href="{current_page}" aria-current="page"'
        )

    # Marquee sits AFTER the page header (dark header -> ochre marquee -> body),
    # matching how the static content pages place it. Suppressed on individual
    # post pages because the post hero image clashes with the marquee strip.
    if show_marquee:
        marquee = (f'<div class="marquee-bar" aria-hidden="true" role="marquee">\n'
                   f'  <div class="marquee-track">{SHELL["MARQUEE_ITEMS"]}\n'
                   f'  </div>\n</div>')
        if "</header>" in page_html:
            head, rest = page_html.split("</header>", 1)
            page_html_with_marquee = head + "</header>\n" + marquee + rest
        else:
            page_html_with_marquee = marquee + page_html
    else:
        page_html_with_marquee = page_html

    schema_block = (f'<script type="application/ld+json">{schema_json}</script>'
                    if schema_json else "")

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
{GTAG}
  <title>{title}</title>
  <meta name="description" content="{html.escape(meta_desc, quote=True)}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="https://onlinefdr.com.au{canonical}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(meta_desc, quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://onlinefdr.com.au{canonical}">
  <meta property="og:site_name" content="onlinefdr.com.au">
  <meta property="og:locale" content="en_AU">
  <meta property="og:image" content="https://onlinefdr.com.au/images/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://onlinefdr.com.au/images/og-default.jpg">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/images/favicon-192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
  <meta name="theme-color" content="#F2EDE4">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
  {schema_block}
  <style>
{BASE_CSS}
{BLOG_CSS}
{extra_css}
  </style>
</head>
<body>

<a href="#main" class="skip-to-content">Skip to main content</a>

{SHELL["SOCIAL_RAIL"]}

<nav class="nav" id="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-brand" aria-label="onlinefdr.com.au home">
      <svg class="nav-brand-mark" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C4873A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
        <path d="m11 17 2 2a1 1 0 1 0 3-3"/>
        <path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/>
        <path d="m21 3 1 11h-2"/>
        <path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/>
        <path d="M3 4h8"/>
      </svg>
      <span class="nav-brand-text">
        <span class="nav-brand-name">online<span class="brand-fdr">fdr</span>.com.au</span>
        <span class="nav-brand-tag">Accredited Online FDR</span>
      </span>
    </a>
    <ul class="nav-links" id="nav-links" role="list">{nav_links}
    </ul>
    <div class="nav-cta-wrap">{SHELL["NAV_CTA"]}</div>
    <button class="nav-toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</nav>

<main id="main">
{page_html_with_marquee}
</main>

{SHELL["SOCIAL_INLINE"]}

{SHELL["ENTITY_BAR"]}

{SHELL["FOOTER"]}

{SHELL["BASE_JS"]}
</body>
</html>"""


def render_filters(active_category=None):
    """Render the category filter pill row."""
    pills = []
    all_class = "filter-pill" + (" active" if active_category is None else "")
    pills.append(f'<a href="/blog/" class="{all_class}">All</a>')
    for cat in CATEGORIES:
        slug = CATEGORY_SLUGS[cat]
        cls = "filter-pill" + (" active" if active_category == cat else "")
        pills.append(f'<a href="/blog/category/{slug}/" class="{cls}">{cat}</a>')
    return f"""<div class="blog-filters">
  <div class="blog-filters-inner">
    <span class="blog-filters-label">Filter:</span>
    {' '.join(pills)}
  </div>
</div>"""


def fmt_date(d):
    """Format date for display: '19 May 2026'."""
    return d.strftime("%-d %B %Y")


PLACEHOLDER_SVG = """<div class="post-card-image-placeholder">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
</div>"""


def render_post_card(post):
    """Render a single post card for the blog index / category grid."""
    cat = post["category"]
    cat_slug = CATEGORY_SLUGS[cat]
    title_safe = html.escape(post["title"])
    excerpt_safe = html.escape(post["excerpt"])

    pinned_badge = ""
    if post.get("pin_order") is not None:
        pinned_badge = ('<span class="post-card-pinned">'
                        '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14.4 2.6a1 1 0 0 0-1.5.1l-1 1.3-5.1 1.7a1 1 0 0 0-.4 1.6l3 3-4.6 4.6a1 1 0 0 0 1.4 1.4L10.8 17l3 3a1 1 0 0 0 1.6-.4l1.7-5.1 1.3-1a1 1 0 0 0 .1-1.5z"/></svg>'
                        'Pinned</span>')

    if post.get("hero_image"):
        img_block = f'<img src="/blog/images/{post["hero_image"]}" alt="{title_safe}" loading="lazy">'
    else:
        img_block = PLACEHOLDER_SVG

    return f"""<a href="/blog/{post['slug']}/" class="post-card">
  <div class="post-card-image">{img_block}</div>
  <div class="post-card-body">
    <div class="post-card-meta">
      {pinned_badge}<span class="post-card-cat">{cat}</span>
      <span class="post-card-date">{fmt_date(post['date'])}</span>
    </div>
    <h2>{title_safe}</h2>
    <p class="post-card-excerpt">{excerpt_safe}</p>
    <span class="post-card-read">Read article <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
  </div>
</a>"""


def render_pagination(current_page, total_pages, base_url):
    """Render pagination links. base_url ends with /."""
    if total_pages <= 1:
        return ""

    parts = []
    # Prev
    if current_page > 1:
        prev_url = base_url if current_page == 2 else f"{base_url}page/{current_page - 1}/"
        parts.append(f'<a href="{prev_url}" class="page-link">‹ Prev</a>')
    else:
        parts.append('<span class="page-link disabled">‹ Prev</span>')

    # Numbered
    for p in range(1, total_pages + 1):
        url = base_url if p == 1 else f"{base_url}page/{p}/"
        cls = "page-link" + (" active" if p == current_page else "")
        parts.append(f'<a href="{url}" class="{cls}">{p}</a>')

    # Next
    if current_page < total_pages:
        parts.append(f'<a href="{base_url}page/{current_page + 1}/" class="page-link">Next ›</a>')
    else:
        parts.append('<span class="page-link disabled">Next ›</span>')

    return f'<nav class="blog-pagination" aria-label="Pagination">{" ".join(parts)}</nav>'


def render_index_page(posts, page_num, total_pages, active_category=None, category_label=None):
    """Render one page of the blog index or a category page."""
    if active_category:
        cat_slug = CATEGORY_SLUGS[active_category]
        canonical = f"/blog/category/{cat_slug}/" if page_num == 1 else f"/blog/category/{cat_slug}/page/{page_num}/"
        base_url = f"/blog/category/{cat_slug}/"
        title = f"{active_category} — Blog · onlinefdr.com.au"
        meta_desc = f"Articles on {active_category.lower()} from the team at onlinefdr.com.au, Australia's accredited online Family Dispute Resolution practice."
        header_label = active_category
        header_h1 = f"{active_category} <span class=\"accent\">articles</span>."
        header_intro = f"Practical, current writing on {active_category.lower()} for separating Australians. Updated daily."
    else:
        canonical = "/blog/" if page_num == 1 else f"/blog/page/{page_num}/"
        base_url = "/blog/"
        title = "Blog · onlinefdr.com.au"
        meta_desc = "Daily writing on separation, parenting, financial settlement, and Family Dispute Resolution in Australia. Practical, current, and accredited."
        header_label = "Blog"
        header_h1 = "Daily writing on <span class=\"accent\">separation in Australia</span>."
        header_intro = "Practical, current, and accredited. New articles every day on parenting, financial settlement, and the process of Family Dispute Resolution."

    if posts:
        cards = "\n".join(render_post_card(p) for p in posts)
        grid = f'<div class="blog-grid">\n{cards}\n</div>'
    else:
        grid = """<div class="blog-empty">
  <h2>No posts yet</h2>
  <p>New articles are published daily. Check back soon.</p>
</div>"""

    page_html = f"""<header class="blog-page-header">
  <div class="wrap">
    <div class="blog-page-header-inner">
      <span class="page-label">{header_label}</span>
      <h1>{header_h1}</h1>
      <p class="page-intro">{header_intro}</p>
    </div>
  </div>
</header>

{render_filters(active_category)}

<section class="blog-grid-wrap">
  {grid}
  {render_pagination(page_num, total_pages, base_url)}
</section>"""

    # Schema for a Blog or CollectionPage
    schema = '{"@context":"https://schema.org","@type":"Blog","name":"onlinefdr.com.au Blog","url":"https://onlinefdr.com.au/blog/","publisher":{"@type":"Organization","name":"onlinefdr.com.au","url":"https://onlinefdr.com.au/"}}'

    return shell(
        title=title,
        meta_desc=meta_desc,
        canonical=canonical,
        schema_json=schema,
        page_html=page_html,
    )


def render_post_page(post):
    """Render a single blog post page."""
    cat = post["category"]
    cat_slug = CATEGORY_SLUGS[cat]
    title_safe = html.escape(post["title"])
    canonical = f"/blog/{post['slug']}/"

    # Hero image block
    if post.get("hero_image"):
        hero_block = f"""<div class="post-hero-image">
  <div class="post-hero-image-inner">
    <img src="/blog/images/{post['hero_image']}" alt="{title_safe}">
  </div>
</div>"""
    else:
        hero_block = f"""<div class="post-hero-image">
  <div class="post-hero-image-inner">
    <div class="post-hero-placeholder">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      <span>Hero image pending</span>
    </div>
  </div>
</div>"""

    # Related pages
    related_html = "".join(
        f'<a href="{p}" class="post-related-link">{PAGE_LABELS.get(p, p)}<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>'
        for p in post["related_pages"]
    )

    # TLDR block (only if frontmatter provides one)
    if post.get("tldr"):
        tldr_safe = html.escape(post["tldr"])
        tldr_block = f"""  <aside class="post-tldr" aria-label="Summary">
    <div class="post-tldr-inner">
      <span class="post-tldr-label">In short</span>
      <p class="post-tldr-text">{tldr_safe}</p>
    </div>
  </aside>
"""
    else:
        tldr_block = ""

    page_html = f"""<header class="post-header">
  <div class="post-header-inner">
    <a href="/blog/category/{cat_slug}/" class="post-cat-pill">{cat}</a>
    <h1>{title_safe}</h1>
    <div class="post-meta">
      <span>{fmt_date(post['date'])}</span>
      <span class="post-meta-sep">·</span>
      <span>{post['reading_time']} min read</span>
    </div>
  </div>
</header>

{hero_block}

<section class="post-body-wrap">
{tldr_block}  <article class="post-body">
{post['body_html']}
  </article>

  <aside class="post-related" aria-label="Related">
    <div class="post-related-inner">
      <h3>Related</h3>
      <div class="post-related-links">
{related_html}
      </div>
    </div>
  </aside>

  <aside class="post-cta">
    <div class="post-cta-inner">
      <h3>Have a question about your situation?</h3>
      <p>Book a free discovery call. No obligation, no pressure, just a chance to ask whether Family Dispute Resolution is the right path for you.</p>
      <a href="/book/" class="btn">Book a discovery call <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
    </div>
  </aside>
</section>"""

    # BlogPosting schema. Build as a dict and json.dumps it so all string
    # values (title, description) are correctly JSON-escaped. Using xml_escape
    # here was a bug: it does not escape the double-quotes that JSON requires,
    # so a title containing " produced invalid JSON-LD (Search Console parsing
    # error "Missing ',' or '}'").
    iso_date = post["date"].isoformat()
    schema_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["meta_description"],
        "datePublished": iso_date,
        "dateModified": iso_date,
        "author": {"@type": "Organization", "name": "onlinefdr.com.au", "url": "https://onlinefdr.com.au/"},
        "publisher": {"@type": "Organization", "name": "onlinefdr.com.au", "url": "https://onlinefdr.com.au/", "logo": {"@type": "ImageObject", "url": "https://onlinefdr.com.au/images/og-default.jpg"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://onlinefdr.com.au{canonical}"},
        "articleSection": cat,
    }
    schema = json.dumps(schema_obj, ensure_ascii=False, separators=(",", ":"))

    return shell(
        title=f"{post['title']} · onlinefdr.com.au",
        meta_desc=post["meta_description"],
        canonical=canonical,
        schema_json=schema,
        page_html=page_html,
        show_marquee=False,
    )


# ─────────────────────────────────────────────────────────────────
# SITEMAP
# ─────────────────────────────────────────────────────────────────

def update_sitemap(posts):
    """Rewrite sitemap.xml to include /blog/, category pages, and posts."""
    static_entries = [
        ("/", "1.0"),
        ("/about/", "0.8"),
        ("/what-is-fdr/", "0.8"),
        ("/how-it-works/", "0.8"),
        ("/parenting/", "0.9"),
        ("/financial-settlement/", "0.9"),
        ("/section-60i/", "0.9"),
        ("/faq/", "0.7"),
        ("/locations/", "0.7"),
        ("/book/", "0.9"),
        ("/get-help/", "0.6"),
        # Noindex pages (join-the-team, privacy, terms, complaints) intentionally excluded from the sitemap
    ]

    today = datetime.now().date().isoformat()

    urls = []
    for path, priority in static_entries:
        urls.append(f"""  <url>
    <loc>https://onlinefdr.com.au{path}</loc>
    <lastmod>{today}</lastmod>
    <priority>{priority}</priority>
  </url>""")

    # Blog index
    urls.append(f"""  <url>
    <loc>https://onlinefdr.com.au/blog/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.8</priority>
  </url>""")

    # Category pages
    for cat in CATEGORIES:
        slug = CATEGORY_SLUGS[cat]
        urls.append(f"""  <url>
    <loc>https://onlinefdr.com.au/blog/category/{slug}/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.6</priority>
  </url>""")

    # Posts
    for post in posts:
        urls.append(f"""  <url>
    <loc>https://onlinefdr.com.au/blog/{post['slug']}/</loc>
    <lastmod>{post['date'].isoformat()}</lastmod>
    <priority>0.7</priority>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    with open(SITEMAP_PATH, "w") as f:
        f.write(xml)
    print(f"  Sitemap rebuilt: {len(static_entries) + 1 + len(CATEGORIES) + len(posts)} URLs")


# ─────────────────────────────────────────────────────────────────
# BUILD ORCHESTRATION
# ─────────────────────────────────────────────────────────────────

def write_page(html_content, *path_parts):
    """Write content to /site/blog/<path_parts>/index.html, creating dirs."""
    target_dir = OUT_DIR
    for part in path_parts:
        target_dir = target_dir / part
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "index.html"
    with open(target, "w") as f:
        f.write(html_content)
    rel = target.relative_to(SITE_ROOT)
    print(f"  Wrote {rel}")


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def build():
    print("Loading posts...")
    posts = load_all_posts()
    print(f"  {len(posts)} post(s) loaded")

    # ── Blog index (paginated) ──
    print("\nBuilding blog index...")
    if not posts:
        # Render empty state at /blog/
        html_out = render_index_page([], page_num=1, total_pages=1)
        write_page(html_out)
    else:
        chunks = list(chunk(posts, POSTS_PER_PAGE))
        total = len(chunks)
        for i, page_posts in enumerate(chunks, start=1):
            html_out = render_index_page(page_posts, page_num=i, total_pages=total)
            if i == 1:
                write_page(html_out)
            else:
                write_page(html_out, "page", str(i))

    # ── Category pages (paginated) ──
    print("\nBuilding category pages...")
    for cat in CATEGORIES:
        cat_posts = [p for p in posts if p["category"] == cat]
        slug = CATEGORY_SLUGS[cat]
        if not cat_posts:
            html_out = render_index_page([], page_num=1, total_pages=1, active_category=cat)
            write_page(html_out, "category", slug)
            continue
        chunks = list(chunk(cat_posts, POSTS_PER_PAGE))
        total = len(chunks)
        for i, page_posts in enumerate(chunks, start=1):
            html_out = render_index_page(
                page_posts, page_num=i, total_pages=total, active_category=cat
            )
            if i == 1:
                write_page(html_out, "category", slug)
            else:
                write_page(html_out, "category", slug, "page", str(i))

    # ── Individual posts ──
    print("\nBuilding post pages...")
    for post in posts:
        html_out = render_post_page(post)
        write_page(html_out, post["slug"])

    # ── Sitemap ──
    print("\nUpdating sitemap.xml...")
    update_sitemap(posts)

    print("\nDone.")


if __name__ == "__main__":
    build()
