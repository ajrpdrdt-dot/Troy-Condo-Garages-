# Amenity map section CSS + page inserts
from pathlib import Path

css_path = Path("site/css/theme.css")
css = css_path.read_text(encoding="utf-8")
marker = "/* ——— Footer ——— */"
block = """/* ——— Facility / amenity map ——— */
.facility-map {
  display: grid;
  gap: 2rem;
  grid-template-columns: 1.35fr 1fr;
  align-items: start;
}

.facility-map-visual {
  margin: 0;
}

.facility-map-visual img {
  width: 100%;
  height: auto;
  display: block;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  background: #111;
}

.facility-map-visual figcaption {
  margin-top: 0.65rem;
  font-size: 0.9rem;
  color: var(--color-muted);
}

.facility-map-legend {
  list-style: none;
  margin: 0;
  padding: 0;
  counter-reset: amenity;
}

.facility-map-legend li {
  display: grid;
  grid-template-columns: 2rem 1fr;
  gap: 0.75rem;
  padding: 0.7rem 0;
  border-bottom: 1px solid #e2e2e2;
  color: var(--color-muted);
}

.facility-map-legend li::before {
  counter-increment: amenity;
  content: counter(amenity);
  font-family: var(--font-display);
  font-size: 1.15rem;
  color: var(--color-accent);
  line-height: 1.2;
}

.facility-map-legend strong {
  display: block;
  color: var(--color-ink);
  font-family: var(--font-display);
  letter-spacing: 0.03em;
  text-transform: uppercase;
  font-size: 0.95rem;
  font-weight: 400;
  margin-bottom: 0.15rem;
}

.facility-exteriors {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 2rem;
}

.facility-exteriors figure {
  margin: 0;
}

.facility-exteriors img {
  width: 100%;
  aspect-ratio: 3 / 2;
  object-fit: cover;
  display: block;
}

.facility-exteriors figcaption {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--color-muted);
}

.directions-block {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e2e2;
}

.directions-block p {
  color: var(--color-muted);
  max-width: 40rem;
}

@media (max-width: 900px) {
  .facility-map {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .facility-exteriors {
    grid-template-columns: 1fr;
  }
}

"""

if "/* ——— Facility / amenity map ——— */" not in css:
    css_path.write_text(css.replace(marker, block + marker, 1), encoding="utf-8")
    print("theme.css: amenity map styles added")
else:
    print("theme.css: styles already present")

UNITS_SECTION = '''
    <section class="section section-muted" id="amenity-map">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Hudson facility</p>
          <h2>Amenity map &amp; site overview</h2>
          <p class="lead">Aerial view of Troy Condo Garages at 663 Valerie Ave — gated grounds, wide aisles, and room to move oversized vehicles.</p>
        </div>
        <div class="facility-map">
          <figure class="facility-map-visual">
            <img src="/assets/Troy-Condo-Garages-Hudson-WI-aerial-2025.webp" alt="Aerial view of Troy Condo Garages facility in Hudson, WI" width="1600" height="1000" loading="lazy" />
            <figcaption>2025 aerial of the Hudson campus — unit rows, drive aisles, playground, and landscaped grounds.</figcaption>
          </figure>
          <ol class="facility-map-legend">
            <li><span><strong>Gated entry &amp; fence</strong>Secured perimeter with controlled access and well-lit grounds.</span></li>
            <li><span><strong>Condo garage buildings</strong>Steel unit rows with overhead doors, service doors, and private ownership.</span></li>
            <li><span><strong>Wide drive aisles</strong>About 60′ clearance for RVs, trailers, and oversized toys.</span></li>
            <li><span><strong>Paved access</strong>Blacktop roads from Valerie Ave into the cul-de-sac turnaround.</span></li>
            <li><span><strong>Playground</strong>On-site play area for families visiting the facility.</span></li>
            <li><span><strong>Open grounds</strong>Maintained lawn, retention ponds, and year-round site care.</span></li>
            <li><span><strong>24/7 surveillance</strong>Video monitoring across the campus for peace of mind.</span></li>
          </ol>
        </div>
        <div class="facility-exteriors">
          <figure>
            <img src="/assets/troy-condo-garage-row-exterior.jpg" alt="Exterior row of Troy Condo Garages units" width="1200" height="800" loading="lazy" />
            <figcaption>Unit row exterior — numbered service doors and overhead garage doors.</figcaption>
          </figure>
          <figure>
            <img src="/assets/Troy-Condo-Garages-Hudson-WI-Property.webp" alt="Troy Condo Garages property exterior" width="1200" height="800" loading="lazy" />
            <figcaption>Property exterior — steel construction and paved drive lanes.</figcaption>
          </figure>
        </div>
        <div class="directions-block">
          <h3>Directions</h3>
          <p>663 Valerie Ave, Hudson, WI 54016 — St. Croix Valley, a short drive from River Falls, New Richmond, and the Twin Cities metro. Tours by appointment.</p>
          <div class="btn-row" style="margin-top:1rem;">
            <a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&amp;destination=663+Valerie+Ave,+Hudson,+WI+54016" target="_blank" rel="noopener">Get directions</a>
            <a class="btn btn-secondary" href="/contact/#lead-form">Schedule a Tour</a>
          </div>
        </div>
      </div>
    </section>
'''

