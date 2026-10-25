# Cursor Task: Troy Condo Garages homepage SEO and AI-visibility update

**How to use:** Drop this file in the root of the website project. Open Cursor Agent (Cmd/Ctrl+I, Agent mode) and send:

> Follow @CURSOR_HOMEPAGE_TASK.md exactly, Part 0 through Part 7.

**Official contact info (use everywhere):**
- Phone: **(651) 247-8384**, written `+1-651-247-8384` in schema and `tel:6512478384` in links (the format the site already uses)
- Email: **troycondogaragesbyvalmark@gmail.com**

---

## Rules for the agent
- Edit **only** what this file lists. Don't restyle, reformat, or "improve" anything else.
- If the homepage is generated from a template, partial, or component, edit the **source** file, not the built output.
- Match each "find" string exactly. If a find string isn't found, **stop and tell me**. Don't guess.
- When finished, show a summary diff of every file changed.

---

## Part 0: Quick scan (no edits)

1. Find the homepage source file and note its path.
2. Search the **whole project** for every phone number and email address. Note each value and the files it appears in.
3. Find the Facebook and Instagram profile URLs used on the Contact page (or anywhere in the project).
4. Note: `/js/call-tracking.js` fires a Google Ads conversion when someone clicks a `tel:` link ending in 6512478384. Don't edit it.

Include these findings in your final summary, then continue.

---

## Part 1: Head tags (homepage)

**1a. Title.** Replace:
```html
<title>Troy Condo Garages | Hudson, WI Garage Storage Solutions</title>
```
with:
```html
<title>Garage Condos for Sale &amp; Rent in Hudson, WI | Troy Condo Garages</title>
```

**1b. Meta description.** Replace:
```html
<meta name="description" content="Premium garage condos for sale and rent in Hudson, WI. Secure, customizable personal-use space near the Twin Cities.">
```
with:
```html
<meta name="description" content="Own a deeded garage condo in Hudson, WI, about 20 min from St. Paul. 1,000–2,400+ sq ft units for cars, RVs, boats and workshops. Buy or rent.">
```

