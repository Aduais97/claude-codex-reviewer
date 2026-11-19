#!/usr/bin/env python3
"""
ASG Bars & Events Security — Guard Field Manual (final).
Single content model -> renders BOTH an editable .docx and a polished .pdf.

Incorporates the ETR review pass:
- Legal-accuracy fixes (citizen's-arrest Crimes Act qualifier; COA penalty citation; skill-standard set note).
- Practical/duty-of-care additions (Part 4: welfare, medical/recovery position & positional asphyxia,
  vulnerable/spiked/distressed patrons, discrimination/Human Rights Act, weapons & crush, drugs, guard wellbeing),
  plus de-escalation model, cultural competence, BWC, cash handling, glossary and contact card.
"""
import os, html
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)

OUT_DIR = os.path.expanduser("~/Desktop/ASG/Operations/Training")
os.makedirs(OUT_DIR, exist_ok=True)
DOCX = os.path.join(OUT_DIR, "ASG Bars & Events Security - Guard Field Manual (July 2026).docx")
PDF = os.path.join(OUT_DIR, "ASG Bars & Events Security - Guard Field Manual (July 2026).pdf")

NAVY = "1F3B63"; BLUE = "2E5C8A"; GREY = "666666"; RED = "B00000"; GREEN = "1E6B3A"; WHITE = "FFFFFF"
LAW_FILL = "EAF1FB"; WARN_FILL = "FDECEC"; TIP_FILL = "EAF6EE"; LEGEND_FILL = "EEF3F9"

# ---------------- content model ----------------
B = []
def emit(t, **kw): B.append((t, kw))
def P(runs, align=None, after=5, before=0, size=10.5):
    if isinstance(runs, str): runs = [(runs, {})]
    emit("p", runs=runs, align=align, after=after, before=before, size=size)
def H1(text, num=None): emit("h1", text=text, num=num)
def H2(text): emit("h2", text=text)
def H3(text): emit("h3", text=text)
def BUL(runs, sub=False):
    if isinstance(runs, str): runs = [(runs, {})]
    emit("bullet", runs=runs, sub=sub)
def NUM(runs):
    if isinstance(runs, str): runs = [(runs, {})]
    emit("num", runs=runs)
def CALL(kind, lines):
    lines = [[(x, {})] if isinstance(x, str) else x for x in lines]
    emit("callout", kind=kind, lines=lines)
def LAW(lines): CALL("law", lines)
def WARN(lines): CALL("warn", lines)
def TIP(lines): CALL("tip", lines)
def TBL(headers, rows, widths=None, fs=9): emit("table", headers=headers, rows=rows, widths=widths, fs=fs)
def TRN(text): emit("trainer", text=text)
def PB(): emit("pagebreak")
def SP(h=6): emit("spacer", h=h)
def OBJ(items):
    H3("Learning objectives — you can:")
    for it in items: BUL(it)

def module(n, title, focus, points, objs, extra=None):
    H2(f"Module {n} — {title}"); P(focus)
    for pt in points:
        if isinstance(pt, tuple): BUL([(pt[0], {"bold": True}), (pt[1], {})])
        else: BUL(pt)
    if extra: extra()
    OBJ(objs)

b = lambda t: (t, {"bold": True})
r = lambda t: (t, {})


