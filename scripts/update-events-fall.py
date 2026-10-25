from pathlib import Path

path = Path("site/events.html")
text = path.read_text(encoding="utf-8")

old_calendar = '''    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">2026</p>
          <h2>Calendar highlights</h2>
          <p class="lead">Stay tuned for more 2026 events. We also show up at major regional meets.</p>
        </div>
        <div class="grid-2">
          <div class="size-block">
            <h3>June</h3>
            <p><strong>6/19–6/21</strong> — MSRA Back to the 50s</p>
          </div>
          <div class="size-block">
            <h3>July</h3>
            <p><strong>7/17–7/19</strong> — Street Machine Nationals</p>
          </div>
        </div>
      </div>
    </section>'''

new_calendar = '''    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">2026</p>
          <h2>Upcoming events</h2>
          <p class="lead">Open houses every Sunday through October, plus a customer appreciation day mid-month.</p>
        </div>
        <div class="grid-2">
          <div class="size-block">
            <h3>Sunday open houses</h3>
            <p><strong>Every Sunday through October</strong> · 11:00 AM – 1:00 PM</p>
            <p>Tour units <strong>401</strong> and <strong>402</strong> at Troy Condo Garages, 663 Valerie Ave, Hudson, WI.</p>
          </div>
          <div class="size-block">
            <h3>Customer appreciation</h3>
            <p><strong>Saturday, October 17</strong></p>
            <p>Customer appreciation event at Troy Condo Garages — details and schedule shared closer to the date.</p>
          </div>
        </div>
      </div>
    </section>'''

if old_calendar not in text:
    raise SystemExit("calendar section not found")
text = text.replace(old_calendar, new_calendar, 1)

old_featured = '''    <section class="section section-muted">
      <div class="container grid-2">
        <div>
          <img src="/assets/728215898_987170777408768_5618628321560603380_n-682x1024.jpg" alt="Open House and Cars &amp; Condos flyer" width="682" height="1024" loading="lazy" />
        </div>
        <div>
          <p class="eyebrow">Featured event</p>
          <h2>Open House + Cars &amp; Condos</h2>
          <p><strong>Saturday, July 11</strong> · 11:00 AM – 2:00 PM<br />Troy Condo Garages · Hudson, WI</p>
          <p>Join us for a free open house. Tour available units, meet current owners, and see why garage condo ownership is a strong fit for car enthusiasts and hobbyists. All makes and models welcome. Refreshments provided.</p>
          <p class="note">Hosted by Aaron &amp; Sami Real Estate Team, brokered by eXp Realty.</p>
          <div class="btn-row" style="margin-top: 1.25rem;">
            <a class="btn btn-primary" href="tel:6512478384">Call (651) 247-8384</a>
            <a class="btn btn-secondary" href="mailto:info@troycondogarages.com">Email Us</a>
          </div>
        </div>
      </div>
    </section>'''

new_featured = '''    <section class="section section-muted">
      <div class="container grid-2">
        <div>
          <img src="/assets/728215898_987170777408768_5618628321560603380_n-682x1024.jpg" alt="Troy Condo Garages open house" width="682" height="1024" loading="lazy" />
        </div>
        <div>
          <p class="eyebrow">Now through October</p>
          <h2>Sunday open houses</h2>
          <p><strong>Every Sunday through October</strong> · 11:00 AM – 1:00 PM<br />Units <strong>401</strong> &amp; <strong>402</strong> · 663 Valerie Ave, Hudson, WI</p>
          <p>Walk available garage condo units, ask questions on site, and see the facility in person. No appointment needed for open house hours — private tours are still available any day by request.</p>
          <div class="btn-row" style="margin-top: 1.25rem;">
            <a class="btn btn-primary" href="/contact/#lead-form">Schedule a Tour</a>
            <a class="btn btn-secondary" href="tel:6512478384">Call (651) 247-8384</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container grid-2">
        <div>
          <p class="eyebrow">Special event</p>
          <h2>Customer appreciation</h2>
          <p><strong>Saturday, October 17, 2026</strong><br />Troy Condo Garages · Hudson, WI</p>
          <p>Join us for a customer appreciation event celebrating owners, renters, and friends of Troy Condo Garages. More details will be posted here as the date approaches.</p>
          <div class="btn-row" style="margin-top: 1.25rem;">
            <a class="btn btn-primary" href="/contact/#lead-form">Get event updates</a>
          </div>
        </div>
        <div>
          <img src="/assets/Troy-Condo-Garages-Hudson-WI-Property.webp" alt="Troy Condo Garages Hudson WI property" width="900" height="600" loading="lazy" />
        </div>
      </div>
    </section>'''

if old_featured not in text:
    raise SystemExit("featured section not found")
text = text.replace(old_featured, new_featured, 1)

text = text.replace(
    "Open houses, car shows, and community gatherings at our Hudson, WI facility.",
    "Sunday open houses through October, plus customer appreciation on October 17.",
    1,
)
text = text.replace(
    'content="Open houses, car shows, and 2026 calendar events at Troy Condo Garages in Hudson, WI."',
    'content="Sunday open houses through October (11 AM–1 PM, units 401 & 402) and October 17 customer appreciation at Troy Condo Garages in Hudson, WI."',
    1,
)

# Relabel July archive as past
text = text.replace(
    """          <p class="eyebrow">Past highlight</p>
          <h2>Open House + Car Show</h2>
          <p><strong>Friday, May 30</strong> · 11:00 AM – 3:00 PM<br />Troy Condo Garages · Hudson, WI</p>
          <p>We hosted an open house for available garage condo units plus a car show — tours, horsepower, and networking on site.</p>
          <p class="note">Archive event — check back here for the next open house date.</p>""",
    """          <p class="eyebrow">Past highlight</p>
          <h2>Open House + Car Show</h2>
          <p><strong>Friday, May 30</strong> · 11:00 AM – 3:00 PM<br />Troy Condo Garages · Hudson, WI</p>
          <p>We hosted an open house for available garage condo units plus a car show — tours, horsepower, and networking on site.</p>
          <p class="note">Archive event — Sunday open houses continue through October.</p>""",
    1,
)

path.write_text(text, encoding="utf-8")
print("events.html updated")
