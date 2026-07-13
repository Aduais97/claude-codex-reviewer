#!/usr/bin/env python3
"""
Mitre 10 — weekly covert LP report generator (SLS RTC).
Reads the 3 weekly xlsx exports (Guard Incident Report, Recovered Packaging,
Store Assessment) from a week folder and produces, into that same folder:
  1. <prefix>_LP_Report.pdf       — incidents + recovered packaging, all stores
  2. <prefix>_Store_Assessment.pdf — store security findings (per assessing store)
  3. <prefix>_Email_Summary.docx   — client email summary

Usage: python3 build_week_report.py "<week folder>" "<period label>"
Reusable each week — point it at the week's folder.
"""
import sys, os, glob, base64, subprocess, datetime
import openpyxl

WEEK = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/Mitre10/Week ending 28th June")
PERIOD = sys.argv[2] if len(sys.argv) > 2 else "22 – 28 June 2026"
PREFIX = "Mitre10_Week_Ending_28_June"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")

ACC="#1f3a5f"; SUB="#5b6472"; LINE="#dfe3e8"; RED="#b23a3a"; GREEN="#1d7a4d"; CARD="#f6f8fa"; AMBER="#c98a1a"

# Product value recovered per incident (keyed by the report "#" id) — entered manually
# from the guard recovery values (not captured in the incident xlsx export).
RECOVERIES_BY_ID = {32: 7.26, 31: 35.92, 29: 57.04, 28: 41.30, 26: 184.18}

def find(key):
    g = glob.glob(os.path.join(WEEK, f"*{key}*.xlsx"))
    return g[0] if g else None

def rows(fp):
    wb = openpyxl.load_workbook(fp, data_only=True); ws = wb.active
    rr = list(ws.iter_rows(values_only=True))
    hdr = [("" if h is None else str(h).strip()) for h in rr[0]]
    out = []
    for r in rr[1:]:
        if not any(v is not None and str(v).strip() for v in r): continue
        out.append({h: v for h, v in zip(hdr, r) if h})
    return out

def col(d, *cands):
    for k in d:
        for c in cands:
            if c.lower() in k.lower():
                return d[k]
    return None

def short_store(s):
    s = str(s or "")
    if "New Lynn" in s: return "New Lynn"
    if "Albany" in s: return "Albany"
    return s.replace("Mitre 10 MEGA", "").strip()

def hhmm(t):
    if isinstance(t, (datetime.datetime, datetime.time)):
        return t.strftime("%H:%M")
    return str(t or "")[:5]

def ddmm(d):
    if isinstance(d, datetime.datetime):
        return d.strftime("%d/%m")
    return str(d or "")[:5]

# ---------- parse ----------
inc = []
for d in rows(find("Guard Incident")):
    cat = str(col(d, "Incident Category") or "").strip()
    cause = col(d, "Cause/Reason for Intervention")
    if cat == "Deterrent":
        cause = col(d, "Type of Deterrent") or "Constant surveillance"
    elif cat == "Other":
        cause = col(d, "If other") or "Other"
    try:
        iid = int(float(d.get("#")))
    except (TypeError, ValueError):
        iid = None
    inc.append(dict(
        iid=iid,
        store=short_store(col(d, "Select Mitre 10 Site")),
        date=ddmm(col(d, "Date and Time of Incident - Date")),
        time=hhmm(col(d, "Date and Time of Incident - Time")),
        sev=col(d, "Incident Severity"),
        cat=cat,
        cause=str(cause or "—").strip(),
        vt=str(col(d, "Verbal Trespass") or "No").strip(),
        rec=RECOVERIES_BY_ID.get(iid, 0.0),
    ))
inc.sort(key=lambda x: (x["date"], x["time"]))

pkg = []
for d in rows(find("Recovered Packaging")):
    pkg.append(dict(
        store=short_store(col(d, "Select Mitre 10 Site")),
        date=ddmm(col(d, "Date and Time - Date") or col(d, "Date and Time - Timestamp")),
        aisles=str(col(d, "Select Location/Aisle") or "").strip(),
        cats=str(col(d, "General Product Categories") or "").strip(),
        val=float(col(d, "Receipt Value") or 0),
    ))
pkg.sort(key=lambda x: -x["val"])
PKG_TOTAL = sum(p["val"] for p in pkg)