# =========================================================== CONTENT
def build():
    # -------- COVER --------
    emit("cover")

    # -------- HOW TO USE --------
    H1("How to use this manual")
    P("This manual does two jobs. It is your handbook — who we are, how we work, and the standards you agree to as an ASG guard — and it is your training programme, the modules run at the Thursday induction and refresher.")
    P("Throughout, watch for these boxes:")
    LAW([[r("The actual New Zealand law behind what we do — with the Act and section, so you know it's real, not just company preference.")]])
    WARN([[r("Where YOU personally can get charged, fined, hurt, or lose your Certificate of Approval. These are the lines you do not cross.")]])
    TIP([[r("The practical move — what to actually do or say in the moment.")]])
    H2("Contents")
    for line in ["Part 1 — Welcome & The ASG Way",
                 "Part 2 — Getting Deployed: your licence, training & readiness",
                 "Part 3 — The Law You Work Under (alcohol, force, discrimination, Auckland, health & safety)",
                 "Part 4 — Looking After People: welfare, medical & critical incidents",
                 "Part 5 — The 15 Training Modules",
                 "Part 6 — Quick-Reference, Assessment & Sign-off"]:
        BUL(line)
    PB()

    # ============ PART 1 ============
    H1("Welcome & The ASG Way", "PART 1")
    H2("1.1  About ASG")
    P("Absolute Security Group (ASG) was created in 2022 to close a growing gap in Auckland's hospitality security industry. We stand apart by strategically developing our guards' skillsets and taking a direct, professional approach to service delivery.")
    P("We run a Patrol Branch, a Static Branch and an Events Sector, so guards enjoy diverse work that challenges them to grow. Our mission is simple: every person who approaches our guards or uses our services should feel safe and enjoy their experience with us.")
    P([("Nau mai, haere mai ki Absolute Security Group. Welcome to the team.", {"italic": True, "color": BLUE})])
    H2("1.2  The ASG Style — firm but fair")
    P("The ASG Style is firm but fair. We want security professionals who are part host, part custodian: delivering service with a smile while never compromising safety. Be positive and friendly — but don't let patrons take advantage of that. Keep enforcing the conditions of your venue.")
    P([b("Presentation. "), r("Take pride in your full uniform, correctly worn. Ask: Is my uniform clean and ironed? Does it fit? Are my shoes appropriate and polished?")])
    P([b("Service. "), r("Every patron should have a pleasant experience. A great host is friendly, welcoming, approachable — and always a problem solver.")])
    P([b("Attitude. "), r("You set the mood as the first and last person a patron meets. Am I adding to the energy or subtracting? Am I treating people as I'd like to be treated? Am I creating a safe, approachable environment?")])
    H2("1.3  Uniform & personal presentation")
    P("You provide: plain black dress pants, plain black dress shoes, black dress socks, a black dress belt. For corporate events, provide your own plain matching black suit jacket and trousers.")
    for x in ["All uniform clean, ironed, worn professionally.",
              "Jewellery is fine if it doesn't detract (small studs, discreet rings, a conservative watch) — avoid large items that are a hazard in a scuffle.",
              "Excellent personal hygiene. Long hair tied back and tidy. Clean-shaven or a neatly groomed beard.",
              "Under-layers black, plain, not visible. No eating, drinking or smoking in uniform on duty."]:
        BUL(x)
    H2("1.4  The uniform bond system")
    P("We bond most uniform items — a portion of your pay is held against an item (max $50 per weekly pay). Return the bonded uniform clean and undamaged when you leave and the full amount comes back to you as a lump sum next pay cycle.")
    LAW([[r("Any deduction from your wages — including a uniform bond — requires your written consent and must be reasonable (Wages Protection Act 1983, ss 5/5A). You'll sign a bond authority first, and each item and amount is confirmed with you before any deduction.")]])
    P([b("Covered by ASG: "), r("damage on duty during an incident, fading logos, general wear and tear.  "), b("Re-bonded to you: "), r("avoidable damage on duty, loss or theft, damage off duty.")])
    H2("1.5  Conduct standards")
    for lead, txt in [
        ("Language.  ", "Respectful, professional, polite at all times — never offensive, abusive, racist or derogatory, to anyone."),
        ("Mobile phone.  ", "No personal phone use on duty; personal calls/texts cleared by your Head Doorman. Work-related exchanges are fine."),
        ("Smoking / eating.  ", "Only on a break, away from the venue, ASG items removed or covered. Eat out of patron view. Never skull drinks in front of patrons."),
        ("Off-duty conduct.  ", "You're held to a higher standard than a patron, even off duty and at non-ASG venues. On your night off at an ASG venue, don't involve yourself — let the on-duty team work."),
        ("Social media.  ", "Take care with anything linkable to ASG; inappropriate posts may lead to disciplinary action."),
        ("Confidentiality.  ", "Never disclose information learned at work about the company, management, clients, customers or colleagues (Privacy Act 2020)."),
        ("Bribes & cash.  ", "Never accept a bribe for entry or any favour — zero tolerance. Where you handle entry fees/cover charge, follow the venue's two-person cash process and never pocket cash — it protects you from theft accusations."),
        ("Lost property.  ", "Hand all lost property to venue bar staff. Never open pockets or reach inside a bag. Carry found property held visibly as you walk it to the bar."),
        ("Body-worn cameras.  ", "Only record on an ASG-issued body-worn camera where ASG policy and the venue allow it, tell people they may be recorded, and treat footage as private (Privacy Act 2020) — secure it, release only to Police/management, keep no personal copies. NEVER film incidents on your personal phone or post them."),
    ]:
        BUL([(lead, {"bold": True}), (txt, {})])
    PB()

    # ============ PART 2 ============
    H1("Getting Deployed", "PART 2")
    P("Before you work a shift, three things must be true: you hold a current Certificate of Approval, you are (or are becoming) trained, and you are fit for duty.")
    H2("2.1  Your Certificate of Approval (COA)")
    P("Door and bar security is 'crowd control' work, and by law you must hold a current Certificate of Approval (COA) in the Crowd Controller class. ASG holds the Company Licence you work under; your COA is your personal authorisation.")
    LAW([
        [b("Private Security Personnel and Private Investigators Act 2010 (PSPPI Act), administered by the PSPLA.")],
        [r("• Door/bar security = the "), b("Crowd Controller"), r(" class. You must be 18+.")],
        [r("• You must "), b("wear your PSPLA ID badge visibly at all times while working"), r(" (s67) and produce your certificate on request. Not displaying it = fine up to $2,000.")],
        [r("• A COA is required under s44. Working without a current COA is an offence — "), ("fine up to $20,000 for you, and up to $20,000 for ASG as employer", {"bold": True, "color": RED}), r(". No COA, no shift.")],
    ])
    TIP([[r("A "), ("Temporary COA", {"bold": True}), r(" (the 'blue' certificate) lets you work while you finish training — about 3 months. Some venues won't accept temporary/blue-COA guards; that's the venue's call.")]])
    H2("2.2  Mandatory training")
    P("To hold a full Crowd Controller COA you must complete the mandatory NZQA training and upload your Record of Achievement. You can start on a temporary COA and finish training within its life.")
    LAW([
        [b("Three NZQA standards are required (Minimum Training Regulations 2013):")],
        [r("• Legal knowledge / intro to the security industry — "), b("Unit Standard 27364"), r(" (licensing, arrest, trespass, use of force, search limits, H&S, reporting).")],
        [r("• Conflict management — "), b("Unit Standards 27360 and 27361"), r(".")],
        [r("• NZQA is moving these to new "), b("skill standards 40145 / 40146 / 40147"), r(", which replace the old three as a set (both are accepted now). Old unit standards are expiring — finish yours by the provider's deadline (advised ~31 Dec 2027). Confirm the exact standards, pairing and credits with your provider.")],
        [r("• Holding the "), b("NZ Certificate in Security (Foundation L3 or Advanced L4)"), r(" also satisfies this. No legal refresher is required — but ASG runs ongoing training you're expected to attend.")],
    ])
    H2("2.3  Staying eligible")
    P("Certain convictions affect whether the PSPLA grants or keeps your COA. Disqualification isn't always an automatic bar — a 'fit and proper' test applies — but be upfront.")
    BUL("Permanent bar: ever sentenced to imprisonment; serious sexual offending; indefinite driving disqualification.")
    BUL("7-year bar (conviction in the last 7 years): dishonesty, violence, serious drug or firearms offences.")
    WARN([[r("Tell ASG immediately if you are charged with or convicted of any offence, or if your COA is suspended, cancelled or not renewed. Working on a COA you're no longer entitled to puts you and ASG in breach.")]])
    H2("2.4  Rostering, sign-in & punctuality")
    for lead, txt in [
        ("Deputy.  ", "Download Deputy — your roster arrives a week ahead in the app."),
        ("Pull-outs / requests.  ", "Pulling out needs 24 hours' notice; late pull-outs and no-shows damage your standing. Genuine shift-change requests are welcome."),
        ("Punctuality.  ", "Be at least 5 minutes early, report to your Head Doorman/Team Leader, be deployed and ready at start (radio on, PPE sorted)."),
        ("Sign in / out.  ", "Clock on in Deputy on arrival (not from a distance — it's flagged). At the end, 'end shift' in Deputy and complete the on-site timesheet, both before you leave."),
        ("Minimum hours.  ", "If your shift is under 3 hours, or is cancelled after you've arrived, you're paid a minimum of 3 hours."),
    ]:
        BUL([(lead, {"bold": True}), (txt, {})])
    H2("2.5  Fitness for duty")
    P("You must arrive fit to work. ASG has zero tolerance for turning up impaired by alcohol or drugs — a safety issue for you, your team and the public. Fatigue counts too: on long or solo nights, being too tired to work safely is a fitness-for-duty issue — flag it, don't push through.")
    WARN([
        [b("If you present unfit for duty you will not be deployed and will be stood down while the matter is dealt with under our fitness-for-duty and disciplinary process.")],
        [r("Never consume alcohol in ASG uniform — on or off an ASG site. Never drink or use drugs on duty.")],
    ])
    LAW([[r("A security worker who is "), b("intoxicated while on duty commits an offence personally"), r(" — Sale and Supply of Alcohol Act 2012, s251, fine up to $2,000.")]])
    P([("Note on pay: a stood-down guard's pay is handled correctly through the process — not 'forfeited' on the spot. Your job is simply to always turn up fit for work.", {"italic": True, "size": 9, "color": GREY})])
    H2("2.6  Who you report to")
    P("All staff report to their Team Leader. On a bar shift you report to the Head Doorman and follow their instructions. Above them: Supervisors and Operations Managers. Escalate anything you're unsure about — early.")
    PB()

    # ============ PART 3 ============
    H1("The Law You Work Under", "PART 3")
    WARN([[b("The single most important thing in this manual: "), r("a licensed guard has no more legal power than any ordinary citizen, plus the venue's right to remove trespassers. Your COA lets you do the job lawfully — it gives you NO special power to use force, search, seize or arrest. The moment your force goes beyond what the law allows, YOU become the offender.")]])

    H2("3.1  The Sale & Supply of Alcohol Act 2012 — your job in law")
    P("The Act's object (s4) is that alcohol is sold, supplied and consumed safely and responsibly, and harm minimised. Almost everything you do at the door serves that object — and earns the venue its legal defences.")
    H3("Intoxication — the legal test (s5)")
    P("A person is 'intoxicated' in law when observably affected by alcohol or drugs so that 2 or more of these are evident: Speech, Coordination, Appearance, Behaviour. It's what you observe — not how many drinks. Remember it as SCAB.")
    TBL(["Sign", "Sober — serve", "Influenced — INTERVENE", "Intoxicated — DENY & REMOVE"],
        [["Speech", "Clear, coherent, normal", "Loud, talkative, interrupts, stumbling words", "Slurring, repetitive, nonsensical, loses the thread"],
         ["Coordination", "Balanced, steady", "Slowed reactions, sway, occasional stagger", "Stumbles, spills, weaves, can't stand unaided"],
         ["Appearance", "Tidy, clear eyes, alert", "Vacant look, smell of alcohol, untidy", "Glazed/bloodshot eyes, can't focus, dishevelled"],
         ["Behaviour", "Sensible, relaxed", "Over-friendly/withdrawn, argumentative, drinking faster", "Aggressive, rude, belligerent, affecting others"]],
        widths=[0.85, 1.75, 2.05, 2.05], fs=8)
    P([("2+ signs from the right column = intoxicated in law. At 'Influenced', intervene early (slow it down, water, food, tell the manager) — that's how the venue avoids the offence of letting someone get intoxicated.", {"size": 9.5})])
    H3("The offences — and who is liable")
    P("These offences fall on the licensee and the certificated duty manager — but your action (or inaction) makes or breaks their defence, and one catches you personally.")
    TBL(["Section", "Offence", "Max penalty"],
        [["s248", "Selling / supplying alcohol to an intoxicated person", "Licensee/manager $10,000 (+ suspension); other person $2,000"],
         ["s249", "Allowing a person to become intoxicated on the premises", "Licensee/manager $10,000"],
         ["s252", "Allowing an intoxicated person to be or remain", "$5,000"],
         ["s253", "Allowing violent / disorderly conduct on the premises", "$10,000"],
         ["s251", "An employee (e.g. a GUARD) being intoxicated on duty", "$2,000 — this one is YOU"],
         ["s239", "Selling / supplying / allowing alcohol to an under-18", "Licensee/manager $10,000; other person $2,000"]],
        widths=[0.7, 3.5, 2.7], fs=8.5)
    LAW([
        [b("The defence you deliver — s252(3) & s253(3).")],
        [r("It's a defence for the venue if, as soon as anyone became aware, "), b("reasonable steps"), r(" were taken to either "), b("take the person to a place of safety on the premises, or remove them"), r(". Prompt, sensible removal — and a note of it — is exactly what the law rewards.")],
    ])
    TIP([[r("So when you remove an intoxicated or disorderly patron you're not throwing your weight around — you're performing the venue's legal defence. Do it calmly, promptly, and log it (time, what you saw, what you did, who you told). And note: 'place of safety on the premises' is the law's FIRST option — see Part 4.1.")]])
    H3("Minors — the purchase age is 18")
    P("Only three documents are acceptable evidence of age: a NZ or overseas passport, a NZ photo driver licence, or the Kiwi Access Card (old HANZ 18+). Nothing else — not a student ID, work ID, or a photo of a document.")
    LAW([
        [r("• s239 — serving/allowing an under-18 (up to $10,000). s245 — allowing a minor into a restricted area. s257 — presenting a fake or someone else's ID is the patron's offence.")],
        [r("• The venue's "), b("defence"), r(" is that an approved ID was produced (or an approved scanner used) and staff believed on reasonable grounds it was genuine and showed the person was 18+. This is why we check — and record — ID.")],
    ])
    TIP([[r("Require ID as a condition of entry and refuse entry if it isn't produced or looks false. You may "), ("not", {"bold": True}), r(" seize or confiscate an ID — that's Police. Suspected fake → refuse entry, tell the duty manager, hand a forgery to Police. A minor found INSIDE: don't detain — quietly escort them out, tell the duty manager, log it. A name/gender that doesn't match the photo (e.g. a trans patron) is NOT grounds to refuse.")]])
    H3("The Duty Manager and host responsibility")
    P("Every on-licence must have a certificated Duty Manager on duty whenever alcohol is served (s214); their name is displayed inside, and they're legally responsible for compliance and reducing harm. You are not the duty manager — you support and escalate to them; refusals, ejections and incidents go to the named manager and get recorded.")
    P([("The venue must also keep free water available, and provide food, low/no-alcohol options and transport info (ss51–54, s110). Don't obstruct water or a taxi at the exit — these are the licensee's legal duties.", {"size": 9.5})])
    H3("Trading hours")
    LAW([[r("National default for on-licences is 8am–4am (s43), but the "), b("hours that apply are the ones on THAT venue's licence"), r(", plus any one-way-door condition (s44, s110). Always work to the venue's licensed close — many close well before 4am. Clearing patrons at close is how the venue avoids the 'open after hours' offence (s256).")]])

    H2("3.2  Your powers & limits — trespass and force")
    H3("Removing an unwanted patron (Trespass Act 1980 + Crimes Act s56)")
    LAW([
        [r("• As a guard you count as an 'occupier' of the venue (Trespass Act s2), so you act on its behalf.")],
        [r("• You may "), b("warn a person to leave"), r(" (s3); refusal is an offence. A verbal warning is valid — note it (s5).")],
        [r("• A "), b("trespass notice"), r(" (warning to stay away) lasts "), b("2 years"), r(" (s4).")],
        [r("• To remove a non-violent trespasser you may use "), b("reasonable force to escort them out — but you must NOT strike them or cause bodily harm (Crimes Act s56)"), r(".")],
    ])
    H3("Self-defence (Crimes Act s48)")
    P("You may use force to defend yourself or another that is reasonable in the circumstances as you genuinely believe them to be. Injury-causing force is lawful only when genuinely defending against a real threat, only in proportion — and you must stop the instant the threat stops.")
    H3("Citizen's arrest — narrow, and dangerous to get wrong (s35 / s36)")
    LAW([
        [b("You may arrest without warrant only:")],
        [r("• a person you "), b("find committing a Crimes Act offence"), r(" whose maximum penalty is "), b("3 years or more"), r("; OR")],
        [r("• "), b("between 9pm and 6am (the legal 'night')"), r(", a person you find committing "), b("any Crimes Act offence"), r(" — with reasonable and probable grounds.")],
        [r("Common assault (max 1 year) and minor theft don't qualify by day. A vague suspicion is never enough. If you arrest, hand the person to Police as soon as possible — you cannot run your own detention.")],
    ])
    WARN([
        [b("Excess force = you are the criminal (Crimes Act s62 → s196 common assault, or s188 wounding, up to 14 years). The classic traps:")],
        [r("strikes or punches during a removal · chokeholds / headlocks · takedowns that injure · kneeling or sitting on someone · continuing force after they've stopped resisting · holding someone with no lawful arrest (false imprisonment).")],
    ])
    H3("What you may NEVER do")
    for lead, txt in [
        ("No weapons. ", "No batons; OC/pepper spray is a restricted weapon under the Arms Act — illegal for guards."),
        ("No routine restraint. ", "Handcuffs/restraints only as part of a lawful arrest, with reasonable, non-injurious force."),
        ("No search / seizure. ", "No searching a person or their bag without consent. A bag check is a condition of entry — if they refuse, refuse entry; you can't force it."),
        ("No unlawful detention. ", "Never detain beyond a lawful arrest, or hold someone to question or search them."),
    ]:
        BUL([(lead, {"bold": True}), (txt, {})])

    H2("3.3  Refusing entry lawfully — discrimination (Human Rights Act 1993)")
    P("You may refuse entry on the venue's behalf — but only for lawful reasons. Refusing someone because of a protected characteristic is unlawful discrimination and can take you and ASG to the Human Rights Review Tribunal.")
    LAW([
        [b("You may NOT refuse or eject someone because of a prohibited ground: "), r("race, colour, ethnic or national origin, sex, sexual orientation, gender identity, disability, age (16+), religious or ethical belief, marital or family status, employment status (Human Rights Act 1993, s21).")],
        [b("You MAY refuse for a genuine, lawful reason applied evenly: "), r("intoxication, being at capacity, a dress code applied to everyone, prior trespass, no acceptable ID / under 18, or genuine safety/behaviour concerns.")],
    ])
    TIP([[r("Always give a specific lawful reason ('sorry, you're too intoxicated tonight' / 'dress code' / 'we're at capacity') — never a person's race, gender or disability. Refusing under-18s from a restricted licensed area is lawful (the Alcohol Act requires it); a disability, guide dog, or someone's ethnicity never is.")]])

    H2("3.4  Auckland rules")
    P("Auckland's Local Alcohol Policy has been in force since December 2024. It controls harm mainly through trading hours (there is no citywide one-way-door rule — a one-way door only applies where a venue's own licence carries it).")
    TBL(["Licence type", "Maximum close (Auckland)"],
        [["On-licence — city centre (bars/pubs/clubs)", "4:00am"],
         ["On-licence — rest of Auckland (suburbs)", "3:00am"],
         ["Club licence", "1:00am"], ["Off-licence (bottle stores/supermarkets)", "9:00pm"]],
        widths=[3.9, 2.1], fs=9)
    P([("These are ceilings — always work to the venue's licensed hours. Four agencies watch premises: the District Licensing Committee, Council Inspectors (who run controlled purchase operations with fake-ID minors), Police, and the Medical Officer of Health. Serving intoxicated patrons or a host-responsibility failure can cost the venue its licence — so your professionalism protects the client's licence and our contract.", {"size": 9.5})])

    H2("3.5  Health & safety (HSWA 2015)")
    LAW([
        [b("You are a 'worker', and BOTH ASG and the venue are 'PCBUs' with duties to keep you and the public safe (ss17, 19, 36).")],
        [r("• Two businesses share the site, so they must "), b("consult, co-operate and co-ordinate"), r(" on safety — staffing, comms, violence controls, escalation (s34).")],
        [r("• You must take reasonable care and follow reasonable safety instructions (s45).")],
        [r("• Serious incidents (a death; a 'notifiable injury' like a serious head injury or laceration; anyone admitted to hospital for immediate treatment) are "), b("notifiable events"), r(" — WorkSafe must be notified as soon as possible (s56) and the scene preserved (s55).")],
    ])
    TIP([[r("Practical: no lone-guarding of high-risk spots; working radio/panic comms; agreed Police-escalation triggers; and if someone is knocked out, seriously injured or hospitalised — tell your supervisor immediately so ASG can assess whether WorkSafe must be notified.")]])
    H2("3.6  Evidence & working with Police")
    BUL("Refer violence — verbal or physical — to Police. It's not the job to 'sort it out' with force.")
    BUL("After a lawful citizen's arrest, hold only as long as needed and hand to Police promptly; don't search or interrogate.")
    BUL("Preserve CCTV before it's overwritten and log the incident (time, people, actions, witnesses). Footage may be given to Police for law enforcement (Privacy Act 2020) — don't post it publicly.")
    PB()

    # ============ PART 4 — WELFARE ============
    H1("Looking After People — Welfare, Medical & Critical Incidents", "PART 4")
    P("The law-and-force part keeps you out of trouble. This part keeps people alive. On a real Auckland night, the danger is rarely a fair fight — it's a vulnerable patron, a medical collapse, a weapon, or a crush. Read this as carefully as Part 3.")

    H2("4.1  Duty of care & 'place of safety' — never eject a vulnerable person into danger")
    P("'Intoxicated → deny & remove' does NOT mean pushing a lone, heavily intoxicated person onto a dark street. The law's first option is a place of safety on the premises (s252(3)). Removing someone into harm is a duty-of-care, coronial and reputational disaster.")
    TIP([
        [b("Before anyone vulnerable leaves, run the safety check:")],
        [r("• Hold them in a safe, supervised spot inside rather than the footpath.")],
        [r("• Find a named, sober friend from their group; don't release them to a stranger.")],
        [r("• Arrange a taxi/rideshare and see them into it; call someone to collect them.")],
        [r("• If they can't safely get themselves home, or are deteriorating — call an ambulance (111) and wait with them.")],
        [r("• Extra care for anyone alone, young, very intoxicated, distressed, or possibly spiked.")],
    ])

    H2("4.2  Vulnerable & at-risk patrons")
    H3("Drink spiking")
    P("Suspect spiking when someone becomes suddenly, disproportionately intoxicated or collapses in a way that doesn't match what they've had — the classic trap is writing them off as 'just drunk' and ejecting them, when they may have been spiked and be at risk of assault.")
    BUL("Treat as a medical event and a possible crime. Move them to a safe place; do NOT let them leave with someone whose relationship you can't confirm.")
    BUL("Call 111 if they're unconscious or deteriorating; keep their glass if you can; note descriptions; tell the duty manager and, where a crime is suspected, Police.")
    H3("Sexual predators & patron safety ('Ask for Angela')")
    P("Door and floor staff are the front line for patron safety. If you see a barely-conscious person being led out by someone, or a patron using a venue safe-word scheme, act.")
    BUL("Know your venue's code word (e.g. 'Ask for Angela' / an 'angel shot') and the discreet response: separate the patron from the person of concern, escort them to safety, arrange a safe ride, involve the manager and Police as needed.")
    BUL([("Support lines: ", {"bold": True}), ("Safe to Talk 0800 044 334 · HELP Auckland 09 623 1700 · emergency 111.", {})])
    H3("Distressed & mental-health-crisis patrons")
    P("Acute distress, panic, or a person in suicidal crisis is NOT defiance — and 'deny & remove' is the wrong tool. Misreading a crisis as aggression gets people hurt.")
    BUL("Recognise crisis vs aggression vs intoxication; use a calm, low-stimulus approach; give space and time; don't crowd or shout.")
    BUL("Do NOT eject an acutely distressed or suicidal person alone. Stay with them, get the manager, and call 111 (Police and mental-health crisis teams attend). 1737 (call/text) is the national mental-health line.")

    H2("4.3  Disability & conditions that look like 'drunk'")
    P("Some medical and disability conditions mimic intoxication — and getting it wrong can kill someone and breach the Human Rights Act.")
    WARN([[r("A "), b("diabetic hypo, epilepsy (post-seizure), a stroke, MS or cerebral palsy"), r(" can all look like SCAB 'intoxicated' — slurred speech, unsteadiness, confusion. Ejecting a diabetic in a hypo onto the street can be fatal.")]])
    BUL("If the signs don't fit the drinking (no smell of alcohol, sudden onset, a medical alert bracelet, the person tells you they're diabetic/epileptic) — consider medical FIRST. Ask, don't assume.")
    BUL("Never refuse or eject someone for a disability. Guide/assistance dogs must be admitted. If in doubt, treat it as a medical issue and get help (Part 4.4).")

    H2("4.4  Medical emergencies — the ones that kill quietly")
    WARN([[b("Positional asphyxia — the killer that connects to Part 3.2. "), r("NEVER hold anyone face-down/prone, and never kneel or sit on someone's chest or back — during or after any restraint. It can suffocate them, and intoxicated people are especially at risk. The 'no kneeling' rule isn't just about an assault charge; it's about not killing someone.")]])
    P("Every guard should hold a current first-aid certificate. The basics that save lives:")
    BUL([("DRSABC: ", {"bold": True}), ("Danger · Response · Send for help (111) · Airway · Breathing · CPR/Compressions.", {})])
    BUL([("Recovery position: ", {"bold": True}), ("an unconscious person who IS breathing goes on their side (recovery position) so they don't choke on vomit — never leave them face-up or alone. Stay and monitor breathing until help arrives.", {})])
    BUL([("Overdose signs: ", {"bold": True}), ("opioids — pinpoint pupils, very slow/absent breathing, blue lips; GHB — sudden deep unconsciousness. Call 111, keep the airway open, be ready to start CPR if breathing stops. Know where the venue's AED is.", {})])
    BUL("Don't move a person with a serious head/neck injury unless they're in immediate danger; preserve the scene; report as a possible notifiable event (Part 3.5).")

    H2("4.5  Weapons — distance and disengagement")
    WARN([[r("You are unarmed by law. Your instinct to step in gets guards killed. "), b("A knife within about 7 metres is lethal. Do not try to disarm or grapple a weapon.")]])
    BUL("Create distance; put barriers/furniture between you and the threat; keep eyes on the weapon.")
    BUL("Move patrons away and direct/evacuate; do not chase.")
    BUL("Call 111 with a clear description, the weapon, and direction of travel. Preserve CCTV. Your job is people's safety, not the arrest.")

    H2("4.6  Crowd safety & crush")
    P("Crowd crush kills silently and fast — at gigs, and at one-out-one-in close. ASG runs Events, so every guard must recognise it early.")
    BUL("Danger signs: people can't lift their arms, involuntary movement, 'waves' or surges through the crowd, people going quiet or calling for help.")
    BUL("Never push a packed crowd toward a wall or barrier. Stop admitting; open all available exits; relieve pressure from the side, not the front; get comms to control immediately.")

    H2("4.7  Drugs found on premises")
    P("You'll regularly find drugs — on a patron, the floor, or in the toilets. Mishandling creates legal exposure for you.")
    BUL("You may refuse entry/eject, and you may NOT search a person or their bag.")
    BUL("Don't keep or dispose of drugs yourself (that's a possession risk). Secure them, hand to Police via the duty manager, and record it. Overdose → treat as medical (Part 4.4).")

    H2("4.8  Your own wellbeing")
    P("HSWA covers psychological harm too. This job asks a lot; look after yourself and each other.")
    BUL("Fatigue is a fitness-for-duty issue on long/solo nights — flag it (Part 2.5).")
    BUL("After a serious incident — an assault, a death, a traumatic scene — ask for a debrief and use the support available (EAP/counselling through ASG). Tell your supervisor; you don't carry it alone.")
    PB()

    # ============ PART 5 — MODULES ============
    H1("The 15 Training Modules", "PART 5")
    P([("Run at the Thursday induction and refresher. Each module carries its own objectives; the legal and welfare modules point back to Parts 3 and 4. Delivery: presentation, discussion, demonstration, role-play and scenario, then Q&A.", {"size": 9.5, "italic": True, "color": GREY})])
    module(1, "ASG Standards",
        "Who we are and the standard you carry: mission, values, professionalism, punctuality, appearance, customer-first mindset, integrity, teamwork, accountability.",
        ["Represent ASG and the venue to the highest standard — you're the first and last impression.",
         "Own your shift: on time, in full uniform, radio on, ready at start.",
         "Firm but fair in every interaction (Part 1.2)."],
        ["Describe ASG's mission and the ASG Style", "Apply the standards to your conduct", "Explain why professionalism protects the venue's licence and our contract"])
    module(2, "Customer Service & Hosting",
        "Great security is great hosting: greeting patrons, positive body language, clear communication, assisting customers, handling complaints, representing the venue and ASG.",
        ["Greet, make eye contact, set a welcoming but controlled tone.",
         "Solve problems: directions, taxis, water, lost property, a calm word.",
         "Handle complaints without ego — listen, acknowledge, escalate if needed."],
        ["Demonstrate a professional door greeting", "De-escalate a minor complaint", "Balance hosting with security awareness"])
    module(3, "Grooming & Professional Conduct",
        "Looking and behaving the part: uniform standards, hygiene, fitness for duty, phone use, confidentiality, social media, body-worn-camera rules.",
        ["Meet the uniform and grooming checklist every shift (Part 1.3).",
         "No personal phone, smoking, eating or drinking in front of patrons on duty.",
         "Confidentiality, careful social media, and correct BWC use (Part 1.5)."],
        ["Meet ASG uniform and grooming standards", "Apply the conduct, phone, BWC and confidentiality rules", "Explain fitness-for-duty expectations"])
    module(4, "Communication",
        "Clear comms keep everyone safe: radio etiquette, the phonetic alphabet, concise transmissions, the escalation path, and communicating with managers, Police and emergency services.",
        [("Radio discipline. ", "Short, clear, one message at a time; wait, speak, confirm."),
         ("Phonetic alphabet. ", "Alpha, Bravo, Charlie … (card in Part 6) for names, plates and IDs."),
         ("Escalation. ", "Guard → Head Doorman → Supervisor/Ops → Police (111). Know your triggers (Module 8).")],
        ["Use correct radio etiquette and the phonetic alphabet", "Give a concise, accurate transmission under pressure", "Follow the escalation path to management and Police"])
    module(5, "Venue Awareness",
        "Know your ground before it's busy: patrol technique, spotting risks early, emergency exits, occupancy/capacity, intoxication monitoring, queue management.",
        ["Walk the venue at start — exits, fire gear, first-aid kit, AED, assembly point, blind spots.",
         "Watch occupancy against the limit; manage the queue fairly and safely.",
         ("Close time. ", "Know the venue's licensed close and any one-way-door condition (Parts 3.1 & 3.4)."),
         "Scan for early signs of intoxication and tension (SCAB — Module 12)."],
        ["Conduct an effective patrol and pre-shift check", "Manage occupancy and queues safely", "Identify risks and the venue's close/one-way-door rules"])
    def m6():
        TIP([[b("The de-escalation model — 5 steps under pressure: "), r("(1) Space & position — angle off, keep a reactionary gap; (2) Engage calmly — low voice, open hands; (3) Acknowledge — 'I hear you'; (4) Offer a face-saving way out; (5) Confirm & act. One guard talks; others support and watch the crowd.")]])
        TIP([[b("Cultural competence: "), r("Auckland's crowd is strongly Māori and Pasifika. Avoid publicly shaming a person or causing loss of mana in front of their mates — a quiet, respectful word off to the side is the single most effective de-escalation lever, and it lowers your discrimination risk (Part 3.3).")]])
    module(6, "Conflict Management",
        "Most incidents are won with words: reading behavioural cues, verbal de-escalation, empathy, active listening, distance and tactical positioning.",
        [("Read early. ", "Spot rising tension (SCAB behaviour signs, body language) and intervene before it escalates."),
         ("Position. ", "Angle off (not square-on), hands visible, exits in mind, never crowd a person."),
         "Work as a team — one talks, others support."],
        ["Recognise pre-incident indicators", "Apply the 5-step de-escalation model and tactical positioning", "Know when talking has failed (Module 7 or 8)"],
        extra=m6)
    def m7():
        TIP([[b("The removal ladder: "), r("(1) ask; (2) warn they must leave (Trespass Act s3); (3) escort with reasonable, non-striking force (Crimes Act s56); (4) if they turn violent it becomes self-defence (s48) — proportionate force only, and stop when it stops. Log it. Vulnerable person? Part 4.1.")]])
    module(7, "Patron Refusal & Removal",
        "The legal heart of the job — see Part 3.2–3.3. Assess, explain calmly, encourage voluntary compliance, work as a team, get supervisor support, use only lawful, proportionate force, and never refuse on a discriminatory ground.",
        ["Refuse entry politely and firmly with a specific lawful reason (never race/gender/disability — Part 3.3).",
         "Reasonable force to remove a trespasser only — NO strikes, chokeholds, takedowns or bodily harm (s56).",
         "Harder force only in genuine self-defence (s48); citizen's arrest is narrow (Part 3.2).",
         "Excess force = you are charged. Distance, teamwork and a calm exit beat a grapple."],
        ["State the lawful basis for refusing entry and removing a patron", "Apply the s56 'no strike / no bodily harm' limit", "Recognise the line between removal, self-defence and unlawful force"],
        extra=m7)
    module(8, "When to Call for Backup / Police",
        "Knowing your limits keeps everyone safe. Triggers: aggressive patrons, multiple offenders, weapons, medical emergencies, crowd disturbances, or anything beyond one guard's control.",
        ["Call early, not late — backup takes time.",
         ("Call 111 for: ", "weapons (disengage — Part 4.5), serious assault, a medical emergency (Part 4.4), a crowd surge/crush (Part 4.6), or a crime in progress you can't safely manage."),
         "Give location, what's happening, numbers, descriptions, injuries.",
         "Refer violence to Police rather than trying to overpower it."],
        ["Identify the triggers for backup and Police", "Make a clear, fast emergency call", "Decide when a situation is beyond safe self-management"])
    module(9, "Incident Reporting",
        "If it isn't written down, it didn't happen. Facts only, chronological, who/what/when/where, witnesses, CCTV reference, actions taken, follow-up.",
        ["Facts not opinions; exact times; names and descriptions.",
         "Reference CCTV (camera, time) and preserve footage before it's overwritten.",
         ("Notifiable check. ", "Anyone knocked out, seriously injured or hospitalised? It may be a WorkSafe notifiable event (Part 3.5)."),
         "Your report is the venue's s252(3) evidence and any Police/licence matter — make it count."],
        ["Write a factual, chronological incident report", "Capture witnesses, CCTV and actions taken", "Recognise and flag a notifiable event"])
    module(10, "End of Shift Reports",
        "Close the loop for the next team and management: venue summary, staffing, incidents, maintenance, confiscated items, Police attendance, recommendations.",
        ["Summarise the night: numbers, mood, refusals/ejections/incidents.",
         "Note anything the next shift needs (faults, hot-spots, banned patrons).",
         "Complete before you sign off in Deputy and leave."],
        ["Produce a complete end-of-shift report", "Hand over effectively"])
    module(11, "Emergency & Medical Procedures",
        "When it counts: fire and evacuation, medical emergencies, lost children, suspicious packages, severe weather — plus the life-saving medical basics in Part 4.4 and your HSWA duties (Part 3.5).",
        ["Know each venue's exits, assembly point, extinguishers, first-aid kit and AED (Module 5).",
         "Evacuation: stay calm, direct firmly, keep exits clear, help vulnerable people, report a headcount.",
         ("Medical: ", "call 111 early; DRSABC; recovery position for an unconscious breathing patron; never prone-restrain (Part 4.4)."),
         "Lost child / suspicious item: follow venue procedure, notify the manager, don't touch suspicious items."],
        ["Execute evacuation and emergency procedures", "Deliver DRSABC and the recovery position", "Apply your HSWA duties in an emergency"])
    def m12():
        TIP([[b("Rule of thumb: "), r("Sober → serve · Influenced → intervene (water/food/slow it/tell the manager) · Intoxicated (2+ SCAB) → deny or stop service and remove to a place of safety (Part 4.1). Then log it — that's the venue's legal defence. And check it isn't a medical/disability issue that just looks like drunk (Part 4.3).")]])
    module(12, "Alcohol & Drug Awareness",
        "The other legal heart of the job — see Part 3.1. Recognising intoxication (SCAB), refusing entry/service, checking ID for minors, spotting spiking, monitoring behaviour, preserving safety.",
        ["Assess on observable signs — 2+ of Speech/Coordination/Appearance/Behaviour = intoxicated (s5).",
         "Intervene at 'influenced' (stops the s249 offence); deny/remove at 'intoxicated' (s248/252).",
         "Minors: age 18; only passport, NZ photo licence or Kiwi Access Card; refuse (don't seize) fakes.",
         "Watch for spiking and vulnerable patrons (Part 4.2); support the duty manager; a guard intoxicated on duty commits an offence (s251)."],
        ["Apply the SCAB test and act at each stage", "Check ID lawfully and spot fakes and spiking", "Explain how prompt removal earns the venue its defence"],
        extra=m12)
    module(13, "Leadership (Head Doorman)",
        "Stepping up: Head Door responsibilities, briefing guards, allocating tasks, mentoring, communicating with venue management.",
        ["Run the pre-shift brief: positions, risks, close time, VIPs, banned patrons.",
         "Allocate and rotate positions; keep comms tight; make the call on refusals/ejections.",
         "Be the link to the duty manager and ASG management; own the incident/end-of-shift reporting.",
         "Mentor newer guards and model the ASG Style."],
        ["Brief and allocate a door team", "Make sound refusal/ejection and escalation decisions", "Liaise professionally with venue management"])
    module(14, "Practical Scenarios",
        "Put it together under pressure: fake ID, intoxicated patron, aggressive group, queue dispute, evacuation drill, radio exercise, report-writing — plus the high-stakes ones.",
        ["Role-play each, then debrief on legal limits (s56/s48), de-escalation and teamwork.",
         ("Add the critical scenarios: ", "a spiked/collapsed patron, an unconscious patron (recovery position), a mental-health crisis, a weapon (disengage), an 'Ask for Angela' request, a suspected diabetic hypo."),
         "Practise the SCAB call and the ID check out loud; write one scenario up as a formal report."],
        ["Apply the manual to realistic scenarios", "Demonstrate lawful, proportionate, safe decisions", "Perform under time pressure as a team"])
    module(15, "Weekly Assessment",
        "Prove competency: a 20-question quiz, a practical radio assessment, a customer-service role-play, an incident-report exercise, trainer feedback and competency sign-off.",
        ["Pass the quiz (licensing, SCAB, force limits, welfare, reporting).",
         "Demonstrate radio, hosting, and a lawful refusal/removal.",
         "Submit a clean incident report; get signed off as competent (or booked for further training)."],
        ["Demonstrate knowledge and practical competency", "Receive and act on trainer feedback", "Achieve competency sign-off"])
    PB()

    # ============ PART 6 — QUICK REFERENCE ============
    H1("Quick-Reference, Assessment & Sign-off", "PART 6")
    H2("Intoxication (SCAB) — pocket card")
    P([("2+ signs = intoxicated in law (s5). Sober → serve · Influenced → INTERVENE · Intoxicated → DENY & REMOVE to a place of safety.", {"bold": True, "size": 10})])
    for x in ["Speech — slurred, loud, repetitive, nonsensical",
              "Coordination — swaying, stumbling, spilling, can't stand unaided",
              "Appearance — glazed/bloodshot eyes, can't focus, dishevelled",
              "Behaviour — aggressive, rude, belligerent, affecting others"]:
        BUL(x)
    P([("Check it isn't a medical/disability issue that mimics drunk (diabetic hypo, epilepsy, stroke) — Part 4.3.", {"size": 9, "italic": True, "color": GREY})])
    H2("'Can I use force?' — the ladder")
    for x in ["Ask them to leave / comply.",
              "Warn them (Trespass Act s3) — refusal to leave is an offence.",
              "Escort out with reasonable force — NO strike, NO bodily harm (Crimes Act s56).",
              "If attacked → self-defence (s48): reasonable, proportionate; STOP when the threat stops.",
              "Never: strikes, chokeholds, takedowns that injure, kneeling on someone, prone restraint, force after they stop. Excess = your assault charge (s62/s196/s188)."]:
        NUM(x)
    H2("'Can I make a citizen's arrest?' — the test")
    BUL("Only if you FIND them committing a Crimes Act offence with a max penalty of 3+ years; OR")
    BUL("Between 9pm–6am, committing ANY Crimes Act offence — with reasonable and probable grounds.")
    BUL("NOT common assault or minor theft by day. Hand to Police ASAP. No search, no interrogation, no cuffs beyond a lawful arrest.")
    H2("Acceptable ID (purchase age 18)")
    BUL("NZ or overseas passport · NZ photo driver licence · Kiwi Access Card (old HANZ 18+).")
    BUL("Nothing else counts. Refuse entry on a bad/absent ID; you may NOT seize or confiscate ID. A trans patron's name/gender mismatch is not grounds to refuse.")
    H2("Auckland licensed close times (ceilings — work to the venue's licence)")
    BUL("City-centre on-licence 4am · suburbs 3am · club 1am · off-licence 9pm. One-way door only if the venue's licence carries it.")
    H2("Emergency & support contacts")
    TBL(["Need", "Contact"],
        [["Emergency (Police / Fire / Ambulance)", "111"],
         ["Health advice (24/7)", "Healthline 0800 611 116"],
         ["Mental-health support (call/text)", "1737"],
         ["Sexual-harm support", "Safe to Talk 0800 044 334 · HELP Auckland 09 623 1700"],
         ["ASG control / supervisor", "____________________ (fill in)"],
         ["Venue duty manager", "____________________ (per site)"]],
        widths=[2.8, 3.2], fs=9)
    H2("Phonetic alphabet")
    P([("A Alpha · B Bravo · C Charlie · D Delta · E Echo · F Foxtrot · G Golf · H Hotel · I India · J Juliet · K Kilo · L Lima · M Mike · N November · O Oscar · P Papa · Q Quebec · R Romeo · S Sierra · T Tango · U Uniform · V Victor · W Whiskey · X X-ray · Y Yankee · Z Zulu.", {"size": 9.5})])
    H2("Incident report — fields")
    P([("Date/time · venue · your name & COA # · who (names/descriptions) · what happened (facts, chronological) · witnesses · CCTV (camera & time) · action taken · injuries · Police/ambulance? · notifiable event? · manager notified · follow-up.", {"size": 9.5})])
    H2("Glossary")
    for term, mean in [
        ("COA", "Certificate of Approval — your personal PSPLA licence to do security work."),
        ("PSPLA", "Private Security Personnel Licensing Authority (Ministry of Justice)."),
        ("Crowd Controller", "The COA class for door/bar/event security."),
        ("SCAB", "Speech, Coordination, Appearance, Behaviour — the intoxication signs."),
        ("Duty Manager", "The certificated manager legally responsible for the licensed premises on shift."),
        ("PCBU", "Person Conducting a Business or Undertaking — ASG and the venue both are, under HSWA."),
        ("LAP", "Local Alcohol Policy — the council rules (e.g. Auckland's trading hours)."),
        ("One-way door", "A licence condition: after a set time, no new entry/re-entry; those inside may stay."),
        ("Notifiable event", "A serious injury/death that must be reported to WorkSafe."),
    ]:
        BUL([(term + " — ", {"bold": True}), (mean, {})], sub=True)
    H2("Trainer competency sign-off")
    TBL(["Field", "Record"],
        [["Guard name", ""], ["Date", ""], ["Module(s) completed", ""], ["Trainer", ""],
         ["Comments", ""], ["Outcome", "[  ] Competent      [  ] Further training required"]],
        widths=[2.0, 4.0], fs=9.5)
    H2("Currency, sources & disclaimer")
    P([("Training material aligned to New Zealand law current at July 2026. Not legal advice — for a live incident or charge, get advice on the specific facts. Reviewed for legal accuracy and practical safety before issue. Key sources:", {"size": 9, "color": GREY})])
    for x in ["Private Security Personnel and Private Investigators Act 2010; PSPLA (justice.govt.nz).",
              "Sale and Supply of Alcohol Act 2012; HPA Intoxication Assessment Tool (alcohol.org.nz).",
              "Trespass Act 1980; Crimes Act 1961; Human Rights Act 1993; Health and Safety at Work Act 2015 (legislation.govt.nz; worksafe.govt.nz).",
              "Auckland Council Local Alcohol Policy (aucklandcouncil.govt.nz)."]:
        BUL(x, sub=True)
    P([("Re-verify periodically: exact NZQA standards/credits and the 2027 transition; PSPLA fees; the Auckland off-licence freeze end date (~Sept 2026); and any change once the 2026 Alcohol Regulation and HSWA Amendment Bills pass.", {"size": 8.5, "italic": True, "color": GREY})])


