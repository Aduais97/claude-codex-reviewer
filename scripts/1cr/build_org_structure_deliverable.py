#!/usr/bin/env python3
"""
1st Call Recruitment — complete org structure deliverable.
Renders the ETR-workflow output (/tmp/1cr_org.json) into a polished HTML org
chart + analysis, then to PDF via headless Chrome.

Output -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os, json, html, subprocess, re

SRC = "/tmp/1cr_org.json"
OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
HTML = os.path.join(OUT, "1CR_Org_Structure.html")
PDF = os.path.join(OUT, "1CR_Org_Structure.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

d = json.load(open(SRC))

def esc(s): return html.escape(str(s)) if s is not None else ""
def short(name):
    return re.split(r"\s*[(—\-]", name)[0].strip()

# index people by short name for flags
def find(nm):
    for p in d["current_org"]:
        if short(p["name"]).lower().startswith(nm.lower()):
            return p
    return None

# card renderer
def card(p, cls=""):
    nm = short(p["name"])
    title = p["title"].split("—")[0].split(" - ")[0].strip()
    comp = p.get("compensation", "")
    comp_short = comp.split(";")[0].split("(")[0].strip()[:34]
    key = "KEY" if p.get("key_person") else ""
    return f"""<div class="node {cls}">
        <div class="nm">{esc(nm)} {'<span class=tag>KEY</span>' if key else ''}</div>
        <div class="ti">{esc(title)}</div>
        <div class="co">{esc(comp_short)}</div>
    </div>"""

ange = find("Ange"); bobby = find("Bobby"); phill = find("Phill")
reports = [find(n) for n in ["Elisha","Deshan","Polly","Tayla","Darren","Patrick"]]
spof_names = {"Deshan","Darren","Ange","Bobby","Payal"}

def rep_card(p):
    nm = short(p["name"]); spof = nm in spof_names
    title = p["title"].split("—")[0].split(" - ")[0].strip()
    comp = p.get("compensation","").split(";")[0].split("(")[0].strip()[:30]
    return f"""<div class="rep {'spof' if spof else ''}">
        <span class="rn">{esc(nm)}{' <b class=spoftag>SPOF</b>' if spof else ''}</span>
        <span class="rt">{esc(title)} · {esc(comp)}</span></div>"""

fiji = d["fiji_centre"]
fiji_cards = "".join(
    f"""<div class="frep"><span class="rn">{esc(short(r['name']))}</span>
        <span class="rt">{esc(r['title'].split('—')[0].strip()[:42])}</span></div>"""
    for r in fiji["roles"])

# control findings (departed / closed / unidentified)
findings = [p for p in d["current_org"] if short(p["name"]) in
            ("Rachael","Wellington office","IT Developer #1","IT Developer #2")]
def finding_card(p):
    nm = short(p["name"])
    red = nm.startswith("Rachael")
    return f"""<div class="finding {'red' if red else 'grey'}">
        <b>{esc(nm)}</b> — {esc(p['title'].split('—')[0].strip()[:60])}</div>"""

# tables
def table(rows, headers, widths):
    h = "".join(f'<th style="width:{w}">{esc(c)}</th>' for c,w in zip(headers,widths))
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'

spans_rows = [(esc(s["manager"]), f'<b>{s["direct_reports_count"]}</b>', esc(s["assessment"]))
              for s in d["spans_of_control"]]
km_rows = [(f'<b>{esc(k["person"])}</b>', esc(k["why_critical"]), esc(k["impact_if_lost"]), esc(k["mitigation"]))
           for k in d["key_man_risks"]]
rec_rows = [(f'<b>{esc(r["action"])}</b>', esc(r["rationale"]), esc(r["financial_impact"]))
            for r in d["restructuring_recommendations"]]

ts = d["target_structure"]
def li(items): return "".join(f"<li>{esc(x)}</li>" for x in items)
hires = "".join(f'<li><b>{esc(h["role"])}</b> <span class=c>{esc(h["cost"])}</span> — {esc(h["rationale"])}</li>'
                for h in ts["new_hires"])
spofs = "".join(f"<li>{esc(x)}</li>" for x in d["single_points_of_failure"])
oq = "".join(f"<li>{esc(x)}</li>" for x in d["open_questions"])

summary = d["summary"]

doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A3 landscape; margin: 14mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; color:#1A1A1A; margin:0; font-size:11px; line-height:1.45; }}
h1 {{ color:#13314F; font-size:26px; margin:0 0 2px; }}
.sub {{ color:#5A6B7B; font-size:12px; margin-bottom:14px; }}
h2 {{ color:#13314F; font-size:16px; margin:26px 0 10px; padding-bottom:5px; border-bottom:2px solid #13314F; page-break-after:avoid; }}
.summary {{ background:#F4F7F9; border-left:4px solid #1C8C8C; padding:12px 16px; font-size:11px; border-radius:4px; }}
/* org tree */
.apex {{ text-align:center; }}
.node {{ display:inline-block; border:2px solid #13314F; border-radius:8px; padding:8px 14px; min-width:150px; text-align:center; background:#fff; vertical-align:top; }}
.node.exit {{ border-style:dashed; border-color:#9AA6B2; background:#F6F7F9; color:#5A6B7B; }}
.node.key {{ border-color:#B5762B; background:#FFF9F0; }}
.node .nm {{ font-weight:700; color:#13314F; font-size:13px; }}
.node.exit .nm {{ color:#5A6B7B; }}
.node .ti {{ font-size:10px; color:#33454F; margin-top:1px; }}
.node .co {{ font-size:9.5px; color:#7A8794; margin-top:2px; }}
.tag {{ background:#B5762B; color:#fff; font-size:8px; padding:1px 5px; border-radius:3px; vertical-align:middle; }}
.connector {{ width:2px; height:18px; background:#C9D3DC; margin:0 auto; }}
.leaders {{ display:flex; justify-content:center; gap:60px; margin-top:0; }}
.lcol {{ display:flex; flex-direction:column; align-items:center; }}
.reps {{ margin-top:10px; width:280px; }}
.reps .lbl {{ font-size:9px; color:#7A8794; text-transform:uppercase; letter-spacing:.5px; margin-bottom:4px; text-align:center; }}
.rep {{ border:1px solid #D5DCE3; border-left:3px solid #1C8C8C; border-radius:5px; padding:5px 9px; margin-bottom:5px; display:flex; flex-direction:column; }}
.rep.spof {{ border-left-color:#C0392B; background:#FCF4F3; }}
.rn {{ font-weight:700; color:#13314F; font-size:11px; }}
.rt {{ font-size:9.5px; color:#5A6B7B; }}
.spoftag {{ background:#C0392B; color:#fff; font-size:7.5px; padding:0 4px; border-radius:3px; }}
.bobbynote {{ font-size:9.5px; color:#5A6B7B; width:200px; text-align:center; margin-top:8px; font-style:italic; }}
/* fiji */
.fiji {{ border:2px dotted #1C8C8C; border-radius:8px; padding:12px 16px; margin-top:14px; background:#F7FBFB; }}
.fiji h3 {{ margin:0 0 8px; color:#13314F; font-size:13px; }}
.frow {{ display:flex; flex-wrap:wrap; gap:8px; }}
.frep {{ border:1px solid #BFE0E0; border-radius:5px; padding:5px 10px; background:#fff; display:flex; flex-direction:column; min-width:160px; }}
/* findings */
.findings {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }}
.finding {{ flex:1; min-width:200px; border-radius:5px; padding:7px 11px; font-size:10px; }}
.finding.red {{ background:#FCF4F3; border:1px solid #E2B7B1; color:#7A2018; }}
.finding.grey {{ background:#F4F6F8; border:1px solid #D5DCE3; color:#5A6B7B; }}
/* tables */
table {{ width:100%; border-collapse:collapse; font-size:10px; margin-top:6px; }}
th {{ background:#13314F; color:#fff; text-align:left; padding:6px 8px; font-size:9.5px; }}
td {{ border-bottom:1px solid #E3E9EE; padding:6px 8px; vertical-align:top; }}
tr:nth-child(even) td {{ background:#F8FAFB; }}
.cols {{ display:flex; gap:18px; }}
.cols > div {{ flex:1; }}
.cols h3 {{ color:#13314F; font-size:12px; margin:0 0 6px; }}
ul {{ margin:4px 0 0; padding-left:18px; }}
li {{ margin-bottom:4px; font-size:10px; }}
.c {{ color:#2E8B57; font-weight:700; }}
.foot {{ margin-top:18px; font-size:8.5px; color:#8895A2; border-top:1px solid #E3E9EE; padding-top:8px; }}
.legend {{ font-size:9px; color:#5A6B7B; margin:6px 0 0; }}
.legend span {{ display:inline-block; margin-right:14px; }}
.dot {{ display:inline-block; width:10px; height:10px; border-radius:2px; vertical-align:middle; margin-right:3px; }}
</style></head><body>

<h1>1st Call Recruitment (JCR 2006 Ltd) — Organisation Structure</h1>
<div class="sub">Current state &amp; post-acquisition target · ASG Group acquisition · Confidential · Generated via ETR multi-agent workflow</div>

<div class="summary">{esc(summary)}</div>

<h2>1 · Current Organisation</h2>
<div class="legend">
  <span><span class="dot" style="background:#FFF9F0;border:2px solid #B5762B"></span>Key person (existential)</span>
  <span><span class="dot" style="background:#FCF4F3;border:1px solid #C0392B"></span>Single point of failure</span>
  <span><span class="dot" style="background:#F6F7F9;border:2px dashed #9AA6B2"></span>Exiting / departed</span>
</div>
<div class="apex" style="margin-top:10px">
  {card(phill,'exit')}
  <div class="connector"></div>
</div>
<div class="leaders">
  <div class="lcol">
    {card(ange,'key')}
    <div class="reps">
      <div class="lbl">Direct reports — span of 6</div>
      {''.join(rep_card(r) for r in reports)}
    </div>
  </div>
  <div class="lcol">
    {card(bobby,'key')}
    <div class="bobbynote">0 direct reports · owns 100% of client relationships &amp; BD · the undisclosed 10% shareholder</div>
  </div>
</div>

<div class="fiji">
  <h3>Fiji Support Centre — {fiji['headcount']} staff · 4-on/4-off 24/7 · dotted line to GM via Rose/Kat</h3>
  <div class="frow">{fiji_cards}</div>
  <div style="font-size:9.5px;color:#5A6B7B;margin-top:8px">Functions: {esc(', '.join(fiji['functions']))}</div>
  <div style="font-size:9px;color:#7A8794;margin-top:3px">{esc(fiji['cost_note'][:200])}</div>
</div>

<div class="findings">{''.join(finding_card(p) for p in findings)}</div>

<h2>2 · Spans of Control</h2>
{table(spans_rows, ["Manager","Reports","Assessment"], ["20%","8%","72%"])}

<h2>3 · Key-Person Risk Register</h2>
{table(km_rows, ["Person","Why critical","Impact if lost","Mitigation"], ["12%","28%","30%","30%"])}

<h2>4 · Single Points of Failure</h2>
<ul>{spofs}</ul>

<h2>5 · Post-Acquisition Target Structure</h2>
<div class="summary" style="border-left-color:#2E8B57;margin-bottom:12px">{esc(ts['narrative'])}</div>
<div class="cols">
  <div><h3>Retain (re-engage on ASG agreements)</h3><ul>{li(ts['retain'])}</ul></div>
  <div><h3>Integrate to group</h3><ul>{li(ts['integrate_to_group'])}</ul></div>
</div>
<div class="cols" style="margin-top:12px">
  <div><h3>Exit / resize</h3><ul>{li(ts['exit_or_resize'])}</ul></div>
  <div><h3>New roles needed</h3><ul>{hires}</ul></div>
</div>

<h2>6 · Restructuring Recommendations</h2>
{table(rec_rows, ["Action","Rationale","Financial impact"], ["22%","48%","30%"])}

<h2>7 · Open Questions &amp; DD Gaps</h2>
<ul>{oq}</ul>

<div class="foot">Source roster: Phill Van Syp salary breakdown (28 May 2026) + FY26 Xero P&amp;L (year ended 31 Mar 2026) + acquisition working files.
Built by an 8-agent ETR workflow (map → synthesise → adversarial critique → finalise). Figures anchored to the corrected 8 Jun normalised P&amp;L (~$401–466K maintainable EBITDA, 20.05% GP). Confidential — ASG Group internal.</div>

</body></html>"""

open(HTML, "w").write(doc)
print("Wrote", HTML)

# render PDF via headless chrome
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}", "--no-margins", HTML],
               capture_output=True, timeout=90)
print("Wrote", PDF if os.path.exists(PDF) else "(PDF FAILED)")
