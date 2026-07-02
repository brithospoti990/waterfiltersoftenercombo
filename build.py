#!/usr/bin/env python3
"""waterfiltersoftenercombo.com static site generator.
Reads content/*.html fragments, wraps them in the site shell, writes to public/.
Usage: python3 build.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "public"

DOMAIN = "https://waterfiltersoftenercombo.com"

# slug -> (output path, <title>, meta description, nav key)
PAGES = {
    "index": {
        "out": "index.html",
        "title": "Best Whole House Water Filter and Softener Combo (2026)",
        "desc": "Searching for the best whole house water softener and filtration system? My 6-month SpringWell combo test: hardness data, real costs, honest verdict.",
        "nav": "home",
        "canonical": "/",
    },
    "about": {
        "out": "about/index.html",
        "title": "About Kelly McClendon | WaterFilterSoftenerCombo.com",
        "desc": "Kelly McClendon founded WaterFilterSoftenerCombo.com after fixing the hard, chlorinated water in his own Mesa, Arizona home. Here's how this site tests and reviews.",
        "nav": "about",
        "canonical": "/about/",
    },
    "contact": {
        "out": "contact/index.html",
        "title": "Contact Us | WaterFilterSoftenerCombo.com",
        "desc": "Questions about water filter and softener combos? Contact Kelly McClendon at WaterFilterSoftenerCombo.com.",
        "nav": "contact",
        "canonical": "/contact/",
    },
    "affiliate-disclosure": {
        "out": "affiliate-disclosure/index.html",
        "title": "Affiliate Disclosure | WaterFilterSoftenerCombo.com",
        "desc": "How WaterFilterSoftenerCombo.com earns commissions and how that does — and doesn't — affect our reviews.",
        "nav": None,
        "canonical": "/affiliate-disclosure/",
    },
    "privacy-policy": {
        "out": "privacy-policy/index.html",
        "title": "Privacy Policy | WaterFilterSoftenerCombo.com",
        "desc": "Privacy policy for WaterFilterSoftenerCombo.com.",
        "nav": None,
        "canonical": "/privacy-policy/",
    },
    "terms-of-service": {
        "out": "terms-of-service/index.html",
        "title": "Terms of Service | WaterFilterSoftenerCombo.com",
        "desc": "Terms of service for WaterFilterSoftenerCombo.com.",
        "nav": None,
        "canonical": "/terms-of-service/",
    },
}

NAV = [("home", "Home", "/"), ("about", "About", "/about/"), ("contact", "Contact", "/contact/")]
# Future silo hubs go here once their pillar pages exist (never link to a 404):
# ("combos", "Combo Reviews", "/best/combo/"), ("softeners", "Water Softeners", "/softeners/"),
# ("filters", "Whole House Filters", "/filters/"), ("well", "Well Water", "/well-water/")

LOGO_SVG = (STATIC / "logo.svg").read_text().replace('width="34" height="34"', 'width="30" height="30"')

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{domain}{canonical}">
<link rel="icon" type="image/svg+xml" href="{rel}favicon.svg">
<link rel="icon" href="{rel}favicon.ico" sizes="48x48">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{domain}{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}styles.css">
</head>
<body>
<header class="site-head">
  <div class="head-inner">
    <a class="brand" href="/">{logo}<span>WaterFilter<b>Softener</b>Combo<span class="tld">.com</span></span></a>
    <nav class="main" aria-label="Main navigation"><ul>{navitems}</ul></nav>
  </div>
</header>
<main>
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="foot-inner">
    <div>
      <div class="foot-brand">{logo_small}<span>WaterFilterSoftenerCombo</span></div>
      <p>Owner-tested guidance on whole-house water filter and softener combos. Real home, real Arizona hard water — not a spec sheet.</p>
    </div>
    <div>
      <h4>Contact</h4>
      <address>
        <strong>Kelly McClendon</strong>, Founder<br>
        4629 Elmwood Avenue<br>
        Mesa, AZ 85205<br>
        <a href="tel:+14804181546">+1 (480) 418-1546</a><br>
        <a href="/contact/">Contact form</a>
      </address>
    </div>
    <div>
      <h4>Site</h4>
      <ul>
        <li><a href="/">Combo Review (Home)</a></li>
        <li><a href="/about/">About Kelly</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-service/">Terms of Service</a></li>
      </ul>
    </div>
  </div>
  <div class="foot-legal">
    <p>Affiliate disclosure: WaterFilterSoftenerCombo.com is reader-supported. When you buy through links on this site, we may earn an affiliate commission at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>
    <p>SpringWell&reg; and all other product names are trademarks of their respective owners. This site is not owned by, operated by, or affiliated with SpringWell Water Filtration Systems.</p>
    <p>&copy; 2026 WaterFilterSoftenerCombo.com. All rights reserved.</p>
  </div>
</footer>
</body>
</html>
"""


def nav_html(active):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "".join(items)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    # static assets -> site root
    for f in STATIC.iterdir():
        shutil.copy2(f, OUT / f.name)
    for slug, meta in PAGES.items():
        body = (CONTENT / f"{slug}.html").read_text()
        depth_prefix = "../" * (len(Path(meta["out"]).parts) - 1)
        body = body.replace('src="/author-kelly.jpg"', f'src="{depth_prefix}author-kelly.jpg"')
        page = (
            HEAD.format(
                title=meta["title"], desc=meta["desc"], domain=DOMAIN,
                canonical=meta["canonical"], logo=LOGO_SVG,
                navitems=nav_html(meta["nav"]),
                rel="../" * (len(Path(meta["out"]).parts) - 1),
            )
            + body
            + FOOT.replace("{logo_small}", LOGO_SVG.replace('width="30" height="30"', 'width="22" height="22"'))
        )
        dest = OUT / meta["out"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
        print(f"built {meta['out']}  ({len(page.split())} words incl. markup)")
    # robots.txt
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    )
    # sitemap.xml
    urls = "".join(
        f"<url><loc>{DOMAIN}{m['canonical']}</loc></url>" for m in PAGES.values()
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>"
    )
    print("built robots.txt, sitemap.xml")


if __name__ == "__main__":
    build()
