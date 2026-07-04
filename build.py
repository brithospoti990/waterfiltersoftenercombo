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
        "ogimage": '\n<meta property="og:image" content="https://waterfiltersoftenercombo.com/springwell-water-filter-softener-combo-installed.jpg">\n<meta property="og:image:width" content="700">\n<meta property="og:image:height" content="500">\n<meta name="twitter:card" content="summary_large_image">',
    },
    "well-water-combo": {
        "out": "best-well-water-filter-and-softener-combo/index.html",
        "title": "Best Well Water Filter & Softener Combo (2026): Tested",
        "desc": "The best whole house water filter and softener combo for well water, tested 12 months: 5.4 ppm iron and 22 gpg hardness down to zero. See the data.",
        "nav": "reviews",
        "canonical": "/best-well-water-filter-and-softener-combo/",
    },
    "city-water-system": {
        "out": "best-water-softener-and-filtration-system-for-city-water/index.html",
        "title": "Best Water Softener & Filtration System for City Water 2026",
        "desc": "I run a softener + filter combo on 19 gpg chloraminated Mesa city water. How to pick the best system for your city's water - sized, priced, tested.",
        "nav": None,
        "canonical": "/best-water-softener-and-filtration-system-for-city-water/",
    },
    "combo-vs-separate": {
        "out": "water-filter-and-softener-combo-vs-separate-units/index.html",
        "title": "Combo vs Separate Water Softener & Filter: 2026 Price Math",
        "desc": "I priced both paths on my own house: the combo saved about $700 vs separate units and a second install fee. The full 10-year math, line by line.",
        "nav": None,
        "canonical": "/water-filter-and-softener-combo-vs-separate-units/",
    },
    "springwell-vs-aquasana": {
        "out": "springwell-vs-aquasana/index.html",
        "title": "SpringWell vs Aquasana (2026): I Own One, Inspected Both",
        "desc": "One truly softens, one conditions scale - not the same machine. My owner's verdict on SpringWell vs Aquasana for genuinely hard water, with the math.",
        "nav": None,
        "canonical": "/springwell-vs-aquasana/",
    },
    "springwell-vs-softpro": {
        "out": "springwell-vs-softpro/index.html",
        "title": "SpringWell vs SoftPro (2026): I Priced Both, Bought One",
        "desc": "I audited SoftPro's 75% salt-savings math against SpringWell's metered head - the real gap is a few bags a year. My refereed verdict, numbers shown.",
        "nav": None,
        "canonical": "/springwell-vs-softpro/",
    },
    "need-both-filter-softener": {
        "out": "water-filter-and-softener-do-you-need-both/index.html",
        "title": "Do You Need Both a Water Filter and Softener? (2026)",
        "desc": "A 4-question check tells you if you need a filter, a softener, both - or neither. From a Mesa homeowner who needed both. No sales pitch.",
        "nav": None,
        "canonical": "/water-filter-and-softener-do-you-need-both/",
    },
    "whole-house-framework": {
        "out": "whole-house-water-softener-and-filtration-system/index.html",
        "title": "Whole House Water Softener & Filtration System: 2026 Guide",
        "desc": "The 7-pillar framework I used to pick my whole-house softener + filter - sizing math, the combo flow-rate trap, and the certification truth.",
        "nav": None,
        "canonical": "/whole-house-water-softener-and-filtration-system/",
    },
    "consumer-reports-intercept": {
        "out": "best-whole-house-water-softener-consumer-reports/index.html",
        "title": "Water Softener Consumer Reports: What CR Actually Says",
        "desc": "Consumer Reports has never rated whole-house softeners. Here's what CR really published - plus a comparison built only from verifiable data.",
        "nav": None,
        "canonical": "/best-whole-house-water-softener-consumer-reports/",
    },
    "2in1-vs-two-tank": {
        "out": "2-in-1-vs-two-tank-water-softener-filter/index.html",
        "title": "2-in-1 vs Two-Tank Water Softener & Filter: Which Fits?",
        "desc": "One tank or two? The real tradeoffs - space, capacity ceilings, and maintenance schedules - from a homeowner who measured for both.",
        "nav": None,
        "canonical": "/2-in-1-vs-two-tank-water-softener-filter/",
    },
    "best-salt-based-water-softener": {
        "out": "best-salt-based-water-softener/index.html",
        "title": "Best Salt-Based Water Softener (2026): Tested at 19 GPG",
        "desc": "I run a salt-based softener on 19 gpg Mesa water. The 2026 picks that survive real ownership - sizing math, salt costs, honest Fleck credit.",
        "nav": None,
        "canonical": "/best-salt-based-water-softener/",
    },
    "salt-based-vs-salt-free": {
        "out": "salt-based-vs-salt-free-water-softener/index.html",
        "title": "Salt-Based vs Salt-Free Water Softener: The Honest Answer",
        "desc": "Salt-based vs salt-free water softeners: one of these isn't really a softener. I've run both - here's which fixes your house, honestly.",
        "nav": None,
        "canonical": "/salt-based-vs-salt-free-water-softener/",
    },
    "what-size-water-softener": {
        "out": "what-size-water-softener-do-i-need/index.html",
        "title": "What Size Water Softener Do I Need? Free 2026 Calculator",
        "desc": "What size water softener do you need? Free iron-adjusted calculator plus the salt-efficient sizing truth sellers skip. Answer in 30 seconds.",
        "nav": None,
        "canonical": "/what-size-water-softener-do-i-need/",
    },
    "how-does-a-water-softener-work": {
        "out": "how-does-a-water-softener-work/index.html",
        "title": "How Does a Water Softener Work? Explained Simply (2026)",
        "desc": "How does a water softener work? Ion exchange explained simply by an owner - with a step-through animation of what happens inside the tank.",
        "nav": None,
        "canonical": "/how-does-a-water-softener-work/",
    },
    "water-softener-salt-usage": {
        "out": "water-softener-salt-usage/index.html",
        "title": "How Much Salt Does a Water Softener Use Per Month? (2026)",
        "desc": "How much salt does a water softener really use? My Mesa logs say half a bag to 3 bags a month - and one setting can nearly halve yours.",
        "nav": None,
        "canonical": "/water-softener-salt-usage/",
    },
    "water-softener-regeneration": {
        "out": "water-softener-regeneration/index.html",
        "title": "Water Softener Regeneration: How Often Is Normal? (2026)",
        "desc": "Water softener regeneration explained: the healthy 5-10 day window, why nightly cycles mean trouble, and the fixes that usually cost nothing.",
        "nav": None,
        "canonical": "/water-softener-regeneration/",
    },
    "is-softened-water-safe-to-drink": {
        "out": "is-softened-water-safe-to-drink/index.html",
        "title": "Is Softened Water Safe to Drink? The Sodium Math (2026)",
        "desc": "Is softened water safe to drink? For most people, yes. The exact sodium math per glass, plus the honest exceptions: infants and low-sodium diets.",
        "nav": None,
        "canonical": "/is-softened-water-safe-to-drink/",
    },
    "water-softener-maintenance": {
        "out": "water-softener-maintenance/index.html",
        "title": "Water Softener Maintenance: The Realistic 2026 Checklist",
        "desc": "Water softener maintenance, minus the myths: the monthly, quarterly, and annual checklist with real times and costs - printable, from a heavy-use owner.",
        "nav": None,
        "canonical": "/water-softener-maintenance/",
    },
    "water-softener-failing-signs": {
        "out": "water-softener-failing-signs/index.html",
        "title": "7 Signs Your Water Softener Is Failing (& the $0 Fixes)",
        "desc": "Is your water softener failing? The 7 signs with 60-second confirmation tests, cheapest-first fixes (most are $0), and honest repair-vs-replace math.",
        "nav": None,
        "canonical": "/water-softener-failing-signs/",
    },
    "water-softener-cost": {
        "out": "water-softener-cost/index.html",
        "title": "Water Softener Cost (2026): Install & Real 10-Year Math",
        "desc": "Water softener cost, disaggregated: why quotes run $400 to $6,000, real install pricing, and the 10-year ownership table the averages hide.",
        "nav": None,
        "canonical": "/water-softener-cost/",
    },
    "what-does-carbon-filter-remove": {
        "out": "what-does-carbon-filter-remove/index.html",
        "title": "What Does a Carbon Filter Actually Remove? (& What It Can't)",
        "desc": "What a whole-house carbon filter actually removes - with numbers - and what it can't: hardness, lead, bacteria. Plus the chloramine catch most guides skip.",
        "nav": None,
        "canonical": "/what-does-carbon-filter-remove/",
    },
    "catalytic-vs-standard-carbon": {
        "out": "catalytic-vs-standard-carbon/index.html",
        "title": "Catalytic Carbon vs GAC: Worth It? The 5-Minute Check",
        "desc": "Catalytic carbon vs standard GAC: real chemistry or upsell adjective? The honest split, the cost math, and the 5-minute check that decides it.",
        "nav": None,
        "canonical": "/catalytic-vs-standard-carbon/",
    },
    "water-filter-micron-rating": {
        "out": "water-filter-micron-rating/index.html",
        "title": "Water Filter Micron Ratings Explained (Smaller Isn't Better)",
        "desc": "Water filter micron ratings explained: what the numbers mean, the nominal-vs-absolute trick, and why smaller isn't better for your water.",
        "nav": None,
        "canonical": "/water-filter-micron-rating/",
    },
    "water-filter-pressure-drop": {
        "out": "water-filter-pressure-drop/index.html",
        "title": "Do Whole House Filters Reduce Water Pressure? (Real Numbers)",
        "desc": "Do whole house filters reduce water pressure? Yes - about 2-3 PSI sized right, unnoticeable. The psi-vs-GPM truth plus a pressure diagnosis tree.",
        "nav": None,
        "canonical": "/water-filter-pressure-drop/",
    },
    "how-long-do-whole-house-filters-last": {
        "out": "how-long-do-whole-house-filters-last/index.html",
        "title": "How Long Do Whole House Water Filters Last? (Real Math)",
        "desc": "How long do whole house water filters last? Cartridges 3-6 months, tank media 6-10 years - plus the math to find YOUR real number.",
        "nav": None,
        "canonical": "/how-long-do-whole-house-filters-last/",
    },
    "sediment-pre-filter": {
        "out": "sediment-pre-filter/index.html",
        "title": "Sediment Pre-Filter: Do You Actually Need One?",
        "desc": "Do you need a sediment pre-filter? Gritty water yes, protected systems check first, clean city water often no. Plus spin-down vs cartridge and placement.",
        "nav": None,
        "canonical": "/sediment-pre-filter/",
    },
    "whole-house-water-filter-installation": {
        "out": "whole-house-water-filter-installation/index.html",
        "title": "Whole House Water Filter Installation: DIY Guide (2026)",
        "desc": "Whole house water filter installation, DIY: most homeowners can do it in an afternoon with push-fit fittings. Triage, parts list, steps, and mistakes.",
        "nav": None,
        "canonical": "/whole-house-water-filter-installation/",
    },
    "well-water-treatment-system": {
        "out": "well-water-treatment-system/index.html",
        "title": "Well Water Treatment System: The Complete Guide (2026)",
        "desc": "Well water treatment done right: test first, then build the train - sediment, iron/sulfur, pH, softening, disinfection. Diagnostic-first, by a well owner.",
        "nav": None,
        "canonical": "/well-water-treatment-system/",
    },
    "best-iron-filter-well-water": {
        "out": "best-iron-filter-well-water/index.html",
        "title": "Best Iron Filter for Well Water (2026): Sort Then Rank",
        "desc": "Best iron filter for well water depends on your iron type: air injection for clear-water iron, a softener for low iron, or chemical injection.",
        "nav": None,
        "canonical": "/best-iron-filter-well-water/",
    },
    "well-water-vs-city-water": {
        "out": "well-water-vs-city-water/index.html",
        "title": "Well Water vs City Water: The Treatment Differences",
        "desc": "Well water vs city water by the owner of both: the responsibility inversion, added-vs-native contaminants, two treatment stacks, and the cost truth.",
        "nav": None,
        "canonical": "/well-water-vs-city-water/",
    },
    "how-to-test-well-water": {
        "out": "how-to-test-well-water/index.html",
        "title": "How to Test Well Water (& What to Test For): 2026 Guide",
        "desc": "How to test well water: the annual panel, the kit-vs-lab-vs-free honesty, and the sampling manual that keeps a bad sample from ruining a good test.",
        "nav": None,
        "canonical": "/how-to-test-well-water/",
    },
    "iron-in-well-water": {
        "out": "iron-in-well-water/index.html",
        "title": "Iron in Well Water: Ferrous vs Ferric vs Bacterial (2026)",
        "desc": "The 3 types of iron in well water - ferrous, ferric, and iron bacteria - and the at-home glass test to identify which you have before you buy treatment.",
        "nav": None,
        "canonical": "/iron-in-well-water/",
    },
    "sulfur-smell-well-water": {
        "out": "sulfur-smell-well-water/index.html",
        "title": "Rotten Egg Smell in Well Water: Causes & Fixes (2026)",
        "desc": "Rotten egg smell in well water: the source fork - hot-only means your anode rod ($40 fix), both hot and cold means the well. Diagnose before you spend.",
        "nav": None,
        "canonical": "/sulfur-smell-well-water/",
    },
    "uv-purification-well-water": {
        "out": "uv-purification-well-water/index.html",
        "title": "Do You Need UV Purification for Well Water? (2026)",
        "desc": "Do you need UV for well water? A test-gated triage: essential after a coliform positive, insurance for at-risk wells, optional for deep clean wells.",
        "nav": None,
        "canonical": "/uv-purification-well-water/",
    },
    "well-water-hardness": {
        "out": "well-water-hardness/index.html",
        "title": "Well Water Hardness: Why Wells Run Harder (2026)",
        "desc": "Why well water skews harder than city water (carbonate geology and contact time), how to read your gpg number, and the 5 ways softening a well differs.",
        "nav": None,
        "canonical": "/well-water-hardness/",
    },
    "water-softener-for-well-water": {
        "out": "water-softener-for-well-water/index.html",
        "title": "Can You Use a Regular Softener on Well Water? (2026)",
        "desc": "Can a regular softener work on well water? Yes below ~1 ppm iron; with fine-mesh and cleaner discipline at 1-3 ppm; pretreat first above 3 ppm.",
        "nav": None,
        "canonical": "/water-softener-for-well-water/",
    },
    "signs-of-hard-water": {
        "out": "signs-of-hard-water/index.html",
        "title": "Signs of Hard Water: Spot It, Confirm It, Fix It (2026)",
        "desc": "The signs of hard water - spots, scum, scale, stiff towels, dry skin - each with its mechanism, impostor checks, free tests, and a severity scale.",
        "nav": None,
        "canonical": "/signs-of-hard-water/",
    },
    "water-hardness-by-state": {
        "out": "water-hardness-by-state/index.html",
        "title": "Water Hardness by State: The Honest Map (2026)",
        "desc": "Water hardness by state: an interactive map and sourced table, plus how to find your city's real number from your utility report.",
        "nav": None,
        "canonical": "/water-hardness-by-state/",
    },
    "chlorine-in-tap-water": {
        "out": "chlorine-in-tap-water/index.html",
        "title": "Chlorine & Chloramine in Tap Water: Straight Story (2026)",
        "desc": "Chlorine and chloramine keep tap water safe at regulated levels. The straight story: why they're there, how the two differ, and how to remove them.",
        "nav": None,
        "canonical": "/chlorine-in-tap-water/",
    },
    "water-tastes-bad": {
        "out": "water-tastes-bad/index.html",
        "title": "Why Does My Water Taste Bad? A Diagnosis Guide (2026)",
        "desc": "Why does your water taste bad? A taste-by-taste diagnosis: metallic, pool, egg, earthy, salty, plastic - each named, explained, and routed to a fix.",
        "nav": None,
        "canonical": "/water-tastes-bad/",
    },
    "pfas-in-drinking-water": {
        "out": "pfas-in-drinking-water/index.html",
        "title": "PFAS in Drinking Water: What Homeowners Should Know",
        "desc": "PFAS in drinking water for homeowners: look up your utility's test results, understand the 4 ppt EPA limits, and choose a certified RO or carbon filter.",
        "nav": None,
        "canonical": "/pfas-in-drinking-water/",
    },
    "cloudy-tap-water": {
        "out": "cloudy-tap-water/index.html",
        "title": "Cloudy or Milky Tap Water: The Two-Minute Test (2026)",
        "desc": "Cloudy tap water clearing from the bottom up is harmless air; particles settling downward mean sediment. The two-minute glass test tells you which.",
        "nav": None,
        "canonical": "/cloudy-tap-water/",
    },
    "orange-brown-stains-toilet": {
        "out": "orange-brown-stains-toilet/index.html",
        "title": "Orange & Brown Stains in Toilets: Causes and How to Fix",
        "desc": "Orange toilet stains are iron - clean with oxalic or citric acid, never bleach (it sets them). Pink rings are airborne bacteria, not your water.",
        "nav": None,
        "canonical": "/orange-brown-stains-toilet/",
    },
    "whole-house-water-treatment-cost": {
        "out": "whole-house-water-treatment-cost/index.html",
        "title": "Whole House Water Treatment Cost (2026): Real Numbers",
        "desc": "Whole house water treatment costs $500-8,000 - because it's your water, not the market. A 2026 guide priced by profile, with the honest worth-it math.",
        "nav": None,
        "canonical": "/whole-house-water-treatment-cost/",
    },
    "water-filter-gpm-sizing": {
        "out": "water-filter-gpm-sizing/index.html",
        "title": "Water Filter GPM & Flow Rate: Sizing It Right (2026)",
        "desc": "A filter spec sheet carries three GPM numbers - service, peak, and backwash flow. Which one matters, how to read them, and how to match your demand.",
        "nav": None,
        "canonical": "/water-filter-gpm-sizing/",
    },
    "water-softener-loop": {
        "out": "water-softener-loop/index.html",
        "title": "Water Softener Loop: What It Is & Do You Have One (2026)",
        "desc": "A softener loop is a pre-plumbed copper U or capped stubs on your garage wall - your builder's head start on a system install. Find yours and its worth.",
        "nav": None,
        "canonical": "/water-softener-loop/",
    },
    "water-softener-installation-cost": {
        "out": "water-softener-installation-cost/index.html",
        "title": "Water Softener Installation Cost: DIY vs Pro (2026)",
        "desc": "Water softener installation costs $200-500 on a loop or $500-1,500 for a cut-in. Both invoices anatomized - the pro's line items and the honest DIY ledger.",
        "nav": None,
        "canonical": "/water-softener-installation-cost/",
    },
    "water-system-maintenance-schedule": {
        "out": "water-system-maintenance-schedule/index.html",
        "title": "Water System Maintenance Schedule (Printable, 2026)",
        "desc": "The whole combo-system maintenance calendar on one printable page: a monthly glance, a quarterly quarter-hour, one annual morning - under two hours a year.",
        "nav": None,
        "canonical": "/water-system-maintenance-schedule/",
    },
    "water-softener-home-value": {
        "out": "water-softener-home-value/index.html",
        "title": "Does a Water Softener Add Home Value? Honest Answer (2026)",
        "desc": "A water softener rarely adds appraised value directly. Its real worth - prevented damage, hard-water appeal, cleaner inspections - priced honestly.",
        "nav": None,
        "canonical": "/water-softener-home-value/",
    },
    "winterize-water-softener": {
        "out": "winterize-water-softener/index.html",
        "title": "How to Winterize a Water Softener (Full Guide, 2026)",
        "desc": "Two different jobs: protect-in-place through freeze country, or the full shutdown drain - plus the spring restart everyone forgets and the antifreeze law.",
        "nav": None,
        "canonical": "/winterize-water-softener/",
    },
    "sitemap": {
        "out": "sitemap/index.html",
        "title": "Sitemap - Every Guide | WaterFilterSoftenerCombo.com",
        "desc": "Every guide on the site, organized by topic: the combo question, reviews, softeners, filtration, well water, diagnostics, costs, and care.",
        "nav": None,
        "canonical": "/sitemap/",
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

NAV = [
    ("home", "Home", "/", []),
    ("reviews", "Reviews", "/best-water-softener-and-filtration-system-for-city-water/", [
        ("Best System for City Water", "/best-water-softener-and-filtration-system-for-city-water/"),
        ("Best Well Water Combo", "/best-well-water-filter-and-softener-combo/"),
        ("Best Salt-Based Softener", "/best-salt-based-water-softener/"),
        ("Best Iron Filter (Wells)", "/best-iron-filter-well-water/"),
        ("SpringWell vs Aquasana", "/springwell-vs-aquasana/"),
        ("SpringWell vs SoftPro", "/springwell-vs-softpro/"),
        ("Best Softener \u201cConsumer Reports\u201d", "/best-whole-house-water-softener-consumer-reports/"),
    ]),
    ("softeners", "Softeners", "/how-does-a-water-softener-work/", [
        ("How a Softener Works", "/how-does-a-water-softener-work/"),
        ("What Size Do I Need?", "/what-size-water-softener-do-i-need/"),
        ("Salt-Based vs Salt-Free", "/salt-based-vs-salt-free-water-softener/"),
        ("Water Softener Cost", "/water-softener-cost/"),
        ("Maintenance", "/water-softener-maintenance/"),
        ("Signs It's Failing", "/water-softener-failing-signs/"),
        ("The Softener Loop", "/water-softener-loop/"),
    ]),
    ("filters", "Filters", "/what-does-carbon-filter-remove/", [
        ("What Carbon Removes", "/what-does-carbon-filter-remove/"),
        ("Catalytic vs Standard Carbon", "/catalytic-vs-standard-carbon/"),
        ("Micron Ratings", "/water-filter-micron-rating/"),
        ("GPM & Flow Sizing", "/water-filter-gpm-sizing/"),
        ("How Long Filters Last", "/how-long-do-whole-house-filters-last/"),
        ("The Install Guide", "/whole-house-water-filter-installation/"),
    ]),
    ("well", "Well Water", "/well-water-treatment-system/", [
        ("Well Treatment System (Pillar)", "/well-water-treatment-system/"),
        ("Iron in Well Water", "/iron-in-well-water/"),
        ("Sulfur / Rotten-Egg Smell", "/sulfur-smell-well-water/"),
        ("How to Test Well Water", "/how-to-test-well-water/"),
        ("UV Purification", "/uv-purification-well-water/"),
        ("Softeners on Well Water", "/water-softener-for-well-water/"),
    ]),
    ("guides", "Costs & Care", "/whole-house-water-treatment-cost/", [
        ("Whole House Cost (Pillar)", "/whole-house-water-treatment-cost/"),
        ("Install Cost: DIY vs Pro", "/water-softener-installation-cost/"),
        ("Maintenance Schedule (Printable)", "/water-system-maintenance-schedule/"),
        ("Winterizing Your System", "/winterize-water-softener/"),
        ("Does a Softener Add Home Value?", "/water-softener-home-value/"),
        ("Hardness by State", "/water-hardness-by-state/"),
        ("Water Tastes Bad (Diagnose)", "/water-tastes-bad/"),
    ]),
    ("about", "About", "/about/", []),
]
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
<meta property="og:url" content="{domain}{canonical}">{ogimage}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}styles.css">
</head>
<body>
<header class="site-head">
  <div class="head-inner">
    <a class="brand" href="/">{logo}<span>WaterFilter<b>Softener</b>Combo<span class="tld">.com</span></span></a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle-cb">
    <label for="nav-toggle" class="nav-toggle" aria-label="Open menu"><span></span><span></span><span></span></label>
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
        <li><a href="/sitemap/">Sitemap</a></li>
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
    for key, label, href, children in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if children:
            subs = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in children)
            items.append(
                f'<li class="has-sub"><a href="{href}"{cur}>{label}<span class="caret" aria-hidden="true">&#9662;</span></a>'
                f'<ul class="sub">{subs}</ul></li>'
            )
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "".join(items)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    # static assets -> site root
    for f in STATIC.iterdir():
        shutil.copy2(f, OUT / f.name)
    # XML sitemap + robots.txt (auto-generated from PAGES)
    import datetime
    today = datetime.date.today().isoformat()
    urls = "".join(
        f"  <url><loc>{DOMAIN}{m['canonical']}</loc><lastmod>{today}</lastmod></url>\n"
        for m in PAGES.values()
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    )
    for slug, meta in PAGES.items():
        body = (CONTENT / f"{slug}.html").read_text()
        depth_prefix = "../" * (len(Path(meta["out"]).parts) - 1)
        body = body.replace('src="/author-kelly.jpg"', f'src="{depth_prefix}author-kelly.jpg"')
        page = (
            HEAD.format(
                title=meta["title"], desc=meta["desc"], domain=DOMAIN,
                canonical=meta["canonical"], logo=LOGO_SVG,
                ogimage=meta.get("ogimage", ""),
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
