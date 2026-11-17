#!/usr/bin/env python3
"""
SLS RTC Guard Deployment Hours vs Recovery Performance Analysis
Period: January - April 2026

Cross-references timeclock hours data against GIR recovery data
to calculate per-guard ROI, per-store ROI, margin analysis,
and the "lazy reporter" test.
"""

import openpyxl
from datetime import datetime
from collections import defaultdict
import os
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths
WW_TIMECLOCK = '/Users/ahmadduais/Downloads/timeclock-timesheet_overview_2026-01-01_2026-04-30 (1).xlsx'
BUN_TIMECLOCK = '/Users/ahmadduais/Downloads/timeclock-timesheet_overview_2026-01-01_2026-04-30.xlsx'
WW_GIR_FY = '/Users/ahmadduais/Downloads/Woolworths _ Guard Incident Report_66c490e7-0ae6-492b-a579-ff6b7848e3cb.xlsx'
WW_GIR_CURRENT = '/Users/ahmadduais/Downloads/Woolworths _ Guard Incident Report_2e6e169c-463f-4c3f-b882-f5998b157ff2.xlsx'
BUN_GIR = '/Users/ahmadduais/Downloads/Bunnings _ Guard Incident Report _93467dba-f520-495a-858d-6e18a669e4c6.xlsx'
OUTPUT_FILE = '/Users/ahmadduais/Desktop/SLS-RTC/analysis_hours_vs_recovery.txt'

# Billing rates (client rates)
BUN_CLIENT_RATE = 43.00
WW_STANDARD_RATE = 42.10
WW_SENIOR_RATE = 45.00

# Management exclusions
MANAGEMENT_EXCLUSIONS = {'ahmad duais', 'hasi nabawi', 'mark clansey', 'graham zuill'}

# Date filter: Jan-Apr 2026
DATE_START = datetime(2026, 1, 1)
DATE_END = datetime(2026, 4, 30, 23, 59, 59)

# Name normalisation map
NAME_FIXES = {
    'james taylor': 'James Taylor',
    'simmerjit  singh brar': 'Simmerjit Singh Brar',
    'siositeni  maka': 'Siositeni Maka',
    'viliami  fangaiuiha': 'Viliami Fangaiuiha',
    'nirajkumar katwala': 'NirajKumar Katwala',
    'ben connerk': 'Ben Conner',
    'charlie  maka': 'Charlie Maka',
    'bernie  glasgow': 'Bernie Glasgow',
    'jake  webby': 'Jake Webby',
    'kesinova  isoa': 'Kesinova Isoa',
    'adam  sabetian': 'Adam Sabetian',
    'sekai  meleisea': 'Sekai Meleisea',
    'nick  dalton': 'Nick Dalton',
    'fonglee  leolahi': 'Fonglee Leolahi',
    'jahzykeah  papalii': 'Jahzykeah Papalii',
    'awadalla  osman': 'Awadalla Osman',
    'tanielu sam tusi  vagaia': 'Tanielu Sam Tusi Vagaia',
    'sanaul  elahi': 'Sanaul Elahi',
}

# WW Senior guard hourly rate threshold (from timeclock data)
# Guards paid >= $29 are seniors (billing at $45/hr to client)
WW_SENIOR_PAY_THRESHOLD = 29.0

# Default pay rate for guards with missing rate data
DEFAULT_WW_PAY_RATE = 27.0  # median of observed rates


def normalise_name(raw_name):
    """Normalise a guard name: strip, collapse spaces, apply fixes."""
    if not raw_name:
        return ''
    name = str(raw_name).strip()
    # Lowercase for lookup
    name_lower = name.lower()
    # Check direct fix map first (with original spacing for double-space matches)
    if name_lower in NAME_FIXES:
        return NAME_FIXES[name_lower]
    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name)
    name_lower = name.lower()
    if name_lower in NAME_FIXES:
        return NAME_FIXES[name_lower]
    # Title case each word but preserve special cases like NirajKumar
    if name_lower == 'nirajkumar katwala':
        return 'NirajKumar Katwala'
    # Standard title case
    parts = name.split()
    result = ' '.join(p.capitalize() if p.islower() or p.isupper() else p for p in parts)
    return result


def safe_float(val):
    """Convert value to float, returning 0.0 for empty/None."""
    if val is None or val == '':
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def is_in_date_range(dt):
    """Check if datetime is in Jan-Apr 2026."""
    if not isinstance(dt, datetime):
        return False
    return DATE_START <= dt <= DATE_END


def is_travel(store_name):
    """Check if store name indicates travel."""
    if not store_name:
        return False
    return 'travel' in str(store_name).lower()


def is_excluded(name):
    """Check if guard is management exclusion."""
    return name.lower() in MANAGEMENT_EXCLUSIONS


# =============================================================================
# DATA STRUCTURES
# =============================================================================

