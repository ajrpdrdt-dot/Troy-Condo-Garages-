from pathlib import Path
import re

GHL = '''<div class="ghl-form-embed">
          <iframe
            src="https://api.leadconnectorhq.com/widget/form/OdHuTZct7loTGfEhVnJV"
            style="width:100%;height:640px;border:none;border-radius:4px"
            id="inline-OdHuTZct7loTGfEhVnJV"
            data-layout='{"id":"INLINE"}'
            data-trigger-type="alwaysShow"
            data-activation-type="alwaysActivated"
            data-deactivation-type="neverDeactivate"
            data-form-name="Troy Condo Garages - Availability Inquiry"
            data-form-id="OdHuTZct7loTGfEhVnJV"
            data-height="640"
            title="Troy Condo Garages - Availability Inquiry"></iframe>
        </div>
        <p class="form-disclaimer">Submitting this form does not obligate you to purchase or lease. A team member will contact you to discuss availability.</p>'''

# Match any formsubmit form block
form_re = re.compile(
    r'<form class="form-panel" action="https://formsubmit\.co/troycondogaragesbyvalmark@gmail\.com" method="POST">.*?</form>',
    re.DOTALL,
)

for name in ("index.html", "contact.html", "rentals.html"):
    p = Path("site") / name
    t = p.read_text(encoding="utf-8")
    nt, n = form_re.subn(GHL, t, count=1)
    if n != 1:
        raise SystemExit(f"{name}: expected 1 form replace, got {n}")
    nt = nt.replace('<script src="/js/forms.js"></script>', '<script src="https://link.msgsndr.com/js/form_embed.js"></script>')
    p.write_text(nt, encoding="utf-8")
    print(f"{name}: FormSubmit -> GHL embed")

css = Path("site/css/theme.css")
c = css.read_text(encoding="utf-8")
if ".ghl-form-embed" not in c:
    insert = """
.ghl-form-embed {
  width: 100%;
  max-width: 42rem;
  margin: 0 auto;
  background: var(--color-white);
  border-radius: 4px;
  overflow: hidden;
}

.section-dark .ghl-form-embed {
  max-width: 42rem;
}

.ghl-form-embed iframe {
  display: block;
  width: 100%;
  min-height: 640px;
  border: 0;
  background: var(--color-white);
}

"""
    c = c.replace("/* ——— Forms ——— */", "/* ——— Forms ——— */" + insert, 1)
    css.write_text(c, encoding="utf-8")
    print("theme.css: ghl-form-embed styles added")

print("done")
