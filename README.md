# waterfiltersoftenercombo.com

Static affiliate site. Python generator (`build.py`) -> `public/` -> Vercel via GitHub.

## Structure
- `build.py` — generator: wraps `content/*.html` fragments in the shared header/nav/footer shell, copies `static/`, writes `robots.txt` + `sitemap.xml`.
- `content/` — page bodies only (no <head>, no header/footer).
- `static/` — styles.css, logo.svg, favicon.svg, favicon.ico, author-kelly.svg.
- `vercel.json` — cleanUrls, trailing slashes, buildCommand, and the cloaked `/go/*` affiliate redirects (302, permanent:false).

## Deploy (GitHub -> Vercel)
1. `git init && git add -A && git commit -m "Initial site: flagship combo review + core pages"`
2. Create the GitHub repo: `gh repo create waterfiltersoftenercombo --private --source=. --push`
   (or create empty repo on github.com, then `git remote add origin ... && git push -u origin main`)
3. In Vercel: **Add New Project -> Import** the repo. Framework preset: **Other**.
   Build command and output dir are already in `vercel.json` (`python3 build.py` -> `public`).
4. Add the domain `waterfiltersoftenercombo.com` in Vercel -> Project -> Settings -> Domains, and point the domain's DNS (A record 76.76.21.21 or the CNAME Vercel shows you).

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