# Per-guard data
guard_data = defaultdict(lambda: {
    'ww_hours': 0.0,
    'ww_pay_rate': 0.0,  # guard's hourly pay
    'ww_client_rate': 0.0,  # what client pays per hour
    'ww_recovered': 0.0,
    'ww_stolen': 0.0,
    'ww_incidents': 0,
    'bun_hours': 0.0,
    'bun_pay_rate': 0.0,
    'bun_recovered': 0.0,
    'bun_stolen': 0.0,
    'bun_incidents': 0,
    'ww_stores': defaultdict(float),   # store -> hours
    'bun_stores': defaultdict(float),  # store -> hours
})

# Per-store data
store_data = defaultdict(lambda: {
    'client': '',
    'guard_hours': 0.0,
    'cost': 0.0,  # billing cost to client
    'recovered': 0.0,
    'stolen': 0.0,
    'incidents': 0,
    'guards': set(),
})

# =============================================================================
# 1. LOAD WW TIMECLOCK
# =============================================================================
print("Loading WW timeclock...")
wb = openpyxl.load_workbook(WW_TIMECLOCK, read_only=True, data_only=True)
ws = wb.active

current_guard = None
current_rate = 0.0
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue  # header

    fname = str(row[0]).strip() if row[0] else ''
    lname = str(row[1]).strip() if row[1] else ''

    if fname or lname:
        full = f'{fname} {lname}'.strip()
        current_guard = normalise_name(full)
        # Get pay rate from first named row
        rate_val = safe_float(row[27])
        if rate_val > 0:
            current_rate = rate_val
        else:
            current_rate = 0.0

    if not current_guard or is_excluded(current_guard):
        continue

    store = str(row[15]).strip() if row[15] else ''
    if is_travel(store) or not store:
        continue

    start_date = row[17]
    if not is_in_date_range(start_date):
        continue

    hours = safe_float(row[26])
    if hours <= 0:
        continue

    # Determine hourly rate for this row (may differ row-to-row, use row value if available)
    row_rate = safe_float(row[27])
    if row_rate > 0:
        pay_rate = row_rate
    elif current_rate > 0:
        pay_rate = current_rate
    else:
        pay_rate = DEFAULT_WW_PAY_RATE

    # Determine client billing rate based on pay rate
    if pay_rate >= WW_SENIOR_PAY_THRESHOLD:
        client_rate = WW_SENIOR_RATE
    else:
        client_rate = WW_STANDARD_RATE

    gd = guard_data[current_guard]
    gd['ww_hours'] += hours
    if gd['ww_pay_rate'] == 0:
        gd['ww_pay_rate'] = pay_rate
    if gd['ww_client_rate'] == 0:
        gd['ww_client_rate'] = client_rate
    gd['ww_stores'][store] += hours

    # Store data
    sd = store_data[store]
    sd['client'] = 'Woolworths'
    sd['guard_hours'] += hours
    sd['cost'] += hours * client_rate
    sd['guards'].add(current_guard)

wb.close()
print(f"  Loaded WW timeclock: {len([g for g, d in guard_data.items() if d['ww_hours'] > 0])} guards with hours")

# =============================================================================
# 2. LOAD BUNNINGS TIMECLOCK
# =============================================================================
print("Loading Bunnings timeclock...")
wb = openpyxl.load_workbook(BUN_TIMECLOCK, read_only=True, data_only=True)
ws = wb.active

current_guard = None
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue

    fname = str(row[0]).strip() if row[0] else ''
    lname = str(row[1]).strip() if row[1] else ''

    if fname or lname:
        full = f'{fname} {lname}'.strip()
        current_guard = normalise_name(full)

    if not current_guard or is_excluded(current_guard):
        continue

    store = str(row[2]).strip() if row[2] else ''
    if is_travel(store) or not store:
        continue
    # Skip non-Bunnings entries (e.g. "HEAD OFFICE SLSRTC", "Mount Wellington Woolworths")
    if 'bunnings' not in store.lower():
        continue

    start_date = row[4]
    if not is_in_date_range(start_date):
        continue

    hours = safe_float(row[12])
    if hours <= 0:
        continue

    gd = guard_data[current_guard]
    gd['bun_hours'] += hours
    gd['bun_stores'][store] += hours

    # For Bunnings pay rate, use the WW rate if we have it (same guard works both)
    # Otherwise use a reasonable default
    if gd['bun_pay_rate'] == 0 and gd['ww_pay_rate'] > 0:
        gd['bun_pay_rate'] = gd['ww_pay_rate']

    # Store data
    sd = store_data[store]
    sd['client'] = 'Bunnings'
    sd['guard_hours'] += hours
    sd['cost'] += hours * BUN_CLIENT_RATE
    sd['guards'].add(current_guard)

wb.close()

# Set Bunnings pay rates for guards who only have Bunnings data
for gname, gd in guard_data.items():
    if gd['bun_hours'] > 0 and gd['bun_pay_rate'] == 0:
        if gd['ww_pay_rate'] > 0:
            gd['bun_pay_rate'] = gd['ww_pay_rate']
        else:
            gd['bun_pay_rate'] = DEFAULT_WW_PAY_RATE

