# Cursor Task: Restore lost ranking pages, redirect the rest, add a Guides hub

**Why:** The WordPress-to-static rebuild dropped ~60 old pages. Search Console (export 2026-10-24) shows 42 URLs as "Not found (404)" and 9 as "Discovered – currently not indexed", and more 404s are coming: Google still lists 97 pages as indexed, but the live site only has 10 real pages. This task restores the strong pages from the static snapshot that already exists, 301-redirects the rest, and adds a `/guides/` hub so Google can find everything.

**How to use:** This file lives in the project root (`troy condo garages website- Gavin`). In Cursor Agent, send:

> Follow @CURSOR_RESTORE_PAGES_TASK.md exactly. Do Part 0 and show me the report before editing anything.

---

## Facts (already verified, don't re-investigate)
- **Live site source:** `site/` in THIS project. It is linked to Vercel project `troy-condo-garages` (`site/.vercel/project.json`) and deployed from `site/` with the Vercel CLI. The redirect file is **`site/vercel.json`** (it already has `cleanUrls: true`, `trailingSlash: true` and a `headers` block; keep all of those).
- **Old content source:** a fully rendered static snapshot of the old WordPress site at
  `C:\Users\rohla\repos\Troy-Condo-Garages-\public\<slug>\index.html`
  with images under `C:\Users\rohla\repos\Troy-Condo-Garages-\public\wp-content\uploads\`.
  Use this snapshot, not `wordpress-backup/` or the SQL dump.
- Every snapshot page contains the OLD phone/email and must be cleaned (rules below).
- Live pages today (keep, don't touch except the footer link in Part 3): `/`, `/units/`, `/design-your-space/`, `/gallery/`, `/events/`, `/rentals/`, `/about/`, `/contact/`, `/financing/`, `/pricing/`, `/thank-you/` (noindex, correct).

## Rules for the agent
- Official contact info on every page: **(651) 247-8384** as `tel:6512478384`, **troycondogaragesbyvalmark@gmail.com**, **663 Valerie Ave, Hudson, WI 54016**.
- Never output `(715) 567-5456`, `715-567-5456`, `info@troycondogarages.com`, or ZIP `54022`. Replace them in restored content.
- Never change the financing partner numbers: `715-926-4234`, `800-896-1788`.
- Don't edit `js/call-tracking.js` or any embedded LeadConnector form.
- Restored pages keep their **exact original slug**, built as `site/<slug>.html` so they serve at `https://troycondogarages.com/<slug>/` (cleanUrls + trailingSlash).
- Build every restored page on the current `site/` template: same `<head>` scripts in the same order (Google tag `AW-18398757431`, `/js/analytics.js`, `/js/call-tracking.js`, `/js/nav.js`), same header, nav, footer and CSS. Drop all Elementor/WordPress CSS, JS, comments, widgets, shortcodes, sidebars and "related posts" blocks.
- Before you start editing, commit the current working tree (`git add -A && git commit -m "Snapshot before page restore"`). Right now the live site exists only as uncommitted changes.

---

## Part 0: Inventory (no edits)
1. Confirm every slug in the Part 1 list exists in the snapshot and report its word count. Flag any missing slug.
2. Confirm that none of the Part 1 slugs already exists in `site/`.
3. List the `/wp-content/uploads/...` images (only images, not CSS) that the Part 1 pages reference.
4. Report, then **wait for my OK**.

---

## Part 1: Restore these 46 pages from the snapshot

For each page:
1. Keep the original `<title>`, meta description, single H1, headings, body text and content images. Copy each referenced image into `site/wp-content/uploads/` at the **same path**, so the image URLs don't change.
2. Fix contact info and the address per the rules, and remove WordPress leftovers.
3. Repoint internal links: a link to a restored page stays; a link to a redirected URL goes straight to that URL's final destination from Part 2; anything else goes to the closest live page. No link may point at a 404 or a redirect.
4. Add `<link rel="canonical" href="https://troycondogarages.com/<slug>/">` and remove any old canonical, `noindex`, or Yoast/RankMath meta.
5. At the end of the content, add a "Book a tour" button linking to `/#lead-form`, plus a "More guides" line linking to `/guides/` and to 2–3 related restored pages from the same group.
6. Pages marked **[$]** contain prices, fees, rates, taxes or returns. Restore them, but list every dollar amount, percentage and rate they contain in your final report so I can confirm or correct each one. Don't invent or update numbers yourself.