assess = []
for d in rows(find("Store Assessment")):
    assess.append(dict(
        store=short_store(col(d, "select the store")),
        obs=str(col(d, "Description of observation") or "").strip(),
        urg=int(col(d, "urgency") or 3),
        rec=str(col(d, "next steps") or col(d, "Recomendations") or "").strip(),
    ))
assess.sort(key=lambda x: -x["urg"])

# ---------- metrics ----------
_order = {"New Lynn": 0, "Albany": 1}
stores = sorted(set([i["store"] for i in inc] + [p["store"] for p in pkg] + [a["store"] for a in assess]),
                key=lambda s: (_order.get(s, 9), s))
N = len(inc)
interv = sum(1 for i in inc if i["cat"] == "Intervention")
deter = sum(1 for i in inc if i["cat"] == "Deterrent")
other = sum(1 for i in inc if i["cat"] not in ("Intervention", "Deterrent"))
vt = sum(1 for i in inc if i["vt"].lower() == "yes")
INC_REC = sum(i["rec"] for i in inc)
TOTAL_REC = INC_REC + PKG_TOTAL
assess_store = assess[0]["store"] if assess else ""

def m(v): return f"${v:,.2f}"
logo = ""
if os.path.exists(LOGO):
    logo = f'<img src="data:image/png;base64,{base64.b64encode(open(LOGO,"rb").read()).decode()}" style="height:34px;opacity:.9"/>'

def kpi(l, v, c="#1f2933", s=""):
    sub = f'<div style="font-size:8.5px;color:{SUB}">{s}</div>' if s else ""
    return (f'<div style="flex:1"><div style="font-size:8.5px;color:{SUB};text-transform:uppercase;'
            f'letter-spacing:.6px">{l}</div><div style="font-size:21px;font-weight:700;color:{c};margin-top:2px">{v}</div>{sub}</div>')

TH = f'background:{CARD};color:{SUB};font-size:8.5px;text-transform:uppercase;letter-spacing:.5px;padding:6px 8px'
BASE = ("*{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}"
        "body{background:#fff;color:#1f2933;padding:24px 28px}table{width:100%;border-collapse:collapse;font-size:11px}"
        f"tbody tr{{border-bottom:1px solid {LINE}}}h2{{color:{ACC};font-size:13px;letter-spacing:.6px;margin:0 0 6px}}"
        f".lead{{color:{SUB};font-size:11px;line-height:1.5}}")

def inc_rows():
    o = ""
    for i in inc:
        catc = GREEN if i["cat"] == "Intervention" else (ACC if i["cat"] == "Deterrent" else SUB)
        reccell = m(i["rec"]) if i["rec"] else "—"
        o += (f'<tr><td style="padding:4px 8px">{i["date"]}, {i["time"]}</td>'
              f'<td style="padding:4px 8px;color:{SUB}">{i["store"]}</td>'
              f'<td style="text-align:center;color:{catc};font-weight:700">{i["cat"]}</td>'
              f'<td style="padding:4px 8px;color:{SUB}">{i["cause"]}</td>'
              f'<td style="text-align:center;color:{RED if i["vt"].lower()=="yes" else SUB};font-weight:{700 if i["vt"].lower()=="yes" else 400}">{i["vt"]}</td>'
              f'<td style="text-align:right;color:{GREEN if i["rec"] else SUB};font-weight:{600 if i["rec"] else 400}">{reccell}</td></tr>')
    o += (f'<tr style="border-top:2px solid {GREEN}"><td colspan="5" style="padding:6px 8px;font-weight:700">RECOVERED AT INCIDENTS</td>'
          f'<td style="text-align:right;font-weight:700;color:{GREEN}">{m(INC_REC)}</td></tr>')
    return o

def pkg_rows():
    o = ""
    for p in pkg:
        o += (f'<tr><td style="padding:4px 8px;color:{SUB}">{p["date"]}</td>'
              f'<td style="padding:4px 8px;color:{SUB}">{p["aisles"]}</td>'
              f'<td style="padding:4px 8px;color:{SUB};font-size:9.5px">{p["cats"]}</td>'
              f'<td style="text-align:right;color:{GREEN};font-weight:600">{m(p["val"])}</td></tr>')
    return o