**1c. Schema.** Find the existing `<script type="application/ld+json">` block in the homepage head (it contains `"aggregateRating"`). **Replace the entire block** with the one below.
- The phone and email in the block are already the official ones. Don't change them.
- Add the Instagram URL from Part 0 to `sameAs`, after the Facebook URL. Use only URLs that actually exist in the project.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://troycondogarages.com/#business",
      "name": "Troy Condo Garages",
      "legalName": "Troy Condo Garages LLC by ValMark",
      "url": "https://troycondogarages.com/",
      "logo": "https://troycondogarages.com/assets/293856347_101769785949118_3680151206583370806_n-Edited.png",
      "image": [
        "https://troycondogarages.com/assets/Troy-Condo-Garages-Hudson-WI-aerial-2025.webp",
        "https://troycondogarages.com/assets/hero-unit-418.jpg",
        "https://troycondogarages.com/assets/Troy-Condo-Garages-Hudson-WI-Property.webp"
      ],
      "description": "Garage condominiums for sale and rent in Hudson, Wisconsin, about 20 minutes east of St. Paul. Deeded, all-steel units from 1,000 to 2,400+ sq ft for car collectors, RVs, boats, workshops, private lounges, and by-appointment businesses.",
      "telephone": "+1-651-247-8384",
      "email": "troycondogaragesbyvalmark@gmail.com",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "663 Valerie Ave",
        "addressLocality": "Hudson",
        "addressRegion": "WI",
        "postalCode": "54016",
        "addressCountry": "US"
      },
      "areaServed": [
        "Hudson, WI", "River Falls, WI", "New Richmond, WI", "Baldwin, WI",
        "Prescott, WI", "St. Croix Falls, WI", "Menomonie, WI", "Eau Claire, WI",
        "Woodbury, MN", "Stillwater, MN", "St. Paul, MN", "Minneapolis, MN"
      ],
      "sameAs": [
        "https://www.facebook.com/TroyCondoGaragesbyValMark/"
      ],
      "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "12 ft x 14 ft overhead door with opener", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "All-steel construction", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "In-floor heating", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "Fiber optic internet", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "150 amp breaker box", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "Finished half bath with shower rough-in", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "Gated entry with 24/7 video surveillance", "value": true},
        {"@type": "LocationFeatureSpecification", "name": "60 ft drive aisles", "value": true}
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://troycondogarages.com/#website",
      "url": "https://troycondogarages.com/",
      "name": "Troy Condo Garages",
      "publisher": {"@id": "https://troycondogarages.com/#business"}
    },
    {
      "@type": "WebPage",
      "@id": "https://troycondogarages.com/#webpage",
      "url": "https://troycondogarages.com/",
      "name": "Garage Condos for Sale & Rent in Hudson, WI | Troy Condo Garages",
      "isPartOf": {"@id": "https://troycondogarages.com/#website"},
      "about": {"@id": "https://troycondogarages.com/#business"}
    }
  ]
}
</script>
```
After editing, confirm the JSON parses with no errors (for example with `node -e` or `python -m json.tool` on the extracted block).

---

## Part 2: Hero (homepage)

**2a. Headline.** Replace:
```html
<h1 class="reveal">Garage condos for sale <span class="accent">River Falls, WI</span></h1>
```
with:
```html
<h1 class="reveal">Garage Condos for Sale in <span class="accent">Hudson, WI</span></h1>
```

**2b. Lead sentence.** Replace:
```html
<p class="lead reveal reveal-delay">Private, secure personal-use space for collectors and hobbyists — own your unit as real property, or inquire about available rentals.</p>
```
with:
```html
<p class="lead reveal reveal-delay">Garage condos for sale and rent in Hudson, WI, about 20 minutes east of St. Paul. Own a 1,000–2,400+ sq ft unit for your cars, RV, boat, or workshop.</p>
```

---

## Part 3: Service area list (homepage)

In `<ul class="area-list">`:
- Insert these four lines **directly above** `<li>River Falls</li>`:
```html
<li>Woodbury, MN</li>
<li>Stillwater, MN</li>
<li>St. Paul, MN</li>
<li>Minneapolis, MN</li>
```
- Delete `<li>La Crosse</li>`.

---

## Part 4: FAQ section (homepage)

Insert this **directly above** `<section class="section section-dark" id="lead-form">`. It uses the site's existing classes, so no CSS changes are needed. It uses `section-muted` so the background bands keep alternating after the white location section.

```html
    <section class="section section-muted" id="faq">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">FAQ</p>
          <h2>Garage condo questions, answered</h2>
        </div>
        <h3>What is a garage condo?</h3>
        <p>A garage condo is a garage unit you own as real estate inside a managed complex. You can build it out to your needs and sell it later, unlike a rented storage unit.</p>
        <h3>Where is Troy Condo Garages located?</h3>
        <p>663 Valerie Ave, Hudson, WI 54016, in the St. Croix Valley, about 20 minutes east of St. Paul and close to Woodbury and Stillwater, Minnesota.</p>
        <h3>What unit sizes are available?</h3>
        <p>Unit shells run from about 1,000 to 2,400+ square feet. Standard units are 20 to 25 feet wide by 50 feet deep. Combined units and pull-through options starting at 25 x 100 feet are also available.</p>
        <h3>Can I buy or rent a unit?</h3>
        <p>Both. Units are sold as real property, and select units are available to rent.</p>
        <h3>Can I use a unit year-round?</h3>
        <p>Yes. Units are insulated, all-steel buildings with in-floor heating and HVAC-ready infrastructure for Wisconsin winters.</p>
        <h3>Can I run a business from a garage condo?</h3>
        <p>Yes, by appointment only. Storefront retail and residential occupancy are not permitted.</p>
      </div>
    </section>

```

---

## Part 5: llms.txt (new file)

Create `llms.txt` in the **web root**, the same folder that serves `index.html`, so it loads at `https://troycondogarages.com/llms.txt`.

