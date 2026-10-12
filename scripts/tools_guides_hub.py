import re, os, html, glob, json
os.chdir(os.path.join(os.path.dirname(__file__), 'public'))

# Author archive links now 404 -> point to About
for f in glob.glob('**/index.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    n = re.sub(r'href="(https://troycondogarages\.com)?/author/[^"]*"', 'href="/about/"', s)
    if n != s: open(f, 'w', encoding='utf-8').write(n)

pages = [p for p in open('/tmp/guide_pages.txt').read().split('\n') if p and p not in ('events', 'open-house', 'condo-garages-hudson-wi')]
GROUPS = [
    ('Start here: what a garage condo is and what it costs', ['blog-what-is-a-garage-condo', 'how-much-does-a-garage-condo-cost-in-wisconsin', 'car-condo-vs-garage-condo-difference', 'ultimate-guide-to-premium-garage-condos', 'garage-condo-buying-process', 'phase-iii-at-troy-condo-garages-whats-new-for-buyers', 'can-you-live-in-a-garage-condo-wisconsin-zoning-rules']),
    ('Costs, financing, taxes and HOA', ['garage-condo-financing-hudson-wi', 'garage-condo-financing-rates-2027', 'hoa-fees-troy-condo-garages-hudson-wi', 'garage-condo-property-taxes-st-croix-county', 'garage-condo-insurance-wisconsin', 'garage-condo-tax-benefits-section-179-wisconsin', 'garage-condo-investment-wisconsin', 'garage-condo-resale-value', 'garage-condo-ownership-vs-401k-building-equity']),
    ('Compare your options', ['blog-garage-condo-vs-storage-unit', 'garage-condo-vs-storage-unit-hudson-wi', 'garage-condo-vs-pole-barn', 'garage-condo-vs-renting-commercial-warehouse-space-hudson-wi', 'best-garage-condo-communities-near-hudson-wi-western-wisconsin']),
    ('Storage by vehicle and use', ['rv-storage-hudson-wi', 'boat-storage-hudson-wi', 'classic-car-storage-near-hudson-wi', 'motorcycle-storage-hudson-wi', 'snowmobile-atv-storage-hudson-wi', 'jet-ski-watercraft-storage-hudson-wi', 'enclosed-trailer-storage-hudson-wi', 'toy-hauler-camper-van-storage-hudson-wi', 'measure-rv-boat-garage-condo', 'garage-condo-small-business-storage-hudson-wi', 'why-car-collectors-contractors-choose-garage-condo-ownership']),
    ('Build out your unit', ['garage-condo-mezzanine-ideas', 'car-lift-installation-garage-condo-hudson-wi', 'epoxy-garage-floor-coating-hudson-wi', 'garage-condo-climate-control', 'home-gym-garage-condo-hudson-wi', 'man-cave-garage-wisconsin', '5-ways-to-transform-your-troy-condo-garage-into-a-private-workshop']),
    ('Nearby areas', ['garage-condos-for-sale-near-twin-cities-minnesota', 'garage-condos-near-stillwater-mn', 'garage-condos-near-woodbury-lake-elmo-mn']),
]
used = {p for _, g in GROUPS for p in g}
leftover = [p for p in pages if p not in used]
if leftover: GROUPS.append(('More guides', leftover))

def meta(p):
    s = open(p + '/index.html', encoding='utf-8').read()
    t = re.search(r'<title>([^<]*)</title>', s).group(1)
    t = re.sub(r'\s*[-|]\s*Troy Condo Garages.*$', '', html.unescape(t)).strip()
    d = re.search(r'<meta content="([^"]*)" name="description"/>', s)
    d = html.unescape(d.group(1)) if d else ''
    if len(d) > 150: d = d[:147].rsplit(' ', 1)[0] + '...'
    return t, d

body = ['<article class="page type-page" id="guides-hub"><div style="max-width:1000px;margin:0 auto;padding:40px 20px;">',
        '<h1 style="font-size:clamp(30px,5vw,46px);margin:0 0 12px;">Garage Condo Guides for Hudson, WI Buyers</h1>',
        '<p style="font-size:18px;line-height:1.6;max-width:760px;">Everything we&#8217;ve written about owning a garage condo at Troy Condo Garages: what they are, what they cost, how financing and HOA fees work, and how owners build them out. When you&#8217;re ready, <a href="#request-availability">get the price &amp; floor-plan sheet</a> or see <a href="/garage-condos-for-sale-hudson-wi-pricing-size/">garage condos for sale in Hudson, WI</a>.</p>']
