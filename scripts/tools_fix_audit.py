import re, os, html, glob, datetime
os.chdir(os.path.join(os.path.dirname(__file__), 'public'))
FORM_ID = 'OdHuTZct7loTGfEhVnJV'
changed = set()

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    open(p, 'w', encoding='utf-8').write(s); changed.add(p)

# 1. tel links -> E.164
for f in glob.glob('**/*.html', recursive=True):
    s = rd(f); o = s
    s = s.replace('tel:6512478384', 'tel:+16512478384').replace('tel:7155675456', 'tel:+17155675456').replace('tel:7159264234', 'tel:+17159264234')
    if s != o: wr(f, s)

# 2. Titles / metas / H1
def set_meta(p, title=None, desc=None, h1=None, ogimg=None):
    f = p + '/index.html'; s = rd(f)
    if title:
        s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % html.escape(title, quote=False), s, 1)
        s = re.sub(r'<meta content="[^"]*" property="og:title"/>', '<meta content="%s" property="og:title"/>' % html.escape(title), s, 1)
    if desc:
        d = html.escape(desc)
        if re.search(r'<meta content="[^"]*" name="description"/>', s):
            s = re.sub(r'<meta content="[^"]*" name="description"/>', '<meta content="%s" name="description"/>' % d, s, 1)
        else:
            s = s.replace('</title>', '</title>\n<meta content="%s" name="description"/>' % d, 1)
        s = re.sub(r'<meta content="[^"]*" property="og:description"/>', '<meta content="%s" property="og:description"/>' % d, s, 1)
        s = re.sub(r'<meta content="[^"]*" name="twitter:description"/>', '<meta content="%s" name="twitter:description"/>' % d, s, 1)
    if h1:
        s = re.sub(r'(<h1[^>]*>)BLOG(</h1>)', r'\g<1>%s\g<2>' % html.escape(h1, quote=False), s, 1)
    if ogimg and 'property="og:image"' not in s:
        s = s.replace('property="og:description"/>', 'property="og:description"/>\n<meta content="%s" property="og:image"/>' % ogimg, 1)
    wr(f, s)

OG = 'https://troycondogarages.com/wp-content/uploads/2026/03/TroyCondoGaragesofWesternWI.Storagespaceyoucanown.webp'
set_meta('garage-condos-for-sale-hudson-wi-pricing-size',
    'Garage Condos for Sale Hudson, WI | Pricing & Sizes 2026',
    'Current pricing, unit sizes and availability for Troy Condo Garages in Hudson, WI. Heated, private garage condos you own. Get the floor-plan sheet.')
set_meta('blog-what-is-a-garage-condo',
    'What Is a Garage Condo? Costs, Uses & Ownership Guide',
    'A garage condo is a private, deeded garage you own like real estate. See typical costs, HOA fees, uses and how Troy Condo Garages in Hudson compares.')
set_meta('open-house',
    'Open House & Tours | Troy Condo Garages in Hudson, WI',
    'Tour heated garage condos at Troy Condo Garages in Hudson, WI. See finished units, mezzanine options and pricing in person. Save your spot today.')
set_meta('condo-garages-hudson-wi', 'Condo Garages in Hudson, WI: Guides & Ownership Tips | Troy Condo Garages',
    None, h1='Condo Garages in Hudson, WI: Guides & Ownership Tips', ogimg=OG)

# 3. Lead capture on guide pages
SKIP = {'accessibility-statement', 'documents', 'privacy-policy', 'terms-of-service', 'thank-you', 'author', 'category', 'wp-content', 'wp-includes'}
MID = ('<div class="tcg-guide-cta" style="background:#111;color:#fff;border-left:4px solid #e3191e;border-radius:6px;padding:18px 20px;margin:24px 0;">'
       '<p style="margin:0 0 6px;font-size:19px;font-weight:700;color:#fff;">Get the price &amp; floor-plan sheet</p>'
       '<p style="margin:0 0 12px;color:#ddd;font-size:15px;line-height:1.5;">Current unit sizes, pricing from $194,900 and what&#8217;s available in Phase III. Sent by the Troy Condo Garages team.</p>'
       '<a href="#request-availability" style="display:inline-block;background:#e3191e;color:#fff;padding:10px 18px;border-radius:4px;font-weight:700;text-decoration:none;">Send me the sheet</a>'
       ' <a href="tel:+16512478384" style="color:#fff;margin-left:10px;text-decoration:underline;">or call (651) 247-8384</a></div>')