print(f"  Loaded Bunnings timeclock: {len([g for g, d in guard_data.items() if d['bun_hours'] > 0])} guards with hours")

# =============================================================================
# 3. LOAD WW GIR DATA (deduplicated from FY + Current)
# =============================================================================
print("Loading WW GIR data (FY file + Current file, deduped)...")

# First load FY file (master set)
ww_incidents_set = set()  # (name_normalised, date_str, region) for dedup
ww_incident_records = []  # list of (guard, date, recovered, stolen, store)

wb = openpyxl.load_workbook(WW_GIR_FY, read_only=True, data_only=True)
ws = wb.active
fy_count = 0
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue
    name_raw = row[1]
    date_val = row[4]
    recovered = safe_float(row[60])
    stolen = safe_float(row[71])
    region = str(row[6]).strip() if row[6] else ''
    store = str(row[7]).strip() if row[7] else ''

    if not name_raw or not isinstance(date_val, datetime):
        continue
    if not is_in_date_range(date_val):
        continue

    guard = normalise_name(name_raw)
    if is_excluded(guard):
        continue

    date_str = date_val.strftime('%Y-%m-%d %H:%M')
    dedup_key = (guard.lower(), date_str, region.lower())
    ww_incidents_set.add(dedup_key)
    ww_incident_records.append((guard, date_val, recovered, stolen, store))
    fy_count += 1

wb.close()
print(f"  FY file: {fy_count} incidents in Jan-Apr 2026")

# Now load Current file (dedup against FY)
wb = openpyxl.load_workbook(WW_GIR_CURRENT, read_only=True, data_only=True)
ws = wb.active
cur_count = 0
cur_deduped = 0
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue
    name_raw = row[1]
    date_val = row[4]
    recovered = safe_float(row[55])
    stolen = safe_float(row[62])
    region = str(row[6]).strip() if row[6] else ''
    store = str(row[7]).strip() if row[7] else ''

    if not name_raw or not isinstance(date_val, datetime):
        continue
    if not is_in_date_range(date_val):
        continue

    guard = normalise_name(name_raw)
    if is_excluded(guard):
        continue

    date_str = date_val.strftime('%Y-%m-%d %H:%M')
    dedup_key = (guard.lower(), date_str, region.lower())

    if dedup_key in ww_incidents_set:
        cur_deduped += 1
        continue

    ww_incidents_set.add(dedup_key)
    ww_incident_records.append((guard, date_val, recovered, stolen, store))
    cur_count += 1

wb.close()
print(f"  Current file: {cur_count} new incidents added, {cur_deduped} duplicates skipped")

# Assign WW incidents to guards and stores
for guard, date_val, recovered, stolen, store in ww_incident_records:
    gd = guard_data[guard]
    gd['ww_incidents'] += 1
    gd['ww_recovered'] += recovered
    gd['ww_stolen'] += stolen

    if store:
        sd = store_data[store]
        if not sd['client']:
            sd['client'] = 'Woolworths'
        sd['recovered'] += recovered
        sd['stolen'] += stolen
        sd['incidents'] += 1

print(f"  Total WW incidents (deduped): {len(ww_incident_records)}")

# =============================================================================
# 4. LOAD BUNNINGS GIR DATA
# =============================================================================
print("Loading Bunnings GIR data...")
wb = openpyxl.load_workbook(BUN_GIR, read_only=True, data_only=True)
ws = wb.active
bun_count = 0
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue
    name_raw = row[1]
    date_val = row[6]
    recovered = safe_float(row[14])
    stolen = safe_float(row[15])
    store = str(row[9]).strip() if row[9] else ''

    if not name_raw or not isinstance(date_val, datetime):
        continue
    if not is_in_date_range(date_val):
        continue

    guard = normalise_name(name_raw)
    if is_excluded(guard):
        continue

    gd = guard_data[guard]
    gd['bun_incidents'] += 1
    gd['bun_recovered'] += recovered
    gd['bun_stolen'] += stolen
    bun_count += 1

    if store:
        sd = store_data[store]
        if not sd['client']:
            sd['client'] = 'Bunnings'
        sd['recovered'] += recovered
        sd['stolen'] += stolen
        sd['incidents'] += 1

wb.close()
print(f"  Bunnings GIR: {bun_count} incidents in Jan-Apr 2026")

# =============================================================================
# FIX: Set pay rates for guards who only appear in GIR but not timeclock
# =============================================================================
for gname, gd in guard_data.items():
    if gd['ww_pay_rate'] == 0 and gd['ww_hours'] == 0 and gd['ww_incidents'] > 0:
        gd['ww_pay_rate'] = DEFAULT_WW_PAY_RATE
        gd['ww_client_rate'] = WW_STANDARD_RATE
    if gd['bun_pay_rate'] == 0 and gd['bun_hours'] == 0 and gd['bun_incidents'] > 0:
        gd['bun_pay_rate'] = DEFAULT_WW_PAY_RATE