items = []
for title, group in GROUPS:
    group = [p for p in group if os.path.isfile(p + '/index.html')]
    if not group: continue
    body.append('<h2 style="font-size:26px;margin:36px 0 14px;">%s</h2>' % html.escape(title))
    body.append('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;">')
    for p in group:
        t, d = meta(p)
        items.append((p, t))
        body.append('<a href="/%s/" style="display:block;border:1px solid #ddd;border-radius:6px;padding:16px;text-decoration:none;color:#111;background:#fff;"><strong style="display:block;font-size:17px;margin-bottom:6px;color:#111;">%s</strong><span style="font-size:14px;color:#555;line-height:1.5;">%s</span></a>' % (p, html.escape(t), html.escape(d)))
    body.append('</div>')
body.append('</div></article>')

tpl = open('blog-what-is-a-garage-condo/index.html', encoding='utf-8').read()
a0 = tpl.find('<article'); a1 = tpl.find('</article>') + len('</article>')
s = tpl[:a0] + '\n'.join(body) + tpl[a1:]
# remove the mid-article CTA from template (the hub has its own intro link)
s = re.sub(r'<div class="tcg-guide-cta".*?</div>', '', s, count=1, flags=re.S)
T = 'Garage Condo Guides | Troy Condo Garages, Hudson, WI'
D = 'Guides to garage condo costs, financing, HOA fees, storage uses and build-outs in Hudson, WI. Get the Troy Condo Garages price and floor-plan sheet.'
s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % T, s, count=1)
for prop, val in (('og:title', T), ('og:description', D), ('og:url', 'https://troycondogarages.com/guides/'), ('og:type', 'website')):
    s = re.sub(r'<meta content="[^"]*" property="%s"/>' % prop, '<meta content="%s" property="%s"/>' % (html.escape(val), prop), s, count=1)
s = re.sub(r'<meta content="[^"]*" name="description"/>', '<meta content="%s" name="description"/>' % html.escape(D), s, count=1)
s = re.sub(r'<meta content="[^"]*" name="twitter:(title|description)"/>', '', s)
s = re.sub(r'<meta content="[^"]*" property="article:[^"]*"/>\n?', '', s)
s = re.sub(r'<link href="[^"]*" rel="canonical"/>', '', s)
s = s.replace('</title>', '</title>\n<link href="https://troycondogarages.com/guides/" rel="canonical"/>', 1)
schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": T, "url": "https://troycondogarages.com/guides/",
          "isPartOf": {"@type": "WebSite", "url": "https://troycondogarages.com/"},
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": "https://troycondogarages.com/%s/" % p, "name": t} for i, (p, t) in enumerate(items)]}}
s = re.sub(r'<script class="yoast-schema-graph" type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(schema), s, count=1, flags=re.S)
os.makedirs('guides', exist_ok=True)
open('guides/index.html', 'w', encoding='utf-8').write(s)
print('hub items', len(items))

# Sitemap: add /guides/ and refresh lastmod on edited money pages
sm = open('sitemap.xml', encoding='utf-8').read()
if '/guides/</loc>' not in sm:
    sm = sm.replace('</urlset>', '  <url>\n    <loc>https://troycondogarages.com/guides/</loc>\n    <lastmod>2026-10-12</lastmod>\n  </url>\n</urlset>')
for p in ['', 'blog-what-is-a-garage-condo/', 'garage-condos-for-sale-hudson-wi-pricing-size/', 'condo-garages-hudson-wi/', 'open-house/', 'how-much-does-a-garage-condo-cost-in-wisconsin/'] + [x + '/' for x in pages]:
    sm = re.sub(r'(<loc>https://troycondogarages\.com/%s</loc>\s*<lastmod>)[^<]*' % re.escape(p), r'\g<1>2026-10-12', sm)
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('inquiry in sitemap:', 'troy-condo-garages-inquiry' in sm)
