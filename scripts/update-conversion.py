from pathlib import Path
Path("site/js/conversion-lead.js").write_text(
    '/* Event snippet for Form/Book Submission conversion page */\n'
    'gtag("event", "conversion", {\n'
    '  send_to: "AW-18398757431/yPqRCJON7fAcELeEm8VE",\n'
    '  value: 1.0,\n'
    '  currency: "USD",\n'
    '});\n',
    encoding="utf-8",
)
print(Path("site/js/conversion-lead.js").read_text(encoding="utf-8"))