# =============================================================================
# CALCULATE DERIVED METRICS
# =============================================================================
print("\nCalculating metrics...")

results = []
for gname, gd in guard_data.items():
    total_hours = gd['ww_hours'] + gd['bun_hours']
    total_incidents = gd['ww_incidents'] + gd['bun_incidents']
    total_recovered = gd['ww_recovered'] + gd['bun_recovered']
    total_stolen = gd['ww_stolen'] + gd['bun_stolen']

    # Cost to company (hours x guard pay rate)
    ww_cost = gd['ww_hours'] * gd['ww_pay_rate'] if gd['ww_pay_rate'] > 0 else gd['ww_hours'] * DEFAULT_WW_PAY_RATE
    bun_cost = gd['bun_hours'] * gd['bun_pay_rate'] if gd['bun_pay_rate'] > 0 else gd['bun_hours'] * DEFAULT_WW_PAY_RATE
    total_cost = ww_cost + bun_cost

    # Revenue (hours x client billing rate)
    ww_client_rate = gd['ww_client_rate'] if gd['ww_client_rate'] > 0 else WW_STANDARD_RATE
    ww_revenue = gd['ww_hours'] * ww_client_rate
    bun_revenue = gd['bun_hours'] * BUN_CLIENT_RATE
    total_revenue = ww_revenue + bun_revenue

    # Gross margin
    gross_margin = total_revenue - total_cost
    margin_pct = (gross_margin / total_revenue * 100) if total_revenue > 0 else 0

    # ROI metrics
    guard_roi = (total_recovered / total_cost) if total_cost > 0 else 0
    client_roi = (total_recovered / total_revenue) if total_revenue > 0 else 0

    # Incidents per 100 hours
    incidents_per_100h = (total_incidents / total_hours * 100) if total_hours > 0 else 0

    results.append({
        'name': gname,
        'ww_hours': gd['ww_hours'],
        'ww_pay_rate': gd['ww_pay_rate'],
        'ww_client_rate': ww_client_rate,
        'ww_recovered': gd['ww_recovered'],
        'ww_stolen': gd['ww_stolen'],
        'ww_incidents': gd['ww_incidents'],
        'bun_hours': gd['bun_hours'],
        'bun_pay_rate': gd['bun_pay_rate'],
        'bun_recovered': gd['bun_recovered'],
        'bun_stolen': gd['bun_stolen'],
        'bun_incidents': gd['bun_incidents'],
        'total_hours': total_hours,
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'total_recovered': total_recovered,
        'total_stolen': total_stolen,
        'total_incidents': total_incidents,
        'gross_margin': gross_margin,
        'margin_pct': margin_pct,
        'guard_roi': guard_roi,
        'client_roi': client_roi,
        'incidents_per_100h': incidents_per_100h,
    })

