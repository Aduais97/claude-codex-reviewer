#!/usr/bin/env python3
"""The Warehouse Takanini — Store Hardening Recommendations (clean white, client-facing)."""
import asyncio, base64
from pathlib import Path
LOGO=Path.home()/"Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUTS=[Path.home()/"Desktop/WarehouseGroup/The Warehouse Takanini - Store Hardening Recommendations.pdf",
      Path.home()/"Desktop/SLS-RTC/Operations/The Warehouse/The Warehouse Takanini - Store Hardening Recommendations.pdf"]
ACC="#1f3a5f"; SUB="#5b6472"; LINE="#dfe3e8"; RED="#b23a3a"; GREEN="#1d7a4d"; CARD="#f6f8fa"
recs=[
 ("Self-service / checkout layout","Medium","The checkout lanes are not blocked, leaving an open exit path behind the self-service area.",
  "Block or redirect the gap behind self-service so the only exit is past a staffed/monitored point. Low-cost layout change with immediate effect on walk-outs."),
 ("Entry-door walk-out deterrent","High","The left entry door has no physical deterrent to customers walking out through it.",
  "Install one-way gates (“sharks-teeth” / anti-return) on the entry door so it cannot be used as an exit. A standard, high-impact control for big-box retail."),
 ("EAS tagging on televisions","High","TVs are merchandised in bulk on the shop floor. EAS soft tags are applied to the top of most boxes only, which frequently does not activate the antenna.",
  "Apply two EAS soft tags per box — one on each side — to maximise antenna activation. High-value stock that is a prime walk-out target."),
 ("Early-morning coverage","High","High-value walk-outs are a real and elevated risk in the early-morning period.",
  "Prioritise covert presence and floor coverage at and shortly after opening, when walk-out attempts peak and staffing is lightest."),
]
sev_c={"High":RED,"Medium":"#c98a1a","Low":SUB}
def card(t,sev,obs,rec,i):
    return f"""<div style="background:{CARD};border:1px solid {LINE};border-left:4px solid {sev_c[sev]};border-radius:6px;padding:12px 15px;margin-bottom:10px">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <div style="font-size:13px;font-weight:700;color:{ACC}">{i}. {t}</div>
        <div style="font-size:9px;font-weight:700;color:{sev_c[sev]};text-transform:uppercase">{sev} priority</div></div>
      <div style="margin-top:6px;font-size:10.5px;color:{SUB}"><b style="color:#1f2933">Observed:</b> {obs}</div>
      <div style="margin-top:4px;font-size:10.5px;color:{SUB}"><b style="color:{GREEN}">Recommendation:</b> {rec}</div></div>"""
logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
HTML=f"""<html><head><meta charset='utf-8'><style>*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:#fff;color:#1f2933;padding:26px 30px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:21px;font-weight:800">STORE HARDENING RECOMMENDATIONS</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">The Warehouse Takanini · SLS RTC Limited · Loss-Prevention Walkthrough, 17 June 2026</div></div>
  <img src="{logo}" style="height:34px;opacity:.9"/></div>
<p style="color:{SUB};font-size:11px;line-height:1.5;margin:14px 0">During our launch-week covert loss-prevention deployment, our team identified the following practical, low-cost measures to reduce walk-out loss. Recoveries and deterrents were already actioned on the floor during the visit; the items below address the underlying physical and process gaps that drive avoidable loss.</p>
{''.join(card(t,s,o,r,i+1) for i,(t,s,o,r) in enumerate(recs))}
<div style="margin-top:8px;background:{CARD};border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  Prepared by SLS RTC Limited following an on-site walkthrough. We are happy to assist with implementation (EAS tagging standards, gate/layout specification) and to re-assess after changes are made. Priorities reflect loss exposure observed on the day.</div>
</body></html>"""
async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); p=await b.new_page(); await p.set_content(HTML,wait_until="networkidle")
        for o in OUTS:
            o.parent.mkdir(parents=True,exist_ok=True)
            await p.pdf(path=str(o),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()
if __name__=="__main__":
    asyncio.run(render()); print("WROTE hardening one-pager (b) to WarehouseGroup + ops folder")
