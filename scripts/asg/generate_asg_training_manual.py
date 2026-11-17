#!/usr/bin/env python3
"""
ASG Bars & Events Security — Guard Field Manual & Training Programme.

Merges ASG's induction handbook (booklet.docx) + the 15-module training spine
(Training Booklet.pdf) and grounds both in current NZ law (verified July 2026):
PSPLA/COA licensing + mandatory training, Sale & Supply of Alcohol Act 2012,
Trespass Act 1980 / Crimes Act 1961 use-of-force limits, Auckland LAP, HSWA 2015.

Output: editable .docx (professionally styled) to ~/Desktop/ASG/Operations/Training/.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT_DIR = os.path.expanduser("~/Desktop/ASG/Operations/Training")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "ASG Bars & Events Security - Guard Field Manual (July 2026).docx")

NAVY = RGBColor(0x1F, 0x3B, 0x63)
BLUE = RGBColor(0x2E, 0x5C, 0x8A)
GREY = RGBColor(0x66, 0x66, 0x66)
RED = RGBColor(0xB0, 0x00, 0x00)
GREEN = RGBColor(0x1E, 0x6B, 0x3A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(10.5)
for s in doc.sections:
    s.top_margin = Inches(0.85); s.bottom_margin = Inches(0.85)
    s.left_margin = Inches(0.9); s.right_margin = Inches(0.9)


# ---------------- helpers ----------------
def _shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), hexcolor); tcPr.append(shd)

def para(text="", bold=False, italic=False, size=10.5, color=None, after=5, before=0, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align: p.alignment = align
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        if color: r.font.color.rgb = color
    return p

def rich(segs, after=5, before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    for t, a in segs:
        r = p.add_run(t)
        r.bold = a.get("bold", False); r.italic = a.get("italic", False)
        r.font.size = Pt(a.get("size", 10.5))
        if a.get("color"): r.font.color.rgb = a["color"]
    return p

def h1(text, n=None):
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '10'); bottom.set(qn('w:space'), '3'); bottom.set(qn('w:color'), '1F3B63')
    pbdr.append(bottom); pPr.append(pbdr)
    r = p.add_run((f"{n}   " if n else "") + text); r.bold = True; r.font.size = Pt(16); r.font.color.rgb = NAVY
    return p

def h2(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(9); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(12.5); r.font.color.rgb = BLUE
    return p

def h3(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(10.5)
    return p

def bullet(text, lead=None, sub=False):
    p = doc.add_paragraph(style="List Bullet 2" if sub else "List Bullet")
    p.paragraph_format.space_after = Pt(1.5)
    if lead:
        r = p.add_run(lead); r.bold = True
    p.add_run(text)
    return p

def numbered(text, lead=None):
    p = doc.add_paragraph(style="List Number"); p.paragraph_format.space_after = Pt(2)
    if lead:
        r = p.add_run(lead); r.bold = True
    p.add_run(text); return p

def callout(label, lines, fill="EEF3F9", labelcolor=NAVY):
    """Shaded single-cell box. lines = list of (text, {attrs}) OR plain str."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"
    cell = t.rows[0].cells[0]; _shade(cell, fill)
    cell.paragraphs[0].text = ""
    lp = cell.paragraphs[0]; lp.paragraph_format.space_after = Pt(2)
    lr = lp.add_run(label); lr.bold = True; lr.font.size = Pt(9.5); lr.font.color.rgb = labelcolor
    for ln in lines:
        p = cell.add_paragraph(); p.paragraph_format.space_after = Pt(1.5)
        if isinstance(ln, str):
            r = p.add_run(ln); r.font.size = Pt(9.5)
        else:
            for seg, a in ln:
                r = p.add_run(seg); r.font.size = Pt(a.get("size", 9.5))
                r.bold = a.get("bold", False); r.italic = a.get("italic", False)
                if a.get("color"): r.font.color.rgb = a["color"]
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return t

def law(lines):     callout("⚖  THE LAW", lines, fill="EAF1FB", labelcolor=NAVY)
def warn(lines):    callout("⚠  RISK — READ THIS", lines, fill="FDECEC", labelcolor=RED)
def field_tip(lines): callout("★  ON THE DOOR", lines, fill="EAF6EE", labelcolor=GREEN)

def table(headers, rows, widths=None, fontsize=9, header_fill="1F3B63"):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
    hc = t.rows[0].cells
    for i, hh in enumerate(headers):
        _shade(hc[i], header_fill); hc[i].paragraphs[0].text = ""
        r = hc[i].paragraphs[0].add_run(hh); r.bold = True; r.font.size = Pt(fontsize); r.font.color.rgb = WHITE
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].paragraphs[0].text = ""
            r = cells[i].paragraphs[0].add_run(str(val)); r.font.size = Pt(fontsize)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return t

def objectives(items):
    h3("Learning objectives — you can:")
    for it in items:
        bullet(it)

def trainer(method):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Trainer method:  "); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = GREY
    r2 = p.add_run(method); r2.font.size = Pt(9); r2.italic = True; r2.font.color.rgb = GREY

def pagebreak(): doc.add_page_break()


