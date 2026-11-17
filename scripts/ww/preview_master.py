#!/usr/bin/env python3
"""Render the new master v2 sheets as a branded HTML preview -> PNG, to eyeball the look."""
import openpyxl, os
from datetime import datetime
from playwright.sync_api import sync_playwright

F = os.path.expanduser("~/Desktop/Woolworths /Woolworths Master Data FY27.xlsx")
OUT = "/tmp/ww_master_preview.png"
wb = openpyxl.load_workbook(F)


def cell(v):
    if isinstance(v, datetime):
        return v.strftime("%d %b")
    if isinstance(v, float):
        return f"{v:,.2f}" if abs(v) >= 100 or v != int(v) else f"{int(v):,}"
    if isinstance(v, int):
        return f"{v:,}"
    return "" if v is None else str(v)


def sheet_html(name, rmax=None):
    ws = wb[name]
    rmax = rmax or ws.max_row
    ncol = ws.max_column
    title = ws.cell(1, 1).value
    sub = ws.cell(2, 1).value
    rows = []
    for r in range(3, rmax + 1):
        tds = []
        first = ws.cell(r, 1).value
        is_reg = isinstance(first, str) and first.startswith("▍")
        is_grand = isinstance(first, str) and ("GRAND TOTAL" in first or "NETWORK" in first)
        is_hdr = (r == 3)
        for c in range(1, ncol + 1):
            v = cell(ws.cell(r, c).value)
            cls = "lab" if c == 1 else "num"
            lab = ws.cell(r, 1).value or ""
            if isinstance(lab, str) and "TOTAL LOSS" in lab:
                cls += " totalloss"
            tds.append(f'<td class="{cls}">{v}</td>')
        rcls = "hdr" if is_hdr else ("reg" if is_reg else ("grand" if is_grand else ""))
        if is_reg or is_grand:
            rows.append(f'<tr class="{rcls}"><td class="lab" colspan="{ncol}">{cell(first)}</td></tr>')
        else:
            rows.append(f'<tr class="{rcls}">{"".join(tds)}</tr>')
    return f'<div class="card"><div class="ttl">{title}</div><div class="sub">{sub}</div><table>{"".join(rows)}</table></div>'


html = f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Helvetica Neue',Arial,sans-serif;background:#eef2f6;padding:26px;color:#1f2733}}
.card{{background:#fff;border-radius:10px;box-shadow:0 2px 10px rgba(30,42,58,.10);margin-bottom:22px;overflow:hidden}}
.ttl{{background:#1E2A3A;color:#fff;font-size:15px;font-weight:700;padding:11px 16px}}
.sub{{color:#5A6675;font-size:10.5px;font-style:italic;padding:7px 16px 3px}}
table{{width:100%;border-collapse:collapse;font-size:11px}}
td{{padding:5px 10px;border-bottom:1px solid #eef1f5}}
td.lab{{text-align:left;color:#31404f}}
td.num{{text-align:right;color:#1f2733;font-variant-numeric:tabular-nums}}
tr.hdr td{{background:#1E2A3A;color:#fff;font-weight:700;text-align:center}}
tr.hdr td:first-child{{text-align:left}}
tr.reg td{{background:#D9E1EA;color:#1E2A3A;font-weight:700;font-size:11.5px}}
tr.grand td{{background:#C8952A;color:#1E2A3A;font-weight:800}}
td.totalloss{{background:#fbf3e2;font-weight:800;color:#1E2A3A}}
tr:hover td{{background:#f7fafc}}
h1{{font-size:16px;color:#1E2A3A;margin-bottom:16px;font-weight:800}}
</style></head><body>
<h1>Woolworths NZ — Master Data FY27 · from 01 Jul 2026 · region-grouped · self-reconciling</h1>
{sheet_html("National Summary")}
{sheet_html("Region Summary", rmax=25)}
{sheet_html("Reconciliation")}
{sheet_html("Store Comparison", rmax=22)}
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 1400}, device_scale_factor=2)
    pg.set_content(html, wait_until="networkidle")
    pg.screenshot(path=OUT, full_page=True)
    b.close()
print("wrote", OUT)