# =============================================================================
# OUTPUT
# =============================================================================

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, 'w') as f:
    def w(line=''):
        f.write(line + '\n')

    w('=' * 120)
    w('SLS RTC -- GUARD DEPLOYMENT HOURS vs RECOVERY PERFORMANCE')
    w(f'Analysis Period: January - April 2026')
    w(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    w('=' * 120)

    # -----------------------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------------------
    guards_with_hours = [r for r in results if r['total_hours'] > 0]
    guards_with_incidents = [r for r in results if r['total_incidents'] > 0]
    total_all_hours = sum(r['total_hours'] for r in results)
    total_all_revenue = sum(r['total_revenue'] for r in results)
    total_all_cost = sum(r['total_cost'] for r in results)
    total_all_recovered = sum(r['total_recovered'] for r in results)
    total_all_stolen = sum(r['total_stolen'] for r in results)
    total_all_incidents = sum(r['total_incidents'] for r in results)
    total_all_margin = total_all_revenue - total_all_cost

    w()
    w('EXECUTIVE SUMMARY')
    w('-' * 120)
    w(f'  Total guards deployed (with hours):      {len(guards_with_hours)}')
    w(f'  Total guards with incidents:              {len(guards_with_incidents)}')
    w(f'  Total guard-hours worked:                 {total_all_hours:,.1f}')
    w(f'  Total client revenue (invoiced):          ${total_all_revenue:,.2f}')
    w(f'  Total guard cost (payroll):               ${total_all_cost:,.2f}')
    w(f'  Total gross margin:                       ${total_all_margin:,.2f} ({total_all_margin/total_all_revenue*100:.1f}%)')
    w(f'  Total recovered $:                        ${total_all_recovered:,.2f}')
    w(f'  Total stolen (reported):                  ${total_all_stolen:,.2f}')
    w(f'  Total incidents:                          {total_all_incidents}')
    w(f'  Overall client ROI (recovered/invoiced):  {total_all_recovered/total_all_revenue:.2f}x' if total_all_revenue > 0 else '')
    w(f'  Overall guard ROI (recovered/cost):       {total_all_recovered/total_all_cost:.2f}x' if total_all_cost > 0 else '')
    w(f'  Incidents per 100 guard-hours:            {total_all_incidents/total_all_hours*100:.1f}' if total_all_hours > 0 else '')

    # -----------------------------------------------------------------
    # SECTION 1: PER-GUARD COMBINED ROI (sorted by client ROI desc)
    # -----------------------------------------------------------------
    w()
    w()
    w('=' * 120)
    w('SECTION 1: PER-GUARD COMBINED ROI (Jan-Apr 2026)')
    w('Sorted by Client ROI (recovered $ / invoiced $) descending')
    w('=' * 120)

    sorted_roi = sorted([r for r in results if r['total_hours'] > 0 or r['total_incidents'] > 0],
                        key=lambda x: x['client_roi'], reverse=True)

    w()
    w(f'{"Guard":<25} {"WW Hrs":>8} {"WW Rec$":>10} {"WW Inc":>6} '
      f'{"BUN Hrs":>8} {"BUN Rec$":>10} {"BUN Inc":>7} '
      f'{"Tot Hrs":>8} {"Cost$":>10} {"Rev$":>10} {"Rec$":>10} '
      f'{"G-ROI":>7} {"C-ROI":>7} {"Inc/100h":>8}')
    w('-' * 155)

    for r in sorted_roi:
        w(f'{r["name"]:<25} '
          f'{r["ww_hours"]:>8.1f} '
          f'{r["ww_recovered"]:>10,.2f} '
          f'{r["ww_incidents"]:>6} '
          f'{r["bun_hours"]:>8.1f} '
          f'{r["bun_recovered"]:>10,.2f} '
          f'{r["bun_incidents"]:>7} '
          f'{r["total_hours"]:>8.1f} '
          f'{r["total_cost"]:>10,.2f} '
          f'{r["total_revenue"]:>10,.2f} '
          f'{r["total_recovered"]:>10,.2f} '
          f'{r["guard_roi"]:>7.2f}x '
          f'{r["client_roi"]:>6.2f}x '
          f'{r["incidents_per_100h"]:>8.1f}')

    w()
    w(f'{"TOTAL":<25} '
      f'{sum(r["ww_hours"] for r in sorted_roi):>8.1f} '
      f'{sum(r["ww_recovered"] for r in sorted_roi):>10,.2f} '
      f'{sum(r["ww_incidents"] for r in sorted_roi):>6} '
      f'{sum(r["bun_hours"] for r in sorted_roi):>8.1f} '
      f'{sum(r["bun_recovered"] for r in sorted_roi):>10,.2f} '
      f'{sum(r["bun_incidents"] for r in sorted_roi):>7} '
      f'{sum(r["total_hours"] for r in sorted_roi):>8.1f} '
      f'{sum(r["total_cost"] for r in sorted_roi):>10,.2f} '
      f'{sum(r["total_revenue"] for r in sorted_roi):>10,.2f} '
      f'{sum(r["total_recovered"] for r in sorted_roi):>10,.2f}')

    # Detailed breakdown for each guard
    w()
    w()
    w('--- DETAILED GUARD BREAKDOWN ---')
    for r in sorted_roi:
        if r['total_hours'] == 0 and r['total_incidents'] == 0:
            continue
        w()
        w(f'  {r["name"]}')
        w(f'    WW:  {r["ww_hours"]:.1f} hrs @ ${r["ww_pay_rate"]:.2f}/hr pay, ${r["ww_client_rate"]:.2f}/hr bill | '
          f'Recovered: ${r["ww_recovered"]:,.2f} | Stolen: ${r["ww_stolen"]:,.2f} | Incidents: {r["ww_incidents"]}')
        w(f'    BUN: {r["bun_hours"]:.1f} hrs @ ${r["bun_pay_rate"]:.2f}/hr pay, ${BUN_CLIENT_RATE:.2f}/hr bill | '
          f'Recovered: ${r["bun_recovered"]:,.2f} | Stolen: ${r["bun_stolen"]:,.2f} | Incidents: {r["bun_incidents"]}')
        w(f'    COMBINED: {r["total_hours"]:.1f} hrs | Cost: ${r["total_cost"]:,.2f} | Rev: ${r["total_revenue"]:,.2f} | '
          f'Margin: ${r["gross_margin"]:,.2f} ({r["margin_pct"]:.1f}%)')
        w(f'    Guard ROI: {r["guard_roi"]:.2f}x | Client ROI: {r["client_roi"]:.2f}x | '
          f'Incidents/100h: {r["incidents_per_100h"]:.1f}')

    # -----------------------------------------------------------------
    # SECTION 2: PER-STORE ROI
    # -----------------------------------------------------------------
    w()
    w()
    w('=' * 120)
    w('SECTION 2: PER-STORE ROI (All Stores, Both Clients)')
    w('ROI = Recovered $ / Billing Cost')
    w('FLAG: Stores with ROI < 0.20 (spending $5+ for every $1 recovered)')
    w('=' * 120)

    store_results = []
    for sname, sd in store_data.items():
        roi = (sd['recovered'] / sd['cost']) if sd['cost'] > 0 else 0
        flag = 'LOW ROI' if roi < 0.20 and sd['cost'] > 0 else ''
        store_results.append({
            'name': sname,
            'client': sd['client'],
            'hours': sd['guard_hours'],
            'cost': sd['cost'],
            'recovered': sd['recovered'],
            'stolen': sd['stolen'],
            'incidents': sd['incidents'],
            'roi': roi,
            'flag': flag,
            'guards': len(sd['guards']),
        })

    store_results.sort(key=lambda x: x['roi'], reverse=True)

    w()
    w(f'{"Store":<40} {"Client":<10} {"Hours":>8} {"Cost$":>12} {"Rec$":>10} {"Stolen$":>10} {"Inc":>5} {"ROI":>7} {"#Grd":>5} {"Flag":<10}')
    w('-' * 130)

    for sr in store_results:
        if sr['hours'] > 0 or sr['incidents'] > 0:
            w(f'{sr["name"]:<40} '
              f'{sr["client"]:<10} '
              f'{sr["hours"]:>8.1f} '
              f'{sr["cost"]:>12,.2f} '
              f'{sr["recovered"]:>10,.2f} '
              f'{sr["stolen"]:>10,.2f} '
              f'{sr["incidents"]:>5} '
              f'{sr["roi"]:>7.3f} '
              f'{sr["guards"]:>5} '
              f'{sr["flag"]:<10}')

    # Summary: flagged stores
    flagged = [sr for sr in store_results if sr['flag'] and sr['hours'] > 0]
    w()
    w(f'Flagged stores (ROI < 0.20): {len(flagged)} of {len([s for s in store_results if s["hours"] > 0])} stores with hours')
    if flagged:
        w()
        for sr in sorted(flagged, key=lambda x: x['roi']):
            w(f'  ** {sr["name"]}: ROI={sr["roi"]:.3f}, Cost=${sr["cost"]:,.2f}, Recovered=${sr["recovered"]:,.2f}, '
              f'Incidents={sr["incidents"]}')

    # -----------------------------------------------------------------
    # SECTION 3: MARGIN ANALYSIS PER GUARD
    # -----------------------------------------------------------------
    w()
    w()
    w('=' * 120)
    w('SECTION 3: MARGIN ANALYSIS PER GUARD')
    w('Revenue = Hours x Client Rate | Cost = Hours x Guard Pay Rate')
    w('=' * 120)

    margin_sorted = sorted([r for r in results if r['total_hours'] > 0],
                           key=lambda x: x['gross_margin'], reverse=True)

    w()
    w(f'{"RANK BY MARGIN":<5}')
    w(f'{"#":>3} {"Guard":<25} {"Hours":>8} {"Revenue$":>12} {"Cost$":>12} {"Margin$":>12} {"Margin%":>8} {"Rec$":>10} {"Rec/Hr":>8}')
    w('-' * 110)

    for rank, r in enumerate(margin_sorted, 1):
        rec_per_hr = r['total_recovered'] / r['total_hours'] if r['total_hours'] > 0 else 0
        w(f'{rank:>3} '
          f'{r["name"]:<25} '
          f'{r["total_hours"]:>8.1f} '
          f'{r["total_revenue"]:>12,.2f} '
          f'{r["total_cost"]:>12,.2f} '
          f'{r["gross_margin"]:>12,.2f} '
          f'{r["margin_pct"]:>7.1f}% '
          f'{r["total_recovered"]:>10,.2f} '
          f'{rec_per_hr:>8.2f}')

    w()
    w(f'{"":>3} '
      f'{"TOTAL":<25} '
      f'{sum(r["total_hours"] for r in margin_sorted):>8.1f} '
      f'{sum(r["total_revenue"] for r in margin_sorted):>12,.2f} '
      f'{sum(r["total_cost"] for r in margin_sorted):>12,.2f} '
      f'{sum(r["gross_margin"] for r in margin_sorted):>12,.2f} '
      f'{"":>8} '
      f'{sum(r["total_recovered"] for r in margin_sorted):>10,.2f}')

    # Rank by recovery
    w()
    w()
    recovery_sorted = sorted([r for r in results if r['total_hours'] > 0],
                             key=lambda x: x['total_recovered'], reverse=True)

    w(f'{"RANK BY RECOVERY":<5}')
    w(f'{"#":>3} {"Guard":<25} {"Hours":>8} {"Rec$":>12} {"Rec/Hr":>8} {"Inc":>5} {"Inc/100h":>8} {"Margin$":>12}')
    w('-' * 95)

    for rank, r in enumerate(recovery_sorted, 1):
        rec_per_hr = r['total_recovered'] / r['total_hours'] if r['total_hours'] > 0 else 0
        w(f'{rank:>3} '
          f'{r["name"]:<25} '
          f'{r["total_hours"]:>8.1f} '
          f'{r["total_recovered"]:>12,.2f} '
          f'{rec_per_hr:>8.2f} '
          f'{r["total_incidents"]:>5} '
          f'{r["incidents_per_100h"]:>8.1f} '
          f'{r["gross_margin"]:>12,.2f}')

    # Margin vs Recovery rank comparison
    w()
    w()
    w('--- MARGIN RANK vs RECOVERY RANK COMPARISON ---')
    w(f'{"Guard":<25} {"Margin Rank":>12} {"Recovery Rank":>14} {"Delta":>7} {"Assessment":<30}')
    w('-' * 95)

    margin_ranks = {r['name']: i+1 for i, r in enumerate(margin_sorted)}
    recovery_ranks = {r['name']: i+1 for i, r in enumerate(recovery_sorted)}

    for r in margin_sorted:
        m_rank = margin_ranks[r['name']]
        r_rank = recovery_ranks[r['name']]
        delta = m_rank - r_rank
        if delta > 5:
            assessment = "HIGH MARGIN, LOW RECOVERY"
        elif delta < -5:
            assessment = "LOW MARGIN, HIGH RECOVERY"
        elif r['total_recovered'] == 0 and r['total_hours'] > 100:
            assessment = "ZERO RECOVERY - INVESTIGATE"
        elif r['client_roi'] > 1.0:
            assessment = "CLIENT ROI POSITIVE"
        else:
            assessment = ""
        w(f'{r["name"]:<25} {m_rank:>12} {r_rank:>14} {delta:>+7} {assessment:<30}')

    # -----------------------------------------------------------------
    # SECTION 4: THE "LAZY REPORTER" TEST
    # -----------------------------------------------------------------
    w()
    w()
    w('=' * 120)
    w('SECTION 4: THE "LAZY REPORTER" TEST')
    w('Incidents Reported per 100 Hours Worked')
    w('=' * 120)

    # Only guards with meaningful hours (>= 50 hours in period)
    active_guards = [r for r in results if r['total_hours'] >= 50]

    if active_guards:
        # Calculate percentiles for bucketing
        rates = sorted([r['incidents_per_100h'] for r in active_guards])
        n = len(rates)
        p25 = rates[n // 4] if n >= 4 else rates[0]
        p75 = rates[3 * n // 4] if n >= 4 else rates[-1]
        median_rate = rates[n // 2]

        # Buckets
        high_threshold = p75
        low_threshold = p25

        w()
        w(f'  Active guards (50+ hours): {len(active_guards)}')
        w(f'  Median incident rate:      {median_rate:.1f} per 100 hours')
        w(f'  High reporter threshold:   > {high_threshold:.1f} per 100 hours (75th percentile)')
        w(f'  Low reporter threshold:    < {low_threshold:.1f} per 100 hours (25th percentile)')
        w()

        # Bucket guards
        high_reporters = []
        normal_reporters = []
        low_reporters = []

        for r in active_guards:
            rate = r['incidents_per_100h']
            if rate > high_threshold:
                high_reporters.append(r)
            elif rate < low_threshold:
                low_reporters.append(r)
            else:
                normal_reporters.append(r)

        def print_bucket(title, bucket, is_concern=False):
            bucket.sort(key=lambda x: x['incidents_per_100h'], reverse=True)
            w(f'  {title} ({len(bucket)} guards):')
            w(f'  {"Guard":<25} {"Hours":>8} {"Incidents":>10} {"Inc/100h":>10} {"Rec$":>12} {"Rec/Inc":>10}')
            w(f'  {"-"*80}')
            for r in bucket:
                rec_per_inc = r['total_recovered'] / r['total_incidents'] if r['total_incidents'] > 0 else 0
                marker = ' ***' if is_concern and r['total_hours'] > 200 and r['incidents_per_100h'] < low_threshold else ''
                w(f'  {r["name"]:<25} '
                  f'{r["total_hours"]:>8.1f} '
                  f'{r["total_incidents"]:>10} '
                  f'{r["incidents_per_100h"]:>10.1f} '
                  f'{r["total_recovered"]:>12,.2f} '
                  f'{rec_per_inc:>10,.2f}{marker}')
            w()

        print_bucket('HIGH REPORTERS', high_reporters)
        print_bucket('NORMAL REPORTERS', normal_reporters)
        print_bucket('LOW REPORTERS (potential concern)', low_reporters, is_concern=True)

        # Flag specific concerns
        w()
        w('  --- FLAGGED: High hours, low reporting ---')
        w('  Guards working 200+ hours with below-median incident rates:')
        w()

        flagged_lazy = [r for r in active_guards
                        if r['total_hours'] >= 200 and r['incidents_per_100h'] < median_rate]
        flagged_lazy.sort(key=lambda x: x['incidents_per_100h'])

        if flagged_lazy:
            for r in flagged_lazy:
                expected = r['total_hours'] * median_rate / 100
                actual = r['total_incidents']
                gap = expected - actual
                rec_per_inc = r['total_recovered'] / r['total_incidents'] if r['total_incidents'] > 0 else 0
                w(f'  ** {r["name"]}:')
                w(f'     {r["total_hours"]:.1f} hours worked, {actual} incidents reported '
                  f'(expected ~{expected:.0f} at median rate)')
                w(f'     Incident gap: {gap:.0f} fewer incidents than expected')
                w(f'     Recovery: ${r["total_recovered"]:,.2f} total, '
                  f'${rec_per_inc:,.2f} per incident')
                w(f'     Rate: {r["incidents_per_100h"]:.1f} per 100h vs {median_rate:.1f} median')
                w()
        else:
            w('  None flagged.')

        # Compare guards with similar hours but different incident rates
        w()
        w('  --- PEER COMPARISON: Guards with similar hours, different outcomes ---')
        w()

        # Group by hours buckets (200-300, 300-400, 400-500, 500+)
        hour_buckets = [
            ('100-200 hours', 100, 200),
            ('200-300 hours', 200, 300),
            ('300-400 hours', 300, 400),
            ('400-500 hours', 400, 500),
            ('500+ hours', 500, 9999),
        ]

        for label, lo, hi in hour_buckets:
            bucket_guards = [r for r in active_guards if lo <= r['total_hours'] < hi]
            if len(bucket_guards) < 2:
                continue
            bucket_guards.sort(key=lambda x: x['incidents_per_100h'], reverse=True)
            w(f'  {label} ({len(bucket_guards)} guards):')
            for r in bucket_guards:
                bar_len = int(r['incidents_per_100h'] / 2)  # scale for display
                bar = '#' * bar_len
                w(f'    {r["name"]:<25} {r["total_hours"]:>7.1f}h  '
                  f'{r["total_incidents"]:>4} inc  '
                  f'{r["incidents_per_100h"]:>6.1f}/100h  '
                  f'${r["total_recovered"]:>9,.2f} rec  '
                  f'{bar}')
            w()

    # Guards with incidents but zero hours (appear in GIR but not timeclock)
    ghost_guards = [r for r in results if r['total_hours'] == 0 and r['total_incidents'] > 0]
    if ghost_guards:
        w()
        w('  --- GHOST GUARDS: Incidents reported but no timeclock hours ---')
        w('  These guards appear in GIR data but have zero hours in the timeclock system.')
        w()
        for r in sorted(ghost_guards, key=lambda x: x['total_incidents'], reverse=True):
            w(f'  {r["name"]}: {r["total_incidents"]} incidents, '
              f'${r["total_recovered"]:,.2f} recovered, '
              f'${r["total_stolen"]:,.2f} stolen')

    # =================================================================
    # FINAL VERDICT
    # =================================================================
    w()
    w()
    w('=' * 120)
    w('FINAL ANALYSIS: VALUE vs COST CLASSIFICATION')
    w('=' * 120)

    # Classify guards
    value_guards = []
    neutral_guards = []
    concern_guards = []

    for r in [x for x in results if x['total_hours'] >= 50]:
        # Value: Client ROI > 0.5 OR incidents/100h above median
        if r['client_roi'] > 0.5 or (r['incidents_per_100h'] > median_rate and r['total_recovered'] > 0):
            value_guards.append(r)
        # Concern: Low incidents AND low recovery AND significant hours
        elif r['incidents_per_100h'] < low_threshold and r['total_recovered'] < 500:
            concern_guards.append(r)
        else:
            neutral_guards.append(r)

    w()
    w(f'  VALUE GENERATORS ({len(value_guards)} guards) - High ROI and/or high incident reporting:')
    for r in sorted(value_guards, key=lambda x: x['client_roi'], reverse=True):
        w(f'    + {r["name"]:<25} ROI:{r["client_roi"]:.2f}x  Rec:${r["total_recovered"]:>9,.2f}  '
          f'Inc/100h:{r["incidents_per_100h"]:.1f}  Hours:{r["total_hours"]:.0f}')

    w()
    w(f'  NEUTRAL ({len(neutral_guards)} guards) - Average performance:')
    for r in sorted(neutral_guards, key=lambda x: x['client_roi'], reverse=True):
        w(f'    ~ {r["name"]:<25} ROI:{r["client_roi"]:.2f}x  Rec:${r["total_recovered"]:>9,.2f}  '
          f'Inc/100h:{r["incidents_per_100h"]:.1f}  Hours:{r["total_hours"]:.0f}')

    w()
    w(f'  CONCERN ({len(concern_guards)} guards) - Low activity, investigate:')
    for r in sorted(concern_guards, key=lambda x: x['incidents_per_100h']):
        w(f'    - {r["name"]:<25} ROI:{r["client_roi"]:.2f}x  Rec:${r["total_recovered"]:>9,.2f}  '
          f'Inc/100h:{r["incidents_per_100h"]:.1f}  Hours:{r["total_hours"]:.0f}')

    w()
    w('=' * 120)
    w('END OF REPORT')
    w('=' * 120)

print(f"\nReport saved to: {OUTPUT_FILE}")
