# HOTC Report Structure & Conventions

## Folder Structure
```
~/Desktop/HOTC Claude/
├── 2024/          # April–December (10 months)
├── 2025/          # January–December (12 months, complete)
├── 2026/          # January–March (ongoing)
│   ├── January/
│   │   ├── Week 1 1st January - 4th January/
│   │   │   ├── Monday 1st January/
│   │   │   │   ├── HOTC Daily Log.docx      # Original 24hr guard report (unmodified, with branding/logos)
│   │   │   │   └── HOTC Report Analysis.docx # Clean consolidated summary
│   │   │   └── Weekly Data Report.xlsx
│   │   └── ...
│   ├── February/
│   └── March/
├── ASG_HOTC_Performance_Case_Study.docx   # Main analytics report (March 2024–present)
└── random docs/   # Supporting files (aggregated JSON, etc.)
```

## Daily Files (per day folder)
1. **HOTC Daily Log.docx** — Original branded 24hr shift report from guards. Preserved unmodified with logos/images, Heading 1/3 styles.
2. **HOTC Report Analysis.docx** — Clean consolidated summary with:
   - "Daily Report" title + date (D/M/YY)
   - **Incidents** (Heading 3): Bullet points with bold timestamps
   - **Business Calls** (Heading 3): Bullet points with bold timestamps
   - Footer sections (underlined bold headers): Pro-active engagement, Calls to Police, Assistance, HOTC, Comments, Routes and Times
   - Routes as bullet points (~17/day, Alpha/Bravo/Charlie/Delta rotation)

## Incident Consolidation Rules
- Related timestamps about the same incident → ONE bullet point with multiple timestamps
- Vagrant/routine situations → brief summary: "moved along without issue" / "had already left prior to arrival"
- Serious incidents (assaults, arrests, thefts, trespass) → full factual detail preserved
- Classification: response calls from businesses go under "Business Calls", other notable incidents under "Incidents"
- Skip: shift deployments, lunch breaks, routine welfare checks, equipment lists, patrol resumes

## Weekly Data Report.xlsx
- Metrics tracked per day (Mon–Sun + Total): Calls Made From Businesses, Police Calls, Aggressive Behavior, Public Drinking/Cannabis, Assistance Provided
- Patrol routes: Alpha, Bravo, Charlie, Delta (4 routes, NOT 5)
- Area Hotspot Analysis: 12 areas with checkup counts and status

## Case Study Report (ASG_HOTC_Performance_Case_Study.docx)
12 sections:
1. Executive Summary (key metrics table: 2024/2025/2026 Q1)
2. Contract Overview (NOTE: contract details need verification from Ahmad — values were AI-generated, not from verified source docs)
3. Performance Analytics (monthly breakdown table of all metrics)
4. Incident Analysis (aggression trends, police vs assistance, common incident types)
5. Patrol Coverage & Route Analysis
6. Area Hotspot Analysis (Critical/High/Moderate priority table)
7. Day-of-Week Patterns
8. Year-on-Year Comparison (8.1: 2024 vs 2025 full year, 8.2: Jan-Feb like-for-like)
9. 2026 Early Trends (Q1 monthly analysis + March daily report insights)
10. Key Findings (Strengths + Areas Requiring Attention)
11. Service Improvement Recommendations (priority table: HIGH/MEDIUM/LOW)
12. Proposed Enhanced Service Model (Technology, Ops, Community, Expected Outcomes)

## Source Data
- Guard daily reports: `~/Desktop/March /` (trailing space in folder name)
- Aggregated JSON: `~/Desktop/random docs/hotc_aggregated.json`
- Template for Report Analysis formatting: `~/Desktop/HOTC Claude/2026/February/Week 1 2nd Feb - 8th Feb/Friday 6th February/Daily Report.docx`

## Key Corrections Applied (ETR March 2026)
- Business calls YoY: +2.4% (not +2.6%)
- Aggression: "flat at ~46-47/month" (not "marginal increase")
- Public drinking: -15% (not -16%)
- Jan 2025 aggression: 69 (not 79 — was a data error)
- Queen Street: ~28% of activity (not >40%)
- July 2025: reporting gap (2 weeks submitted), not operational shortfall