```text
# Troy Condo Garages

> Troy Condo Garages LLC by ValMark sells and rents garage condominiums in Hudson, Wisconsin (St. Croix Valley), about 20 minutes east of St. Paul. Units are owned as real property and used by car collectors, RV and boat owners, workshops, private lounges, and by-appointment businesses. Non-residential use only.

## Key facts
- Address: 663 Valerie Ave, Hudson, WI 54016
- Phone: (651) 247-8384
- Email: troycondogaragesbyvalmark@gmail.com
- Buy or rent: units are sold as real estate; select units are available to rent
- Unit sizes: 1,000 to 2,400+ sq ft shells; standard 20–25 ft x 50 ft; pull-through from 25 x 100 ft
- Features: 12 x 14 ft overhead door, all-steel construction, in-floor heating, fiber internet, 150-amp panel, half bath with shower rough-in
- Site: gated entry, security fence, 24/7 video surveillance, 60 ft drive aisles
- Not allowed: residential occupancy, storefront retail
- Service area: Hudson, River Falls, New Richmond, Baldwin, Prescott, St. Croix Falls, Menomonie, Eau Claire, Woodbury, Stillwater, St. Paul, Minneapolis

## Pages
- [Available units](https://troycondogarages.com/units/)
- [Pricing](https://troycondogarages.com/pricing/)
- [Rentals](https://troycondogarages.com/rentals/)
- [Financing](https://troycondogarages.com/financing/)
- [Design your space](https://troycondogarages.com/design-your-space/)
- [Contact and tours](https://troycondogarages.com/contact/)
```

---

## Part 6: Make contact info match across the whole site

This is the only part that touches pages other than the homepage.

1. In every page, template, and schema block, replace:
   - `(715) 567-5456` and any other format of `715-567-5456` → `(651) 247-8384`
   - `tel:` links to 7155675456 → `tel:6512478384`
   - `info@troycondogarages.com` → `troycondogaragesbyvalmark@gmail.com`, including `mailto:` links
2. **Never change these numbers.** They belong to the financing partner, Alliance Bank (Gordon Boos), on the Financing page: `715-926-4234`, `tel:7159264234`, and `800-896-1788`.
3. **Every business phone number shown on the site must be a clickable `tel:6512478384` link.** If you find (651) 247-8384 as plain text that isn't linked, wrap it: `<a href="tel:6512478384">(651) 247-8384</a>`. This is what makes Google Ads count the call.
4. **Do not edit `/js/call-tracking.js`** or any analytics or ad-tracking code.
5. Leave form, CRM, and email-routing settings alone, including the embedded LeadConnector form. Change only the text visitors see and the links.
6. If none of the old values exist in the project, say so and move on. (The old man-cave page that used 715-567-5456 now returns a 404 on the live site.)

---

## Part 7: Final check
1. Show the diff of every changed file.
2. Confirm: one `<h1>` on the homepage, the JSON-LD parses, the FAQ sits above `#lead-form`, `llms.txt` is in the web root, and a project-wide search finds no remaining `715-567-5456` or `info@troycondogarages.com` outside tracking scripts.
3. Confirm the financing partner numbers (715-926-4234, 800-896-1788) are untouched.
4. Report the Part 0 findings.
5. List anything you skipped and why.

---

## Manual steps for Austin (Cursor can't do these)
1. **Deploy** the changes the way you normally publish the site.
2. **Rich Results Test:** paste the homepage URL into https://search.google.com/test/rich-results. You should see "Local business" with no errors.
3. **Search Console:** URL Inspection on the homepage, then **Request Indexing**.
4. **Manual actions check:** in Search Console, open **Security & Manual Actions → Manual actions**. Only if a penalty is listed, upload `troycondogarages-disavow.txt`.
5. **Stock photo:** swap the Unsplash image in the Security column for a real gate photo, then ask Cursor to set its alt to `Gated entry and security cameras at Troy Condo Garages in Hudson, WI`.
6. **Google reviews link:** once you have your Google Business Profile review link, ask Cursor to add `<p><a href="LINK" target="_blank" rel="noopener">Read all reviews on Google →</a></p>` under the reviews, and add the profile URL to `sameAs`.
7. **Confirm heat with Troy:** the FAQ says units have in-floor heating, as the site already claims. If it's an upgrade rather than standard, tell Cursor to change that answer.
