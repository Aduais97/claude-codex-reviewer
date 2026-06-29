#!/usr/bin/env python3
"""
1st Call Recruitment — SIMPLE classic org chart (white bg, black rounded boxes,
elbow connectors, 3-line labels). Rendered to PDF + PNG via headless Chrome.

Output -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os, subprocess

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
HTML = os.path.join(OUT, "1CR_Org_Chart_Simple.html")
PDF = os.path.join(OUT, "1CR_Org_Chart_Simple.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def node(name, title, dept):
    return (f'<div class="node"><div class="nm">{name}</div>'
            f'<div class="ti">{title}</div><div class="de">{dept}</div></div>')

# main tree
reports = [
    ("Elisha", "Operations Manager", "Operations"),
    ("Deshan", "Payroll Officer", "Finance"),
    ("Polly", "Recruitment Consultant", "Auckland"),
    ("Tayla", "Recruitment Consultant", "Hamilton"),
    ("Darren", "Recruitment Consultant", "Christchurch"),
    ("Patrick", "Contract Consultant", "Commission-only"),
]
reports_li = "".join(f"<li>{node(*r)}</li>" for r in reports)

fiji = [
    ("Payal", "Accounts Lead", "Fiji"),
    ("Rose", "Team Leader", "Fiji"),
    ("Kat", "Team Leader", "Fiji"),
    ("Support Team ×10", "After-hours Support", "Fiji"),
]
fiji_li = "".join(f"<li>{node(*r)}</li>" for r in fiji)

doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A3 landscape; margin: 16mm; }}
body {{ font-family: Helvetica, Arial, sans-serif; color:#111; background:#fff; margin:0; }}
h1 {{ font-size:20px; color:#111; margin:0 0 2px; }}
.sub {{ color:#666; font-size:12px; margin-bottom:26px; }}

.tree {{ text-align:center; }}
.tree ul {{ position:relative; padding-top:22px; display:flex; justify-content:center; list-style:none; margin:0; }}
.tree li {{ list-style:none; position:relative; padding:22px 10px 0; }}
/* connectors */
.tree li::before, .tree li::after {{
  content:''; position:absolute; top:0; right:50%;
  border-top:1.6px solid #222; width:50%; height:22px;
}}
.tree li::after {{ right:auto; left:50%; border-left:1.6px solid #222; }}
.tree li:only-child::after, .tree li:only-child::before {{ display:none; }}
.tree li:only-child {{ padding-top:22px; }}
.tree li:first-child::before, .tree li:last-child::after {{ border:0 none; }}
.tree li:last-child::before {{ border-right:1.6px solid #222; }}
.tree ul ul::before {{
  content:''; position:absolute; top:0; left:50%;
  border-left:1.6px solid #222; width:0; height:22px;
}}
.tree > ul {{ padding-top:0; }}
.tree > ul > li {{ padding-top:0; }}
.tree > ul > li::before, .tree > ul > li::after {{ display:none; }}

.node {{
  display:inline-block; border:1.7px solid #1a1a1a; border-radius:11px;
  padding:11px 20px; background:#fff; min-width:140px; line-height:1.45;
}}
.nm {{ font-weight:700; font-size:14px; color:#111; }}
.ti {{ font-size:12.5px; color:#222; }}
.de {{ font-size:12.5px; color:#444; }}
.node.exit {{ border-style:dashed; border-color:#888; color:#666; }}
.node.exit .nm {{ color:#555; }}

.caption {{ font-size:11px; color:#666; margin:30px 0 4px; }}
.caption b {{ color:#111; }}
.dotwrap .node-head {{ }}
.fiji .node {{ border-style:dotted; }}
</style></head><body>

<h1>1st Call Recruitment (JCR 2006 Ltd) — Organisation Chart</h1>
<div class="sub">Current structure &middot; ~22 staff &middot; Confidential</div>

<div class="tree">
  <ul><li>
    {node("Phill Van Syp", "Owner &amp; Director", "Exiting on sale")}
    <ul>
      <li>
        {node("Ange", "General Manager", "Auckland")}
        <ul>{reports_li}</ul>
      </li>
      <li>{node("Bobby", "National Sales Manager", "Sales &amp; BD")}</li>
    </ul>
  </li></ul>
</div>

<div class="caption">Fiji Support Centre &mdash; <b>14 staff &middot; 4-on/4-off</b> &middot; reports to the GM (Ange) via Team Leaders Rose &amp; Kat</div>
<div class="tree fiji">
  <ul><li>
    {node("Fiji Support Centre", "Shared services", "After-hours / payroll / accounts")}
    <ul>{fiji_li}</ul>
  </li></ul>
</div>

</body></html>"""

open(HTML, "w").write(doc)
print("Wrote", HTML)
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}", "--no-margins", HTML],
               capture_output=True, timeout=90)
print("Wrote", PDF if os.path.exists(PDF) else "(PDF FAILED)")
