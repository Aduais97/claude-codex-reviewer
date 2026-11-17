#!/usr/bin/env python3
"""Curated weekly "Incidents in Focus" — SHARED by both the National LP & Safety Report
(gen_ww_safety_report.py) and the Weekly Security Performance & Value Report (gen_value_report.py),
so the two never drift.

Weekly curation: update the list below each week from the week's notable GIR rows.
Rules (enforced by the value report's lint gate): ANONYMISED (no names, gender-neutral where possible),
and legally-safe verbs only — observed / kept under observation / intercepted / recovered / deterred /
de-escalated / issued trespass / notified Police. NEVER apprehend / arrest / detain / restrain / "took
the" / physically stop, and do NOT describe the team approaching, challenging or searching a person.
Each entry: h (heading), occ (what happened), hand (how the team handled it), out (outcome).

W17 (19-25 Oct 2026). Guard names stripped (GIR narrative named two team members — removed).
"""

INCIDENTS = [
 {"h":"Newtown (Wellington) · about $215 recovered · concealment intercepted before walk-out",
  "occ":"An individual entered with a large unmarked bag inside a trolley, moved directly to "
        "the meat section for several high-value cuts, then circled multiple aisles adding "
        "items before concealing everything in the bag.",
  "hand":"The team read the pattern from entry and kept coordinated observation across the "
         "aisles, intercepting before the individual reached the front of the store.",
  "out":"About $215 of goods recovered, led by high-value meat, and a verbal trespass issued."},
 {"h":"Manukau (Auckland) · about $361 recovered · the week's largest interception",
  "occ":"An individual filled a trolley with goods and moved to leave the store without paying.",
  "hand":"The team, already maintaining observation, intercepted at the exit.",
  "out":"About $361 of goods recovered in full — the week's largest single interception."},
 {"h":"Te Rapa (Waikato) · about $279 recovered · concealment intercepted at self-checkout",
  "occ":"An individual was observed filling a shopping bag through the aisles, then walked past "
        "the point of sale making no attempt to pay.",
  "hand":"Covert team members maintained observation to the self-checkout and intercepted past "
         "the point of sale; the goods were recovered without resistance.",
  "out":"About $279 recovered in full. When advised Police would be asked to formalise the "
        "trespass, the individual left the store."},
 {"h":"Northlands (Canterbury) · Severity 3 · trespass breach · Police called",
  "occ":"A recognised repeat offender, already subject to a Woolworths-wide trespass, entered "
        "and bagged multiple items.",
  "hand":"On interception the individual became verbally aggressive and refused to leave. "
         "Following protocol for known higher-risk offenders, the team called Police immediately "
         "and store security assisted at the front of the store.",
  "out":"A portion of the goods was recovered and the breach of trespass is with Police — an "
        "example of the escalation pathway working as designed."},
 {"h":"Greenlane (Auckland) · Severity 3 · recovered in full · Police notified",
  "occ":"An individual concealed health-and-beauty items in a jacket pocket while moving "
        "through the aisles.",
  "hand":"On interception the goods were returned, but the individual then refused to leave and "
         "became argumentative at the front of the store; the team de-escalated and notified "
         "Police.",
  "out":"About $85 of goods recovered in full and a verbal trespass issued."},
]
