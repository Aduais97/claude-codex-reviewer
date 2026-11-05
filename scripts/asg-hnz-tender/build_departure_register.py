#!/usr/bin/env python3
"""ASG Contract Departure Register for HNZ RFP 0018709 (Attachment B MSA).

Ten commercially moderate departures. Dash-free. Output DOCX.
Usage: .venv/bin/python build_departure_register.py <out.docx>
"""
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

NAVY = RGBColor(0x1B, 0x2A, 0x4A)

ITEMS = [
 ("29.2, 29.8 (price adjustment)",
  "The Price is fixed and all-inclusive for a term of up to four years, with adjustment only by a Variation that Health NZ is not obliged to agree. Security officer services are labour-cost driven, and statutory settings (minimum wage, KiwiSaver, ACC levies, leave entitlements) change annually.",
  "Insert an annual price adjustment on each anniversary of the Supply Schedule equal to the movement in the Labour Cost Index (all labour costs, private sector) or CPI, whichever is greater, plus pass-through of the demonstrable cost impact of changes in statutory labour settings from their effective date, evidenced to Health NZ on request."),
 ("47.1, 47.2(b) (liability)",
  "There is no monetary cap on direct loss anywhere in the Agreement, and clause 47.2(b) disapplies even the clause 47.1 consequential-loss exclusion for negligence, the primary claim type in guarding services. The combined effect is unlimited exposure that cannot be fully insured.",
  "Insert an aggregate liability cap of the greater of two times the annual fees under the relevant Supply Schedule or the insurance cover required under clause 49, with carve-outs limited to fraud, Wilful Default, and death or personal injury caused by the Supplier. Remove negligence from clause 47.2(b) so it sits within the cap."),
 ("48.3 (failure to supply indemnity)",
  "The indemnity covers all extra costs including patient care costs, applies to any failure for whatever reason (a single unfilled shift is arguably captured), and the force majeure carve-out depends on what Health NZ considers to be force majeure.",
  "Limit the indemnity to the direct incremental cost of procuring replacement security services, apply it where a failure persists beyond 24 hours after notice and escalation, and make the force majeure test objective (an event meeting the Force Majeure Event definition, acting reasonably)."),
 ("44.5 (liquidated damages)",
  "Liquidated damages apply at a Supply Schedule rate not yet visible to Respondents, are expressly not a sole remedy, and the clause 43.1(e) safe harbour requires one month's advance notice, which is not operable for same-day absence, the realistic failure mode in guarding.",
  "Specify the LD rate before contract signature; make LDs the sole financial remedy for the relevant failure event short of termination; apply an annual LD cap of ten percent of annual Supply Schedule fees; and provide a grace mechanism where a replacement officer is deployed within an agreed window after an unforeseen absence."),
 ("46.4 (termination for convenience)",
  "Health NZ may terminate without cause on three months notice, with compensation limited to Deliverables supplied and pre-agreed unavoidable expenses. Mobilisation investment (vetting, screening, training, uniforms, vehicles) is unrecoverable, and the Supplier has no reciprocal right.",
  "Extend convenience termination notice to six months, and provide for recovery of demonstrable unamortised mobilisation costs and unavoidable redundancy costs arising from a no-fault termination, whether or not pre-agreed."),
 ("Force Majeure (definition, 42.2)",
  "No clause suspends Service obligations during a Force Majeure Event: the only force majeure references operate as carve-outs from liquidated damages (44.5) and the failure to supply indemnity (48.3), the latter depending on what Health NZ considers force majeure, while clause 42.2 intensifies obligations during emergencies.",
  "Insert a mutual force majeure clause suspending affected obligations for the duration of the event, subject to notice and mitigation duties, with an objective test. Pre-agree an emergency surge rate mechanism in the Supply Schedule so emergency response is never delayed by commercial negotiation."),
 ("23.1(d) (quality warranty), 56.2 (supplier accreditation)",
  "The Supplier warrants a quality management system that complies with the requirements of ISO 9001. ASG operates a documented, annually reviewed integrated management system and is a member of the New Zealand Security Association, but does not currently hold ISO 9001 certification.",
  "Amend clause 23.1(d) to: the Supplier will operate a quality management system appropriate to security services that is consistent with the principles of ISO 9001, and will achieve ISO 9001 certification within twelve months of the Start Date. For clause 56.2, ASG will demonstrate its New Zealand Security Association membership as an approved industry accreditation per the alternative route that clause already provides."),
 ("50.1(k) (data residency)",
  "Clause 50.1(k) restricts hosting of Health NZ Data outside New Zealand, while clause 50.1(k)(ii) contemplates locations agreed in writing in the Supply Schedule. Widely used workforce platforms in the New Zealand security industry host data in Australia.",
  "Populate the clause 50.1(k)(ii) mechanism at signature: a schedule of named subprocessors and platforms with disclosed hosting locations agreed in writing in the Supply Schedule, with any change subject to prior written notice and approval."),
 ("59.3 (non-solicitation)",
  "The restraint is one-way: the Supplier may not solicit or employ Health NZ personnel with whom it has had material dealings, during the term and for two months after, while Health NZ and any successor supplier remain free to hire Supplier staff whom Health NZ has trained during the contract.",
  "Make the restraint mutual for the same scope and period, and confine it to solicitation, so that unsolicited applications in either direction are not captured."),
 ("46.1(b) (termination for breach)",
  "Termination is available for any breach not remedied within ten Business Days, with no materiality threshold, and clause 60.1 makes time of the essence for all obligations, so minor operational lapses are technically termination events.",
  "Insert a materiality threshold (breach having more than a minor effect on the Services), extend the cure period to twenty Business Days for breaches not capable of remedy within ten, and confine clause 60.1 to obligations expressly identified as time-critical in the Supply Schedule."),
]