units = Path("site/units.html")
ut = units.read_text(encoding="utf-8")
if 'id="amenity-map"' not in ut:
    anchor = '    <section class="section section-muted">\n      <div class="container">\n        <h2>Frequently asked questions</h2>'
    if anchor not in ut:
        raise SystemExit("units.html FAQ anchor not found")
    ut = ut.replace(anchor, UNITS_SECTION + "\n" + anchor, 1)
    ut = ut.replace(
        '<p>Call <a href="tel:6512478384">(651) 247-8384</a> or use the <a href="/contact/">contact form</a>.</p>',
        '<p>Call <a href="tel:6512478384">(651) 247-8384</a> or use the <a href="/contact/#lead-form">contact form</a>.</p>',
        1,
    )
    units.write_text(ut, encoding="utf-8")
    print("units.html: amenity map section added")
else:
    print("units.html: already has amenity map")

CONTACT_SECTION = '''
    <section class="section section-muted" id="directions">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Visit us</p>
          <h2>Directions &amp; facility overview</h2>
          <p class="lead">Find Troy Condo Garages in Hudson, then tour the gated campus in person.</p>
        </div>
        <div class="facility-map">
          <figure class="facility-map-visual">
            <img src="/assets/Troy-Condo-Garages-Hudson-WI-aerial-2025.webp" alt="Aerial amenity map view of Troy Condo Garages" width="1600" height="1000" loading="lazy" />
            <figcaption>Aerial amenity overview — see the full labeled map on <a href="/units/#amenity-map">Our Units</a>.</figcaption>
          </figure>
          <div>
            <h3>Getting here</h3>
            <p><strong>Address:</strong> 663 Valerie Ave, Hudson, WI 54016</p>
            <p>From the Twin Cities, take I-94 east into Hudson, then local roads to Valerie Ave in the St. Croix Valley. Convenient to River Falls and New Richmond.</p>
            <p><strong>Hours:</strong> Monday – Sunday, 6 AM – 12 AM · Tours by appointment</p>
            <div class="btn-row" style="margin-top:1.25rem;">
              <a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&amp;destination=663+Valerie+Ave,+Hudson,+WI+54016" target="_blank" rel="noopener">Get directions</a>
              <a class="btn btn-secondary" href="/units/#amenity-map">View amenity map</a>
            </div>
            <iframe class="map-embed" style="margin-top:1.5rem;" title="Troy Condo Garages map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=663%20Valerie%20Ave%2C%20Hudson%2C%20WI%2054016&amp;t=m&amp;z=13&amp;output=embed&amp;iwloc=near"></iframe>
          </div>
        </div>
        <div class="facility-exteriors">
          <figure>
            <img src="/assets/troy-condo-garage-row-exterior.jpg" alt="Exterior of garage condo unit row" width="1200" height="800" loading="lazy" />
            <figcaption>Exterior unit row on site.</figcaption>
          </figure>
          <figure>
            <img src="/assets/troy-condo-garage-exterior-open-door.jpg" alt="Garage condo with open overhead door" width="1200" height="800" loading="lazy" />
            <figcaption>Overhead door access for vehicles and trailers.</figcaption>
          </figure>
        </div>
      </div>
    </section>
'''

