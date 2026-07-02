# waterfiltersoftenercombo.com

Static affiliate site. Python generator (`build.py`) -> `public/` -> Vercel via GitHub.

## Structure
- `build.py` — generator: wraps `content/*.html` fragments in the shared header/nav/footer shell, copies `static/`, writes `robots.txt` + `sitemap.xml`.
- `content/` — page bodies only (no <head>, no header/footer).
- `static/` — styles.css, logo.svg, favicon.svg, favicon.ico, author-kelly.svg.
- `vercel.json` — cleanUrls, trailing slashes, buildCommand, and the cloaked `/go/*` affiliate redirects (302, permanent:false).

## Deploy (GitHub -> Vercel) — NO BUILD STEP
The `public/` folder is pre-built and committed. Vercel serves it directly; there is no build command.
**Repo root MUST contain, side by side:** `vercel.json`, `public/`, `build.py`, `content/`, `static/`, `README.md`.
(If `vercel.json` ends up in a subfolder, redirects silently stop working.)

1. On github.com, open the repo -> delete any old/stray files so the root is clean.
2. Upload ALL files and folders from this zip so `vercel.json` and `public/` sit at the TOP LEVEL of the repo (not inside a wrapper folder).
3. Vercel redeploys automatically. In Vercel Project Settings -> Build & Development, make sure Build Command and Output Directory show "vercel.json overrides" / no manual override.

## Editing content later
Edit `content/*.html`, run `python3 build.py` locally (rebuilds `public/`), commit BOTH the source change and the regenerated `public/` files, push.

## Before going live — checklist
- [x] **Affiliate destinations verified.** All 9 `/go/*` redirects use the exact Everflow tracking URLs from `tracking_links.csv` (verified programmatically against the export, 2026-07-02).
- [x] Author headshot in place: `static/author-kelly.jpg` (400x400 progressive JPG, 25 KB).
- [ ] Activate the FormSubmit endpoint: submit the contact form once from the live site and click the confirmation email sent to kelly@waterfiltersoftenercombo.com (create that mailbox/alias first).
- [ ] Add GSC + Bing verification files to `static/` (they'll be copied to site root on build).
- [ ] `robots.txt` disallows `/go/` (keeps redirect URLs out of the index) — no action needed, just FYI.

## Adding articles later
Add a fragment to `content/`, register it in the `PAGES` dict in `build.py`, and add nav/silo links only once the target page exists (never link to a 404). Run `python3 build.py` locally to test.

## Link/oid map (Everflow affid=40)
combo=10, filter(CF)=1, softener(SS)=9, well-combo=5, well iron=3, RO under-sink=34, UV=12, test kit=8, sediment spin-down=13