def main(out):
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(10)

    h = doc.add_heading('Contract Departure Register', 0)
    for r in h.runs: r.font.color.rgb = NAVY
    p = doc.add_paragraph()
    p.add_run('Absolute Security Group Limited  |  RFP 0018709 Security Officer Services  |  '
              'Attachment B, Proposed Contract (Master Agreement)  |  5 November 2026').font.size = Pt(9)

    intro = doc.add_paragraph()
    intro.add_run(
        'Absolute Security Group Limited confirms its willingness to contract on the Proposed Contract, '
        'subject to negotiating the clauses below. Each position is offered constructively: our objective '
        'is a sustainable, long-term supply relationship, and we welcome discussion on every item. '
        'Except as set out below, the Proposed Contract is accepted as drafted.').font.size = Pt(10)

    t = doc.add_table(rows=1, cols=4)
    t.style = 'Table Grid'
    hdr = ['#', 'Clause', 'Concern', 'Proposed solution']
    for i, htxt in enumerate(hdr):
        c = t.rows[0].cells[i]
        c.paragraphs[0].text = ''
        run = c.paragraphs[0].add_run(htxt)
        run.bold = True
        run.font.size = Pt(10)
    for n, (clause, concern, solution) in enumerate(ITEMS, 1):
        row = t.add_row()
        vals = [str(n), clause, concern, solution]
        for i, v in enumerate(vals):
            cp = row.cells[i].paragraphs[0]
            cp.text = ''
            run = cp.add_run(v)
            run.font.size = Pt(9.5)
    # column widths via cell width hints
    from docx.shared import Cm
    widths = [Cm(0.9), Cm(3.6), Cm(6.3), Cm(6.6)]
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w

    end = doc.add_paragraph()
    end.add_run('\nAuthorised for and on behalf of Absolute Security Group Limited: '
                'Ahmad Duais, Chief Executive, 5 November 2026.').font.size = Pt(10)

    doc.save(out)
    print('Written:', out)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'ASG_Contract_Departure_Register.docx')