storelist = " & ".join(stores)
HTML = f"""<html><head><meta charset='utf-8'><style>{BASE}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:21px;font-weight:800">MITRE 10 — WEEKLY COVERT LP REPORT</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">Mitre 10 MEGA {storelist} · SLS RTC Limited · {PERIOD}</div></div>
  {logo}</div>
<div style="display:flex;gap:6px;background:{CARD};border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
  {kpi("Stores", str(len(stores)), ACC)}{kpi("Incidents", str(N))}{kpi("Interventions", str(interv), GREEN)}{kpi("Verbal Trespasses", str(vt), RED if vt else "#1f2933")}{kpi("Recovered", m(INC_REC), GREEN, f"{sum(1 for i in inc if i['rec'])} incidents")}{kpi("Recovered Pkg", m(PKG_TOTAL), GREEN, f"{len(pkg)} finds")}{kpi("Total Recovered", m(TOTAL_REC), ACC)}</div>
<p class="lead">SLS RTC continued covert loss-prevention across <b>Mitre 10 MEGA {storelist}</b> this week. The team actioned <b>{N} incidents</b>
({interv} interventions, {deter} deterrent{'s' if deter!=1 else ''}{f', {other} other' if other else ''}), issued <b>{vt} verbal trespass notice{'s' if vt!=1 else ''}</b>,
recovered <b>{m(INC_REC)}</b> of product at incidents and a further <b>{m(PKG_TOTAL)}</b> of product packaging as theft evidence — <b>{m(TOTAL_REC)}</b> total — across the week,
all logged for submission into Auror. A covert store security assessment was completed at {assess_store} (see separate report).</p>
<div style="display:flex;gap:18px;margin-top:14px">
  <div style="flex:2.2"><h2>INCIDENT LOG</h2>
  <table><thead><tr><th style="{TH};text-align:left">Date/Time</th><th style="{TH};text-align:left">Store</th><th style="{TH};text-align:center">Category</th><th style="{TH};text-align:left">Cause</th><th style="{TH};text-align:center">Verbal Trespass</th><th style="{TH};text-align:right">Recovered</th></tr></thead><tbody>{inc_rows()}</tbody></table></div>
  <div style="flex:1.1"><h2 style="color:{GREEN}">RECOVERED PACKAGING — {m(PKG_TOTAL)}</h2>
  <table><thead><tr><th style="{TH};text-align:left">Date</th><th style="{TH};text-align:left">Aisles</th><th style="{TH};text-align:left">Categories</th><th style="{TH};text-align:right">Receipt Value</th></tr></thead><tbody>{pkg_rows()}
  <tr style="border-top:2px solid {GREEN}"><td colspan="3" style="padding:6px 8px;font-weight:700">TOTAL</td><td style="text-align:right;font-weight:700;color:{GREEN}">{m(PKG_TOTAL)}</td></tr></tbody></table></div></div>
<div style="margin-top:16px;background:{CARD};border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  <b style="color:{ACC}">Week 2 · scaling to two stores.</b> "Recovered" is the value of product recovered at the incident; "recovered packaging" is the receipt value of empty product packaging
  located in-aisle — quantified theft evidence. Both are logged to Auror (the cumulative offending record that builds the threshold for Police escalation). Interventions stop theft in
  progress; deterrents are surveillance-driven prevention. Source: SLS RTC covert LP reporting (Auror-linked incidents).</div>
</body></html>"""

# ---------- assessment ----------
def risk(u): return ("High", RED) if u >= 4 else (("Medium", AMBER) if u == 3 else ("Low", GREEN))
def acard(i, a):
    sv, c = risk(a["urg"])
    return f"""<div style="background:{CARD};border:1px solid {LINE};border-left:4px solid {c};border-radius:6px;padding:12px 15px;margin-bottom:10px">
      <div style="display:flex;justify-content:space-between"><div style="font-size:12px;font-weight:700;color:{ACC}">Finding {i}</div>
      <div style="font-size:9px;font-weight:700;color:{c};text-transform:uppercase">{sv} risk · urgency {a['urg']}/5</div></div>
      <div style="margin-top:6px;font-size:10.5px;color:{SUB}"><b style="color:#1f2933">Observation:</b> {a['obs']}</div>
      <div style="margin-top:4px;font-size:10.5px;color:{SUB}"><b style="color:{GREEN}">Recommended action:</b> {a['rec']}</div></div>"""