# =========================================================== DOCX RENDERER
def hx(h): return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def render_docx(path):
    doc = Document()
    s = doc.styles["Normal"]; s.font.name = "Calibri"; s.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.top_margin = Inches(0.85); sec.bottom_margin = Inches(0.85)
        sec.left_margin = Inches(0.9); sec.right_margin = Inches(0.9)

    def shade(cell, hexc):
        tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
        sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc); tcPr.append(sh)

    def add_runs(p, runs, base=10.5):
        for t, a in runs:
            rr = p.add_run(t); rr.bold = a.get("bold", False); rr.italic = a.get("italic", False)
            rr.font.size = Pt(a.get("size", base))
            if a.get("color"): rr.font.color.rgb = hx(a["color"])

    CO = {"law": ("⚖  THE LAW", LAW_FILL, NAVY), "warn": ("⚠  RISK — READ THIS", WARN_FILL, RED),
          "tip": ("★  ON THE DOOR", TIP_FILL, GREEN)}

    for typ, kw in B:
        if typ == "cover":
            for _ in range(2): doc.add_paragraph()
            def cp(txt, sz, col, after=6, bold=True, it=False):
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(after)
                rr = p.add_run(txt); rr.bold = bold; rr.italic = it; rr.font.size = Pt(sz); rr.font.color.rgb = hx(col)
            cp("ABSOLUTE SECURITY GROUP", 26, NAVY, 2); cp("Bars & Events Security", 18, BLUE, 14)
            cp("GUARD FIELD MANUAL", 22, "000000", 0); cp("& Training Programme", 15, GREY, 18)
            cp("“Firm but fair — the ASG Style”", 13, BLUE, 26, bold=False, it=True)
            cp("Weekly Thursday Induction & Refresher Course", 11, "000000", 2, bold=False)
            cp("Edition: July 2026", 11, "000000", 2)
            cp("Aligned to New Zealand law current as at July 2026", 10, GREY, 40, bold=False)
            cp("PRIVATE & CONFIDENTIAL — property of Absolute Security Group. For issued ASG personnel only.", 9, GREY, 0, bold=False, it=True)
            doc.add_page_break()
        elif typ == "h1":
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
            pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
            bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '10'); bt.set(qn('w:space'), '3'); bt.set(qn('w:color'), NAVY)
            pbdr.append(bt); pPr.append(pbdr)
            rr = p.add_run((f"{kw['num']}   " if kw.get("num") else "") + kw["text"]); rr.bold = True; rr.font.size = Pt(16); rr.font.color.rgb = hx(NAVY)
        elif typ == "h2":
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(9); p.paragraph_format.space_after = Pt(2)
            rr = p.add_run(kw["text"]); rr.bold = True; rr.font.size = Pt(12.5); rr.font.color.rgb = hx(BLUE)
        elif typ == "h3":
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(1)
            rr = p.add_run(kw["text"]); rr.bold = True; rr.font.size = Pt(10.5)
        elif typ == "p":
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(kw["after"]); p.paragraph_format.space_before = Pt(kw["before"])
            if kw.get("align") == "c": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, kw["runs"], kw["size"])
        elif typ == "bullet":
            p = doc.add_paragraph(style="List Bullet 2" if kw["sub"] else "List Bullet"); p.paragraph_format.space_after = Pt(1.5)
            add_runs(p, kw["runs"])
        elif typ == "num":
            p = doc.add_paragraph(style="List Number"); p.paragraph_format.space_after = Pt(2); add_runs(p, kw["runs"])
        elif typ == "callout":
            label, fill, lc = CO[kw["kind"]]
            t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; cell = t.rows[0].cells[0]; shade(cell, fill)
            cell.paragraphs[0].text = ""; lp = cell.paragraphs[0]; lp.paragraph_format.space_after = Pt(2)
            lr = lp.add_run(label); lr.bold = True; lr.font.size = Pt(9.5); lr.font.color.rgb = hx(lc)
            for ln in kw["lines"]:
                pp = cell.add_paragraph(); pp.paragraph_format.space_after = Pt(1.5); add_runs(pp, ln, 9.5)
            doc.add_paragraph().paragraph_format.space_after = Pt(3)
        elif typ == "table":
            hs = kw["headers"]; t = doc.add_table(rows=1, cols=len(hs)); t.style = "Table Grid"
            for i, hh in enumerate(hs):
                c = t.rows[0].cells[i]; shade(c, NAVY); c.paragraphs[0].text = ""
                rr = c.paragraphs[0].add_run(hh); rr.bold = True; rr.font.size = Pt(kw["fs"]); rr.font.color.rgb = hx(WHITE)
            for row in kw["rows"]:
                cs = t.add_row().cells
                for i, v in enumerate(row):
                    cs[i].paragraphs[0].text = ""; rr = cs[i].paragraphs[0].add_run(str(v)); rr.font.size = Pt(kw["fs"])
            if kw.get("widths"):
                for i, w in enumerate(kw["widths"]):
                    for row in t.rows: row.cells[i].width = Inches(w)
            doc.add_paragraph().paragraph_format.space_after = Pt(3)
        elif typ == "trainer":
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
            rr = p.add_run("Trainer method:  "); rr.bold = True; rr.font.size = Pt(9); rr.font.color.rgb = hx(GREY)
            r2 = p.add_run(kw["text"]); r2.font.size = Pt(9); r2.italic = True; r2.font.color.rgb = hx(GREY)
        elif typ == "spacer":
            doc.add_paragraph().paragraph_format.space_after = Pt(kw["h"])
        elif typ == "pagebreak":
            doc.add_page_break()
    doc.save(path)


