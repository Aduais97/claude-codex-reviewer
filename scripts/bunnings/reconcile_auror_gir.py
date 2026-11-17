#!/usr/bin/env python3
"""Reconcile the Connecteam Guard Incident Report (our DB) against the Bunnings Auror
export (client DB) for a month. Join key = GIR 'Auror Report Number' (e.g. e2121493,
strip e/spaces/'(Partial)') -> Auror EVENTID (2121493). Reports matches, gaps both ways,
and value discrepancies so the two systems can be signed off as reconciled before reporting.

Usage: python3 reconcile_auror_gir.py <GIR.xlsx> <Events.csv> <YYYY-MM>
"""
import sys, re, csv, datetime, openpyxl
from collections import defaultdict

GIR, AUROR, MONTH = sys.argv[1], sys.argv[2], sys.argv[3]
YY, MM = int(MONTH.split("-")[0]), int(MONTH.split("-")[1])

def num(v):
    if v in (None, ""): return 0.0
    try: return float(str(v).replace(",", "").replace("$", "").strip())
    except: return 0.0
def pdate(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.date() if isinstance(v, datetime.datetime) else v
    s = str(v or "").split("T")[0].split(" ")[0].strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d/%m/%y"):
        try: return datetime.datetime.strptime(s, f).date()
        except: pass
    return None
def auror_key(v):
    """Normalise a GIR Auror Report Number to the bare Auror EVENTID digits."""
    m = re.search(r"e?\s*(\d{5,})", str(v or "").strip().lower())
    return m.group(1) if m else None

# ---- load GIR (resolve columns by header name; raw export offsets differ from the master) ----
wb = openpyxl.load_workbook(GIR, read_only=True, data_only=True); ws = wb.active
rows = list(ws.iter_rows(values_only=True)); H = [str(h or "").strip().lower() for h in rows[0]]
def gc(name):
    return next((i for i, h in enumerate(H) if name.lower() in h), None)
c_auror, c_date, c_site, c_reg = gc("auror report number"), gc("date and time of incident - date"), gc("bunnings site"), gc("region of site")
c_rec, c_stol, c_sev = gc("recovered reciept value"), gc("estimated stolen value"), gc("incident severity")
gir = []
for r in rows[1:]:
    d = pdate(r[c_date])
    if not d or d.year != YY or d.month != MM: continue
    gir.append({"key": auror_key(r[c_auror]), "raw_auror": str(r[c_auror] or "").strip(),
                "date": d, "site": str(r[c_site] or "").strip(),
                "rec": num(r[c_rec]), "stol": num(r[c_stol])})
wb.close()

# ---- load Auror events ----
arows = list(csv.reader(open(AUROR, newline="", encoding="utf-8-sig"))); AH = arows[0]
def ac(n): return AH.index(n)
OCC, EID, REPBY, RECV, TOTV, UNREC, STORE, ETYPE = (ac("OCCURREDAT"), ac("EVENTID"),
    ac("EVENTREPORTEDBYJOBTITLE"), ac("RECOVEREDVALUE"), ac("TOTALVALUE"),
    ac("UNRECOVEREDVALUE"), ac("STORENAME"), ac("EVENTTYPE"))
auror = {}
for r in arows[1:]:
    d = pdate(r[OCC])
    if not d or d.year != YY or d.month != MM: continue
    auror[str(r[EID]).strip()] = {"date": d, "rep": str(r[REPBY] or "").strip(),
        "rec": num(r[RECV]), "tot": num(r[TOTV]), "unrec": num(r[UNREC]),
        "store": str(r[STORE] or "").strip(), "type": str(r[ETYPE] or "").strip()}

def is_ours(rep): return "covert" in rep.lower() or "cover secur" in rep.lower()

# ---- reconcile ----
gir_keys = [g["key"] for g in gir]
gir_keyset = set(k for k in gir_keys if k)
auror_ids = set(auror)
auror_ours = {k for k, v in auror.items() if is_ours(v["rep"])}

matched = gir_keyset & auror_ids
gir_no_key = [g for g in gir if not g["key"]]
gir_unmatched = sorted(gir_keyset - auror_ids)
dupe_keys = sorted({k for k in gir_keys if k and gir_keys.count(k) > 1})
ours_not_in_gir = sorted(auror_ours - gir_keyset)

print(f"====== AUGUST {MONTH} — Connecteam GIR  vs  Bunnings Auror ======\n")
print(f"Connecteam GIR incidents (our DB)   : {len(gir)}")
print(f"  with a usable Auror number         : {len(gir_keyset)} unique ({len(gir_no_key)} blank/unparseable)")
print(f"  duplicate Auror numbers in GIR     : {len(dupe_keys)}  {dupe_keys[:8]}")
print(f"Auror events (client DB), all        : {len(auror)}")
print(f"  reported by OUR covert team        : {len(auror_ours)}")
print(f"  reported by store staff / other    : {len(auror) - len(auror_ours)}\n")
print(f"MATCHED (GIR number found in Auror)  : {len(matched)}  of {len(gir_keyset)} GIR numbers")
print(f"GIR numbers NOT found in Auror       : {len(gir_unmatched)}  {gir_unmatched[:12]}")
print(f"OUR Auror events NOT in Connecteam   : {len(ours_not_in_gir)}  {ours_not_in_gir[:12]}")

# ---- $ reconciliation on matched pairs ----
print("\n------ value reconciliation on matched pairs (GIR vs Auror) ------")
dr = dt = 0.0; badrec = []; badtot = []
gir_by_key = defaultdict(lambda: {"rec": 0.0, "stol": 0.0})
for g in gir:
    if g["key"]: gir_by_key[g["key"]]["rec"] += g["rec"]; gir_by_key[g["key"]]["stol"] += g["stol"]
for k in sorted(matched):
    grec, gid = gir_by_key[k]["rec"], gir_by_key[k]["rec"] + gir_by_key[k]["stol"]
    arec, atot = auror[k]["rec"], auror[k]["tot"]
    dr += grec - arec; dt += gid - atot
    if abs(grec - arec) > 0.5: badrec.append((k, grec, arec))
    if abs(gid - atot) > 0.5: badtot.append((k, gid, atot))
gtot_rec = sum(g["rec"] for g in gir); gtot_id = sum(g["rec"] + g["stol"] for g in gir)
atot_rec = sum(v["rec"] for v in auror.values()); atot_tot = sum(v["tot"] for v in auror.values())
print(f"GIR total (our DB)   : recovered ${gtot_rec:,.2f} | identified ${gtot_id:,.2f}  (all {len(gir)} rows)")
print(f"Auror total (client) : recovered ${atot_rec:,.2f} | total ${atot_tot:,.2f}       (all {len(auror)} events)")
print(f"matched-pair recovered $ diff (GIR-Auror): ${dr:,.2f}  | rows off >$0.50: {len(badrec)}")
print(f"matched-pair identified/total $ diff     : ${dt:,.2f}  | rows off >$0.50: {len(badtot)}")
if badrec[:6]: print("  sample recovered mismatches (key, GIR, Auror):", [(k, round(a,2), round(b,2)) for k,a,b in badrec[:6]])
if ours_not_in_gir:
    miss_val = sum(auror[k]["rec"] for k in ours_not_in_gir)
    print(f"\n  ⚠ {len(ours_not_in_gir)} covert Auror events missing from Connecteam carry ${miss_val:,.2f} recovered — GIR under-reports these.")