**A. Priority: these held the rankings (13)**
```
garage-condo-climate-control
garage-condos-for-sale-near-twin-cities-minnesota
garage-condo-mezzanine-ideas
blog-garage-condo-vs-storage-unit
blog-what-is-a-garage-condo
car-condo-vs-garage-condo-difference
garage-condos-near-stillwater-mn
st-croix-falls
river-falls
new-richmond-wi
man-cave-garage-wisconsin
enclosed-trailer-storage-hudson-wi
condos
```

**B. From the Search Console 404 / Discovered lists (12)**
```
garage-condos-near-woodbury-lake-elmo-mn
car-lift-installation-garage-condo-hudson-wi
classic-car-storage-near-hudson-wi
snowmobile-atv-storage-hudson-wi
can-you-live-in-a-garage-condo-wisconsin-zoning-rules
hoa-fees-troy-condo-garages-hudson-wi            [$]
baldwin
prescott
jet-ski-watercraft-storage-hudson-wi
toy-hauler-camper-van-storage-hudson-wi
why-car-collectors-contractors-choose-garage-condo-ownership
5-ways-to-transform-your-troy-condo-garage-into-a-private-workshop
```

**C. Strong content still in Google's index that will 404 next (17)**
```
boat-storage-hudson-wi
rv-storage-hudson-wi
motorcycle-storage-hudson-wi
home-gym-garage-condo-hudson-wi
epoxy-garage-floor-coating-hudson-wi
garage-condo-small-business-storage-hudson-wi
garage-condo-buying-process
garage-condo-insurance-wisconsin
garage-condo-investment-wisconsin
garage-condo-ownership-vs-401k-building-equity   [$]
garage-condo-property-taxes-st-croix-county      [$]
garage-condo-resale-value                        [$]
garage-condo-vs-pole-barn
garage-condo-vs-renting-commercial-warehouse-space-hudson-wi
best-garage-condo-communities-near-hudson-wi-western-wisconsin
how-much-does-a-garage-condo-cost-in-wisconsin   [$]
garage-condo-financing-hudson-wi                 [$]
```

**D. Legal / owner pages (4).** The Google Ads and lead forms need the legal pages.
```
privacy-policy
terms-of-service
accessibility-statement
documents        (HOA documents. Build it as site/documents/index.html, NOT documents.html,
                  and copy its 5 PDFs to site/documents/legal/: original-declaration.pdf,
                  1st-amendment.pdf, 2nd-amendment.pdf, 3rd-amendment.pdf, 4th-amendment.pdf)
```

**Merges:** while restoring `blog-what-is-a-garage-condo` and `blog-garage-condo-vs-storage-unit`, check `ultimate-guide-to-premium-garage-condos` and `garage-condo-vs-storage-unit-hudson-wi`. Move any section that isn't already covered into the restored page, under its own H2. Those two old URLs get redirected in Part 2.

---

## Part 2: 301 redirects in `site/vercel.json`

Add a `"redirects"` array. Use `"statusCode": 301` on every entry (not `"permanent": true`, which sends a 308). Put the exact entries first and the patterns last. Sources and destinations use trailing slashes, exactly as written here.