# ================= COVER =================
for _ in range(2): doc.add_paragraph()
para("ABSOLUTE SECURITY GROUP", bold=True, size=26, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("Bars & Events Security", bold=True, size=18, color=BLUE, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para("GUARD FIELD MANUAL", bold=True, size=22, color=RGBColor(0,0,0), align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
para("& Training Programme", bold=True, size=15, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=18)
para("“Firm but fair — the ASG Style”", italic=True, size=13, color=BLUE, align=WD_ALIGN_PARAGRAPH.CENTER, after=26)
para("Weekly Thursday Induction & Refresher Course", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("Edition: July 2026", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("Aligned to New Zealand law current as at July 2026", size=10, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=40)
para("PRIVATE & CONFIDENTIAL — property of Absolute Security Group. For issued ASG personnel only.",
    size=9, color=GREY, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
pagebreak()

# ================= HOW TO USE / CONTENTS =================
h1("How to use this manual")
para("This manual does two jobs. It is your handbook — who we are, how we work, and the standards you agree to as an ASG guard — and it is your training programme, the 15 modules run at the Thursday induction and refresher.")
para("Throughout, watch for these boxes:")
callout("⚖  THE LAW", [[("The actual New Zealand law behind what we do — with the Act and section, so you know it is real, not just company preference.", {})]])
callout("⚠  RISK — READ THIS", [[("Where you personally can get charged, fined, or lose your Certificate of Approval. These are the lines you do not cross.", {})]], fill="FDECEC", labelcolor=RED)
callout("★  ON THE DOOR", [[("The practical move — what to actually do or say in the moment.", {})]], fill="EAF6EE", labelcolor=GREEN)
para("")
h2("Contents")
for line in [
    "Part 1 — Welcome & The ASG Way",
    "Part 2 — Getting Deployed: your licence, training & readiness",
    "Part 3 — The Law You Work Under (alcohol, force, Auckland, health & safety)",
    "Part 4 — The 15 Training Modules",
    "Part 5 — Quick-Reference Cards, Assessment & Sign-off",
]:
    bullet(line)
pagebreak()

# ================= PART 1 — WELCOME =================
h1("Welcome & The ASG Way", "PART 1")
h2("1.1  About ASG")
para("Absolute Security Group (ASG) was created in 2022 to close a growing gap in Auckland's hospitality security industry. We have stood apart from other providers by strategically developing our guards' skillsets and taking a more direct, professional approach to service delivery.")
para("We run a Patrol Branch, a Static Branch and an Events Sector, so our guards enjoy a diverse range of work and roles that challenge them to grow. Our mission is simple: every person who approaches our guards or uses our services should feel safe and enjoy their experience with us.")
para("Nau mai, haere mai ki Absolute Security Group. Welcome to the team.", italic=True, color=BLUE)

h2("1.2  The ASG Style — firm but fair")
para("The ASG Style is the perfect balance of firm but fair. We want security professionals who are part host, part custodian: delivering service with a smile while never compromising safety. Always engage in a positive, friendly manner — but don't let patrons take advantage of that positivity. Keep enforcing the conditions of your venue.")
para("Three things make a great host and guard:", bold=True)
para("Presentation.", bold=True, after=1)
para("Take pride in your full uniform, correctly worn — a fully uniformed team creates a cohesive, professional image. Ask yourself: Is my uniform clean and ironed? Does it fit? Are my shoes appropriate and polished?", after=4)
para("Service.", bold=True, after=1)
para("It is our duty to ensure every patron has a pleasant experience. A great host is friendly, welcoming, approachable, pleasant — and always a problem solver. Seek to exceed expectations.", after=4)
para("Attitude.", bold=True, after=1)
para("You set the mood as the first and last person a patron meets. Ask yourself:", after=1)
bullet("Am I contributing to the energy of the venue, or subtracting from it?")
bullet("Am I treating people the way I'd like to be treated?")
bullet("Am I creating a safe, approachable environment for patrons and staff?")

h2("1.3  Uniform & personal presentation")
para("You are required to provide: plain black dress pants, plain black dress shoes, black dress socks, and a black dress belt. For corporate events you must provide your own plain, matching black suit jacket and trousers.")
h3("Grooming standards")
bullet("All uniform must be clean, ironed and worn professionally.")
bullet("Jewellery may be worn if it doesn't detract from the uniform (small stud earrings, discreet rings, a conservative watch). Avoid large, heavy items that can be a hazard in a scuffle.")
bullet("Excellent personal hygiene is essential.")
bullet("Long hair tied back, tidy and well maintained.")
bullet("Clean-shaven or a neatly groomed beard.")
bullet("Under-layers must be black and plain, and not visible.")
bullet("No eating, drinking or smoking while in uniform and on duty.")

h2("1.4  The uniform bond system")
para("We bond most uniform items. A bond means a portion of your pay is held against an item; the maximum we deduct is $50 per weekly pay. When you leave ASG and return the bonded uniform clean and undamaged, the full amount is returned to you as a lump sum in the next pay cycle.")
para("Example: an ASG polo ($50) and coat ($200) = $250 bonded at $50/week for 5 weeks; returned clean on exit, you receive $250 back next pay cycle.", italic=True, size=9.5, color=GREY)
law([[("Any deduction from your wages — including a uniform bond — requires your written consent and must be reasonable (Wages Protection Act 1983, s5/s5A). You will be asked to sign a bond authority before any deduction is made, and each item and amount will be confirmed with you first.", {})]])
h3("Replacements")
rich([("Covered by ASG: ", {"bold": True}), ("damage on duty during an incident, fading of logos, general wear and tear.", {})])
rich([("Re-bonded to you: ", {"bold": True}), ("avoidable damage on duty, loss or theft, damage off duty.", {})])

h2("1.5  Conduct standards")
bullet("Respectful, professional, polite language at all times — never offensive, abusive, racist or derogatory, to anyone (patrons, staff or colleagues).", lead="Language.  ")
bullet("No personal phone use on duty. Personal calls/texts must be cleared by your Head Doorman or supervisor. Work-related exchanges (intel from other sites, management contact) are fine.", lead="Mobile phone.  ")
bullet("No smoking in uniform on shift — only on a break, away from the venue, ASG items removed or covered. Eat out of patron view and only when cleared. Never skull drinks in front of patrons.", lead="Smoking / eating.  ")
bullet("You are held to a higher standard than an average patron, even off duty and at non-ASG venues. At an ASG venue on your night off, do not involve yourself in situations or advise on-duty guards — let them work.", lead="Off-duty conduct.  ")
bullet("Take particular care with anything that can be linked to ASG. Inappropriate posts may lead to disciplinary action.", lead="Social media.  ")
bullet("Never disclose information learned at work about the company, management, clients, customers or colleagues (Privacy Act 2020).", lead="Confidentiality.  ")
bullet("Never accept a bribe of any kind for entry or any favour. Zero tolerance — you will be reprimanded and may be dismissed.", lead="Bribes.  ")
bullet("Hand all lost property to venue bar staff. Never remove property that isn't yours, and never open pockets or reach inside a bag. Tip: carry found property held visibly above waist height as you walk it to the bar.", lead="Lost property.  ")
pagebreak()

# ================= PART 2 — GETTING DEPLOYED =================
h1("Getting Deployed", "PART 2")
para("Before you work a single shift, three things must be true: you hold a current Certificate of Approval, you are (or are becoming) trained, and you are fit for duty. This Part is the law and the process behind being deployable.")

h2("2.1  Your Certificate of Approval (COA)")
para("Door and bar security is “crowd control” work, and by law you must hold a current Certificate of Approval (COA) in the Crowd Controller class to do it. ASG holds the Company Licence you work under; your COA is your personal authorisation.")
law([
    [("Private Security Personnel and Private Investigators Act 2010 (PSPPI Act), administered by the PSPLA.", {"bold": True})],
    [("• Door/bar security = the ", {}), ("Crowd Controller", {"bold": True}), (" class (checking who enters, keeping order, removing people). You must be 18+.", {})],
    [("• You must ", {}), ("wear your PSPLA ID badge so it is visible at all times while working", {"bold": True}), (" (s67) and produce your certificate on request to Police, a PSPLA officer, or a person you deal with. Not displaying it = fine up to $2,000.", {})],
    [("• Working ", {}), ("without a current COA is an offence — fine up to $20,000 for you AND for ASG", {"bold": True, "color": RED}), (" (s44). This is why we check every guard's COA before deployment — no COA, no shift.", {})],
])
field_tip([[("A ", {}), ("Temporary COA", {"bold": True}), (" (the “blue” certificate) lets you work while you finish training — it lasts about 3 months. Some venues won't accept temporary/blue-COA guards where they want experience; that's the venue's call.", {})]])

h2("2.2  Mandatory training")
para("To hold a full Crowd Controller COA you must complete the mandatory NZQA training and upload your Record of Achievement. You can start on a temporary COA and finish training within its life.")
law([
    [("Three NZQA standards are required (Minimum Training Regulations 2013):", {"bold": True})],
    [("• Legal knowledge / introduction to the security industry — ", {}), ("Unit Standard 27364", {"bold": True}), (" (covers licensing, arrest, trespass, use of force, search limits, H&S, reporting).", {})],
    [("• Conflict management — ", {}), ("Unit Standards 27360 and 27361", {"bold": True}), (".", {})],
    [("• NZQA is moving these to new ", {}), ("skill standards 40145 / 40146 / 40147", {"bold": True}), ("; both sets are accepted now, but the old unit standards expire ", {}), ("31 December 2027", {"bold": True}), (" — finish yours before then. Confirm the exact standards/credits with your training provider.", {})],
    [("• Holding the ", {}), ("NZ Certificate in Security (Foundation L3 or Advanced L4)", {"bold": True}), (" also satisfies this. No refresher is legally required — but ASG runs ongoing training you're expected to attend.", {})],
])

h2("2.3  Staying eligible")
para("Certain convictions affect whether the PSPLA will grant or keep your COA. Being disqualified is not always an automatic bar — the Authority applies a “fit and proper” test — but you must be upfront.")
bullet("Permanent bar: ever sentenced to imprisonment; serious sexual offending; indefinite driving disqualification.", lead="")
bullet("7-year bar (conviction in the last 7 years): dishonesty, violence, serious drug or firearms offences.", lead="")
warn([[("Tell ASG immediately if you are charged with or convicted of any offence, or if your COA is suspended, cancelled or not renewed. Working on a COA you're no longer entitled to puts you and ASG in breach.", {})]])

h2("2.4  Rostering, sign-in & punctuality")
bullet("Download Deputy — you'll get your roster a week ahead through the app.", lead="Deputy.  ")
bullet("Pulling out needs 24 hours' notice. Late pull-outs and no-shows damage your standing — don't abuse it. Genuine shift-change requests (later start, early finish) are welcome; we'll work with you where feasible.", lead="Pull-outs / requests.  ")
bullet("Be at least 5 minutes early, report to your Head Doorman / Team Leader, and be deployed and ready the moment your shift starts (radio on, PPE sorted).", lead="Punctuality.  ")
bullet("Clock on in Deputy when you arrive on site (don't try to clock on from a distance — the system flags it). At the end, “end shift” in Deputy and complete the on-site timesheet. Both before you leave.", lead="Sign in / out.  ")
bullet("If your individual shift is under 3 hours, or is cancelled after you've arrived on site, you're paid a minimum of 3 hours.", lead="Minimum hours.  ")

h2("2.5  Fitness for duty (alcohol & drugs)")
para("You must arrive fit to work. ASG has a zero-tolerance policy on turning up impaired by alcohol or drugs — it's a safety issue for you, your team and the public.")
warn([
    [("If you present unfit for duty you will not be deployed and will be stood down while the matter is dealt with under our fitness-for-duty and disciplinary process.", {"bold": True})],
    [("Never consume alcohol in ASG uniform — on or off an ASG site. Never drink or use drugs while on duty; doing so will result in you being stood down and disciplined.", {})],
])
law([[("A security worker who is ", {}), ("intoxicated while on duty commits an offence personally", {"bold": True}), (" — Sale and Supply of Alcohol Act 2012, s251, fine up to $2,000. Your fitness for duty is also your own legal responsibility, not just a company rule.", {})]])
para("Note on pay: we don't automatically “forfeit” a stood-down guard's pay on the spot — pay is handled correctly through the process. Your job is simply to always turn up fit for work.", size=9, italic=True, color=GREY)

h2("2.6  Who you report to")
para("All staff report to their Team Leader. On a bar shift you report directly to the Head Doorman and follow their instructions. Above them sit Supervisors and Operations Managers. Escalate anything you're unsure about — early.")
pagebreak()

# ================= PART 3 — THE LAW =================
h1("The Law You Work Under", "PART 3")
warn([[("The single most important thing in this manual: ", {"bold": True}), ("a licensed guard has no more legal power than any ordinary citizen, plus the venue's right to remove trespassers. Your COA lets you do the job lawfully — it gives you NO special power to use force, search, seize or arrest. The moment your force goes beyond what the law allows, YOU become the offender.", {})]])

h2("3.1  The Sale & Supply of Alcohol Act 2012 — your job in law")
para("The Act's object (s4) is that alcohol is sold, supplied and consumed safely and responsibly, and that alcohol-related harm is minimised. Almost everything you do at the door serves that object — and earns the venue its legal defences.")

h3("Intoxication — the legal test (s5)")
para("A person is “intoxicated” in law when they are observably affected by alcohol or drugs to the degree that 2 or more of these are evident: Speech, Coordination, Appearance, Behaviour. It's about what you observe — not how many drinks. Remember it as SCAB.")
table(
    ["Sign", "Sober — monitor & serve", "Influenced — INTERVENE", "Intoxicated — DENY & REMOVE"],
    [
     ["Speech", "Clear, coherent, normal", "Loud, talkative, interrupts, stumbles over words", "Slurring, repetitive, nonsensical, loses the thread"],
     ["Coordination", "Balanced, steady", "Slowed reactions, sway, occasional stagger", "Stumbles, spills, weaves, can't stand unaided"],
     ["Appearance", "Tidy, clear eyes, alert", "Vacant look, smell of alcohol, untidy", "Glazed/bloodshot eyes, can't focus, dishevelled, sleepy"],
     ["Behaviour", "Sensible, relaxed", "Over-friendly/withdrawn, argumentative, drinking faster", "Aggressive, rude, belligerent, affecting others"],
    ],
    widths=[0.9, 1.9, 2.1, 2.1], fontsize=8)
para("Two or more signs from the right-hand column = intoxicated in law. At the “Influenced” stage the correct move is to intervene early (slow things down, water, food, a word to the manager) — that's how the venue avoids the offence of letting someone get intoxicated.", size=9.5)

h3("The offences — and who is liable")
para("The alcohol offences fall on the licensee and the certificated duty manager, not on you as such. But your action (or inaction) is what makes or breaks their defence — and one offence catches you personally.")
table(
    ["Section", "Offence", "Max penalty"],
    [
     ["s248", "Selling / supplying alcohol to an intoxicated person", "Licensee/manager $10,000 (+ licence suspension); other person $2,000"],
     ["s249", "Allowing a person to become intoxicated on the premises", "Licensee/manager $10,000"],
     ["s252", "Allowing an intoxicated person to be or remain on the premises", "$5,000"],
     ["s253", "Allowing violent / disorderly conduct on the premises", "$10,000"],
     ["s251", "An employee (e.g. a GUARD) being intoxicated on duty", "$2,000 — this one is YOU"],
     ["s239", "Selling / supplying / allowing alcohol to an under-18", "Licensee/manager $10,000; other person $2,000"],
    ],
    widths=[0.7, 3.6, 2.7], fontsize=8.5)

law([
    [("The defence you deliver — s252(3) & s253(3).", {"bold": True})],
    [("It is a defence for the venue if, as soon as anyone became aware, ", {}), ("reasonable steps", {"bold": True}), (" were taken to either ", {}), ("take the person to a place of safety on the premises, or remove them", {"bold": True}), (". Prompt, sensible removal — and a note of it — is exactly what the law rewards. Slow or no action destroys the defence.", {})],
])
field_tip([[("So when you remove an intoxicated or disorderly patron, you are not “throwing your weight around” — you are performing the venue's legal defence. Do it calmly, promptly, and log it (time, what you saw, what you did, who you told).", {})]])

h3("Minors — the purchase age is 18")
para("Only three documents are acceptable evidence of age: a New Zealand or overseas passport, a New Zealand photo driver licence, or the Kiwi Access Card (the old HANZ 18+ card). Nothing else — not a student ID, not a work ID, not a photo of a document.")
law([
    [("• s239 — serving/allowing an under-18 to be served (up to $10,000). s245 — allowing a minor into a restricted area. s257 — presenting a fake, altered or someone else's ID is an offence for the patron.", {})],
    [("• The venue's ", {}), ("defence", {"bold": True}), (" is that an approved ID was produced (or an approved scanning system used) and staff believed on reasonable grounds it was genuine and showed the person was 18+. ", {}), ("This is why we check — and record — ID at the door.", {"bold": True})],
])
field_tip([[("You may require ID as a condition of entry and refuse entry if it isn't produced or looks false. You may ", {}), ("not", {"bold": True}), (" seize or confiscate an ID — that's a Police power. If you believe an ID is fake, refuse entry and tell the duty manager; hand a suspected forgery to Police, don't keep it yourself.", {})]])

h3("The Duty Manager and host responsibility")
para("Every on-licence must have a certificated Duty Manager on duty whenever alcohol is served (s214). Their name is displayed inside, and they are legally responsible for compliance and reducing harm. You are not the duty manager — you support them and escalate to them. Refusals, ejections and incidents go to the named manager, and get recorded.")
para("The venue must also (by law) keep free drinking water available, and provide food, low/no-alcohol options and transport information (ss51–54, s110). Don't obstruct patrons getting water or help with a taxi at the exit — these are the licensee's legal duties too.", size=9.5)

h3("Trading hours")
law([[("The national default for on-licences is 8am–4am (s43), but the ", {}), ("hours that actually apply are the ones printed on THAT venue's licence", {"bold": True}), (", plus any one-way-door condition (s44, s110). Always work to the venue's licensed close time — many close well before 4am. Clearing patrons out at close is how the venue avoids the “open after hours” offence (s256).", {})]])

h2("3.2  Your powers & limits — trespass and force")
h3("Removing an unwanted patron (Trespass Act 1980 + Crimes Act s56)")
law([
    [("• As a guard you count as an “occupier” of the venue (Trespass Act s2), so you can act on its behalf.", {})],
    [("• You may ", {}), ("warn a person to leave", {"bold": True}), (" (s3). If they refuse, they are committing an offence. A verbal warning is legally valid — note it down (s5).", {})],
    [("• A ", {}), ("trespass notice", {"bold": True}), (" (warning to stay away) lasts ", {}), ("2 years", {"bold": True}), (" (s4).", {})],
    [("• To physically remove a non-violent trespasser you may use ", {}), ("reasonable force to escort/steer them out — but you must NOT strike them or cause bodily harm (Crimes Act s56)", {"bold": True}), (".", {})],
])
h3("Self-defence (Crimes Act s48)")
para("You may use force to defend yourself or another that is reasonable in the circumstances as you genuinely believe them to be. Injury-causing force is lawful only when you are genuinely defending against a real threat, and only in proportion — and you must stop the instant the threat stops.")
h3("Citizen's arrest — narrow, and dangerous to get wrong (s35 / s36)")
law([
    [("You may arrest without warrant only:", {"bold": True})],
    [("• a person you ", {}), ("find committing", {"bold": True}), (" an offence with a maximum penalty of ", {}), ("3 years or more", {"bold": True}), ("; OR", {})],
    [("• ", {}), ("between roughly 9pm and 6am", {"bold": True}), (", a person you find committing ", {}), ("any", {"bold": True}), (" Crimes Act offence — with reasonable and probable grounds.", {})],
    [("Common assault (max 1 year) and minor theft do ", {}), ("not", {"bold": True}), (" qualify by day. A vague suspicion is never enough. If you arrest, hand the person to Police as soon as possible — you cannot run your own detention.", {})],
])
warn([
    [("Excess force = you are the criminal (Crimes Act s62 → s196 common assault, or s188 wounding, up to 14 years). The classic traps that turn “doing the job” into a charge:", {"bold": True})],
    [("strikes or punches during a removal · chokeholds / headlocks · takedowns that injure · kneeling or sitting on someone · continuing force after they've stopped resisting · holding someone with no lawful arrest (that's false imprisonment).", {})],
])
h3("What you may NEVER do")
bullet("Carry or use weapons — no batons, and OC/pepper spray is a restricted weapon under the Arms Act. Illegal for guards.", lead="No weapons. ")
bullet("Use handcuffs or restraints as a matter of course — only ever as part of a lawful arrest, with reasonable, non-injurious force.", lead="No routine restraint. ")
bullet("Search a person or their bag, or go through their property, without consent. A bag check is a condition of entry — if they refuse, refuse them entry; you cannot force it.", lead="No search / seizure. ")
bullet("Detain anyone beyond a lawful arrest, or hold them to question or search them.", lead="No unlawful detention. ")

h2("3.3  Auckland rules")
para("Auckland's Local Alcohol Policy has been in force since December 2024. It controls harm mainly through trading hours (there is no citywide one-way-door rule — a one-way door only applies where an individual venue's licence carries it).")
table(
    ["Licence type", "Maximum close (Auckland)"],
    [["On-licence — city centre (bars/pubs/clubs)", "4:00am"],
     ["On-licence — rest of Auckland (suburbs)", "3:00am"],
     ["Club licence", "1:00am"],
     ["Off-licence (bottle stores/supermarkets)", "9:00pm"]],
    widths=[3.9, 2.1], fontsize=9)
para("These are ceilings — always work to the individual venue's licensed hours. Four agencies watch licensed premises: the District Licensing Committee, Council Licensing Inspectors (who run controlled purchase operations with fake-ID minors), Police, and the Medical Officer of Health. Serving intoxicated patrons or a host-responsibility failure can cost a venue its licence — so your professionalism directly protects the client's licence and our contract.", size=9.5)

h2("3.4  Health & safety (HSWA 2015)")
law([
    [("You are a “worker”, and BOTH ASG and the venue are “PCBUs” with duties to keep you and the public safe (ss17, 19, 36).", {"bold": True})],
    [("• Because two businesses share the site, they must ", {}), ("consult, co-operate and co-ordinate", {"bold": True}), (" on safety — staffing, comms, violence controls, escalation (s34).", {})],
    [("• You must take reasonable care and follow reasonable safety instructions (s45).", {})],
    [("• Serious incidents (a death, a “notifiable injury” such as a serious head injury, serious laceration, or anyone admitted to hospital for immediate treatment) are ", {}), ("notifiable events", {"bold": True}), (" — ASG/the venue must notify WorkSafe as soon as possible and preserve the scene (ss23–25, 55–56).", {})],
])
field_tip([[("Practical: no lone-guarding of high-risk spots, working radio/panic comms, agreed Police-escalation triggers, and if someone is knocked out, seriously injured or taken to hospital — tell your supervisor immediately so ASG can assess whether WorkSafe must be notified.", {})]])

h2("3.5  Evidence & working with Police")
bullet("Refer violence — verbal or physical — to Police. It is not part of the job to “sort it out” with force.")
bullet("If you make a lawful citizen's arrest, hold only as long as needed and hand over to Police promptly. Don't search or interrogate.")
bullet("Preserve CCTV before it's overwritten and log the incident (time, people, actions, witnesses). Footage may be given to Police for law enforcement (Privacy Act 2020) — don't post it publicly.")
pagebreak()

# ================= PART 4 — MODULES =================
h1("The 15 Training Modules", "PART 4")
para("Run at the Thursday induction and refresher. Each module now carries real content and its own objectives; the legal modules point back to Part 3. Every module is delivered by presentation, discussion, demonstration, role-play and scenario, then Q&A.", size=9.5, color=GREY, italic=True)

def module(n, title, focus, points, objs, extra=None):
    h2(f"Module {n} — {title}")
    para(focus)
    for pt in points:
        if isinstance(pt, tuple): bullet(pt[1], lead=pt[0])
        else: bullet(pt)
    if extra: extra()
    objectives(objs)

module(1, "ASG Standards",
    "Who we are and the standard you carry: mission, values, professionalism, punctuality, appearance, the customer-first mindset, integrity, teamwork and accountability.",
    ["Represent ASG and the venue to the highest standard — you are the first and last impression.",
     "Own your shift: on time, in full uniform, radio on, ready at start.",
     "Firm but fair in every interaction (Part 1.2)."],
    ["Describe ASG's mission and the ASG Style", "Apply the standards to your own conduct on shift", "Explain why professionalism protects the venue's licence and our contract"])

module(2, "Customer Service & Hosting",
    "Great security is great hosting. Greeting patrons, positive body language, clear communication, assisting customers, handling complaints, and representing the venue and ASG.",
    ["Greet, make eye contact, set a welcoming but controlled tone at the door.",
     "Solve problems: directions, taxis, water, lost property, a calm word.",
     "Handle complaints without ego — listen, acknowledge, escalate to the manager if needed."],
    ["Demonstrate a professional door greeting and hosting manner", "De-escalate a minor complaint calmly", "Balance hosting with security awareness"])

module(3, "Grooming & Professional Conduct",
    "Looking the part and behaving the part: uniform standards, hygiene, fitness for duty, phone use, confidentiality and social-media expectations.",
    ["Meet the uniform and grooming checklist every shift (Part 1.3).",
     "No personal phone, smoking, eating or drinking in front of patrons on duty.",
     "Confidentiality and careful social-media use — nothing that reflects badly on ASG (Part 1.5)."],
    ["Meet ASG uniform and grooming standards", "Apply the conduct, phone and confidentiality rules", "Explain fitness-for-duty expectations"])

module(4, "Communication",
    "Clear comms keep everyone safe: radio etiquette, the phonetic alphabet, concise transmissions, the escalation path, and communicating with venue managers, Police and emergency services.",
    [("Radio discipline. ", "Short, clear, one message at a time; wait, then speak; confirm you're understood."),
     ("Phonetic alphabet. ", "Alpha, Bravo, Charlie … (full card in Part 5) for names, plates and IDs."),
     ("Escalation. ", "Guard → Head Doorman → Supervisor/Ops → Police (111). Know your triggers (Module 8).")],
    ["Use correct radio etiquette and the phonetic alphabet", "Give a concise, accurate transmission under pressure", "Follow the escalation path to management and Police"])

module(5, "Venue Awareness",
    "Know your ground before it gets busy: patrol technique, spotting risks early, emergency exits, occupancy/capacity, monitoring for intoxication, and queue management.",
    ["Walk the venue at start of shift — exits, fire equipment, first-aid, assembly point, blind spots.",
     "Watch occupancy against the venue's limit; manage the queue fairly and safely.",
     ("Close time. ", "Know the venue's licensed close and any one-way-door condition (Part 3.1 & 3.3); manage the wind-down and exit."),
     "Scan constantly for the early signs of intoxication and tension (SCAB — Module 12)."],
    ["Conduct an effective patrol and pre-shift check", "Manage occupancy and queues safely", "Identify risks and the venue's licensed close/one-way-door rules"])

module(6, "Conflict Management",
    "Most incidents are won with words. Reading behavioural cues, verbal de-escalation, empathy, active listening, keeping distance and tactical positioning.",
    [("Read early. ", "Spot rising tension (SCAB behaviour signs, body language) and intervene before it escalates."),
     ("De-escalate. ", "Calm voice, open posture, acknowledge, offer a face-saving way out, keep a safe reactionary gap."),
     ("Position. ", "Angle off (not square-on), hands visible, exits in mind, never crowd a person."),
     "Work as a team — one talks, others support and watch the crowd."],
    ["Recognise pre-incident indicators", "Apply a verbal de-escalation model and tactical positioning", "Know when talking has failed and it's time for Module 7 or 8"])

def m7_extra():
    field_tip([[("The removal ladder: ", {"bold": True}), ("(1) ask, (2) warn they must leave (Trespass Act s3), (3) escort with reasonable, non-striking force (Crimes Act s56), (4) if they turn violent it becomes self-defence (s48) — only then, proportionate force, and stop when it stops. Log it.", {})]])
module(7, "Patron Refusal & Removal",
    "The legal heart of the job — see Part 3.2. Assess, explain your decision calmly, encourage voluntary compliance, work as a team, get supervisor support, and use only lawful, proportionate force.",
    ["Refusing entry is your right on the venue's behalf — do it politely, firmly, with a brief reason.",
     "Reasonable force to remove a trespasser only — NO strikes, chokeholds, takedowns or bodily harm (s56).",
     "Harder force is lawful only in genuine self-defence (s48); citizen's arrest is narrow (Part 3.2).",
     "Excess force = you are charged. Distance, teamwork and a calm exit beat a grapple every time."],
    ["State the lawful basis for refusing entry and removing a patron", "Apply the s56 “no strike / no bodily harm” limit", "Recognise the line between removal, self-defence and unlawful force"],
    extra=m7_extra)

module(8, "When to Call for Backup / Police",
    "Knowing your limits keeps everyone safe. Triggers for calling backup or Police: aggressive patrons, multiple offenders, suspected weapons, medical emergencies, crowd disturbances, or anything beyond one guard's control.",
    ["Call early, not late — backup takes time to arrive.",
     ("Call 111 for: ", "weapons, serious assault/violence, a medical emergency, a crowd surge, or a crime in progress you can't safely manage."),
     "Give a clear location, what's happening, numbers, descriptions and whether anyone's injured.",
     "Refer violence to Police rather than trying to overpower it (Part 3.5)."],
    ["Identify the triggers for backup and for Police", "Make a clear, fast emergency call", "Decide when a situation is beyond safe self-management"])

module(9, "Incident Reporting",
    "If it isn't written down, it didn't happen. Facts only, chronological order, who/what/when/where, witness details, CCTV reference, actions taken and follow-up.",
    ["Write facts, not opinions; times as exact as you can; names and descriptions.",
     "Reference CCTV (camera, time) and preserve footage before it's overwritten.",
     ("Notifiable check. ", "If anyone was knocked out, seriously injured or hospitalised, flag it — it may be a WorkSafe notifiable event (Part 3.4)."),
     "Your report is the venue's evidence for its s252(3) defence and any Police/licence matter — make it count."],
    ["Write a factual, chronological incident report", "Capture witnesses, CCTV and actions taken", "Recognise and flag a notifiable event"])

module(10, "End of Shift Reports",
    "Close the loop for the next team and for management: venue summary, staffing, incidents, maintenance issues, confiscated items, Police attendance and recommendations.",
    ["Summarise the night: numbers, mood, any refusals/ejections/incidents.",
     "Note anything the venue or next shift needs to know (faults, hot-spots, banned patrons).",
     "Complete before you sign off in Deputy and leave site."],
    ["Produce a complete end-of-shift report", "Hand over effectively to management and the next team"])

module(11, "Emergency Procedures",
    "When it counts: fire and evacuation, medical emergencies, lost children, suspicious packages and severe weather — plus your health-and-safety duties (Part 3.4).",
    ["Know each venue's exits, assembly point, extinguishers and first-aid kit (from Module 5).",
     "Evacuation: stay calm, direct firmly, keep exits clear, help vulnerable people, report headcount.",
     "Medical: call 111 early, don't move seriously injured people unless in danger, preserve the scene.",
     "Lost child / suspicious item: follow venue procedure, notify the manager, don't touch suspicious items."],
    ["Execute evacuation and emergency procedures", "Respond to a medical emergency safely", "Apply your HSWA duties in an emergency"])

def m12_extra():
    field_tip([[("The rule of thumb: ", {"bold": True}), ("Sober → serve · Influenced → intervene (water/food/slow it/tell the manager) · Intoxicated (2+ SCAB signs) → deny entry or stop service and remove to safety. Then log it — that's the venue's legal defence.", {})]])
module(12, "Alcohol & Drug Awareness",
    "The other legal heart of the job — see Part 3.1. Recognising intoxication (SCAB), refusing entry and service, checking ID for minors, monitoring behaviour and preserving safety.",
    ["Assess on observable signs — 2+ of Speech/Coordination/Appearance/Behaviour = intoxicated in law (s5).",
     "Intervene at the “influenced” stage to stop the s249 offence; deny/remove at “intoxicated” (s248/252).",
     "Minors: purchase age 18; only passport, NZ photo licence or Kiwi Access Card are acceptable ID; refuse (don't seize) suspected fakes.",
     "You support the duty manager — escalate and record; a guard intoxicated on duty commits an offence (s251)."],
    ["Apply the SCAB intoxication test and act at each stage", "Check ID lawfully and spot fakes", "Explain how prompt removal earns the venue its legal defence"],
    extra=m12_extra)

module(13, "Leadership (Head Doorman)",
    "Stepping up: Head Door responsibilities, briefing guards, allocating tasks, mentoring, and communicating with venue management.",
    ["Run the pre-shift brief: positions, risks, close time, VIPs, any banned patrons.",
     "Allocate and rotate positions; keep comms tight; make the call on refusals/ejections.",
     "Be the link to the duty manager and to ASG management; own the incident/end-of-shift reporting.",
     "Mentor newer guards and model the ASG Style."],
    ["Brief and allocate a door team", "Make sound refusal/ejection and escalation decisions", "Liaise professionally with venue management"])

module(14, "Practical Scenarios",
    "Put it together under pressure: fake ID, intoxicated patron, aggressive group, queue dispute, evacuation drill, radio exercise and a report-writing assessment.",
    ["Role-play each scenario; debrief on legal limits (s56/s48), de-escalation and teamwork.",
     "Practise the SCAB call and the ID check out loud.",
     "Run a radio exercise and write up one scenario as a formal incident report."],
    ["Apply the manual to realistic scenarios", "Demonstrate lawful, proportionate decisions", "Perform under time pressure as a team"])

module(15, "Weekly Assessment",
    "Prove competency: a 20-question quiz, a practical radio assessment, a customer-service role-play, an incident-report exercise, trainer feedback and competency sign-off.",
    ["Pass the quiz (licensing, SCAB, force limits, reporting).",
     "Demonstrate radio, hosting and a lawful refusal/removal.",
     "Submit a clean incident report.",
     "Get signed off as competent (or booked for further training) — see Part 5."],
    ["Demonstrate knowledge and practical competency", "Receive and act on trainer feedback", "Achieve competency sign-off"])
pagebreak()

# ================= PART 5 — QUICK REFERENCE =================
h1("Quick-Reference, Assessment & Sign-off", "PART 5")

h2("Intoxication (SCAB) — pocket card")
para("2 or more signs = intoxicated in law (s5). Sober → serve · Influenced → INTERVENE · Intoxicated → DENY & REMOVE.", bold=True, size=10)
bullet("Speech — slurred, loud, repetitive, nonsensical")
bullet("Coordination — swaying, stumbling, spilling, can't stand unaided")
bullet("Appearance — glazed/bloodshot eyes, can't focus, dishevelled")
bullet("Behaviour — aggressive, rude, belligerent, affecting others")

h2("“Can I use force?” — the ladder")
numbered("Ask them to leave / comply.")
numbered("Warn them (Trespass Act s3) — refusal to leave is an offence.")
numbered("Escort out with reasonable force — NO strike, NO bodily harm (Crimes Act s56).")
numbered("If they attack you or someone else → self-defence (s48): reasonable, proportionate force; STOP when the threat stops.")
numbered("Never: strikes, chokeholds, takedowns that injure, kneeling on someone, force after they stop resisting. Excess = your assault charge (s62/s196/s188).")

h2("“Can I make a citizen's arrest?” — the test")
bullet("Only if you FIND them committing an offence with a max penalty of 3+ years; OR")
bullet("Between ~9pm–6am, committing ANY Crimes Act offence — with reasonable and probable grounds.")
bullet("NOT for common assault or minor theft by day. Hand to Police ASAP. No search, no interrogation, no cuffs beyond a lawful arrest.")

h2("Acceptable ID (purchase age 18)")
bullet("NZ or overseas passport · NZ photo driver licence · Kiwi Access Card (old HANZ 18+ card).")
bullet("Nothing else counts. Refuse entry on a bad/absent ID; you may NOT seize or confiscate ID — that's Police.")

h2("Auckland licensed close times (ceilings — work to the venue's licence)")
bullet("City-centre on-licence 4am · suburbs 3am · club 1am · off-licence 9pm. One-way door only if the venue's licence carries it.")

h2("Phonetic alphabet")
para("A Alpha · B Bravo · C Charlie · D Delta · E Echo · F Foxtrot · G Golf · H Hotel · I India · J Juliet · K Kilo · L Lima · M Mike · N November · O Oscar · P Papa · Q Quebec · R Romeo · S Sierra · T Tango · U Uniform · V Victor · W Whiskey · X X-ray · Y Yankee · Z Zulu.", size=9.5)

h2("Incident report — fields")
para("Date/time · venue · your name & COA # · who (names/descriptions) · what happened (facts, chronological) · witnesses · CCTV (camera & time) · action taken · injuries · Police/ambulance? · notifiable event? · manager notified · follow-up.", size=9.5)

h2("Trainer competency sign-off")
table(
    ["Field", "Record"],
    [["Guard name", ""], ["Date", ""], ["Module(s) completed", ""], ["Trainer", ""],
     ["Comments", ""], ["Outcome", "☐ Competent    ☐ Further training required"]],
    widths=[2.0, 4.0], fontsize=9.5)

h2("Currency, sources & disclaimer")
para("This manual is training material aligned to New Zealand law current at July 2026. It is not legal advice; for a live incident or charge, get advice on the specific facts. Key sources:", size=9, color=GREY)
bullet("Private Security Personnel and Private Investigators Act 2010; PSPLA (justice.govt.nz).", sub=True)
bullet("Sale and Supply of Alcohol Act 2012; HPA Intoxication Assessment Tool (alcohol.org.nz).", sub=True)
bullet("Trespass Act 1980; Crimes Act 1961; Health and Safety at Work Act 2015 (legislation.govt.nz; worksafe.govt.nz).", sub=True)
bullet("Auckland Council Local Alcohol Policy (aucklandcouncil.govt.nz).", sub=True)
para("Items to re-verify periodically: exact NZQA standards/credits and the 2027 transition; PSPLA fees; the Auckland off-licence freeze end date (~Sept 2026); any change once the 2026 Alcohol Regulation and HSWA Amendment Bills pass.", size=8.5, color=GREY, italic=True)

doc.save(OUT)
print("Saved:", OUT)
import subprocess
try:
    nwords = sum(len(p.text.split()) for p in doc.paragraphs)
    print("Approx paragraphs:", len(doc.paragraphs), "| tables:", len(doc.tables), "| ~words:", nwords)
except Exception:
    pass
