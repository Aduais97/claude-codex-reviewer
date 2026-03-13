#!/usr/bin/env python3
"""
Store-Level ROI Analysis for ASG Retail Clients (Woolworths & Bunnings)

Extracts billing data from:
- Woolworths ZFI Excel files (per-store revenue breakdown)
- Bunnings PDF invoices (per-store guarding hours)
- SalesInvoices CSV (cross-reference for payment status & progressive spend)

Generates:
- Excel workbook with per-store ROI analysis
- PDF analytical report

Usage:
    python3 store_roi_analysis.py
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = "/Users/ahmadduais/Desktop/Payslips"
WOOLWORTHS_DIR = os.path.join(BASE_DIR, "Woolworths ZFI files")
BUNNINGS_DIR = os.path.join(BASE_DIR, "Bunnings invoices")
CSV_PATH = os.path.join(BASE_DIR, "SalesInvoices_SLS RTC_2026-Mar-13.01.44.18.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "performance_analysis", "store_analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, "ASG_Store_ROI_Analysis.xlsx")
PDF_OUTPUT = os.path.join(OUTPUT_DIR, "ASG_Store_ROI_Analysis.pdf")

# ---------------------------------------------------------------------------
# Cost assumptions (per hour, NZD)
# ---------------------------------------------------------------------------
# Average guard wage ~$26.50/hr + oncosts (ACC 1.4%, KiwiSaver 3%, annual leave 8%, sick leave 2.5%)
# Total oncost multiplier ~1.15
AVG_GUARD_WAGE = 26.50
ONCOST_MULTIPLIER = 1.15
AVG_GUARD_COST_PER_HR = AVG_GUARD_WAGE * ONCOST_MULTIPLIER  # ~$30.48
# Senior guard premium
SENIOR_GUARD_WAGE = 28.50
SENIOR_GUARD_COST_PER_HR = SENIOR_GUARD_WAGE * ONCOST_MULTIPLIER  # ~$32.78

print(f"Cost assumptions: Guard ${AVG_GUARD_COST_PER_HR:.2f}/hr, Senior ${SENIOR_GUARD_COST_PER_HR:.2f}/hr")


# ===================================================================
# PHASE 1: DATA EXTRACTION
# ===================================================================

def extract_woolworths_data() -> list[dict]:
    """Extract per-store billing data from all Woolworths ZFI Excel files."""
    import openpyxl

    records = []
    files = sorted(os.listdir(WOOLWORTHS_DIR))
    print(f"\n--- Woolworths ZFI Extraction ---")
    print(f"Files to process: {len([f for f in files if f.endswith('.xlsx')])}")

    for fname in files:
        if not fname.endswith(".xlsx"):
            continue

        filepath = os.path.join(WOOLWORTHS_DIR, fname)
        # Extract invoice number from filename
        inv_match = re.search(r"96011219\s+(\d+)", fname)
        file_inv_num = inv_match.group(1) if inv_match else None

        try:
            wb = openpyxl.load_workbook(filepath, data_only=True, read_only=True)
            ws = wb.active

            row_count = 0
            for row in ws.iter_rows(min_row=2, values_only=False):
                vals = {}
                for c in row:
                    if c.value is not None:
                        vals[c.column_letter] = c.value

                # Skip empty rows - check for store name or amount
                if "N" not in vals and "J" not in vals:
                    # If we've already read data rows and hit empty, stop
                    if row_count > 0:
                        break
                    continue

                store_name = str(vals.get("N", "")).strip()
                if not store_name:
                    if row_count > 0:
                        break
                    continue

                inv_num = str(vals.get("D", file_inv_num or ""))
                inv_date = vals.get("E", None)
                store_num = str(vals.get("I", ""))
                amt_excl = float(vals.get("J", 0) or 0)
                gst = float(vals.get("K", 0) or 0)
                amt_incl = float(vals.get("L", 0) or 0)
                hours = float(vals.get("Q", 0) or 0)

                # Parse date
                if isinstance(inv_date, datetime):
                    date_str = inv_date.strftime("%Y-%m-%d")
                elif isinstance(inv_date, str):
                    date_str = inv_date
                else:
                    date_str = ""

                records.append({
                    "client": "Woolworths",
                    "store_name": store_name,
                    "store_num": store_num,
                    "invoice_num": inv_num,
                    "invoice_date": date_str,
                    "hours": hours,
                    "revenue_excl_gst": amt_excl,
                    "gst": gst,
                    "revenue_incl_gst": amt_incl,
                    "service_type": "Covert Guarding",
                    "hourly_rate": round(amt_excl / hours, 2) if hours > 0 else 0,
                    "source_file": fname,
                })
                row_count += 1

            wb.close()
        except Exception as e:
            print(f"  ERROR reading {fname}: {e}")

    print(f"  Extracted {len(records)} store-invoice records")

    # Normalize store names (fix typos/variants)
    name_map = {
        "Keltson": "Kelston",
        "Claudlands ": "Claudelands",
        "Claudelands ": "Claudelands",
        "Fielding": "Feilding",
        "New Market": "Newmarket",
        "Mt Roskill": "Mount Roskill",
        "Mt Eden": "Mount Eden",
        "Mt Wellington": "Mount Wellington",
        "Manukau ": "Manukau",
        "Manukay City": "Manukau City Mall",
        "Ponsonby ": "Ponsonby",
        "Palmerston North ": "Palmerston North",
        "Te Atatu ": "Te Atatu South",
        "Roselands ": "Roselands",
        "Highland Park ": "Highland Park",
        "Waiata Shores ": "Waiata Shores",
        "Hamilton ": "Hamilton Central",
        "Paraparaumu ": "Paraparaumu",
        "Bridge Street ": "Bridge Street",
        "Amberley ": "Amberley",
        "Bridge St": "Bridge Street",
        "Levin St": "Levin",
        "Rangitikei St": "Rangitikei",
        "Whanarei": "Whangarei",
    }
    for rec in records:
        n = rec["store_name"]
        if n in name_map:
            rec["store_name"] = name_map[n]

    return records


def extract_bunnings_data() -> list[dict]:
    """Extract per-store billing data from all Bunnings PDF invoices."""
    from PyPDF2 import PdfReader

    records = []
    files = sorted(os.listdir(BUNNINGS_DIR))
    pdf_files = [f for f in files if f.endswith(".pdf")]
    print(f"\n--- Bunnings Invoice Extraction ---")
    print(f"Files to process: {len(pdf_files)}")

    for fname in pdf_files:
        filepath = os.path.join(BUNNINGS_DIR, fname)
        inv_match = re.search(r"INV-(\d+)", fname)
        inv_num = inv_match.group(0) if inv_match else fname

        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

            # Extract invoice date
            date_match = re.search(r"Invoice Date\s*\n?\s*(\d{1,2}\s+\w+\s+\d{4})", text)
            inv_date = ""
            if date_match:
                try:
                    dt = datetime.strptime(date_match.group(1), "%d %b %Y")
                    inv_date = dt.strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        dt = datetime.strptime(date_match.group(1), "%d %B %Y")
                        inv_date = dt.strftime("%Y-%m-%d")
                    except ValueError:
                        inv_date = date_match.group(1)

            # Extract line items: "Bunnings <Store> <Type> Guarding <qty> <rate> <amount>"
            # Pattern handles multi-word store names and service types
            line_pattern = re.compile(
                r"Bunnings\s+(.+?)\s+(Covert|Senior Covert|Uniformed)\s+Guarding\s+"
                r"([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)"
            )

            for match in line_pattern.finditer(text):
                raw_store = match.group(1).strip()
                service_type = match.group(2).strip()
                hours = float(match.group(3).replace(",", ""))
                rate = float(match.group(4).replace(",", ""))
                amount = float(match.group(5).replace(",", ""))

                # Clean store name - remove "Public Holiday" suffix for grouping
                store_clean = re.sub(r"\s*Public Holiday\s*$", "", raw_store).strip()
                is_public_holiday = "Public Holiday" in raw_store

                records.append({
                    "client": "Bunnings",
                    "store_name": store_clean,
                    "store_num": "",
                    "invoice_num": inv_num,
                    "invoice_date": inv_date,
                    "hours": hours,
                    "revenue_excl_gst": amount,
                    "gst": round(amount * 0.15, 2),
                    "revenue_incl_gst": round(amount * 1.15, 2),
                    "service_type": f"{'Senior ' if 'Senior' in service_type else ''}Covert Guarding"
                                    + (" (PH)" if is_public_holiday else ""),
                    "hourly_rate": rate,
                    "is_public_holiday": is_public_holiday,
                    "source_file": fname,
                })

        except Exception as e:
            print(f"  ERROR reading {fname}: {e}")

    # Normalize store names
    name_map = {
        "Takanini Lynn": "Takanini",
    }
    for rec in records:
        n = rec["store_name"]
        if n in name_map:
            rec["store_name"] = name_map[n]

    print(f"  Extracted {len(records)} store-invoice line items")
    return records


def extract_sales_invoices() -> dict:
    """Extract payment/status data from SalesInvoices CSV for cross-reference."""
    data = defaultdict(lambda: {
        "total": 0, "paid": 0, "due": 0, "invoices": {},
        "date_range": {"earliest": None, "latest": None}
    })

    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contact = row["ContactName"]
            inv_num = row["InvoiceNumber"]
            total = float(row["Total"] or 0)
            paid = float(row["InvoiceAmountPaid"] or 0)
            due = float(row["InvoiceAmountDue"] or 0)
            status = row["Status"]
            inv_date = row["InvoiceDate"]
            qty = float(row["Quantity"] or 0)
            unit_amt = float(row["UnitAmount"] or 0)
            line_amt = float(row["LineAmount"] or 0)

            if inv_num not in data[contact]["invoices"]:
                data[contact]["invoices"][inv_num] = {
                    "date": inv_date,
                    "total": total,
                    "paid": paid,
                    "due": due,
                    "status": status,
                    "lines": [],
                }
            data[contact]["invoices"][inv_num]["lines"].append({
                "qty": qty, "unit_amt": unit_amt, "line_amt": line_amt
            })

    print(f"\n--- SalesInvoices CSV ---")
    for contact, info in data.items():
        print(f"  {contact}: {len(info['invoices'])} invoices")

    return dict(data)


# ===================================================================
# PHASE 2: ANALYSIS & AGGREGATION
# ===================================================================

def aggregate_store_data(records: list[dict]) -> dict:
    """Aggregate records into per-store summaries."""
    stores = defaultdict(lambda: {
        "total_revenue": 0, "total_gst": 0, "total_incl": 0,
        "total_hours": 0, "invoice_count": set(),
        "monthly_revenue": defaultdict(float),
        "monthly_hours": defaultdict(float),
        "service_breakdown": defaultdict(lambda: {"hours": 0, "revenue": 0}),
        "dates": [],
    })

    for rec in records:
        store = rec["store_name"]
        stores[store]["total_revenue"] += rec["revenue_excl_gst"]
        stores[store]["total_gst"] += rec["gst"]
        stores[store]["total_incl"] += rec["revenue_incl_gst"]
        stores[store]["total_hours"] += rec["hours"]
        stores[store]["invoice_count"].add(rec["invoice_num"])

        # Monthly aggregation
        date_str = rec["invoice_date"]
        if date_str:
            try:
                month_key = date_str[:7]  # YYYY-MM
            except Exception:
                month_key = "unknown"
            stores[store]["monthly_revenue"][month_key] += rec["revenue_excl_gst"]
            stores[store]["monthly_hours"][month_key] += rec["hours"]

        # Service type breakdown
        svc = rec.get("service_type", "Covert Guarding")
        stores[store]["service_breakdown"][svc]["hours"] += rec["hours"]
        stores[store]["service_breakdown"][svc]["revenue"] += rec["revenue_excl_gst"]

        if date_str:
            stores[store]["dates"].append(date_str)

    # Calculate derived metrics
    for store, data in stores.items():
        data["invoice_count"] = len(data["invoice_count"])
        data["avg_hourly_rate"] = (
            data["total_revenue"] / data["total_hours"]
            if data["total_hours"] > 0 else 0
        )
        # Estimate cost
        data["estimated_cost"] = data["total_hours"] * AVG_GUARD_COST_PER_HR
        data["gross_margin"] = data["total_revenue"] - data["estimated_cost"]
        data["margin_pct"] = (
            (data["gross_margin"] / data["total_revenue"] * 100)
            if data["total_revenue"] > 0 else 0
        )
        data["roi_pct"] = (
            (data["gross_margin"] / data["estimated_cost"] * 100)
            if data["estimated_cost"] > 0 else 0
        )
        # Revenue per invoice
        data["avg_revenue_per_invoice"] = (
            data["total_revenue"] / data["invoice_count"]
            if data["invoice_count"] > 0 else 0
        )
        # Date range
        if data["dates"]:
            data["first_date"] = min(data["dates"])
            data["last_date"] = max(data["dates"])
        else:
            data["first_date"] = ""
            data["last_date"] = ""

    return dict(stores)


def build_progressive_spend(csv_data: dict) -> dict:
    """Build progressive (cumulative) spend by client by month."""
    progressive = defaultdict(lambda: defaultdict(float))

    for contact, info in csv_data.items():
        for inv_num, inv_data in info["invoices"].items():
            date_str = inv_data["date"]
            total = inv_data["total"]
            try:
                # Parse DD/MM/YY format
                dt = datetime.strptime(date_str, "%d/%m/%y")
                month_key = dt.strftime("%Y-%m")
            except ValueError:
                month_key = "unknown"
            progressive[contact][month_key] += total

    # Make cumulative
    result = {}
    for contact, months in progressive.items():
        sorted_months = sorted(months.items())
        cumulative = 0
        result[contact] = []
        for month, amount in sorted_months:
            cumulative += amount
            result[contact].append({
                "month": month,
                "monthly_total": round(amount, 2),
                "cumulative_total": round(cumulative, 2),
            })

    return result


# ===================================================================
# PHASE 3: EXCEL GENERATION
# ===================================================================

def generate_excel(
    woolworths_stores: dict,
    bunnings_stores: dict,
    woolworths_records: list[dict],
    bunnings_records: list[dict],
    csv_data: dict,
    progressive: dict,
):
    """Generate comprehensive Excel workbook."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
    from openpyxl.utils import get_column_letter

    wb = Workbook()

    # Styles
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
    alt_fill = PatternFill(start_color="F0F4F8", end_color="F0F4F8", fill_type="solid")
    money_fmt = '#,##0.00'
    pct_fmt = '0.0%'
    num_fmt = '#,##0.0'
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    title_font = Font(name="Calibri", bold=True, size=14, color="003366")
    subtitle_font = Font(name="Calibri", bold=True, size=11, color="003366")

    def style_header(ws, row, cols):
        for col in range(1, cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", wrap_text=True)
            cell.border = thin_border

    def style_data_row(ws, row, cols, alt=False):
        for col in range(1, cols + 1):
            cell = ws.cell(row=row, column=col)
            if alt:
                cell.fill = alt_fill
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center")

    def auto_width(ws, cols, min_w=10, max_w=25):
        for col in range(1, cols + 1):
            letter = get_column_letter(col)
            max_len = min_w
            for row in ws.iter_rows(min_col=col, max_col=col, values_only=True):
                val = str(row[0]) if row[0] else ""
                max_len = max(max_len, min(len(val) + 2, max_w))
            ws.column_dimensions[letter].width = max_len

    # ---------------------------------------------------------------
    # Sheet 1: Executive Summary
    # ---------------------------------------------------------------
    ws = wb.active
    ws.title = "Executive Summary"
    ws.sheet_properties.tabColor = "003366"

    ws.cell(row=1, column=1, value="ASG Store-Level ROI Analysis").font = title_font
    ws.cell(row=2, column=1, value=f"Report Date: {datetime.now():%d %B %Y}").font = subtitle_font
    ws.cell(row=3, column=1, value="Absolute Security Group - Covert Guarding Division").font = Font(italic=True, size=10)

    # Summary metrics
    ww_total_rev = sum(s["total_revenue"] for s in woolworths_stores.values())
    ww_total_hrs = sum(s["total_hours"] for s in woolworths_stores.values())
    ww_total_cost = sum(s["estimated_cost"] for s in woolworths_stores.values())
    ww_margin = ww_total_rev - ww_total_cost

    bn_total_rev = sum(s["total_revenue"] for s in bunnings_stores.values())
    bn_total_hrs = sum(s["total_hours"] for s in bunnings_stores.values())
    bn_total_cost = sum(s["estimated_cost"] for s in bunnings_stores.values())
    bn_margin = bn_total_rev - bn_total_cost

    row = 5
    headers = ["Metric", "Woolworths", "Bunnings", "Combined"]
    for ci, h in enumerate(headers, 1):
        ws.cell(row=row, column=ci, value=h)
    style_header(ws, row, len(headers))

    metrics = [
        ("Total Revenue (excl GST)", ww_total_rev, bn_total_rev, ww_total_rev + bn_total_rev),
        ("Total Hours", ww_total_hrs, bn_total_hrs, ww_total_hrs + bn_total_hrs),
        ("Avg Hourly Rate", ww_total_rev / ww_total_hrs if ww_total_hrs else 0,
         bn_total_rev / bn_total_hrs if bn_total_hrs else 0,
         (ww_total_rev + bn_total_rev) / (ww_total_hrs + bn_total_hrs) if (ww_total_hrs + bn_total_hrs) else 0),
        ("Estimated Labour Cost", ww_total_cost, bn_total_cost, ww_total_cost + bn_total_cost),
        ("Gross Margin", ww_margin, bn_margin, ww_margin + bn_margin),
        ("Margin %", ww_margin / ww_total_rev if ww_total_rev else 0,
         bn_margin / bn_total_rev if bn_total_rev else 0,
         (ww_margin + bn_margin) / (ww_total_rev + bn_total_rev) if (ww_total_rev + bn_total_rev) else 0),
        ("ROI %", ww_margin / ww_total_cost if ww_total_cost else 0,
         bn_margin / bn_total_cost if bn_total_cost else 0,
         (ww_margin + bn_margin) / (ww_total_cost + bn_total_cost) if (ww_total_cost + bn_total_cost) else 0),
        ("Number of Stores", len(woolworths_stores), len(bunnings_stores),
         len(woolworths_stores) + len(bunnings_stores)),
        ("Number of Invoices", len(set(r["invoice_num"] for r in woolworths_records)),
         len(set(r["invoice_num"] for r in bunnings_records)),
         len(set(r["invoice_num"] for r in woolworths_records)) + len(set(r["invoice_num"] for r in bunnings_records))),
    ]

    for i, (label, ww, bn, combined) in enumerate(metrics):
        r = row + 1 + i
        ws.cell(row=r, column=1, value=label)
        for ci, val in enumerate([ww, bn, combined], 2):
            cell = ws.cell(row=r, column=ci, value=val)
            if "%" in label and "Number" not in label:
                cell.number_format = pct_fmt
            elif "Hours" in label or "Stores" in label or "Invoices" in label:
                cell.number_format = num_fmt
            else:
                cell.number_format = money_fmt
        style_data_row(ws, r, len(headers), alt=(i % 2 == 0))

    auto_width(ws, len(headers), min_w=18)

    # ---------------------------------------------------------------
    # Sheet 2: Woolworths Store Summary
    # ---------------------------------------------------------------
    ws2 = wb.create_sheet("Woolworths Stores")
    ws2.sheet_properties.tabColor = "006400"

    headers2 = [
        "Store", "Region", "Total Revenue", "Total Hours",
        "Avg Rate/Hr", "Est. Labour Cost", "Gross Margin",
        "Margin %", "ROI %", "Invoices", "Avg Rev/Invoice",
        "First Date", "Last Date"
    ]
    for ci, h in enumerate(headers2, 1):
        ws2.cell(row=1, column=ci, value=h)
    style_header(ws2, 1, len(headers2))

    # Determine region from invoice numbers cross-referenced to CSV
    inv_to_region = {}
    for contact, info in csv_data.items():
        if "Woolworths" not in contact:
            continue
        region = contact.split(" - ")[-1].replace("Woolworths ", "") if " - " in contact else contact
        for inv_num in info["invoices"]:
            # Extract number from INV-XXXX or CN-XXXX, strip leading zeros
            num_match = re.search(r"(\d+)", inv_num)
            if num_match:
                inv_to_region[str(int(num_match.group(1)))] = region

    # Assign region to each store based on which invoices it appears in
    store_regions = defaultdict(lambda: defaultdict(int))
    for rec in woolworths_records:
        inv = str(int(float(rec["invoice_num"]))) if rec["invoice_num"] else ""
        region = inv_to_region.get(inv, "Unknown")
        store_regions[rec["store_name"]][region] += 1

    # Most common region for each store
    store_region_map = {}
    for store, regions in store_regions.items():
        store_region_map[store] = max(regions, key=regions.get)

    sorted_stores = sorted(
        woolworths_stores.items(),
        key=lambda x: x[1]["total_revenue"],
        reverse=True
    )

    for i, (store, data) in enumerate(sorted_stores):
        r = i + 2
        region = store_region_map.get(store, "Unknown")
        ws2.cell(row=r, column=1, value=store)
        ws2.cell(row=r, column=2, value=region)
        ws2.cell(row=r, column=3, value=data["total_revenue"]).number_format = money_fmt
        ws2.cell(row=r, column=4, value=data["total_hours"]).number_format = num_fmt
        ws2.cell(row=r, column=5, value=data["avg_hourly_rate"]).number_format = money_fmt
        ws2.cell(row=r, column=6, value=data["estimated_cost"]).number_format = money_fmt
        ws2.cell(row=r, column=7, value=data["gross_margin"]).number_format = money_fmt
        margin_cell = ws2.cell(row=r, column=8, value=data["margin_pct"] / 100)
        margin_cell.number_format = pct_fmt
        if data["margin_pct"] >= 25:
            margin_cell.fill = green_fill
        elif data["margin_pct"] < 15:
            margin_cell.fill = red_fill
        else:
            margin_cell.fill = yellow_fill
        ws2.cell(row=r, column=9, value=data["roi_pct"] / 100).number_format = pct_fmt
        ws2.cell(row=r, column=10, value=data["invoice_count"])
        ws2.cell(row=r, column=11, value=data["avg_revenue_per_invoice"]).number_format = money_fmt
        ws2.cell(row=r, column=12, value=data["first_date"])
        ws2.cell(row=r, column=13, value=data["last_date"])
        style_data_row(ws2, r, len(headers2), alt=(i % 2 == 0))

    # Region subtotals
    r = len(sorted_stores) + 3
    ws2.cell(row=r, column=1, value="REGION SUBTOTALS").font = subtitle_font
    r += 1
    region_headers = ["Region", "Stores", "Total Revenue", "Total Hours", "Avg Rate", "Est. Cost", "Margin", "Margin %"]
    for ci, h in enumerate(region_headers, 1):
        ws2.cell(row=r, column=ci, value=h)
    style_header(ws2, r, len(region_headers))

    region_totals = defaultdict(lambda: {"stores": set(), "revenue": 0, "hours": 0, "cost": 0})
    for store, data in woolworths_stores.items():
        region = store_region_map.get(store, "Unknown")
        region_totals[region]["stores"].add(store)
        region_totals[region]["revenue"] += data["total_revenue"]
        region_totals[region]["hours"] += data["total_hours"]
        region_totals[region]["cost"] += data["estimated_cost"]

    for i, (region, rt) in enumerate(sorted(region_totals.items(), key=lambda x: x[1]["revenue"], reverse=True)):
        rr = r + 1 + i
        margin = rt["revenue"] - rt["cost"]
        ws2.cell(row=rr, column=1, value=region)
        ws2.cell(row=rr, column=2, value=len(rt["stores"]))
        ws2.cell(row=rr, column=3, value=rt["revenue"]).number_format = money_fmt
        ws2.cell(row=rr, column=4, value=rt["hours"]).number_format = num_fmt
        ws2.cell(row=rr, column=5, value=rt["revenue"] / rt["hours"] if rt["hours"] else 0).number_format = money_fmt
        ws2.cell(row=rr, column=6, value=rt["cost"]).number_format = money_fmt
        ws2.cell(row=rr, column=7, value=margin).number_format = money_fmt
        ws2.cell(row=rr, column=8, value=margin / rt["revenue"] if rt["revenue"] else 0).number_format = pct_fmt
        style_data_row(ws2, rr, len(region_headers), alt=(i % 2 == 0))

    auto_width(ws2, len(headers2))

    # ---------------------------------------------------------------
    # Sheet 3: Bunnings Store Summary
    # ---------------------------------------------------------------
    ws3 = wb.create_sheet("Bunnings Stores")
    ws3.sheet_properties.tabColor = "CC0000"

    headers3 = [
        "Store", "Total Revenue", "Total Hours",
        "Avg Rate/Hr", "Est. Labour Cost", "Gross Margin",
        "Margin %", "ROI %", "Invoices", "Avg Rev/Invoice",
        "Senior Hours", "Standard Hours", "First Date", "Last Date"
    ]
    for ci, h in enumerate(headers3, 1):
        ws3.cell(row=1, column=ci, value=h)
    style_header(ws3, 1, len(headers3))

    sorted_bn = sorted(
        bunnings_stores.items(),
        key=lambda x: x[1]["total_revenue"],
        reverse=True
    )

    for i, (store, data) in enumerate(sorted_bn):
        r = i + 2
        senior_hrs = sum(
            v["hours"] for k, v in data["service_breakdown"].items()
            if "Senior" in k
        )
        standard_hrs = data["total_hours"] - senior_hrs

        ws3.cell(row=r, column=1, value=store)
        ws3.cell(row=r, column=2, value=data["total_revenue"]).number_format = money_fmt
        ws3.cell(row=r, column=3, value=data["total_hours"]).number_format = num_fmt
        ws3.cell(row=r, column=4, value=data["avg_hourly_rate"]).number_format = money_fmt
        ws3.cell(row=r, column=5, value=data["estimated_cost"]).number_format = money_fmt
        ws3.cell(row=r, column=6, value=data["gross_margin"]).number_format = money_fmt
        margin_cell = ws3.cell(row=r, column=7, value=data["margin_pct"] / 100)
        margin_cell.number_format = pct_fmt
        if data["margin_pct"] >= 30:
            margin_cell.fill = green_fill
        elif data["margin_pct"] < 20:
            margin_cell.fill = red_fill
        else:
            margin_cell.fill = yellow_fill
        ws3.cell(row=r, column=8, value=data["roi_pct"] / 100).number_format = pct_fmt
        ws3.cell(row=r, column=9, value=data["invoice_count"])
        ws3.cell(row=r, column=10, value=data["avg_revenue_per_invoice"]).number_format = money_fmt
        ws3.cell(row=r, column=11, value=senior_hrs).number_format = num_fmt
        ws3.cell(row=r, column=12, value=standard_hrs).number_format = num_fmt
        ws3.cell(row=r, column=13, value=data["first_date"])
        ws3.cell(row=r, column=14, value=data["last_date"])
        style_data_row(ws3, r, len(headers3), alt=(i % 2 == 0))

    auto_width(ws3, len(headers3))

    # ---------------------------------------------------------------
    # Sheet 4: Combined ROI Ranking
    # ---------------------------------------------------------------
    ws4 = wb.create_sheet("Combined ROI Ranking")
    ws4.sheet_properties.tabColor = "FF6600"

    headers4 = [
        "Rank", "Client", "Store", "Total Revenue", "Total Hours",
        "Avg Rate", "Est. Cost", "Gross Margin", "Margin %", "ROI %",
        "Revenue/Month"
    ]
    for ci, h in enumerate(headers4, 1):
        ws4.cell(row=1, column=ci, value=h)
    style_header(ws4, 1, len(headers4))

    all_stores_combined = []
    for store, data in woolworths_stores.items():
        months_active = len(data["monthly_revenue"]) or 1
        all_stores_combined.append(("Woolworths", store, data, months_active))
    for store, data in bunnings_stores.items():
        months_active = len(data["monthly_revenue"]) or 1
        all_stores_combined.append(("Bunnings", store, data, months_active))

    all_stores_combined.sort(key=lambda x: x[2]["total_revenue"], reverse=True)

    for i, (client, store, data, months) in enumerate(all_stores_combined):
        r = i + 2
        ws4.cell(row=r, column=1, value=i + 1)
        ws4.cell(row=r, column=2, value=client)
        ws4.cell(row=r, column=3, value=store)
        ws4.cell(row=r, column=4, value=data["total_revenue"]).number_format = money_fmt
        ws4.cell(row=r, column=5, value=data["total_hours"]).number_format = num_fmt
        ws4.cell(row=r, column=6, value=data["avg_hourly_rate"]).number_format = money_fmt
        ws4.cell(row=r, column=7, value=data["estimated_cost"]).number_format = money_fmt
        ws4.cell(row=r, column=8, value=data["gross_margin"]).number_format = money_fmt
        ws4.cell(row=r, column=9, value=data["margin_pct"] / 100).number_format = pct_fmt
        ws4.cell(row=r, column=10, value=data["roi_pct"] / 100).number_format = pct_fmt
        ws4.cell(row=r, column=11, value=data["total_revenue"] / months).number_format = money_fmt
        style_data_row(ws4, r, len(headers4), alt=(i % 2 == 0))

    auto_width(ws4, len(headers4))

    # ---------------------------------------------------------------
    # Sheet 5: Monthly Trends (Woolworths)
    # ---------------------------------------------------------------
    ws5 = wb.create_sheet("Woolworths Monthly")
    ws5.sheet_properties.tabColor = "006400"

    # Get all months
    all_months = set()
    for data in woolworths_stores.values():
        all_months.update(data["monthly_revenue"].keys())
    all_months = sorted(m for m in all_months if m != "unknown")

    headers5 = ["Store"] + all_months + ["Total"]
    for ci, h in enumerate(headers5, 1):
        ws5.cell(row=1, column=ci, value=h)
    style_header(ws5, 1, len(headers5))

    for i, (store, data) in enumerate(sorted_stores):
        r = i + 2
        ws5.cell(row=r, column=1, value=store)
        total = 0
        for mi, month in enumerate(all_months):
            val = data["monthly_revenue"].get(month, 0)
            total += val
            ws5.cell(row=r, column=mi + 2, value=val).number_format = money_fmt
        ws5.cell(row=r, column=len(all_months) + 2, value=total).number_format = money_fmt
        style_data_row(ws5, r, len(headers5), alt=(i % 2 == 0))

    # Monthly totals row
    r = len(sorted_stores) + 2
    ws5.cell(row=r, column=1, value="TOTAL").font = Font(bold=True)
    for mi, month in enumerate(all_months):
        total = sum(d["monthly_revenue"].get(month, 0) for d in woolworths_stores.values())
        ws5.cell(row=r, column=mi + 2, value=total).number_format = money_fmt
        ws5.cell(row=r, column=mi + 2).font = Font(bold=True)

    auto_width(ws5, len(headers5), min_w=12)

    # ---------------------------------------------------------------
    # Sheet 6: Monthly Trends (Bunnings)
    # ---------------------------------------------------------------
    ws6 = wb.create_sheet("Bunnings Monthly")
    ws6.sheet_properties.tabColor = "CC0000"

    bn_months = set()
    for data in bunnings_stores.values():
        bn_months.update(data["monthly_revenue"].keys())
    bn_months = sorted(m for m in bn_months if m != "unknown")

    headers6 = ["Store"] + bn_months + ["Total"]
    for ci, h in enumerate(headers6, 1):
        ws6.cell(row=1, column=ci, value=h)
    style_header(ws6, 1, len(headers6))

    for i, (store, data) in enumerate(sorted_bn):
        r = i + 2
        ws6.cell(row=r, column=1, value=store)
        total = 0
        for mi, month in enumerate(bn_months):
            val = data["monthly_revenue"].get(month, 0)
            total += val
            ws6.cell(row=r, column=mi + 2, value=val).number_format = money_fmt
        ws6.cell(row=r, column=len(bn_months) + 2, value=total).number_format = money_fmt
        style_data_row(ws6, r, len(headers6), alt=(i % 2 == 0))

    # Monthly totals row
    r = len(sorted_bn) + 2
    ws6.cell(row=r, column=1, value="TOTAL").font = Font(bold=True)
    for mi, month in enumerate(bn_months):
        total = sum(d["monthly_revenue"].get(month, 0) for d in bunnings_stores.values())
        ws6.cell(row=r, column=mi + 2, value=total).number_format = money_fmt
        ws6.cell(row=r, column=mi + 2).font = Font(bold=True)

    auto_width(ws6, len(headers6), min_w=12)

    # ---------------------------------------------------------------
    # Sheet 7: Progressive Spend
    # ---------------------------------------------------------------
    ws7 = wb.create_sheet("Progressive Spend")
    ws7.sheet_properties.tabColor = "4B0082"

    # Get all months across all clients
    prog_months = set()
    for client_data in progressive.values():
        for entry in client_data:
            prog_months.add(entry["month"])
    prog_months = sorted(prog_months)

    # Woolworths regions + Bunnings
    prog_clients = sorted([c for c in progressive.keys() if "Woolworths" in c or "Bunnings" in c])

    headers7 = ["Client"] + prog_months + ["Grand Total"]
    for ci, h in enumerate(headers7, 1):
        ws7.cell(row=1, column=ci, value=h)
    style_header(ws7, 1, len(headers7))

    for i, client in enumerate(prog_clients):
        r = i + 2
        ws7.cell(row=r, column=1, value=client.replace("Progressive Foods Limited - ", ""))
        month_map = {e["month"]: e["monthly_total"] for e in progressive[client]}
        total = 0
        for mi, month in enumerate(prog_months):
            val = month_map.get(month, 0)
            total += val
            ws7.cell(row=r, column=mi + 2, value=val).number_format = money_fmt
        ws7.cell(row=r, column=len(prog_months) + 2, value=total).number_format = money_fmt
        style_data_row(ws7, r, len(headers7), alt=(i % 2 == 0))

    # Cumulative row
    r = len(prog_clients) + 3
    ws7.cell(row=r, column=1, value="CUMULATIVE TOTAL (All Retail)").font = subtitle_font
    r += 1
    for ci, h in enumerate(headers7, 1):
        ws7.cell(row=r, column=ci, value=h)
    style_header(ws7, r, len(headers7))

    for i, client in enumerate(prog_clients):
        rr = r + 1 + i
        ws7.cell(row=rr, column=1, value=client.replace("Progressive Foods Limited - ", ""))
        cum_map = {e["month"]: e["cumulative_total"] for e in progressive[client]}
        for mi, month in enumerate(prog_months):
            val = cum_map.get(month, 0)
            ws7.cell(row=rr, column=mi + 2, value=val).number_format = money_fmt
        style_data_row(ws7, rr, len(headers7), alt=(i % 2 == 0))

    auto_width(ws7, len(headers7), min_w=12)

    # ---------------------------------------------------------------
    # Sheet 8: Invoice Cross-Reference
    # ---------------------------------------------------------------
    ws8 = wb.create_sheet("Invoice Cross-Reference")
    ws8.sheet_properties.tabColor = "333333"

    headers8 = ["Client", "Invoice #", "Date", "Total (incl GST)", "Paid", "Outstanding", "Status"]
    for ci, h in enumerate(headers8, 1):
        ws8.cell(row=1, column=ci, value=h)
    style_header(ws8, 1, len(headers8))

    row_idx = 2
    for contact in sorted(csv_data.keys()):
        if "Woolworths" not in contact and "Bunnings" not in contact:
            continue
        info = csv_data[contact]
        for inv_num in sorted(info["invoices"].keys()):
            inv = info["invoices"][inv_num]
            short_name = contact.replace("Progressive Foods Limited - ", "")
            ws8.cell(row=row_idx, column=1, value=short_name)
            ws8.cell(row=row_idx, column=2, value=inv_num)
            ws8.cell(row=row_idx, column=3, value=inv["date"])
            ws8.cell(row=row_idx, column=4, value=inv["total"]).number_format = money_fmt
            ws8.cell(row=row_idx, column=5, value=inv["paid"]).number_format = money_fmt
            ws8.cell(row=row_idx, column=6, value=inv["due"]).number_format = money_fmt
            status_cell = ws8.cell(row=row_idx, column=7, value=inv["status"])
            if "Paid" in inv["status"]:
                status_cell.fill = green_fill
            elif "Awaiting" in inv["status"]:
                status_cell.fill = yellow_fill
            elif "Overdue" in inv["status"]:
                status_cell.fill = red_fill
            style_data_row(ws8, row_idx, len(headers8), alt=(row_idx % 2 == 0))
            row_idx += 1

    auto_width(ws8, len(headers8))

    # ---------------------------------------------------------------
    # Sheet 9: Woolworths Store Detail (all line items)
    # ---------------------------------------------------------------
    ws9 = wb.create_sheet("WW Store Detail")
    ws9.sheet_properties.tabColor = "006400"

    headers9 = ["Invoice #", "Date", "Store", "Store #", "Hours", "Revenue (excl GST)", "Rate/Hr"]
    for ci, h in enumerate(headers9, 1):
        ws9.cell(row=1, column=ci, value=h)
    style_header(ws9, 1, len(headers9))

    ww_sorted = sorted(woolworths_records, key=lambda x: (x["store_name"], x["invoice_date"]))
    for i, rec in enumerate(ww_sorted):
        r = i + 2
        ws9.cell(row=r, column=1, value=rec["invoice_num"])
        ws9.cell(row=r, column=2, value=rec["invoice_date"])
        ws9.cell(row=r, column=3, value=rec["store_name"])
        ws9.cell(row=r, column=4, value=rec["store_num"])
        ws9.cell(row=r, column=5, value=rec["hours"]).number_format = num_fmt
        ws9.cell(row=r, column=6, value=rec["revenue_excl_gst"]).number_format = money_fmt
        ws9.cell(row=r, column=7, value=rec["hourly_rate"]).number_format = money_fmt
        style_data_row(ws9, r, len(headers9), alt=(i % 2 == 0))

    auto_width(ws9, len(headers9))

    # ---------------------------------------------------------------
    # Sheet 10: Bunnings Store Detail (all line items)
    # ---------------------------------------------------------------
    ws10 = wb.create_sheet("BN Store Detail")
    ws10.sheet_properties.tabColor = "CC0000"

    headers10 = ["Invoice #", "Date", "Store", "Service Type", "Hours", "Rate", "Revenue (excl GST)"]
    for ci, h in enumerate(headers10, 1):
        ws10.cell(row=1, column=ci, value=h)
    style_header(ws10, 1, len(headers10))

    bn_sorted = sorted(bunnings_records, key=lambda x: (x["store_name"], x["invoice_date"]))
    for i, rec in enumerate(bn_sorted):
        r = i + 2
        ws10.cell(row=r, column=1, value=rec["invoice_num"])
        ws10.cell(row=r, column=2, value=rec["invoice_date"])
        ws10.cell(row=r, column=3, value=rec["store_name"])
        ws10.cell(row=r, column=4, value=rec["service_type"])
        ws10.cell(row=r, column=5, value=rec["hours"]).number_format = num_fmt
        ws10.cell(row=r, column=6, value=rec["hourly_rate"]).number_format = money_fmt
        ws10.cell(row=r, column=7, value=rec["revenue_excl_gst"]).number_format = money_fmt
        style_data_row(ws10, r, len(headers10), alt=(i % 2 == 0))

    auto_width(ws10, len(headers10))

    # Save
    wb.save(EXCEL_OUTPUT)
    print(f"\nExcel saved: {EXCEL_OUTPUT}")
    return wb


# ===================================================================
# PHASE 4: PDF ANALYSIS REPORT
# ===================================================================

def generate_pdf_report(
    woolworths_stores: dict,
    bunnings_stores: dict,
    woolworths_records: list[dict],
    bunnings_records: list[dict],
    store_region_map: dict,
    progressive: dict,
):
    """Generate analytical PDF report."""
    from fpdf import FPDF

    def sanitize(text: str) -> str:
        replacements = {
            "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u2022": "*",
            "\u00a0": " ", "\u200b": "", "\u2192": "->", "\u2713": "[Y]",
            "\u2717": "[X]", "\u25cf": "*", "\u00b7": "-",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.encode("latin-1", errors="replace").decode("latin-1")

    class ReportPDF(FPDF):
        def header(self):
            if self.page_no() == 1:
                return
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, sanitize("CONFIDENTIAL - ASG Store-Level ROI Analysis"), align="C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- Cover page ---
    pdf.add_page()
    pdf.set_fill_color(0, 51, 102)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_y(70)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 14, sanitize("Store-Level ROI Analysis"), align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 18)
    pdf.multi_cell(0, 10, sanitize("Woolworths NZ & Bunnings NZ"), align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.multi_cell(0, 8, sanitize("Prepared for: Absolute Security Group Limited"), align="C")
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Date: {datetime.now():%d %B %Y}", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 6, "CONFIDENTIAL", align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5, sanitize(
        "This report analyses per-store return on investment across ASG's retail covert guarding contracts.\n"
        "Data sourced from Woolworths ZFI expense uploads and Bunnings invoices.\n"
        "Cost estimates based on average guard wage rates plus statutory oncosts."
    ), align="C")

    # --- Helper functions ---
    def heading(text, level=1):
        pdf.set_text_color(0, 0, 0)
        if level == 1:
            pdf.ln(6)
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(0, 10, sanitize(text))
            pdf.set_draw_color(0, 51, 102)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
        elif level == 2:
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(0, 8, sanitize(text))
            pdf.ln(2)
        elif level == 3:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(51, 51, 51)
            pdf.multi_cell(0, 7, sanitize(text))
            pdf.ln(1)
        pdf.set_text_color(0, 0, 0)

    def body(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, sanitize(text))
        pdf.ln(1)

    def bullet(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_x(15)
        pdf.multi_cell(0, 5, sanitize(f"  -  {text}"))

    def render_table(headers, rows, col_widths=None):
        """Render table with proper text wrapping."""
        num_cols = len(headers)
        page_width = 190
        line_h = 5
        min_col_w = 18

        if col_widths is None:
            # Auto-calculate based on content
            col_max_len = [len(str(h)) for h in headers]
            for row in rows:
                for ci, cell in enumerate(row):
                    if ci < len(col_max_len):
                        col_max_len[ci] = max(col_max_len[ci], len(str(cell)))
            total_len = sum(col_max_len) or 1
            col_widths = [max(min_col_w, (clen / total_len) * page_width) for clen in col_max_len]
            scale = page_width / sum(col_widths)
            col_widths = [w * scale for w in col_widths]

        def count_lines(text, width):
            if not text:
                return 1
            chars_per_line = max(1, int(width / 2.0))
            return max(1, math.ceil(len(str(text)) / chars_per_line))

        def draw_row(cells, is_header=False, is_alt=False):
            if is_header:
                pdf.set_font("Helvetica", "B", 9)
            else:
                pdf.set_font("Helvetica", "", 9)

            max_lines = 1
            for ci, cell in enumerate(cells):
                if ci < len(col_widths):
                    nl = count_lines(str(cell), col_widths[ci] - 2)
                    max_lines = max(max_lines, nl)
            row_h = max_lines * line_h

            if pdf.get_y() + row_h > pdf.h - pdf.b_margin:
                pdf.add_page()
                draw_row(headers, is_header=True)

            x_start = pdf.get_x()
            y_start = pdf.get_y()

            for ci, cell in enumerate(cells):
                if ci >= len(col_widths):
                    break
                x_pos = x_start + sum(col_widths[:ci])
                pdf.set_xy(x_pos, y_start)

                if is_header:
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.set_fill_color(0, 51, 102)
                    pdf.set_text_color(255, 255, 255)
                else:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(0, 0, 0)
                    if is_alt:
                        pdf.set_fill_color(240, 240, 240)
                    else:
                        pdf.set_fill_color(255, 255, 255)

                pdf.rect(x_pos, y_start, col_widths[ci], row_h, "DF")
                pdf.set_xy(x_pos + 1, y_start + 1)
                align = "C" if is_header else "L"
                pdf.multi_cell(col_widths[ci] - 2, line_h, sanitize(str(cell)), align=align)

            pdf.set_xy(x_start, y_start + row_h)
            pdf.set_text_color(0, 0, 0)

        draw_row(headers, is_header=True)
        for ri, row in enumerate(rows):
            draw_row(row, is_alt=(ri % 2 == 0))
        pdf.ln(3)

    # ===== CONTENT =====
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    # Calculate totals
    ww_total_rev = sum(s["total_revenue"] for s in woolworths_stores.values())
    ww_total_hrs = sum(s["total_hours"] for s in woolworths_stores.values())
    ww_total_cost = sum(s["estimated_cost"] for s in woolworths_stores.values())
    ww_margin = ww_total_rev - ww_total_cost

    bn_total_rev = sum(s["total_revenue"] for s in bunnings_stores.values())
    bn_total_hrs = sum(s["total_hours"] for s in bunnings_stores.values())
    bn_total_cost = sum(s["estimated_cost"] for s in bunnings_stores.values())
    bn_margin = bn_total_rev - bn_total_cost

    combined_rev = ww_total_rev + bn_total_rev
    combined_margin = ww_margin + bn_margin
    combined_cost = ww_total_cost + bn_total_cost

    # --- Executive Summary ---
    heading("1. Executive Summary")
    body(
        f"This report provides a comprehensive store-level return on investment (ROI) analysis for "
        f"ASG's two largest retail covert guarding contracts: Woolworths New Zealand and Bunnings New Zealand. "
        f"The analysis covers {len(set(r['invoice_num'] for r in woolworths_records))} Woolworths invoices "
        f"across {len(woolworths_stores)} stores and {len(set(r['invoice_num'] for r in bunnings_records))} "
        f"Bunnings invoices across {len(bunnings_stores)} stores."
    )

    heading("Key Findings", 2)
    render_table(
        ["Metric", "Woolworths", "Bunnings", "Combined"],
        [
            ["Total Revenue (excl GST)", f"${ww_total_rev:,.2f}", f"${bn_total_rev:,.2f}", f"${combined_rev:,.2f}"],
            ["Total Hours", f"{ww_total_hrs:,.1f}", f"{bn_total_hrs:,.1f}", f"{ww_total_hrs + bn_total_hrs:,.1f}"],
            ["Avg Hourly Rate", f"${ww_total_rev/ww_total_hrs:.2f}" if ww_total_hrs else "$0",
             f"${bn_total_rev/bn_total_hrs:.2f}" if bn_total_hrs else "$0",
             f"${combined_rev/(ww_total_hrs+bn_total_hrs):.2f}" if (ww_total_hrs+bn_total_hrs) else "$0"],
            ["Est. Labour Cost", f"${ww_total_cost:,.2f}", f"${bn_total_cost:,.2f}", f"${combined_cost:,.2f}"],
            ["Gross Margin", f"${ww_margin:,.2f}", f"${bn_margin:,.2f}", f"${combined_margin:,.2f}"],
            ["Margin %", f"{ww_margin/ww_total_rev*100:.1f}%" if ww_total_rev else "0%",
             f"{bn_margin/bn_total_rev*100:.1f}%" if bn_total_rev else "0%",
             f"{combined_margin/combined_rev*100:.1f}%" if combined_rev else "0%"],
        ]
    )

    # --- Woolworths Analysis ---
    heading("2. Woolworths New Zealand - Store Analysis")

    # Region summary
    heading("2.1 Regional Overview", 2)
    region_totals = defaultdict(lambda: {"stores": set(), "revenue": 0, "hours": 0, "cost": 0})
    for store, data in woolworths_stores.items():
        region = store_region_map.get(store, "Unknown")
        region_totals[region]["stores"].add(store)
        region_totals[region]["revenue"] += data["total_revenue"]
        region_totals[region]["hours"] += data["total_hours"]
        region_totals[region]["cost"] += data["estimated_cost"]

    region_rows = []
    for region in sorted(region_totals.keys(), key=lambda x: region_totals[x]["revenue"], reverse=True):
        rt = region_totals[region]
        margin = rt["revenue"] - rt["cost"]
        margin_pct = margin / rt["revenue"] * 100 if rt["revenue"] else 0
        region_rows.append([
            region, str(len(rt["stores"])),
            f"${rt['revenue']:,.2f}", f"{rt['hours']:,.1f}",
            f"${margin:,.2f}", f"{margin_pct:.1f}%"
        ])
    render_table(["Region", "Stores", "Revenue", "Hours", "Margin", "Margin %"], region_rows)

    # Top 20 stores
    heading("2.2 Top 20 Stores by Revenue", 2)
    sorted_ww = sorted(woolworths_stores.items(), key=lambda x: x[1]["total_revenue"], reverse=True)
    top20_rows = []
    for store, data in sorted_ww[:20]:
        region = store_region_map.get(store, "")
        top20_rows.append([
            store, region, f"${data['total_revenue']:,.2f}",
            f"{data['total_hours']:,.1f}",
            f"${data['gross_margin']:,.2f}", f"{data['margin_pct']:.1f}%"
        ])
    render_table(["Store", "Region", "Revenue", "Hours", "Margin", "Margin %"], top20_rows)

    # Bottom 10 stores
    heading("2.3 Bottom 10 Stores by Revenue", 2)
    body("These stores generate the least revenue and may warrant review for cost-effectiveness:")
    bottom10_rows = []
    for store, data in sorted_ww[-10:]:
        region = store_region_map.get(store, "")
        bottom10_rows.append([
            store, region, f"${data['total_revenue']:,.2f}",
            f"{data['total_hours']:,.1f}",
            f"${data['gross_margin']:,.2f}", f"{data['margin_pct']:.1f}%"
        ])
    render_table(["Store", "Region", "Revenue", "Hours", "Margin", "Margin %"], bottom10_rows)

    # Average rate analysis
    heading("2.4 Hourly Rate Analysis", 2)
    ww_rates = [(s, d["avg_hourly_rate"]) for s, d in sorted_ww if d["total_hours"] > 0]
    avg_rate = sum(r for _, r in ww_rates) / len(ww_rates) if ww_rates else 0
    max_rate_store = max(ww_rates, key=lambda x: x[1]) if ww_rates else ("", 0)
    min_rate_store = min(ww_rates, key=lambda x: x[1]) if ww_rates else ("", 0)

    body(f"Average hourly charge rate across all Woolworths stores: ${avg_rate:.2f}/hr")
    bullet(f"Highest rate: {max_rate_store[0]} at ${max_rate_store[1]:.2f}/hr")
    bullet(f"Lowest rate: {min_rate_store[0]} at ${min_rate_store[1]:.2f}/hr")
    bullet(f"Rate spread: ${max_rate_store[1] - min_rate_store[1]:.2f}/hr")

    # --- Bunnings Analysis ---
    heading("3. Bunnings New Zealand - Store Analysis")

    heading("3.1 Store Performance Summary", 2)
    sorted_bn = sorted(bunnings_stores.items(), key=lambda x: x[1]["total_revenue"], reverse=True)

    bn_rows = []
    for store, data in sorted_bn:
        senior_hrs = sum(v["hours"] for k, v in data["service_breakdown"].items() if "Senior" in k)
        bn_rows.append([
            store, f"${data['total_revenue']:,.2f}",
            f"{data['total_hours']:,.1f}",
            f"${data['avg_hourly_rate']:.2f}",
            f"${data['gross_margin']:,.2f}", f"{data['margin_pct']:.1f}%",
        ])
    render_table(["Store", "Revenue", "Hours", "Avg Rate", "Margin", "Margin %"], bn_rows)

    # Service type breakdown
    heading("3.2 Service Type Breakdown", 2)
    body("Bunnings utilises both standard covert guards ($43/hr) and senior covert guards ($45/hr):")

    total_senior_hrs = 0
    total_standard_hrs = 0
    total_senior_rev = 0
    total_standard_rev = 0
    for store, data in bunnings_stores.items():
        for svc, svc_data in data["service_breakdown"].items():
            if "Senior" in svc:
                total_senior_hrs += svc_data["hours"]
                total_senior_rev += svc_data["revenue"]
            else:
                total_standard_hrs += svc_data["hours"]
                total_standard_rev += svc_data["revenue"]

    render_table(
        ["Service Type", "Hours", "Revenue", "Avg Rate"],
        [
            ["Standard Covert", f"{total_standard_hrs:,.1f}", f"${total_standard_rev:,.2f}",
             f"${total_standard_rev/total_standard_hrs:.2f}" if total_standard_hrs else "$0"],
            ["Senior Covert", f"{total_senior_hrs:,.1f}", f"${total_senior_rev:,.2f}",
             f"${total_senior_rev/total_senior_hrs:.2f}" if total_senior_hrs else "$0"],
            ["Total", f"{total_senior_hrs+total_standard_hrs:,.1f}",
             f"${total_senior_rev+total_standard_rev:,.2f}", ""],
        ]
    )

    # --- Combined ROI Analysis ---
    heading("4. Combined ROI Analysis")

    heading("4.1 Top 15 Highest ROI Stores (All Clients)", 2)
    all_combined = []
    for store, data in woolworths_stores.items():
        all_combined.append(("Woolworths", store, data))
    for store, data in bunnings_stores.items():
        all_combined.append(("Bunnings", store, data))
    all_combined.sort(key=lambda x: x[2]["roi_pct"], reverse=True)

    top_roi_rows = []
    for client, store, data in all_combined[:15]:
        top_roi_rows.append([
            client, store, f"${data['total_revenue']:,.2f}",
            f"${data['gross_margin']:,.2f}",
            f"{data['margin_pct']:.1f}%", f"{data['roi_pct']:.1f}%"
        ])
    render_table(["Client", "Store", "Revenue", "Margin", "Margin %", "ROI %"], top_roi_rows)

    heading("4.2 Lowest ROI Stores (Review Candidates)", 2)
    body("Stores with the lowest ROI may require operational review, rate renegotiation, or reallocation of resources:")

    low_roi = [x for x in all_combined if x[2]["total_hours"] > 50]  # Only stores with meaningful volume
    low_roi.sort(key=lambda x: x[2]["roi_pct"])

    low_roi_rows = []
    for client, store, data in low_roi[:15]:
        low_roi_rows.append([
            client, store, f"${data['total_revenue']:,.2f}",
            f"${data['gross_margin']:,.2f}",
            f"{data['margin_pct']:.1f}%", f"{data['roi_pct']:.1f}%"
        ])
    render_table(["Client", "Store", "Revenue", "Margin", "Margin %", "ROI %"], low_roi_rows)

    # --- Recommendations ---
    heading("5. Strategic Recommendations")

    heading("5.1 Rate Optimisation", 2)
    body(
        "The analysis reveals significant variation in charge rates across stores and clients. "
        "Woolworths stores average a lower hourly rate than Bunnings, presenting an opportunity "
        "for rate review at contract renewal."
    )
    bullet(f"Woolworths average rate: ${ww_total_rev/ww_total_hrs:.2f}/hr" if ww_total_hrs else "N/A")
    bullet(f"Bunnings average rate: ${bn_total_rev/bn_total_hrs:.2f}/hr" if bn_total_hrs else "N/A")
    bullet(f"Rate gap: ${(bn_total_rev/bn_total_hrs)-(ww_total_rev/ww_total_hrs):.2f}/hr advantage to Bunnings" if (ww_total_hrs and bn_total_hrs) else "")

    heading("5.2 Store Portfolio Optimisation", 2)
    low_volume = [(c, s, d) for c, s, d in all_combined if d["total_hours"] < 100]
    body(
        f"There are {len(low_volume)} stores with fewer than 100 total hours across the analysis period. "
        f"These low-volume sites may not justify the overhead of guard scheduling and management. "
        f"Consider consolidating coverage or negotiating minimum deployment guarantees."
    )

    heading("5.3 High-Performing Store Expansion", 2)
    high_performers = [x for x in all_combined if x[2]["margin_pct"] > 25 and x[2]["total_revenue"] > 10000]
    body(
        f"There are {len(high_performers)} stores achieving both strong margins (>25%) and meaningful revenue (>$10K). "
        f"These represent the core portfolio. Opportunities to increase hours or expand services at these sites "
        f"should be prioritised."
    )

    heading("5.4 Cost Control", 2)
    body(
        f"Labour cost is estimated at ${AVG_GUARD_COST_PER_HR:.2f}/hr including oncosts. "
        f"Reducing average cost per hour by even $1.00 would improve combined margins by "
        f"${(ww_total_hrs + bn_total_hrs) * 1.0:,.0f} over the analysis period. "
        f"Strategies include optimising rostering efficiency, reducing travel time between stores, "
        f"and investing in guard retention to reduce recruitment costs."
    )

    # --- Methodology ---
    heading("6. Methodology & Assumptions")
    body("Data Sources:")
    bullet(f"Woolworths: {len(set(r['invoice_num'] for r in woolworths_records))} ZFI expense upload files")
    bullet(f"Bunnings: {len(set(r['invoice_num'] for r in bunnings_records))} PDF invoices")
    bullet("SalesInvoices CSV export from Xero (cross-reference)")
    pdf.ln(2)
    body("Cost Assumptions:")
    bullet(f"Average guard hourly wage: ${AVG_GUARD_WAGE:.2f}")
    bullet(f"Oncost multiplier: {ONCOST_MULTIPLIER:.0%} (ACC, KiwiSaver, leave provisions)")
    bullet(f"Effective cost per hour: ${AVG_GUARD_COST_PER_HR:.2f}")
    bullet("Senior guard wage premium not separately modelled (conservative approach)")
    pdf.ln(2)
    body("Limitations:")
    bullet("Labour costs are estimated using average rates - actual per-store costs may vary")
    bullet("Overhead allocation (management, travel, admin) not included in per-store ROI")
    bullet("Public holiday surcharges in Bunnings invoices use standard cost base")
    bullet("Some Woolworths store name variants have been normalised - verify mappings")

    pdf.output(PDF_OUTPUT)
    print(f"PDF saved: {PDF_OUTPUT}")
    print(f"  Pages: {pdf.pages_count}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 60)
    print("ASG STORE-LEVEL ROI ANALYSIS")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")

    # Phase 1: Extract
    woolworths_records = extract_woolworths_data()
    bunnings_records = extract_bunnings_data()
    csv_data = extract_sales_invoices()

    # Phase 2: Aggregate
    print("\n--- Aggregating store data ---")
    woolworths_stores = aggregate_store_data(woolworths_records)
    bunnings_stores = aggregate_store_data(bunnings_records)
    progressive = build_progressive_spend(csv_data)
    print(f"  Woolworths: {len(woolworths_stores)} unique stores")
    print(f"  Bunnings: {len(bunnings_stores)} unique stores")

    # Build region map for Woolworths
    inv_to_region = {}
    for contact, info in csv_data.items():
        if "Woolworths" not in contact:
            continue
        region = contact.split(" - ")[-1].replace("Woolworths ", "") if " - " in contact else contact
        for inv_num in info["invoices"]:
            num_match = re.search(r"(\d+)", inv_num)
            if num_match:
                inv_to_region[str(int(num_match.group(1)))] = region

    store_regions = defaultdict(lambda: defaultdict(int))
    for rec in woolworths_records:
        inv = str(int(float(rec["invoice_num"]))) if rec["invoice_num"] else ""
        region = inv_to_region.get(inv, "Unknown")
        store_regions[rec["store_name"]][region] += 1

    store_region_map = {}
    for store, regions in store_regions.items():
        store_region_map[store] = max(regions, key=regions.get)

    # Phase 3: Excel
    print("\n--- Generating Excel ---")
    generate_excel(
        woolworths_stores, bunnings_stores,
        woolworths_records, bunnings_records,
        csv_data, progressive,
    )

    # Phase 4: PDF
    print("\n--- Generating PDF ---")
    generate_pdf_report(
        woolworths_stores, bunnings_stores,
        woolworths_records, bunnings_records,
        store_region_map, progressive,
    )

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print(f"  Excel: {EXCEL_OUTPUT}")
    print(f"  PDF:   {PDF_OUTPUT}")
    print("=" * 60)


if __name__ == "__main__":
    main()
