"""HOTC CBD Safety Team — Daily Patrol Reports, 16-18 July 2026.

Rebuilds the raw guard logs (thursday/friday/sat.docx) into the locked
HOTC daily-report format: shifts in chronological order, entries sorted,
typos normalised, business names preserved as the guards spelled them.

Dual-saves: ~/Downloads (for sending) + canonical Operations tree.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x38, 0x64)
RED = RGBColor(0xB0, 0x1E, 0x1E)
GREY = RGBColor(0x55, 0x55, 0x55)
SUBNAVY = RGBColor(0x2E, 0x4A, 0x7A)

HOME = os.path.expanduser('~')
WEEK_DIR = os.path.join(HOME, 'Desktop/ASG/Operations/Clients/HOTC/2026/July/Week 3 13th - 19th July')


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)


def bottom_border(p, color="1F3864", sz="12"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz); b.set(qn('w:space'), '4'); b.set(qn('w:color'), color)
    pbdr.append(b); pPr.append(pbdr)


def build_day(day):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.8)
        s.left_margin = s.right_margin = Cm(2.0)
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10.5)

    # ---- Title block ----
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run('HEART OF THE CITY — CBD SAFETY TEAM'); r.bold = True; r.font.size = Pt(17); r.font.color.rgb = NAVY
    st = doc.add_paragraph(); st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run('Daily Patrol Report'); r.font.size = Pt(12); r.font.color.rgb = GREY
    sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run('Absolute Security Group  |  Auckland CBD'); r.font.size = Pt(9); r.font.color.rgb = GREY
    bottom_border(sub)
    doc.add_paragraph()

    # ---- Meta table ----
    meta = [('Date', day['date']),
            ('Operating Area', 'Auckland CBD (Heart of the City)'),
            ('Shift Coverage', day['coverage']),
            ('Prepared By', '______________________')]
    tbl = doc.add_table(rows=0, cols=2); tbl.style = 'Table Grid'
    for k, v in meta:
        row = tbl.add_row().cells
        p = row[0].paragraphs[0]; run = p.add_run(k); run.bold = True; run.font.size = Pt(9.5); run.font.color.rgb = NAVY
        shade(row[0], 'EDF0F7')
        p = row[1].paragraphs[0]; run = p.add_run(v); run.font.size = Pt(9.5)
    tbl.columns[0].width = Cm(4.5); tbl.columns[1].width = Cm(12)
    doc.add_paragraph()

    def heading(text):
        p = doc.add_paragraph()
        r = p.add_run(text); r.bold = True; r.font.size = Pt(12.5); r.font.color.rgb = NAVY
        bottom_border(p)
        p.paragraph_format.space_after = Pt(6); p.paragraph_format.space_before = Pt(12)

    def subhead(text):
        p = doc.add_paragraph()
        r = p.add_run(text); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = SUBNAVY
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)

    def entry(time, text, tag=None):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(3)
        rt = p.add_run(time + '  '); rt.bold = True; rt.font.color.rgb = NAVY
        p.add_run('—  ')
        if tag:
            rtag = p.add_run('[' + tag + '] '); rtag.bold = True; rtag.font.color.rgb = RED
        p.add_run(text)

    def bullets(items):
        for it in items:
            p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.left_indent = Cm(1.4)
            run = p.add_run(it); run.font.size = Pt(10)

    def note(text):
        p = doc.add_paragraph()
        r = p.add_run(text); r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = GREY

    for section in day['sections']:
        heading(section['title'])
        for item in section['items']:
            kind = item[0]
            if kind == 'sub':
                subhead(item[1])
            elif kind == 'e':
                entry(item[1], item[2])
            elif kind == 'ei':
                entry(item[1], item[2], tag='INCIDENT')
            elif kind == 'er':
                entry(item[1], item[2], tag='RESPONSE')
            elif kind == 'b':
                bullets(item[1])
            elif kind == 'n':
                note(item[1])

    doc.add_paragraph()
    np_ = doc.add_paragraph(); bottom_border(np_, color="CCCCCC", sz="6")
    note('Note: All photos and videos will be provided at the end of the shift report.')

    # Dual-save: Downloads + canonical Operations tree
    dl = os.path.join(HOME, 'Downloads', day['fname'])
    doc.save(dl)
    ops_dir = os.path.join(WEEK_DIR, day['ops_day'], 'Report')
    os.makedirs(ops_dir, exist_ok=True)
    ops = os.path.join(ops_dir, 'Daily Report.docx')
    doc.save(ops)
    print('SAVED:', dl)
    print('SAVED:', ops)


# ============================ THURSDAY 16 JULY ============================
THURSDAY = {
    'date': 'Thursday, 16 July 2026',
    'fname': 'HOTC Daily Report - Thursday 16 July 2026.docx',
    'ops_day': 'Thursday 16th July',
    'coverage': 'Morning (Team 1) · Day (Team 2) · Afternoon/Evening · Night (Alpha, Beta, Delta, Echo & Charlie Routes)',
    'sections': [
        {'title': 'Morning Shift — Team 1 (06:37 – 14:30)', 'items': [
            ('sub', 'Alpha Route'),
            ('e', '06:37', 'Equipment on, ready to start patrols. Heading down Queen St — Alpha Route commenced.'),
            ('e', '06:43', 'Arrived at the corner of Queen & Wyndham St intersection. Streets still fairly empty considering the time. No issues thus far. Continuing en route.'),
            ('e', '06:47', 'Arrived at the corner of Queen & Shortland St intersection. Same observation as the previous update. Continuing en route.'),
            ('e', '06:55', 'Arrived at T4 Square. Carrying out a sweep of the area. Moderate flow of civilians heading to work. No concerning issues thus far.'),
            ('e', '07:03', "Standing by at Britomart McDonald's for a brief period to display presence, considering the matter reported there earlier this week regarding a male vagrant."),
            ('e', '07:18', "Leaving our station at Britomart McDonald's. Heading back up Queen St for patrols."),
            ('e', '07:23', 'Arrived at New World Metro. A vagrant was outside gathering his belongings — appears to be relocating from the area. No concerns regarding the male in question.'),
            ('e', '07:25', 'Quick check of Vulcan Lane adjacent to our position. Brief sweep carried out.'),
            ('e', '07:29', 'Moderate traffic in the area. No concerns thus far. Continuing en route.'),
            ('er', '07:46', 'Received a call from Jo & Joes regarding what appeared to be a vagrant loitering in their lobby. Assistance was requested in moving him along. En route to the location.'),
            ('e', '07:51', 'Call back received from Jo & Joes — the male has removed himself from the vicinity. No further issues.'),
            ('e', '07:59', 'Despite the call back, we inspected the area to ensure the male had left and was not static out front. All clear. Resuming route.'),
            ('e', '08:10', 'Arrived at the Civic. No concerns in view. All clear, moving on.'),
            ('e', '08:13', 'Arrived at Aotea Square. Commencing floor checks in the area.'),
            ('e', '08:19', 'Aotea Square all clear. No concerns thus far. Moving on.'),
            ('e', '08:20', 'Heading to Atrium Shopping Centre for a sweep.'),
            ('e', '08:26', 'Arrived at Atrium Shopping Centre. Carrying out floor checks.'),
            ('e', '08:33', 'Atrium all clear. No signs of distress or concern in the area. Moving on.'),
            ('ei', '08:36', 'While heading back to Queen St we heard a commotion nearby. On inspection it was a vagrant in front of Yoyoso in distress. We approached to check on the male’s welfare.'),
            ('e', '08:41', 'Male was non-aggressive and received our concern well. Standing by to ensure no escalation.'),
            ('e', '08:46', 'Male vagrant has since calmed down. Resuming usual patrols.'),
            ('e', '08:55', 'Heading back to HQ for briefing with Team 2.'),
            ('e', '09:10', 'Briefing with Team 2 concluded. Team 2 covering lower Queen St; Team 1 covering upper Queen St.'),
            ('sub', 'Echo Route'),
            ('e', '09:15', 'Arrived at Aotea Square. Standing by to show presence.'),
            ('e', '09:20', 'Commencing welfare checks on upper Queen St.'),
            ('e', '09:30', 'Standby concluded — no issues during our stay. Heading up to Mayoral Drive.'),
            ('e', '09:35', 'Arrived at Mayoral Drive; scoping out the area. Heading down to carry out check-ins and welfare checks.'),
            ('e', '09:40', 'Arrived at Queens Food Court. Commencing welfare checks on stores in the vicinity.'),
            ('e', '09:48', 'Welfare checks completed. All clear.'),
            ('e', '09:50', 'Welfare checks on Monster Inn and Nandos out on the main street. All clear. Resuming patrols.'),
            ('er', '10:09', 'Received a call from Remedy Cafe regarding a woman screaming up and down Wellesley St, verbally abusing people walking by. The female was being disruptive, resulting in staff calling for assistance.'),
            ('e', '10:15', 'Arrived at Remedy Cafe and spoke to staff, who relayed that the female had moved on shortly after contacting us. An in-depth description was provided. No female matching the description was spotted on our way to the location — she may have gone the opposite direction, and staff were unsure which way she went. Will keep a lookout for the individual in question.'),
            ('er', '10:29', 'Received a call from Mecca regarding five individuals hanging around out front of the store being disruptive and stopping potential customers from entering. The staff member relayed that she regularly deals with these specific individuals. En route to the location to assist.'),
            ('e', '10:36', 'Arrived at Mecca; speaking to staff regarding the situation.'),
            ('e', '10:47', 'Spoke with the manager on shift, who gave a description of the group of five involved. She specifically pointed out a female whom they have reported to Police a number of times for slanging to fellow homeless in front of staff members at the corner of Queen & Victoria St West. The group was last seen heading down lower Queen St. Photos will be sent to the Ops phone when obtained by Mecca staff, and an Auror report will be submitted when received. Team 2 has been advised of the group. Standing by at Queen St & Wellesley St to show presence.'),
            ('e', '11:02', 'Team 2 close by in the area. The group has not returned. Resuming patrols.'),
            ('e', '11:10', 'Arrived at Footlocker on the way up to Mayoral Drive for a quick welfare check. No reports from staff. All clear.'),
            ('e', '11:13', 'Welfare checks completed at the following stores:'),
            ('b', ['Footlocker', 'Cosmetic Clinic', 'Strand Arcade', 'Ippondo', 'Unichem Pharmacy', 'Cuecity', 'Avachi',
                   "McDonald's Queen Street", 'Mrs Higgins', 'Timezone', 'Banhi Mi', 'Mid City Centre', '77 Convenience',
                   'Chop Panda', 'BBQ Village', 'Acceco', 'NZ Muscle', 'Remedy Coffee', 'Father Teds', 'The Civic',
                   'Yogurt Story', '24Yes Convenience Store', 'Daiso Japan', 'Game On', 'Burger Fuel', 'Metro Entertainment City']),
            ('n', 'All clear, no issues.'),
            ('e', '11:30', 'Lorne St all clear. Welfare check at Sierra Cafe — no issues for them so far today.'),
            ('e', '11:32', 'Standing by to show presence. Moderate traffic in the area.'),
            ('e', '11:50', 'All clear. Heading back to the office.'),
            ('e', '12:00', 'Interval commenced.'),
            ('e', '12:20', 'Interval concluded. Brief with Team 2.'),
            ('e', '12:30', 'Team 2 dispatched to cover upper High St. Charging Ops phone (11%).'),
            ('e', '13:15', 'Ops phone at 25%. Heading out for another patrol down Queen St.'),
            ('e', '13:18', 'Commencing welfare checks down lower Queen St.'),
            ('e', '13:27', 'Arrived at Imperial Lane. Floor checks completed. Standing by to show presence.'),
            ('e', '13:37', 'Leaving Imperial Lane. Heading down to T4 Square for another sweep.'),
            ('e', '13:45', 'Arrived at T4 Square. Area is active, but no issues of concern at the moment. Standing by, awaiting any possible response calls.'),
            ('er', '13:47', 'Received a call from Ippondo regarding two vagrants in front of the store. Assistance was requested in moving them away from the entry. Team 2 dispatched to resolve the matter.'),
            ('e', '14:00', 'All clear at T4 Square. Youths in the area, but behaviour is satisfactory. No issues to report.'),
            ('e', '14:01', 'Heading back to HQ for 30-minute break and handover to the afternoon team.'),
            ('e', '14:12', 'Taking lunch break now; preparing for changeover to the afternoon shift.'),
            ('e', '14:30', 'Handover completed. No further issues to report. Morning shift concluded.'),
        ]},
        {'title': 'Day Shift — Team 2 (09:10 – 17:00)', 'items': [
            ('e', '09:10', 'Debrief with Team 1 complete. Commencing patrols onto upper Queen St, completing welfare checks along the way.'),
            ('e', '09:30', 'Welfare checks on upper Queen St stores complete. No issues to report. Heading to Aotea Square to maintain a visible presence.'),
            ('e', '09:40', 'Thorough sweep of Aotea Square conducted. All clear, no issues to report. Heading to Victoria St via Federal St.'),
            ('e', '09:45', 'Federal St all clear, no issues. Standing by on Victoria St maintaining security presence.'),
            ('ei', '09:50', 'While on standby, a convenience store owner reported that a male had stolen a drink. The male was last seen heading down Victoria St West. Description:'),
            ('b', ['White male', 'Black jacket and sweatpants', 'Approx. 5’9”']),
            ('e', '10:00', 'Victoria St West all clear, no issues to report. Heading down Victoria St to commence patrols up Lorne St.'),
            ('e', '10:05', 'Welfare checks on Lorne St complete. Standing by maintaining a visible presence.'),
            ('e', '10:30', 'Arrived at upper Queen St. No issues or calls to report. Maintaining security presence until further notice.'),
            ('e', '11:15', 'Leaving standby area. No issues to report.'),
            ('e', '11:17', 'Heading back up Victoria St West.'),
            ('e', '11:19', 'Arrived at the corner of Albert St / Victoria St West. Standing by for any nearby response calls while maintaining security presence.'),
            ('e', '12:00', 'Morning shift advised of route changeover. Team 2 covering lower CBD.'),
            ('e', '12:02', 'Heading down Albert St. Welfare checks at:'),
            ('b', ['Albert Mart', 'Skymart', 'Scrunchy Millers']),
            ('n', 'All clear, no issues to report.'),
            ('e', '12:07', 'Arrived at lower Albert St. Welfare checks on Woolworths and Aotea Gifts. All clear, no issues to report.'),
            ('e', '12:09', 'Arrived at Reign N Pour. Welfare check — all clear, no issues to report.'),
            ('e', '12:11', "Arrived at Commercial Bay. Welfare check on McDonald's Britomart. All clear, no issues to report."),
            ('e', '12:21', 'Commercial Bay sweep complete. All clear, no issues to report. Standing by for any problematic issues or vagrants that may occur within the area.'),
            ('er', '13:05', 'Responded to a call from Mirrou regarding a female customer; asked to stand by as the female seemed suspicious. Description:'),
            ('b', ['Female', 'Blonde/orange hair (bun)', 'Black jacket', 'Black handbag', 'Maroon-style dress', 'Tattoo on the back of the neck']),
            ('e', '13:28', 'Mirrou all clear — no further issues to report (photo attached). Standing by maintaining security presence until further notice.'),
            ('e', '14:00', 'Heading up Durham St East.'),
            ('e', '14:04', 'Arrived at Chancery Square / Freyberg Square. Welfare checks on stores along High St. All clear, no issues to report.'),
            ('e', '14:08', 'Chancery Square / Freyberg Square sweep complete. All clear, no issues to report.'),
            ('er', '14:11', 'Arrived at Fort St for check-in. Jo & Joes advised that a few vagrants were outside the store and requested assistance moving them along. We advised them to move along and they complied. No issues to report. Standing by.'),
            ('e', '14:26', 'Leaving standby area — no further issues occurred. Heading back to HQ for debrief with the afternoon shift.'),
            ('e', '14:40', 'Route changeover with the afternoon shift. Team 2 covering upper CBD.'),
            ('e', '14:44', 'Commencing welfare sweeps up Victoria St West.'),
            ('e', '14:52', 'Welfare sweeps on all stores up Victoria St West complete. No issues to report. Crossing over to Federal St and Albert St to continue patrols.'),
            ('e', '15:04', 'Federal St and Albert St complete. No issues to report. Heading to Aotea Square for a full sweep.'),
            ('e', '15:13', 'Sweep of Aotea Square complete. No further issues to report. Standing by maintaining a visible presence.'),
            ('e', '15:45', 'Aotea Square all clear, no further issues to report. Crossing over to Lorne St for a full sweep.'),
            ('e', '15:53', 'Sweep up Lorne St complete. No further issues. Patrolling to Queen St.'),
            ('e', '15:56', 'Arrived at Queen St. Conducting welfare sweeps on all upper Queen St stores.'),
            ('e', '16:10', 'Welfare checks on upper Queen St complete. No further issues to report. Maintaining security presence.'),
            ('er', '16:19', 'Responded to a call from Team 1 regarding a couple suspected of stealing from Peter Alexander. On arrival, the store manager confirmed that no products were stolen. No further issues to report.'),
            ('e', '16:30', 'Queen St all clear, no issues to report. Heading back to HQ for 30-minute break.'),
            ('e', '17:00', 'Break completed. Equipment accounted for and handover completed. Team 2 standing down.'),
        ]},
        {'title': 'Afternoon / Evening Shift (14:40 – 22:30)', 'items': [
            ('e', '14:40', 'Debrief with Team B complete. Nothing to report.'),
            ('e', '14:50', 'Commencing patrols on lower Queen St.'),
            ('e', '15:04', 'Welfare checks from Farmers through to the convenience stores completed.'),
            ('e', '15:15', 'Commencing patrols down Customs St. Full sweep — all clear, no issues to report.'),
            ('e', '15:20', 'Heading down Gore St.'),
            ('e', '15:30', 'Gore St complete. No issues to report.'),
            ('e', '15:40', 'Commencing patrols toward Fort St.'),
            ('e', '15:50', 'Patrols down Fort St complete. All clear, no issues to report. Heading toward Gore St.'),
            ('e', '15:55', 'Heading back onto Queen St to show a security presence to members of the public.'),
            ('e', '16:00', 'Commencing patrols down Shortland St toward Jean Batten Place.'),
            ('e', '16:10', 'Patrols complete on Shortland St and Jean Batten Place. All clear, no issues to report.'),
            ('e', '16:25', 'Commencing welfare checks on all lower Queen St businesses.'),
            ('e', '16:36', 'Welfare checks completed. All clear, no issues to report. Standing by for security presence.'),
            ('e', '16:45', 'Commencing checks on Durham St West.'),
            ('e', '16:47', 'Patrols complete. No issues to report.'),
            ('e', '17:00', 'Commencing patrols down Durham St East, making our presence known toward High St.'),
            ('e', '17:10', 'Durham St East completed. All clear, no further issues to report.'),
            ('e', '17:13', 'Heading to High St for a full sweep.'),
            ('er', '17:20', 'Responding to a call from 188 Queen St.'),
            ('e', '17:27', 'Arrived at the location but no sign of the person who called. Tried calling the number again — no answer.'),
            ('ei', '17:30', 'Witnessed a male being assaulted by a vagrant. We moved in to apprehend the assailant and attempted to reach the victim.'),
            ('e', '17:36', 'Called Police; awaiting their arrival.'),
            ('e', '17:51', 'Police arrived and we assisted with the arrest.'),
            ('e', '18:00', 'Standing by for security presence. Police have left with the POI for processing.'),
            ('e', '18:15', 'Heading to the office to charge the Ops phone (15%).'),
            ('e', '18:33', 'Assisted the manager with setting up training for security.'),
            ('e', '19:00', 'Let security up for training.'),
            ('e', '19:30', 'Heading out on patrol to check the surrounding area.'),
            ('e', '19:40', "Localito, McDonald's Queen St, Timezone, 77 Convenience and Mid City all clear. No issues. Heading toward Aotea Square."),
            ('e', '19:45', 'Arrived at Aotea Square. Commencing patrol.'),
            ('e', '19:47', 'Received a call from the manager asking to use the swipe card to let a guard up.'),
            ('e', '19:52', 'Standing by to let the guard into the building.'),
            ('e', '20:15', 'Guard arrived — let him, the manager and team up. Heading back on patrol up Victoria St.'),
            ('e', '20:27', 'Victoria St all clear. Welfare checks from Woolworths through to 77 Convenience Store. Standing by at the corner of Victoria and Federal St.'),
            ('e', '20:45', 'Heading down Wellesley St toward Lorne St.'),
            ('e', '20:53', 'Heading through Lorne St.'),
            ('e', '20:59', 'Lorne St all clear; welfare checks on businesses completed. No issues to report. Heading to check Elliott St and Darby St.'),
            ('e', '21:07', 'Elliott St and Darby St all clear. No issues to report. Heading to the office for a break.'),
            ('e', '21:15', 'Break commenced.'),
            ('e', '21:25', 'Received a call from Hasi to stand by at Ace.'),
            ('e', '21:50', 'Heading back to the office.'),
            ('e', '22:00', 'Standing by for shift changeover.'),
            ('e', '22:30', 'Handover completed.'),
        ]},
        {'title': 'Night Shift (22:35 – 06:30)', 'items': [
            ('sub', 'Alpha Route'),
            ('e', '22:35', 'Patrolling down Queen St, conducting welfare checks along the way.'),
            ('e', '22:40', 'Welfare check on Q Convenience Store, Queen St. All clear, no issues.'),
            ('e', '22:45', 'Full sweep all around Commercial Bay and Britomart Station. All clear, no issues to report.'),
            ('e', '22:50', 'Patrolling toward the Viaduct to check up on our guards and drop off trespass notice papers for them.'),
            ('e', '23:20', 'Continuing our route, patrolling up Albert St.'),
            ('e', '23:25', 'Welfare checks on Albert Mart and the Japanese restaurant. All clear, no issues.'),
            ('e', '23:30', 'Welfare checks on the karaoke bar and Sky Mart Convenience Store. All clear.'),
            ('e', '23:35', 'Wellesley St and Mayoral Drive all clear.'),
            ('e', '23:45', 'Full sweep all around Aotea Square. All clear, no issues. Standing by at Aotea Square for any nearby calls and showing our presence.'),
            ('e', '23:50', 'Standing by in front of Bar101 to show our presence.'),
            ('ei', '23:55', 'Approached a male under the influence attempting to push his way into Bar101 after being denied entry for intoxication; he refused to leave the front door. We told the male to move along — he complied and walked away with his friend.'),
            ('e', '00:10', 'Heading back to HQ for floor checks.'),
            ('e', '00:15', 'Floor checks commencing.'),
            ('e', '00:30', 'Floor checks complete. Alpha Route complete.'),
            ('sub', 'Beta Route'),
            ('e', '00:35', 'Standing by in front of Bar101 to show our presence.'),
            ('e', '00:50', 'Continuing Beta Route.'),
            ('e', '00:55', "Welfare check on McDonald's Queen St. All clear, no issues."),
            ('e', '01:00', 'Welfare checks on Victoria St and the top of High St.'),
            ('e', '01:10', 'Full sweep all around the Freyberg area and Chancery Square. All clear, no issues.'),
            ('e', '01:20', 'Standing by at Freyberg Square for any nearby calls and showing our presence.'),
            ('e', '01:25', "Patrol through O'Connell St, the bottom of High St, Fort St and the White Lady. All clear, no issues."),
            ('e', '01:30', 'Welfare checks on Gore St and Auckland Harbour Suites. All clear, no issues. Beta Route complete.'),
            ('sub', 'Delta Route'),
            ('e', '01:35', 'Welfare checks on Britomart and Commercial Bay. All clear, no issues.'),
            ('e', '01:40', 'Welfare check on the carpark next to Chemist Warehouse. All clear, no issues.'),
            ('e', '01:45', 'Upper Queen St all clear, no issues.'),
            ('e', '02:00', 'Welfare checks on Aotea Square and Mayoral Drive. All clear, no issues.'),
            ('e', '02:05', 'Welfare check on 77 Convenience Store, Victoria St. All clear, no issues.'),
            ('e', '02:10', 'Welfare check on Albert Mart Convenience Store. All clear, no issues.'),
            ('e', '02:20', 'Patrol down Albert St.'),
            ('e', '02:30', 'Welfare checks on Customs St and Custom Mart Convenience Store. All clear, no issues.'),
            ('e', '02:35', 'Welfare checks on Fort Lane and Jo & Joe, Fort St. All clear, no issues.'),
            ('e', '02:45', 'Welfare checks on High St and High Street Supermarket. All clear, no issues.'),
            ('e', '03:00', 'Welfare checks on Chancery Square, the Freyberg area and upper High St. All clear, no issues.'),
            ('e', '03:20', 'Welfare checks on Lorne St and Auckland Library. All clear, no issues. Delta Route complete.'),
            ('sub', 'Echo Route'),
            ('e', '03:45', 'Checks on Darby St and Elliott St. All clear, no issues.'),
            ('e', '03:55', 'Patrolling up Victoria St. All clear, no issues.'),
            ('e', '04:00', 'Welfare check on 77 Convenience Store. All clear, no issues.'),
            ('e', '04:05', 'Patrolling Federal St toward Wyndham St. All clear, no issues.'),
            ('e', '04:10', 'Patrolling down Wyndham St toward Queen St. All clear, no issues.'),
            ('e', '04:15', 'Welfare checks on Q Convenience Store and Customs Mart. All clear, no issues.'),
            ('e', '04:20', 'Patrolling Fort Lane, Fort St and the bottom of High St. All clear, no issues.'),
            ('e', '04:25', 'Welfare check on High Street Supermarket. All clear, no issues.'),
            ('e', '04:35', 'Full sweep all around Chancery Square and Freyberg Square. All clear, no issues. Echo Route complete.'),
            ('sub', 'Charlie Route'),
            ('e', '04:50', 'Welfare check at the bottom of Hobson St. All clear.'),
            ('e', '05:10', 'Welfare check on 77 Convenience Store at the top of Victoria St. All clear, no issues.'),
            ('e', '05:20', 'Patrol down Victoria St toward Queen St and Lorne St. All clear, no issues. Charlie Route complete.'),
            ('e', '05:30', '30-minute break commenced.'),
            ('e', '06:00', 'Floor checks commencing.'),
            ('e', '06:15', 'Floor checks complete.'),
            ('e', '06:30', 'Handover to morning shift. Night shift concluded.'),
        ]},
    ],
}

# ============================ FRIDAY 17 JULY ============================
FRIDAY = {
    'date': 'Friday, 17 July 2026',
    'fname': 'HOTC Daily Report - Friday 17 July 2026.docx',
    'ops_day': 'Friday 17th July',
    'coverage': 'Morning (Bravo, Charlie & Echo Routes) · Afternoon/Evening · Night (Alpha & Beta Routes)',
    'sections': [
        {'title': 'Morning Shift (06:38 – 14:30)', 'items': [
            ('sub', 'Bravo Route'),
            ('n', 'Bravo Route commenced — patrolling up Queen St ensuring our presence is known.'),
            ('e', '06:38', 'Welfare check on Starbucks. All clear.'),
            ('e', '06:40', "Welfare checks on McDonald's Queen, 77 Convenience Store and Mid City. All clear."),
            ('e', '06:45', 'Welfare check on Remedy Coffee. All clear.'),
            ('e', '06:53', 'Check-in at Aotea Square. Full walkthrough completed around the area, ensuring no issues are present. Standing by to show our presence while awaiting further response calls.'),
            ('e', '07:15', 'Continuing patrols — no concerns or problems visible.'),
            ('e', '07:18', 'Welfare check along Auckland Library. All clear.'),
            ('e', '07:20', 'Check-in at the corner of Lorne and Wellesley St. All clear. Commencing welfare checks along Lorne St stores and businesses.'),
            ('e', '07:28', 'Commencing welfare checks along High St stores and businesses. No issues found.'),
            ('e', '07:33', "Walkthrough completed along Freyberg Place and the Women's Memorial Hall. No issues identified."),
            ('e', '07:35', 'Check-in at Chancery Square. Full sweep completed, ensuring no vagrants or concerns present. Standing by to show our presence and awaiting further response calls.'),
            ('e', '07:55', 'Continuing patrols — no activity requiring our assistance.'),
            ('e', '08:03', 'Check-in at Wilson Carpark. No issues visible. Welfare checks commenced on all stores and businesses within the area. All clear.'),
            ('e', '08:13', 'Check-in at the bottom of Fort St. Welfare checks on all stores and businesses within the area. All clear. Standing by for presence while awaiting response calls.'),
            ('e', '08:35', 'No issues occurred during standby. Bravo Route complete.'),
            ('sub', 'Charlie Route'),
            ('e', '08:40', 'Check-in at Kiwibank. Area scoped for any possible issues. All clear.'),
            ('e', '08:44', 'Check-in at Commercial Bay. Full sweep completed around the area, ensuring no issues present. All clear. Standing by for our presence to be known.'),
            ('e', '09:10', 'Continuing patrols — no activity visible.'),
            ('e', '09:12', 'Welfare checks on Aotea Gifts and Metro Woolworths. All clear.'),
            ('e', '09:17', 'Check-in at the corner of Customs and Albert St intersection. Area thoroughly checked. All clear. Patrolling up Albert St showing our presence.'),
            ('e', '09:21', 'Response message from management requesting our assistance at 37 Galway St at 10:00.'),
            ('e', '09:21', 'Welfare checks completed inside Albert Mart Convenience Store and Discount Dairy. All clear.'),
            ('e', '09:26', 'Arrived at Federal Square and the Cathedral. Wrapped around the area, ensuring no vagrants are causing problems.'),
            ('e', '09:31', 'Welfare checks inside Good To Go Supermarket, Hollywood Cafe, The Coffee Club and Chemist Warehouse. All clear.'),
            ('e', '09:35', 'Arrived at the corner of Queen and Wyndham St intersection. Area thoroughly cleared.'),
            ('e', '09:41', 'Arrived at Imperial Lane. Floor checks completed. No issues found.'),
            ('er', '09:58', "Response call from McDonald's Queen — a male street vagrant inside the store refusing to leave after being told to vacate by managers; the POI was harassing customers for money and food in the lobby. Team split up: one guard heading to the response call, one heading to the meeting at 37 Galway St. Team will regroup at HQ if no further response calls arise."),
            ('e', '10:09', 'Arrived at the response location — the POI had already left the store on hearing of the report call from staff. Guard standing by to ensure our presence is known and awaiting further response calls.'),
            ('e', '11:10', 'Meeting concluded at 37 Galway St with the global headquarters for Auror. Making our way to HQ to regroup with the second guard.'),
            ('e', '11:21', 'Arrived at HQ — team regrouped. Taking morning interval.'),
            ('e', '11:41', 'Continuing patrols and heading back out. Charlie Route complete.'),
            ('sub', 'Echo Route'),
            ('e', '11:45', 'Check-in at Woolworths and Chemist Warehouse, Victoria St. All clear.'),
            ('e', '11:53', 'Check-in at the top of Victoria St. Welfare checks amongst the stores at the location — no issues found. A few streeties hanging around, but no issues or complaints raised. Standing by to ensure our presence while awaiting further response calls.'),
            ('e', '12:25', 'Continuing patrols to the next checkpoint.'),
            ('e', '12:26', 'Welfare checks along AA Insurance, City Convenience Plus and Mr Barber. All clear.'),
            ('e', '12:31', 'Welfare check along Crown Plaza Hotel, making our way down through Atrium on Elliott and the food court. All clear.'),
            ('e', '12:47', 'Check-in at Elliott Street Apartments. Area thoroughly scoped out. No issues visible.'),
            ('e', '12:52', "Check-in at Aotea Square. Full walkthrough completed, ensuring no issues present. Welfare checks on Aotea Centre and Jack's Fried Chicken. All clear. Standing by to show our presence and awaiting further response calls."),
            ('e', '13:17', 'Continuing patrols — no activity visible.'),
            ('e', '13:20', 'Welfare check along Greys Ave. All clear.'),
            ('e', '13:22', 'Check-in at the top of Mayoral Drive. Full view of the area — all clear.'),
            ('e', '13:26', 'Welfare checks inside Queens Food Court, Munster Inn and Nandos. All clear.'),
            ('e', '13:33', 'Welfare checks inside Metro Entertainment City and Game On. Walkthrough completed, ensuring no vagrants or problems found.'),
            ('e', '13:48', 'Welfare checks completed at the following stores:'),
            ('b', ['Burger Fuel', 'Daiso Japan', 'Yoghurt Story', 'Remedy Coffee', 'Acceco Supermarket', 'Sals Pizza',
                   '77 Convenience Store', 'BBQ Village', 'Timezone', 'ChaPanda', 'Mrs Higgins', "McDonald's Queen",
                   'Unichem Pharmacy', 'Hulucat', 'Ava Chi', 'Sale Shop', 'Funtech', 'Strand Arcade', 'Cosmetic Clinic',
                   'Footlocker', 'Localito Convenience Store', 'Daily Drip', 'Cotton On', 'Nike', 'Lotus', 'Starbucks']),
            ('n', 'All clear.'),
            ('e', '14:00', 'Arrived at HQ. Taking lunch break and preparing for changeover to the afternoon shift.'),
            ('e', '14:30', 'Morning shift completed.'),
        ]},
        {'title': 'Afternoon / Evening Shift (14:30 – 20:30)', 'items': [
            ('e', '14:30', 'Ops phone charging; standing by at the office for calls.'),
            ('e', '15:00', "Commencing patrol on Queen St toward Aotea Square. Welfare checks on Nike, Cotton On, Ippondo, Sale Shop, Unichem, McDonald's Queen St, Footlocker, and Smiths and Caugheys. All clear, no issues."),
            ('e', '15:25', 'Aotea Square full sweep — all clear, no issues to report. Standing by for calls.'),
            ('er', '15:27', "Response call from McDonald's Queen St requesting assistance to move along a vagrant inside the venue."),
            ('e', '15:30', 'Vagrant moved along — no further issues. Commencing patrol on Queen St heading toward Commercial Bay.'),
            ('e', '15:45', 'Full sweep of Queen St completed. No issues to report. TK Square all clear.'),
            ('e', '16:00', 'Commercial Bay all clear, no issues to report. Surrounding areas, including the bus interchange, also clear. Standing by at TK Square for calls.'),
            ('e', '16:15', 'Customs St sweep — all clear, no issues to report.'),
            ('e', '16:25', 'Wilson Carpark and Gore St all clear, no issues to report. Fort Lane all clear, no issues to report.'),
            ('e', '16:30', 'High St all clear, no issues to report.'),
            ('e', '16:45', "Pioneer Women's Memorial Hall check — all clear, no issues to report."),
            ('e', '16:55', 'Full sweep of Chancery Square and Freyberg Square. All clear, no issues to report.'),
            ('e', '17:05', 'High St all clear, no issues to report.'),
            ('e', '17:11', 'Darby St all clear, no issues to report.'),
            ('e', '17:20', 'Elliott Stables and Jungle 8 welfare checks — all clear, no issues to report. Standing by for calls.'),
            ('e', '17:35', 'No response calls to report. Continuing patrol, heading to Victoria St.'),
            ('e', '17:44', 'Victoria St welfare checks complete. No further issues to report.'),
            ('e', '17:56', 'Federal St and the Cathedral welfare checks complete. No issues to report. Heading to Albert St.'),
            ('e', '18:23', 'Welfare check on Albert Mart complete — no issues to report there, nor on Albert St. Heading to Commercial Bay.'),
            ('e', '18:35', 'Customs St — no issues to report. Arriving at Commercial Bay.'),
            ('e', '19:00', 'Commercial Bay, Tyler St and Commerce St sweeps complete. No issues to report.'),
            ('e', '19:09', 'Gore St welfare sweep on Giapo, Harbour Suites, the liquor store, the convenience store, Chargrill and King Noodles. No issues to report. Making our way back onto Queen St.'),
            ('e', '19:19', 'Wyndham St — no issues to report, nor any issues on Queen St.'),
            ('e', '19:30', 'Welfare sweeps complete. No issues to report. Standing by for response calls while maintaining security presence.'),
            ('e', '20:00', 'Heading to HQ as one guard signs off.'),
            ('e', '20:10', 'At HQ, standing by for calls.'),
            ('e', '20:30', 'Second guard signs off; relieving guards are on duty.'),
        ]},
        {'title': 'Night Shift (22:52 – 06:30)', 'items': [
            ('ei', '22:52', "Response call to McDonald's Queen St — two males arguing inside. Arrived at 22:55 and separated the parties from the premises. They taunted us and attempted to argue, but ultimately left and moved away from the premises. All clear, no further issues."),
            ('e', '23:10', 'On standby at HQ, charging Ops phone (2%).'),
            ('e', '00:00', 'Commencing floor checks.'),
            ('e', '00:15', 'Floor checks complete.'),
            ('sub', 'Alpha Route'),
            ('e', '00:30', 'Check-in at Chemist Warehouse / Kathmandu. No issues.'),
            ('e', '00:35', 'Check-in at Vulcan Lane. All clear, no issues.'),
            ('e', '00:45', "Check-in at McDonald's Britomart. No issues to report."),
            ('e', '00:47', 'Patrolling Commercial Bay — full sweep commenced.'),
            ('e', '01:07', 'Commercial Bay full sweep complete. All clear, no issues.'),
            ('e', '01:15', 'Full sweep of Quay St. All clear, no issues.'),
            ('e', '01:20', 'Check-in with marina guards on standby. Showing presence.'),
            ('e', '01:40', 'All clear at the Viaduct. No issues.'),
            ('e', '01:50', 'Welfare check on the Albert St convenience store. No issues.'),
            ('e', '02:00', 'Check-in at 77 Convenience Store. No issues.'),
            ('e', '02:12', 'Patrolling Aotea Square — full sweep commenced.'),
            ('e', '02:32', 'Aotea Square full sweep complete. All clear, no issues. Alpha Route complete.'),
            ('sub', 'Beta Route'),
            ('e', '02:45', "Check-in at McDonald's Queen St. No issues to report."),
            ('e', '03:00', 'Full sweep of Freyberg Square, Chancery Square and Kitchener St. All clear, no issues to report.'),
            ('e', '03:15', 'Full sweep of Fort St / Wilson Carpark. All clear, no issues.'),
            ('e', '03:20', 'Check-in at Gore St. All clear.'),
            ('e', '03:35', "Check-in at McDonald's Britomart / Commercial Bay. All clear, no issues."),
            ('e', '03:45', 'Check-in at the corner of Quay St (AA / Providor). All clear, no issues.'),
            ('e', '04:00', 'Welfare check on the marina guards. No issues.'),
            ('e', '04:10', 'Check-in at Aotea Gifts. No issues. Beta Route complete.'),
            ('sub', 'Continued Patrols'),
            ('e', '04:20', "Check-in at St Patrick's Cathedral. All clear, no issues to report."),
            ('e', '04:25', 'Check-in at 77 Convenience Store. No issues.'),
            ('e', '04:35', 'Full sweep of Victoria St. All clear, no issues.'),
            ('e', '04:50', 'Check-in at the corner of Lorne St / Wakefield St. All clear, no issues.'),
            ('e', '05:05', 'Check-in at Aotea Square. All clear, no issues.'),
            ('e', '05:20', "Check-in at McDonald's Queen St. No issues. Heading back to HQ to charge the Ops phone (3%)."),
            ('e', '05:25', 'On standby at HQ, ready to respond to any calls; charging Ops phone.'),
            ('e', '06:00', 'Patrolling upper Queen St until handover.'),
            ('e', '06:25', 'Heading back to HQ for changeover.'),
            ('e', '06:30', 'Night shift concluded. Handover complete.'),
        ]},
    ],
}

# ============================ SATURDAY 18 JULY ============================
SATURDAY = {
    'date': 'Saturday, 18 July 2026',
    'fname': 'HOTC Daily Report - Saturday 18 July 2026.docx',
    'ops_day': 'Saturday 18th July',
    'coverage': 'Morning (single guard until 12:40 — second guard no-show)',
    'sections': [
        {'title': 'Morning Shift (06:30 – 14:30)', 'items': [
            ('e', '06:30', 'Arrived on site. Debriefed with night shift. Standing by for the second guard.'),
            ('e', '07:00', 'Notified managers of a no-show for the second guard. Preparing to patrol alone.'),
            ('e', '07:05', 'Ahmid picked up. Calling guards to see who is available to work.'),
            ('e', '07:30', 'No answer from guards. Heading out to patrol.'),
            ('e', '07:35', 'Advised by Ahmid to stand by at the office and await further orders. Any calls requiring our assistance are to be relayed to him first, to assess whether the call warranted a deviation from SOP.'),
            ('e', '11:40', "Update from Ahmid — patrol and hand out Heart of the City calling cards to businesses or persons who don't have them or request one."),
            ('er', '11:42', "Responding to a call from Britomart McDonald's regarding a petty theft from their location. Heading to the location now."),
            ('e', '11:45', 'Gave our calling card to the new store WCosmetics on Queen St, with a brief description of the service we provide for businesses.'),
            ('ei', '11:56', "Arrived at McDonald's Britomart and received a photo from the store manager regarding the incident. A male had stolen an order belonging to another customer and left with it; moments later he returned to the store and sat down in the lobby area. We were requested to trespass the individual when we come across him. Standing by for security presence."),
            ('ei', '12:03', 'Received a call from Mirrou regarding a female POI — already trespassed from the store — who had entered and stolen items, last seen heading up Victoria St. She has a history of being aggressive and violent. Description:'),
            ('b', ['Female, Māori, fair skin', 'Dressed in all black', 'Red hair, worn out (not tied up)', 'Black Nike bag', 'Greyish shoes', 'Tattoo on the side of her face']),
            ('n', 'No photo of the POI available — the store manager will try to provide a photo or retrieve store CCTV footage.'),
            ('e', '12:15', 'Ran up Wyndham St, then along Albert St; checked around the Sky Tower area and down at Woolworths. No sign of the POI.'),
            ('ei', '12:17', 'A commotion occurred at the bottom of Mecca — vagrants arguing and yelling at another vagrant. Stood by for security presence and conducted a welfare check on the victim being harassed. Standing by for security presence.'),
            ('e', '12:30', 'Heading toward Darby St to do welfare checks on stores.'),
            ('e', '12:39', 'Lumi Cafe, Celine, Recycle Boutique and Pizza Club all clear. Heading to check on surrounding businesses near HQ on Queen St.'),
            ('e', '12:40', 'Second guard arrived. Heading upstairs to update the report and complete Auror reports.'),
            ('e', '13:15', 'Break commenced.'),
            ('e', '13:18', 'Falun Dafa Chinese parade heading up Queen St — showing security presence.'),
            ('e', '13:25', 'Security presence maintained.'),
            ('er', '13:47', 'Response call from Ban-Mi requesting assistance to move loitering vagrants along from the venue.'),
            ('e', '13:55', 'Vagrants moved along — no further issues.'),
            ('e', '14:00', 'Standing by at HQ for response calls while the Ops phone charges.'),
            ('e', '14:30', 'Afternoon shift deployed. Morning shift complete — no outstanding issues.'),
        ]},
    ],
}

for d in (THURSDAY, FRIDAY, SATURDAY):
    build_day(d)