**Exact redirects**
| Old path | → New path | Why |
|---|---|---|
| `/ultimate-guide-to-premium-garage-condos/` | `/blog-what-is-a-garage-condo/` | merged duplicate |
| `/garage-condo-vs-storage-unit-hudson-wi/` | `/blog-garage-condo-vs-storage-unit/` | merged duplicate |
| `/hoa-fees-troy-condo-garage-hudson-wi/` | `/hoa-fees-troy-condo-garages-hudson-wi/` | GSC 404 (singular slug) |
| `/boat-rv-storage/` | `/boat-storage-hudson-wi/` | GSC 404 |
| `/workshop-man-cave/` | `/man-cave-garage-wisconsin/` | GSC 404 |
| `/car-storage-collector-storage/` | `/classic-car-storage-near-hudson-wi/` | GSC 404 |
| `/garage-condo-tax-benefits-section-179-wisconsin/` | `/garage-condo-investment-wisconsin/` | GSC 404; snapshot only 161 words |
| `/real-estate-investment-angle/` | `/garage-condo-investment-wisconsin/` | GSC 404 |
| `/own-vs-rent/` | `/pricing/` | GSC 404 |
| `/garage-condo/` | `/blog-what-is-a-garage-condo/` | GSC 404 |
| `/location-based/` | `/` | GSC 404 |
| `/troy-condo-garages-inquiry/` | `/contact/` | GSC "Page with redirect", now 404 |
| `/6512478384/` | `/contact/` | old broken phone link |
| `/info@troycondogarages.com/` | `/contact/` | old broken email link |
| `/faq/` | `/` | FAQ now lives on the homepage |
| `/condo-garages-hudson-wi/` | `/` | would compete with the homepage |
| `/garage-condos-for-sale-hudson-wi-pricing-size/` | `/pricing/` | would compete with /pricing/ |
| `/garage-condo-financing-rates-2027/` | `/garage-condo-financing-hudson-wi/` | stale rates |
| `/financing-options/` | `/financing/` | replaced |
| `/phase-iii-at-troy-condo-garages-whats-new-for-buyers/` | `/units/` | dated news |
| `/open-house/` | `/events/` | dated event |
| `/open-house-car-show/` | `/events/` | dated event |
| `/eau-claire/` | `/` | outside service area |
| `/chippewa-falls/` | `/` | outside service area |
| `/menomonie/` | `/` | outside service area |
| `/la-crosse/` | `/` | removed from service area |

**Pattern redirects (last, in this order)**
| Source | → Destination |
|---|---|
| `/:path*/feed` | `/` (covers `/feed/`, `/comments/feed/`, and every `/tag/…/feed/` and `/category/…/feed/`) |
| `/tag/:path*` | `/` |
| `/category/:path*` | `/` |
| `/author/:path*` | `/` |

Leave `/wp-content/*`, `/wp-admin/*` and `/wp-includes/*` alone (404/403 is correct for those). No redirect may point to another redirect, and no redirect may have a restored or live page as its source.

---

## Part 3: Guides hub and internal links
1. Create `site/guides.html`, served at `/guides/`. Title: `Garage Condo Guides for Hudson, WI & the Twin Cities | Troy Condo Garages`. Give it one H1 ("Garage Condo Guides"), a short intro, and every page from groups A–C linked under these H2s: **Buying & Costs**, **Storage Uses**, **Build-Out & Design**, **Nearby Areas**. Add a canonical tag and the "Book a tour" button.
2. Add **Guides** (`/guides/`), **HOA Documents** (`/documents/`), **Privacy Policy** (`/privacy-policy/`) and **Terms** (`/terms-of-service/`) links to the footer of every page in `site/`: the 11 live pages, all restored pages, and the guides page itself. The current footer has none of them.
3. On the homepage, add one sentence under the FAQ section: "More answers in our [garage condo guides](/guides/)." Change nothing else on the homepage.

---

## Part 4: Sitemap
Rewrite `site/sitemap.xml` to list: the 10 current URLs, `/guides/`, and every page restored in Part 1 (except `/documents/`). That's 56 URLs, all with trailing slashes. Don't include `/thank-you/` or any redirected URL. Set `<lastmod>` to today.

---

## Part 5: Final check (run `vercel dev` from `site/`; a plain static server won't apply the redirects)
1. Show the diff summary.
2. Each restored page and `/guides/` returns 200 and has exactly one `<h1>`, one canonical tag that matches its URL, `tel:6512478384`, the official email, and `663 Valerie Ave, Hudson, WI 54016`.
3. Every exact redirect returns **301** straight to a page that returns 200 (one hop). Also spot-check `/tag/hudson-wi/`, `/category/rv-storage/`, `/tag/home-gym/feed/` and `/comments/feed/`. Show this as a table: old path → status → new path → final status.
4. `sitemap.xml` is valid XML, has 56 URLs, and every URL returns 200.
5. A search of `site/` finds no `715-567-5456`, `(715) 567-5456`, `info@troycondogarages.com`, `54022`, `elementor` or `wp-json`.
6. List every **[$]** number found (page → figure), so I can check them.
7. `js/call-tracking.js` is unchanged (`git diff --stat` shows no change to it).
8. Commit: `git add -A && git commit -m "Restore 46 legacy pages, add 301s, guides hub, sitemap"`.

**Don't deploy.** Austin publishes.