contact = Path("site/contact.html")
ct = contact.read_text(encoding="utf-8")
if 'id="directions"' not in ct:
    # Simplify contact-meta: keep map link, remove duplicate large img+iframe (now in directions section)
    old_meta_tail = '''          <p><a href="https://www.google.com/maps/search/?api=1&amp;query=663+Valerie+Ave,+Hudson,+WI+54016" target="_blank" rel="noopener">Open in Google Maps</a> · <a href="https://www.google.com/search?q=Troy+Condo+Garages+Hudson+WI+reviews" target="_blank" rel="noopener">Google Reviews</a></p>
          <img src="/assets/475758958_593760273416489_2625868417057502521_n.jpg" alt="Troy Condo Garages facility" width="900" height="600" loading="lazy" style="margin:1rem 0;" />
          <iframe class="map-embed" title="Troy Condo Garages map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=663%20Valerie%20Ave%2C%20Hudson%2C%20WI%2054016&amp;t=m&amp;z=12&amp;output=embed&amp;iwloc=near"></iframe>'''
    new_meta_tail = '''          <p><a href="https://www.google.com/maps/dir/?api=1&amp;destination=663+Valerie+Ave,+Hudson,+WI+54016" target="_blank" rel="noopener">Get directions</a> · <a href="/units/#amenity-map">Amenity map</a> · <a href="https://www.google.com/search?q=Troy+Condo+Garages+Hudson+WI+reviews" target="_blank" rel="noopener">Google Reviews</a></p>'''
    if old_meta_tail in ct:
        ct = ct.replace(old_meta_tail, new_meta_tail, 1)
    ct = ct.replace("  </main>", CONTACT_SECTION + "\n  </main>", 1)
    contact.write_text(ct, encoding="utf-8")
    print("contact.html: directions + amenity overview added")
else:
    print("contact.html: already has directions section")

index = Path("site/index.html")
it = index.read_text(encoding="utf-8")
HOME_TEASER = '''
    <section class="section section-muted" id="amenity-map">
      <div class="container facility-map">
        <figure class="facility-map-visual">
          <img src="/assets/Troy-Condo-Garages-Hudson-WI-aerial-2025.webp" alt="Aerial amenity map of Troy Condo Garages Hudson WI" width="1600" height="1000" loading="lazy" />
          <figcaption>Hudson campus aerial — gated entry, unit rows, and wide drive aisles.</figcaption>
        </figure>
        <div>
          <p class="eyebrow">Facility</p>
          <h2>Amenity map</h2>
          <p class="lead">See how the grounds are laid out before you tour — buildings, aisles, playground, and secure perimeter.</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="/units/#amenity-map">Explore the full map</a>
            <a class="btn btn-secondary" href="/contact/#directions">Directions</a>
          </div>
        </div>
      </div>
    </section>
'''
if 'id="amenity-map"' not in it:
    area = '    <section class="section">\n      <div class="container">\n        <div class="section-head">\n          <p class="eyebrow">Area we serve</p>'
    if area not in it:
        raise SystemExit("index area section not found")
    it = it.replace(area, HOME_TEASER + "\n" + area, 1)
    index.write_text(it, encoding="utf-8")
    print("index.html: amenity map teaser added")
else:
    print("index.html: already has amenity map")

print("done")