HTML2 = f"""<html><head><meta charset='utf-8'><style>{BASE}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:21px;font-weight:800">STORE SECURITY ASSESSMENT</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">Mitre 10 MEGA {assess_store} · SLS RTC Limited · {PERIOD}</div></div>
  {logo}</div>
<p style="color:{SUB};font-size:11px;line-height:1.5;margin:14px 0">During this week's covert deployment our team conducted a security assessment of {assess_store},
identifying the following vulnerabilities and recommended actions, ranked by urgency. Items rated 5/5 represent immediate, addressable loss exposure — including a legal-compliance gap.</p>
{''.join(acard(i+1, a) for i, a in enumerate(assess))}
<div style="margin-top:8px;background:{CARD};border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  Prepared by SLS RTC Limited from on-floor observations. We're happy to help implement these controls and re-assess after changes. Source: SLS RTC Mitre 10 store assessment submissions.</div>
</body></html>"""

# ---------- render ----------
def render(html, out):
    tmp = os.path.join(WEEK, "_tmp.html")
    open(tmp, "w").write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", "--no-margins", tmp], capture_output=True, timeout=90)
    os.remove(tmp)
    print("Wrote", out)

OUT1 = os.path.join(WEEK, f"{PREFIX}_LP_Report.pdf")
OUT2 = os.path.join(WEEK, f"{PREFIX}_Store_Assessment.pdf")
render(HTML, OUT1)
render(HTML2, OUT2)

# ---------- email docx ----------
from docx import Document
from docx.shared import Pt, RGBColor
doc = Document(); st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
def P(t, b=False, sz=11, c=None, sa=6):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(sa)
    r = p.add_run(t); r.bold = b; r.font.size = Pt(sz)
    if c: r.font.color.rgb = RGBColor(*c)
    return p
def B(t):
    p = doc.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(3); p.add_run(t)

P("To:        Mitre 10 — Loss Prevention", sa=0)
P("From:    SLS RTC Limited", sa=0)
P(f"Subject: Mitre 10 MEGA {storelist} — Covert LP Weekly Summary ({PERIOD})", b=True, c=(0x1f,0x3a,0x5f))
P("Hi team,")
P(f"Please find this week's covert loss-prevention summary across Mitre 10 MEGA {storelist}, with the supporting reports attached for "
  "submission into Auror — the platform where the cumulative record of offending is built, breaking the repeat-offender cycle and "
  "establishing the evidence threshold required for Police escalation.")
P("Week in brief", b=True, c=(0x1f,0x3a,0x5f), sa=4)
B(f"{N} incidents actioned ({interv} interventions, {deter} deterrent{'s' if deter!=1 else ''}{f', {other} staff-assist' if other else ''}), with {vt} verbal trespass notice{'s' if vt!=1 else ''} issued.")
B(f"{m(INC_REC)} of product recovered at incidents, plus {m(PKG_TOTAL)} of recovered packaging logged as theft evidence across {len(pkg)} finds — {m(TOTAL_REC)} total for the week.")
B(f"Coverage scaled to {assess_store} this week, with a covert store security assessment completed there.")
P("Store security assessment", b=True, c=(0x1f,0x3a,0x5f), sa=4)
high = [a for a in assess if a["urg"] >= 4]
P(f"Our team identified {len(assess)} addressable vulnerabilities at {assess_store}, {len(high)} rated 5/5 urgency — most notably "
  "insecure/unlocked paint cabinets (a legal-compliance gap), an insecure rear garden-centre gate with no EAS coverage, and unsecured "
  "team uniform items that could let an offender pass as staff. Full findings and recommended actions are in the attached assessment.")
P("Attached", b=True, c=(0x1f,0x3a,0x5f), sa=4)
B("Weekly LP Report — incident activity and recovered packaging for the week.")
B(f"Store Security Assessment — {assess_store} vulnerabilities and recommended actions.")
P("Happy to walk through the assessment findings on a quick call, and to assist with implementing the recommended controls.")
P("Many thanks,", sa=2)
P("Ahmad Duais — Director, SLS RTC Limited", sa=0)
P(f"Attachments: {os.path.basename(OUT1)} · {os.path.basename(OUT2)}", sz=9, c=(0x5b,0x64,0x72))
OUT3 = os.path.join(WEEK, f"{PREFIX}_Email_Summary.docx")
doc.save(OUT3); print("Wrote", OUT3)

print(f"\nSUMMARY: stores={stores} incidents={N} interv={interv} deter={deter} other={other} vt={vt} pkg={m(PKG_TOTAL)} ({len(pkg)}) assess={len(assess)}@{assess_store}")