END = ('<section id="request-availability" style="background:#111;color:#fff;padding:56px 20px;">\n'
       '<div style="max-width:760px;margin:0 auto;text-align:center;">\n'
       '<h2 style="color:#fff;font-size:clamp(26px,4vw,38px);margin:0 0 10px;">Get the <span style="color:#e3191e">Price &amp; Floor-Plan Sheet</span></h2>\n'
       '<p style="color:#ddd;font-size:17px;line-height:1.6;margin:0 0 22px;">Tell us what you want to store or build out. A Troy Condo Garages team member will send open units, floor plans and pricing. Prefer to talk? Call <a href="tel:+16512478384" style="color:#fff;text-decoration:underline;">(651) 247-8384</a>.</p>\n'
       '<div style="background:#fff;border-radius:6px;padding:8px;"><iframe src="https://api.leadconnectorhq.com/widget/form/' + FORM_ID + '" style="width:100%;height:640px;border:none;border-radius:4px;" id="inline-' + FORM_ID + '-g" data-layout="{\'id\':\'INLINE\'}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="Troy Condo Garages - Availability Inquiry" data-height="640" data-layout-iframe-id="inline-' + FORM_ID + '-g" data-form-id="' + FORM_ID + '" title="Troy Condo Garages - Availability Inquiry"></iframe></div>\n'
       '<p style="color:#aaa;font-size:13px;margin:14px 0 0;">Garage condos are non-residential. Submitting this form does not obligate you to purchase.</p>\n'
       '</div></section>\n')
EMBED = '<script src="https://link.msgsndr.com/js/form_embed.js"></script>\n'
guide_pages = []
for d in sorted(os.listdir('.')):
    f = d + '/index.html'
    if d in SKIP or not os.path.isfile(f): continue
    s = rd(f)
    if FORM_ID in s: continue
    if '<footer' not in s: continue
    guide_pages.append(d)
    h1 = s.find('<h1')
    if h1 > 0:
        cnt, pos = 0, h1
        while cnt < 3:
            n = s.find('</p>', pos)
            if n < 0: break
            pos = n + 4; cnt += 1
        if cnt == 3 and pos < s.find('<footer'):
            s = s[:pos] + MID + s[pos:]
    fi = s.find('<footer')
    s = s[:fi] + END + s[fi:]
    if 'form_embed.js' not in s:
        s = s.replace('</body>', EMBED + '</body>', 1)
    wr(f, s)

# 4. Defer UserWay overlay until first interaction (sitewide)
UW_OLD = re.compile(r"\(function\(e\)\{\s*var el = document.createElement\('script'\);\s*el.setAttribute\('data-account', 'mI1NTkbzRJ'\);\s*el.setAttribute\('src', 'https://cdn.userway.org/widget.js'\);\s*document.body.appendChild\(el\);\s*\}\)\(\);")
UW_NEW = ("(function(){var done=false;function load(){if(done)return;done=true;var el=document.createElement('script');"
          "el.setAttribute('data-account','mI1NTkbzRJ');el.setAttribute('src','https://cdn.userway.org/widget.js');document.body.appendChild(el);}"
          "['pointerdown','keydown','touchstart','scroll'].forEach(function(t){window.addEventListener(t,load,{once:true,passive:true});});"
          "setTimeout(load,8000);})();")
for f in glob.glob('**/index.html', recursive=True):
    s = rd(f)
    n = UW_OLD.sub(UW_NEW, s)
    if n != s: wr(f, n)

open('/tmp/guide_pages.txt', 'w').write('\n'.join(guide_pages))
print('guide pages with new form:', len(guide_pages))
print('files changed:', len(changed))