# =========================================================== PDF RENDERER (reportlab)
def esc(t): return html.escape(str(t), quote=False)
def runs_markup(runs):
    out = []
    for t, a in runs:
        s = esc(t)
        if a.get("color"): s = f'<font color="#{a["color"]}">{s}</font>'
        if a.get("italic"): s = f"<i>{s}</i>"
        if a.get("bold"): s = f"<b>{s}</b>"
        out.append(s)
    return "".join(out)

def render_pdf(path):
    usable = A4[0] - 2 * 18 * mm  # ~ page width minus margins
    styles = getSampleStyleSheet()
    base = ParagraphStyle("base", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4)
    h1s = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=15, textColor=colors.HexColor("#"+NAVY),
                         spaceBefore=6, spaceAfter=4, borderWidth=0, borderColor=colors.HexColor("#"+NAVY),
                         borderPadding=0)
    h2s = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#"+BLUE), spaceBefore=8, spaceAfter=2)
    h3s = ParagraphStyle("h3", parent=base, fontName="Helvetica-Bold", fontSize=10, spaceBefore=4, spaceAfter=1)
    bulS = ParagraphStyle("bul", parent=base, leftIndent=12, bulletIndent=2, spaceAfter=1.5)
    subS = ParagraphStyle("sub", parent=bulS, leftIndent=20, bulletIndent=10, fontSize=9)
    cap = ParagraphStyle("cap", parent=base, fontSize=8, textColor=colors.HexColor("#"+GREY))

    CO = {"law": ("⚖  THE LAW", LAW_FILL, NAVY), "warn": ("⚠  RISK — READ THIS", WARN_FILL, RED),
          "tip": ("★  ON THE DOOR", TIP_FILL, GREEN)}
    story = []

    def cell_para(txt, sz, bold=False, white=False):
        stx = ParagraphStyle("c", parent=base, fontSize=sz, leading=sz+2,
                             fontName="Helvetica-Bold" if bold else "Helvetica",
                             textColor=colors.white if white else colors.black)
        return Paragraph(esc(txt), stx)

    for typ, kw in B:
        if typ == "cover":
            def cpara(txt, sz, col, bold=True, it=False, sa=8):
                st = ParagraphStyle("cv", parent=base, alignment=1, fontSize=sz, leading=sz+4,
                                    textColor=colors.HexColor("#"+col),
                                    fontName=("Helvetica-BoldOblique" if bold and it else "Helvetica-Bold" if bold else "Helvetica-Oblique" if it else "Helvetica"),
                                    spaceAfter=sa)
                return Paragraph(esc(txt), st)
            story += [Spacer(1, 60*mm),
                      cpara("ABSOLUTE SECURITY GROUP", 26, NAVY, sa=4),
                      cpara("Bars & Events Security", 18, BLUE, sa=16),
                      cpara("GUARD FIELD MANUAL", 22, "000000", sa=2),
                      cpara("& Training Programme", 15, GREY, sa=20),
                      cpara("“Firm but fair — the ASG Style”", 13, BLUE, bold=False, it=True, sa=30),
                      cpara("Weekly Thursday Induction & Refresher Course", 11, "000000", bold=False, sa=3),
                      cpara("Edition: July 2026", 11, "000000", sa=3),
                      cpara("Aligned to New Zealand law current as at July 2026", 10, GREY, bold=False, sa=40),
                      cpara("PRIVATE & CONFIDENTIAL — property of Absolute Security Group. For issued ASG personnel only.", 9, GREY, bold=False, it=True),
                      PageBreak()]
        elif typ == "h1":
            hh = ParagraphStyle("h1b", parent=h1s, borderWidth=0)
            p = Paragraph((f"{kw['num']} &nbsp; " if kw.get("num") else "") + esc(kw["text"]), h1s)
            # underline via a thin table line
            story.append(Spacer(1, 4))
            story.append(p)
            line = Table([[""]], colWidths=[usable], rowHeights=[1])
            line.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.1, colors.HexColor("#"+NAVY))]))
            story.append(line); story.append(Spacer(1, 4))
        elif typ == "h2":
            story.append(Paragraph(esc(kw["text"]), h2s))
        elif typ == "h3":
            story.append(Paragraph(esc(kw["text"]), h3s))
        elif typ == "p":
            stx = ParagraphStyle("pp", parent=base, fontSize=kw["size"], leading=kw["size"]+2.5,
                                 spaceAfter=kw["after"], spaceBefore=kw["before"],
                                 alignment=1 if kw.get("align") == "c" else 0)
            story.append(Paragraph(runs_markup(kw["runs"]), stx))
        elif typ == "bullet":
            story.append(Paragraph(runs_markup(kw["runs"]), subS if kw["sub"] else bulS, bulletText="•"))
        elif typ == "num":
            story.append(Paragraph(runs_markup(kw["runs"]), bulS, bulletText="•"))
        elif typ == "callout":
            label, fill, lc = CO[kw["kind"]]
            lst = ParagraphStyle("cl", parent=base, fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#"+lc), spaceAfter=2)
            flow = [Paragraph(esc(label), lst)]
            bodyst = ParagraphStyle("cb", parent=base, fontSize=9, leading=11.5, spaceAfter=1.5)
            for ln in kw["lines"]:
                flow.append(Paragraph(runs_markup(ln), bodyst))
            tb = Table([[flow]], colWidths=[usable])
            tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#"+fill)),
                                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#"+lc)),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            story.append(KeepTogether(tb)); story.append(Spacer(1, 4))
        elif typ == "table":
            hs = kw["headers"]; fs = kw["fs"]
            data = [[cell_para(h, fs, bold=True, white=True) for h in hs]]
            for row in kw["rows"]:
                data.append([cell_para(v, fs) for v in row])
            if kw.get("widths"):
                tot = sum(kw["widths"]); cw = [w / tot * usable for w in kw["widths"]]
            else:
                cw = [usable / len(hs)] * len(hs)
            tb = Table(data, colWidths=cw, repeatRows=1)
            tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#"+NAVY)),
                                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
                                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                                    ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story.append(tb); story.append(Spacer(1, 4))
        elif typ == "trainer":
            st = ParagraphStyle("tr", parent=base, fontSize=9, textColor=colors.HexColor("#"+GREY))
            story.append(Paragraph("<b>Trainer method:</b> <i>" + esc(kw["text"]) + "</i>", st))
        elif typ == "spacer":
            story.append(Spacer(1, kw["h"]))
        elif typ == "pagebreak":
            story.append(PageBreak())

    def footer(canvas, docu):
        canvas.saveState(); canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#999999"))
        canvas.drawString(18*mm, 10*mm, "ASG Bars & Events Security — Guard Field Manual · July 2026 · Private & Confidential")
        canvas.drawRightString(A4[0]-18*mm, 10*mm, f"{docu.page}")
        canvas.restoreState()

    d = SimpleDocTemplate(path, pagesize=A4, topMargin=16*mm, bottomMargin=16*mm, leftMargin=18*mm, rightMargin=18*mm,
                          title="ASG Bars & Events Security — Guard Field Manual", author="Absolute Security Group")
    d.build(story, onFirstPage=lambda c, dd: None, onLaterPages=footer)


build()
render_docx(DOCX)
render_pdf(PDF)
print("DOCX:", DOCX)
print("PDF :", PDF)
print("blocks:", len(B))
