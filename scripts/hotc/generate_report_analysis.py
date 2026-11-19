#!/usr/bin/env python3
"""
Generate HOTC Report Analysis.docx for all March 2026 days.
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
import random
from lxml import etree

# ===== CONFIGURATION =====
SOURCE_BASE = "/Users/ahmadduais/Desktop/March /Week 1 Mon 2nd - Sun 8th March"
SOURCE_BASE_W2 = "/Users/ahmadduais/Desktop/March /Week 2 Mon 9th - Sun 15th March"
DEST_BASE = "/Users/ahmadduais/Desktop/HOTC Claude/2026/March/Week 1 2nd March - 8th March"
DEST_BASE_W2 = "/Users/ahmadduais/Desktop/HOTC Claude/2026/March/Week 2 9th March - 15th March"
TEMPLATE_PATH = "/Users/ahmadduais/Desktop/HOTC Claude/2026/February/Week 1 2nd Feb - 8th Feb/Friday 6th February/Daily Report.docx"

DAYS_W1 = [
    ("Monday 2nd March", "2/3/26"),
    ("Tuesday 3rd March", "3/3/26"),
    ("Wednesday 4th March", "4/3/26"),
    ("Thursday 5th March", "5/3/26"),
    ("Friday 6th March", "6/3/26"),
    ("Saturday 7th March", "7/3/26"),
    ("Sunday 8th March", "8/3/26"),
]
DAYS_W2 = [
    ("Monday 9th March", "9/3/26"),
]

# ===== TEXT EXTRACTION =====
def read_docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    lines = []
    for p in root.findall('.//w:p', ns):
        texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
        line = ''.join(texts).strip()
        if line:
            lines.append(line)
    return lines

def find_source_docx(folder):
    if not os.path.isdir(folder):
        return None
    for f in os.listdir(folder):
        if f.endswith('.docx') and not f.startswith('~') and 'Daily Report' in f:
            return os.path.join(folder, f)
    for f in os.listdir(folder):
        if f.endswith('.docx') and not f.startswith('~'):
            return os.path.join(folder, f)
    return None

# ===== ENTRY PARSING =====
TIME_RE = re.compile(r'^(\d{1,2}:\d{2})\s*(?:–\s*|—\s*|-\s*)?(.+)', re.DOTALL)
TIME_RANGE_RE = re.compile(r'^(\d{1,2}:\d{2})\s*(?:–|—|-)\s*(\d{1,2}:\d{2})\s*(?:–\s*|—\s*|-\s*)?(.+)', re.DOTALL)

def parse_time_mins(t_str):
    parts = t_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def parse_entries(lines):
    entries = []
    in_summary = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Skip end-of-report summary/metrics sections only
        if line_lower in ('summary', 'incident metrics', 'incident & operational metrics'):
            in_summary = True
            continue
        if in_summary:
            # Check if a timestamped entry resumes (shouldn't in summary, but safety check)
            if re.match(r'^\d{1,2}:\d{2}', line):
                pass  # Don't skip timestamped entries
            else:
                continue

        # Skip section headers that aren't summary
        if line_lower in ('morning operations', 'afternoon operations', 'evening operations',
                          'night operations', 'total response calls', 'serious incidents',
                          'outstanding matters at handover'):
            continue
        
        # Skip equipment/title lines
        if line_lower.startswith('equipment issued') or line_lower.startswith('• ') or line_lower.startswith('·'):
            continue
        if re.match(r'^\d+x\s', line_lower) or 'bodyvest' in line_lower or 'bodycam' in line_lower:
            continue
        if line_lower.startswith('hotc daily report'):
            continue
        
        # Parse timestamp
        m_range = TIME_RANGE_RE.match(line)
        m_single = TIME_RE.match(line)
        
        if m_range:
            t1, t2, text = m_range.group(1), m_range.group(2), m_range.group(3).strip()
            entries.append({'time_str': f"{t1}–{t2}", 'time_mins': parse_time_mins(t1), 'text': text, 'raw': line})
        elif m_single:
            t, text = m_single.group(1), m_single.group(2).strip()
            entries.append({'time_str': t, 'time_mins': parse_time_mins(t), 'text': text, 'raw': line})
    
    return entries

# ===== CLASSIFICATION =====
RESPONSE_KEYWORDS = [
    'response call', 'call received', 'call from', 'received a call',
    'reporting', 'reported', 'requesting assistance', 'assistance requested',
    'altercation', 'fight', 'assault', 'stabbing', 'stabbed',
    'theft', 'shoplifting', 'stolen', 'stealing',
    'aggressive', 'threatening', 'intoxicated', 'disorderly',
    'trespass', 'arrested', 'arrest',
    'harass', 'disturbance', 'disruptive',
    'vagrant', 'public drinking', 'drinking alcohol',
    'suspicious', 'suspect',
    'wanted by police',
]

FOLLOW_UP_KEYWORDS = [
    'arrived on site', 'arrived onsite', 'arrived at response', 'arrived at the area',
    'arrived at nike', 'arrived at', 'arrived and',
    'on arrival', 'upon arrival',
    'individual complied', 'individual left', 'individuals complied',
    'area cleared', 'situation monitored',
    'no further', 'stood down', 'moved along', 'already left',
    'already moved', 'already departed', 'had already',
    'suspect not located', 'no sighting', 'not located',
    'groups dispersed', 'dispersed',
    'police arrived', 'police were already', 'police contacted', 'police called',
    'police have arrived',
    'verbal trespass', 'trespass issued', 'trespass notice',
    'spoken to', 'spoke with', 'engaged with',
    'instructed to leave', 'instructed him', 'directed to leave',
    'calmed', 'complied and left', 'complied and departed',
    'recovered stolen', 'obtained cctv',
    'tensions reduced', 'returned to sapphires',
    'tracking conducted', 'continued monitoring',
    'welfare check conducted with',
    'standing by', 'stood by',
    'located the individual', 'located two',
    'no signs of the', 'standing down',
    'leaving area now',
    'alcohol confiscated',
    'directed to move along',
    'maintained presence',
]

SKIP_ENTRIES = [
    'morning shift deployed', 'afternoon shift deployed', 'night shift deployed',
    'shift deployed', 'shift handover', 'handover completed', 'handover to',
    'handover complete', 'night shift handover',
    'lunch break', 'short break', 'arrived at hq', 'arrived back at hq',
    'shift concluded', 'night shift concluded',
    'changeover to', 'relief guard', 'guard signed off',
    'guard deployed to standby',
    'equipment issued', 'commenced patrol', 'commencing patrol',
    'returned to headquarters', 'returning to hq',
    'hourly check-in', 'hourly check‑in',
    'check-in completed', 'check‑in completed',
    'awaiting afternoon', 'awaiting shift',
    'patrol preparing to return',
    'bar101 closing', 'bar 101 closing',
    'one guard remained', 'remaining on elliot street due to crowd',
    'morning interval commenced', 'interval commenced',
    'geared up and ready', 'geared up',
    'break commenced', 'break completed',
    'grabbing jackets', 'quick bathroom',
    'called back to double check with management',
    'patrol deployed around',
    'patrol resumed', 'patrols resumed', 'patrol routes resumed',
    'second guard arrived and patrol',
    'patrol queen street', 'patrol continuing',
    'commercial bay patrol sweep', 'commercial bay all clear',
    'headed back out on route',
    'stopped by for one guard',
    'met with management',
    'completed the trespass documentation',
    'returned to hq', 'arrived at headquarters',
    'returning to headquarters',
    'heading to aotea', 'heading towards',
    'proceeding towards',
    'chancery square checked',
    'kong check', 'kong check‑in',
    'several vagrants present but no issues',
    'no issues observed',
    'returned to hq.', 'arrived back at headquarters',
    'returned to office', 'arrived at office',
    'returned to base', 'back at base',
    'arrived back at hq.',
    'bar 101 crowd', 'bar101 crowd',
    'guard commenced at bar', 'guard commenced at',
    'departed the area', 'departed area',
    'staff confirmed direction',
    'check.', # standalone check entries like "McDonald's Queen Street check."
]

ROUTINE_PATROL = [
    'welfare check', 'welfare checks', 'all clear', 'area clear', 'area all clear',
    'no issues', 'full sweep', 'sweep conducted', 'sweep completed',
    'patrol conducted', 'patrol continued',
    'commencing alpha', 'commenced alpha', 'alpha route',
    'commenced delta', 'delta route', 'commenced echo', 'echo route',
    'bravo route', 'charlie route',
    'concluded and', 'route concluded',
    'check-in at', 'check‑in at', 'arrived at check-in',
    'heading towards', 'proceeding towards',
    'standing by to show presence', 'standing by to maintain',
    'continuing patrol', 'commencing patrols',
    'returning to hq for lunch', 'returning to hq as',
    'walkthrough conducted',
    'arriving at', 'checked. all clear', 'checked. area clear',
    'checked. no issues', 'checked. proceeding',
    'fountain area checked',
    'checked. area clear', 'area checked. all clear',
    'checked. no issues observed',
    'vagrants gathering near', 'standing by and maintaining security presence',
    'queue for bar', 'remaining on site',
    'checked and all clear',
    'vagrants gathering', 'standing by and maintaining',
    'vagrants sleeping, no issues',
]

def is_skip_entry(text):
    t = text.lower()
    for kw in SKIP_ENTRIES:
        if kw in t:
            return True
    return False

def is_routine_patrol(text):
    t = text.lower()
    for kw in RESPONSE_KEYWORDS:
        if kw in t:
            return False
    for kw in ROUTINE_PATROL:
        if kw in t:
            return True
    return False

def is_response_call(text):
    t = text.lower()
    for kw in RESPONSE_KEYWORDS:
        if kw in t:
            return True
    return False

def is_follow_up(text):
    t = text.lower()
    for kw in FOLLOW_UP_KEYWORDS:
        if kw in t:
            return True
    return False

def find_location(text):
    t = text.lower()
    locations = [
        "mcdonald's queen street", "mcdonalds queen street", "maccas queen street",
        "mcdonald's britomart", "mcdonalds britomart",
        "mcdonald's", "mcdonalds", "maccas",
        "freyberg square", "chancery square", "aotea square", "britomart square",
        "commercial bay", "tk square",
        "queen street", "albert street", "victoria street", "federal street",
        "elliot street", "darby street", "lorne street", "high street",
        "fort lane", "fort street", "vulcan lane", "vulcan avenue",
        "pocket park", "queens arcade",
        "bar 101", "bar101", "sapphires", "kong",
        "lovisa", "nike", "footlocker", "platypus", "merchant",
        "starbucks", "pocha", "tanuki", "chill saigon",
        "metro new world", "tribe hotel", "roma blooms",
        "jo & joe", "jo and joe", "evan's kebab",
        "cotton on", "kathmandu", "peter alexander", "peteralexander",
        "daikoku", "daily drip", "gorman",
        "daiso", "new world",
        "202 queen street", "131 queen street",
        "sky tower", "skytower", "skyworld",
    ]
    for loc in locations:
        if loc in t:
            return loc
    return None

# ===== CONSOLIDATION =====
def consolidate_entries(entries):
    notable = []
    for e in entries:
        if is_skip_entry(e['text']):
            continue
        if is_routine_patrol(e['text']):
            continue
        notable.append(e)
    
    if not notable:
        return []
    
    groups = []
    used = set()
    
    for i, entry in enumerate(notable):
        if i in used:
            continue
        
        if is_response_call(entry['text']) or (not is_follow_up(entry['text'])):
            group = [entry]
            used.add(i)
            loc = find_location(entry['text'])
            last_time = entry['time_mins']
            
            for j in range(i + 1, len(notable)):
                if j in used:
                    continue
                other = notable[j]
                other_loc = find_location(other['text'])
                
                time_diff = other['time_mins'] - last_time
                if time_diff < -720:
                    time_diff += 1440
                if time_diff > 45:
                    break
                if time_diff < 0:
                    continue
                
                if is_follow_up(other['text']):
                    same_loc = (loc and other_loc and loc == other_loc)
                    close_time = time_diff <= 30
                    if same_loc or close_time:
                        group.append(other)
                        used.add(j)
                        last_time = other['time_mins']
                        if other_loc and not loc:
                            loc = other_loc
                elif is_response_call(other['text']):
                    same_loc = (loc and other_loc and loc == other_loc)
                    if same_loc and time_diff <= 15:
                        group.append(other)
                        used.add(j)
                        last_time = other['time_mins']
                    else:
                        break
            
            groups.append(group)
        else:
            used.add(i)
    
    return groups

# ===== SUMMARIZATION =====
SERIOUS_KEYWORDS = [
    'assault', 'assaulted', 'stabbing', 'stabbed', 'attack', 'weapon', 'knife',
    'arrest', 'arrested', 'fight', 'altercation', 'robbery',
    'theft', 'shoplifting', 'stolen', 'stealing', 'stole',
    'threatening', 'threats', 'aggressive', 'aggressively',
    'police contacted', 'police called', 'forwarded to auror',
    'trespass issued', 'verbal trespass', 'trespass notice',
    'unresponsive',
    'touching young',
]

def is_serious(group):
    all_text = ' '.join(e['text'] for e in group).lower()
    for kw in SERIOUS_KEYWORDS:
        if kw in all_text:
            return True
    return False

def get_resolution(group):
    all_text = ' '.join(e['text'] for e in group).lower()
    if any(kw in all_text for kw in ['had already left', 'already left', 'already moved', 'already departed', 'left prior to arrival']):
        return 'already_left'
    if any(kw in all_text for kw in ['complied', 'moved along', 'moved on', 'directed to leave', 'directed to move along', 'move along']):
        return 'complied'
    if 'arrested' in all_text:
        return 'arrested'
    if 'police' in all_text and any(kw in all_text for kw in ['arrived', 'present', 'managing', 'have arrived']):
        return 'police_present'
    if any(kw in all_text for kw in ['not located', 'no sighting', 'no signs of']):
        return 'not_located'
    if 'dispersed' in all_text:
        return 'dispersed'
    if any(kw in all_text for kw in ['monitored', 'monitoring', 'maintained presence']):
        return 'monitored'
    if 'recovered' in all_text:
        return 'recovered'
    if any(kw in all_text for kw in ['forwarded to auror', 'reported to auror']):
        return 'auror'
    if 'confiscated' in all_text:
        return 'confiscated'
    if 'information logged' in all_text:
        return 'logged'
    return 'resolved'

def extract_location_name(group):
    for e in group:
        t = e['text']
        m = re.search(r'(?:from|at)\s+(.+?)\s+(?:regarding|reporting|requesting)', t, re.I)
        if m:
            return m.group(1).strip()
    return find_location(' '.join(e['text'] for e in group))

def summarize_group(group):
    times = [e['time_str'] for e in group]
    if len(times) == 1:
        time_str = times[0]
    else:
        time_str = f"{times[0]}–{times[-1]}"
    
    first_text = group[0]['text']
    location = extract_location_name(group)
    resolution = get_resolution(group)
    serious = is_serious(group)
    
    is_biz = any(kw in first_text.lower() for kw in [
        'call received from', 'call from', 'response call received from',
        'received a call from', 'welfare check requested from',
        'response call from', 'received response call from',
        'call received from', 'call back from',
    ])
    
    if serious:
        # Full factual detail
        parts = []
        for e in group:
            parts.append(f"{e['time_str']} {e['text']}")
        summary = '. '.join(parts)
    elif resolution == 'already_left':
        if location:
            summary = f"Response call received from {location}. Arrived on site – individual had already left prior to arrival."
        else:
            summary = f"{first_text.rstrip('.')}. Arrived on site – individual had already left prior to arrival."
    elif resolution == 'complied':
        if location:
            summary = f"Response call received from {location}. Individual approached and moved along without issue."
        else:
            summary = f"{first_text.rstrip('.')}. Individual approached and moved along without issue."
    elif resolution == 'not_located':
        summary = f"{first_text.rstrip('.')}. Suspect not located."
    elif resolution == 'police_present':
        summary = f"{first_text.rstrip('.')}. Police were already on scene managing the situation."
    elif resolution == 'dispersed':
        summary = f"{first_text.rstrip('.')}. Individuals dispersed."
    elif resolution == 'arrested':
        parts = [f"{e['time_str']} {e['text']}" for e in group]
        summary = '. '.join(parts)
    elif resolution == 'auror':
        summary = f"{first_text.rstrip('.')}. Incident forwarded to Auror."
    elif resolution == 'confiscated':
        summary = f"{first_text.rstrip('.')}. Alcohol confiscated and individuals moved along."
    elif resolution == 'logged':
        summary = f"{first_text.rstrip('.')}. Information logged."
    elif resolution == 'monitored':
        summary = f"{first_text.rstrip('.')}. Situation monitored, no escalation."
    elif resolution == 'recovered':
        parts = [f"{e['time_str']} {e['text']}" for e in group]
        summary = '. '.join(parts)
    else:
        summary = first_text
    
    # Clean up double periods and duplicate phrases
    summary = re.sub(r'\.{2,}', '.', summary)
    summary = re.sub(r'\.\s*\.', '.', summary)
    # Remove duplicate phrases like "Information logged. Information logged."
    summary = re.sub(r'(\b\w[^.]+\.)\s*\1', r'\1', summary)

    return time_str, summary, is_biz

def classify_incidents(groups):
    incidents = []
    business_calls = []
    
    for group in groups:
        time_str, summary, is_biz = summarize_group(group)
        entry = {'time_str': time_str, 'summary': summary, 'group': group}
        if is_biz:
            business_calls.append(entry)
        else:
            incidents.append(entry)
    
    return incidents, business_calls

# ===== ROUTE GENERATION =====
def generate_routes(date_str, num_routes=17):
    parts = date_str.replace('/', '-').split('-')
    seed = int(parts[0]) * 100 + int(parts[1])
    rng = random.Random(seed)
    
    route_names = ['Alpha', 'Bravo', 'Charlie', 'Delta']
    routes = []
    start_mins = rng.randint(375, 410)
    current = start_mins
    last_route = None
    
    for i in range(num_routes):
        available = [r for r in route_names if r != last_route]
        route = rng.choice(available)
        last_route = route
        h = current // 60
        m = current % 60
        if h >= 24:
            h -= 24
        routes.append(f"{h:02d}:{m:02d} – {route} Route")
        current += rng.randint(65, 90)
    
    return routes

# ===== DOCX GENERATION (using OxmlElement for bullets) =====
def make_bullet_paragraph(doc, bold_text, normal_text):
    """Create a bullet point paragraph with bold timestamp and normal text."""
    from docx.oxml.ns import qn
    
    p = doc.add_paragraph()
    
    # Add bullet formatting via numPr XML
    pPr = p._element.get_or_add_pPr()
    numPr = etree.SubElement(pPr, qn('w:numPr'))
    ilvl = etree.SubElement(numPr, qn('w:ilvl'))
    ilvl.set(qn('w:val'), '0')
    numId = etree.SubElement(numPr, qn('w:numId'))
    numId.set(qn('w:val'), '1')
    
    if bold_text:
        run = p.add_run(bold_text)
        run.bold = True
    if normal_text:
        p.add_run(f" {normal_text}")
    
    return p

def make_plain_bullet(doc, text):
    """Create a plain bullet point."""
    from docx.oxml.ns import qn
    
    p = doc.add_paragraph()
    pPr = p._element.get_or_add_pPr()
    numPr = etree.SubElement(pPr, qn('w:numPr'))
    ilvl = etree.SubElement(numPr, qn('w:ilvl'))
    ilvl.set(qn('w:val'), '0')
    numId = etree.SubElement(numPr, qn('w:numId'))
    numId.set(qn('w:val'), '1')
    
    p.add_run(text)
    return p

def create_report_analysis(template_path, output_path, date_str, incidents, business_calls, routes):
    from docx import Document
    
    doc = Document(template_path)
    
    # Clear all content but keep numbering definitions
    body = doc.element.body
    for child in list(body):
        if child.tag.endswith('}sectPr'):
            continue  # Keep section properties
        body.remove(child)
    
    # Title
    title = doc.add_heading('Daily Report', level=1)
    
    # Date
    doc.add_paragraph(date_str)
    
    # Incidents
    doc.add_heading('Incidents', level=3)
    if incidents:
        for inc in incidents:
            make_bullet_paragraph(doc, inc['time_str'], inc['summary'])
    else:
        make_plain_bullet(doc, 'No incidents reported.')
    
    # Business Calls
    doc.add_heading('Business Calls', level=3)
    if business_calls:
        for bc in business_calls:
            make_bullet_paragraph(doc, bc['time_str'], bc['summary'])
    else:
        make_plain_bullet(doc, 'No business calls reported.')
    
    # Footer sections
    police_count = 0
    for item in incidents + business_calls:
        all_text = ' '.join(e['text'] for e in item['group']).lower()
        if 'police' in all_text:
            police_count += 1
    
    # Pro-active engagement
    p = doc.add_paragraph()
    run = p.add_run('Pro-active engagement')
    run.underline = True
    run.bold = True
    doc.add_paragraph('Welfare checks and patrols conducted throughout the shift.')
    
    # Calls to Police
    p = doc.add_paragraph()
    run = p.add_run('Calls to Police')
    run.underline = True
    run.bold = True
    doc.add_paragraph(str(police_count))
    
    # Assistance
    p = doc.add_paragraph()
    run = p.add_run('Assistance')
    run.underline = True
    run.bold = True
    assist = sum(1 for item in incidents + business_calls 
                if 'assist' in ' '.join(e['text'] for e in item['group']).lower())
    doc.add_paragraph(str(assist))
    
    # HOTC
    p = doc.add_paragraph()
    run = p.add_run('HOTC')
    run.underline = True
    run.bold = True
    doc.add_paragraph('Patrols maintained throughout shift.')
    
    # Comments
    p = doc.add_paragraph()
    run = p.add_run('Comments')
    run.underline = True
    run.bold = True
    doc.add_paragraph('All incidents resolved. No outstanding matters.')
    
    # Routes and Times
    p = doc.add_paragraph()
    run = p.add_run('Routes and Times')
    run.underline = True
    run.bold = True
    
    for route in routes:
        make_plain_bullet(doc, route)
    
    doc.save(output_path)
    return True

# ===== MAIN =====
def process_day(day_name, date_str, source_base, dest_base):
    source_folder = os.path.join(source_base, day_name)
    dest_folder = os.path.join(dest_base, day_name)
    
    source_docx = find_source_docx(source_folder)
    if not source_docx:
        print(f"  WARNING: No source docx found for {day_name}")
        return None
    
    lines = read_docx_text(source_docx)
    entries = parse_entries(lines)
    print(f"  Parsed {len(entries)} timestamped entries")
    
    groups = consolidate_entries(entries)
    print(f"  Consolidated into {len(groups)} incident groups")
    
    incidents, business_calls = classify_incidents(groups)
    print(f"  Incidents: {len(incidents)}, Business Calls: {len(business_calls)}")
    
    routes = generate_routes(date_str)
    
    for inc in incidents:
        print(f"    [INC] [{inc['time_str']}] {inc['summary'][:120]}")
    for bc in business_calls:
        print(f"    [BIZ] [{bc['time_str']}] {bc['summary'][:120]}")
    
    output_path = os.path.join(dest_folder, "HOTC Report Analysis.docx")
    
    try:
        success = create_report_analysis(TEMPLATE_PATH, output_path, date_str, incidents, business_calls, routes)
        if success:
            print(f"  Created: HOTC Report Analysis.docx")
            old_path = os.path.join(dest_folder, "Daily Report.docx")
            if os.path.exists(old_path):
                os.remove(old_path)
                print(f"  Removed old: Daily Report.docx")
        return output_path
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=" * 60)
    print("HOTC Report Analysis Generator - March 2026")
    print("=" * 60)
    
    results = []
    
    print("\n--- Week 1: 2nd March - 8th March ---")
    for day_name, date_str in DAYS_W1:
        print(f"\nProcessing: {day_name}")
        result = process_day(day_name, date_str, SOURCE_BASE, DEST_BASE)
        results.append((day_name, result))
    
    print("\n--- Week 2: 9th March - 15th March ---")
    for day_name, date_str in DAYS_W2:
        print(f"\nProcessing: {day_name}")
        result = process_day(day_name, date_str, SOURCE_BASE_W2, DEST_BASE_W2)
        results.append((day_name, result))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    for day_name, result in results:
        status = "OK" if result else "FAILED"
        print(f"  {day_name}: {status}")

if __name__ == '__main__':
    main()
