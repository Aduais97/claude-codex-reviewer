#!/usr/bin/env python3
"""Convert a Connecteam roster-PRINT PDF ('Woolworths _NZ <dates>.pdf') into the
Schedule-Export shape the FY27 WW pipeline reads (Date, Start, End, Job, Users).

The pipeline aggregates hours BY STORE, so the guard (Users) is not needed for the
hours total — each shift block is assigned to a day by its x-position (7 day columns)
and paired with its store name and time range. Output hours = raw End-Start (deployment
window), matching how the value report / tracker compute hours.

Usage: python3 convert_roster_pdf_schedule.py "<roster.pdf>" "<out Schedule-Export.xlsx>" <YYYY> <MM/DD ... 7 day cols>
(day columns are auto-detected from the header, so usually just: <pdf> <out>)
"""
import sys, re, fitz, openpyxl

def convert(src, out):
    d = fitz.open(src)
    # day-column x-centres from the header date tokens (MM/DD) on page 1
    words = d[0].get_text("words")
    daytok = {}
    for w in words:
        m = re.fullmatch(r'(\d{2})/(\d{2})', w[4])
        if m:
            daytok[w[4]] = (w[0] + w[2]) / 2
    cols = sorted(daytok.items(), key=lambda kv: kv[1])   # [(MM/DD, xcentre), ...] left→right
    if len(cols) < 5:
        raise SystemExit(f"only {len(cols)} day columns found — not a standard roster print")
    # infer year from filename (e.g. ..._2026 ...) else current-ish
    ym = re.search(r'(20\d{2})', src)
    year = ym.group(1) if ym else '2026'

    def nearest_date(xc):
        mmdd = min(cols, key=lambda kv: abs(kv[1] - xc))[0]
        mm, dd = mmdd.split('/')
        return f"{mm}/{dd}/{year}"

    trex = re.compile(r'\b(\d{1,2})(?::(\d{2}))?\s*-\s*(\d{1,2})(?::(\d{2}))?\b')
    srex = re.compile(r"([A-Z][A-Za-z .'/&]+? Woolworths)\s*-")

    ob = openpyxl.Workbook(); ws = ob.active; ws.title = "Schedule"
    ws.append(["Date", "Start", "End", "Job", "Users"])
    n = 0
    for pg in d:
        for b in pg.get_text("blocks"):
            x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
            times = trex.findall(text)
            stores = srex.findall(text)
            if not times or not stores:
                continue
            date = nearest_date((x0 + x1) / 2)
            # pair times to stores in order (a cell may hold a split shift: 2 times + 2 stores)
            for i, t in enumerate(times):
                sh, sm, eh, em = t
                start = f"{int(sh)}:{sm or '00'}"
                end = f"{int(eh)}:{em or '00'}"
                store = (stores[i] if i < len(stores) else stores[-1]).strip()
                ws.append([date, start, end, store, ""])
                n += 1
    ob.save(out)
    print(f"wrote {n} shift rows -> {out}  ({len(cols)} day columns: {[c[0] for c in cols]})")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
