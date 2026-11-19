#!/usr/bin/env python3
"""Draft cover email (docx) for the 1st Call Investor DD Pack."""

from docx import Document
from docx.shared import Pt, RGBColor

OUT = '/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/Investor DD Pack/1CR_DD_Pack_Cover_Email.docx'

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)


def para(text='', bold=False, size=11, space_after=8):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def bullet(text, bold_lead=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_lead:
        r = p.add_run(bold_lead + ' ')
        r.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(4)
    return p


meta = para('Subject: 1st Call Recruitment — full deal file for your due diligence', bold=True, size=12)
meta.runs[0].font.color.rgb = RGBColor(0x1B, 0x2A, 0x4A)
para('Attachments: DD Briefing (PDF) · Correspondence (5 email files) · Source documents (5 PDFs) · Analysis (3 PDFs)',
     size=9, space_after=14)

para('Hi [Name],')
para('Following on from the investment deck, here is the complete deal file on 1st Call Recruitment so you '
     'can begin your own due diligence. Everything we hold is in the pack — the full email record with the '
     'vendor’s broker, every source document we’ve received, and our own findings, stated with their '
     'workings so you can test them.')
para('Start with the DD Briefing — it carries the timeline, where the negotiation stands, what we’ve '
     'verified, and a suggested workplan of the open items. The headlines:')

bullet('Going-concern asset sale of an established ~$12.6M-revenue national labour-hire business; the vendor is exiting and motivated.',
       bold_lead='The deal:')
bullet('vendor asked $2.0M; our structured $1.1M offer was declined on 5 June; his stated floor is $1.6M. Nothing is signed and there is no exclusivity.',
       bold_lead='Price:')
bullet('our corrected maintainable EBITDA is ~$376–441K (the reported margin is flattered by non-cash accrual releases '
       '— the briefing shows the bridge line by line). On that basis we value the business at ~$560–730K fixed, '
       'and we have designed — but not yet tabled — a $750K-plus-earn-out structure that only reaches his $1.6M if revenue actually recovers.',
       bold_lead='Earnings:')
bullet('the KPMG employee-by-employee leave schedule, the bank security release, FY25 monthly figures, and the $451K '
       'temping-sales provision — all flagged in the briefing’s workplan (§10).',
       bold_lead='The load-bearing open items:')

para('Two housekeeping points. First, this material sits under confidentiality arrangements with the broker '
     '(ABC Business Sales) and the vendor — please keep it to your deal team and advisers, and route any '
     'contact with the vendor side through me so we preserve the negotiating position. Second, the vendor-sourced '
     'documents are unaudited — treat every vendor number as unverified until your DD confirms it.')
para('Our full valuation model and working papers sit behind every figure in the briefing — happy to walk '
     'you through them whenever useful. Suggest we get a call in once you’ve had a first pass, and agree '
     'the JV structure and next move on price together.')
para('Cheers,', space_after=2)
para('Ahmad', space_after=0)

doc.save(OUT)
print(f'Saved: {OUT}')
