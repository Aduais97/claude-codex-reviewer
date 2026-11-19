#!/usr/bin/env python3
"""Appendix trend graphs — cleaned. 3-month moving averages, monthly x-grid,
a funding-vs-output showcase, and a merged antisocial-behaviour series.
Full history Mar 2024 -> Jul 2026; quarter (May-Jul 2026) shaded."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

TL=json.load(open("/Users/ahmadduais/Desktop/Dev/Claude/scripts/hotc/data/hotc_quarterly/timeline.json"))
OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/_charts_quarterly"; os.makedirs(OUT,exist_ok=True)
NAVY='#1F3864'; GOLD='#B8912F'; RED='#B01E1E'; GREEN='#2E7D32'; MAROON='#8A1C1C'; PURPLE='#7A5195'
labels=[t['label'] for t in TL]; x=list(range(len(TL)))
def idx(ym): return next(i for i,t in enumerate(TL) if t['ym']==ym)
Q=[idx('2026-07'),idx('2026-08'),idx('2026-09')]
CUT=idx('2025-05'); P0=idx('2026-06'); P1=idx('2026-07')
plt.rcParams.update({'font.size':10,'axes.edgecolor':'#CCCCCC','axes.linewidth':0.8})

def ma(y,w=3):
    out=[]
    for i in range(len(y)):
        lo=max(0,i-w//2); hi=min(len(y),i+w//2+1); seg=y[lo:hi]
        out.append(sum(seg)/len(seg))
    return out

def clean_axis(ax, title, ylab, shade_q=True):
    ax.set_title(title,fontsize=13,color=NAVY,fontweight='bold',loc='left',pad=10)
    ax.set_ylabel(ylab,fontsize=10,color='#333')
    ax.grid(axis='y',color='#EAEAEA',linewidth=0.7)
    ax.spines[['top','right']].set_visible(False)
    ax.xaxis.set_minor_locator(MultipleLocator(1))              # a tick at EVERY month
    ax.tick_params(axis='x',which='minor',length=3,color='#CCCCCC')
    ticks=x[::3]+([x[-1]] if x[-1] not in x[::3] else [])       # always label the final month (Jul 26)
    ax.set_xticks(ticks); ax.set_xticklabels([labels[i] for i in ticks],rotation=45,ha='right',fontsize=8.5)
    ax.set_xlim(-0.5,len(TL)-0.5)
    if shade_q:
        ax.axvspan(Q[0]-0.5,Q[-1]+0.5,color=GOLD,alpha=0.14,zorder=0)
        ymin,ymax=ax.get_ylim()
        ax.text((Q[0]+Q[-1])/2,ymin+(ymax-ymin)*0.03,'Quarter\nJul–Sep 26',ha='center',va='bottom',fontsize=7.5,color=GOLD,fontweight='bold')

# ============ Fig 1: Business calls — raw + 3-mo moving average ============
fig,ax=plt.subplots(figsize=(11,4.4),dpi=200)
y=[t.get('calls',0) for t in TL]
ax.plot(x,y,color=NAVY,lw=0.9,marker='o',ms=3,alpha=0.30,zorder=2,label='Monthly')
ax.plot(x,ma(y),color=NAVY,lw=2.6,zorder=3,label='3-month average')
clean_axis(ax,'Business calls per month — full history (Mar 2024 – Sep 2026)','Calls / month')
ax.axvline(CUT-0.5,color=RED,ls='--',lw=1,alpha=0.7)
ax.text(CUT-0.3,ax.get_ylim()[1]*0.93,' Budget cut\n $800k→$690k',color=RED,fontsize=7.5,va='top')
ax.legend(loc='upper right',fontsize=8.5,frameon=False)
plt.tight_layout(); plt.savefig(f"{OUT}/fig1_calls.png",bbox_inches='tight'); plt.close()

# ============ Fig 2: FUNDING vs OUTPUT showcase (dual axis) ============
fig,ax=plt.subplots(figsize=(11,4.6),dpi=200)
cy=[t.get('calls',0) for t in TL]
ax.plot(x,cy,color=NAVY,lw=0.9,alpha=0.30,marker='o',ms=2.5,zorder=2)
ax.plot(x,ma(cy),color=NAVY,lw=2.6,zorder=3,label='Business calls (3-mo avg)')
clean_axis(ax,'Funding vs output — business calls track the funding level','Calls / month',shade_q=False)
# funding step on right axis
ax2=ax.twinx(); ax2.spines[['top']].set_visible(False)
fund=[800 if i<CUT else 690 for i in x]
ax2.step(x,fund,where='mid',color=GOLD,lw=2.2,zorder=3,label='Funding ($k/yr)')
ax2.set_ylabel('Programme funding ($k / year)',color=GOLD,fontsize=10)
ax2.set_ylim(500,1000); ax2.tick_params(axis='y',colors=GOLD)
ax2.axvspan(P0-0.5,P1+0.5,color=GREEN,alpha=0.10,zorder=0)
ax2.text((P0+P1)/2,930,'+ LCF\nfunded team',ha='center',fontsize=7.5,color=GREEN,fontweight='bold')
ax.text(CUT-0.4,ax.get_ylim()[1]*0.55,'funding cut',color=RED,fontsize=7.5,rotation=90,va='center')
# combined legend
l1,lab1=ax.get_legend_handles_labels(); l2,lab2=ax2.get_legend_handles_labels()
ax.legend(l1+l2,lab1+lab2,loc='lower left',fontsize=8.5,frameon=True,facecolor='white',edgecolor='#DDDDDD',ncol=1)
plt.tight_layout(); plt.savefig(f"{OUT}/fig2_funding_vs_calls.png",bbox_inches='tight'); plt.close()

# ============ Fig 3: Antisocial behaviour (merged) — aggression + drugs/alcohol ============
fig,ax=plt.subplots(figsize=(11,4.4),dpi=200)
anti=[t.get('aggressive',0)+t.get('drinking',0) for t in TL]        # full history
ax.plot(x,anti,color=MAROON,lw=0.9,alpha=0.30,marker='o',ms=3,zorder=2,label='Monthly')
ax.plot(x,ma(anti),color=MAROON,lw=2.6,zorder=3,label='3-month average')
clean_axis(ax,'Antisocial behaviour per month — aggression + drugs/alcohol combined (full history)','Incidents / month')
ax.axvline(CUT-0.5,color=RED,ls='--',lw=1,alpha=0.7)
ax.legend(loc='upper right',fontsize=8.5,frameon=False)
ax.text(0.5,ax.get_ylim()[1]*0.04,'Merged: aggressive behaviour + public drinking / cannabis (both tracked throughout).',
        fontsize=7.5,color='#666')
plt.tight_layout(); plt.savefig(f"{OUT}/fig3_antisocial.png",bbox_inches='tight'); plt.close()

# ============ Fig 4: Detailed incidents handled (stacked, from Mar 2026) ============
sub=[t for t in TL if 'vagrants' in t]; sx=list(range(len(sub))); slab=[t['label'] for t in sub]
fig,ax=plt.subplots(figsize=(9,4.4),dpi=200); bottom=[0]*len(sub)
for k,lab,col in [('vagrants','Vagrants moved on',NAVY),('theft','Shoplifting/theft',GOLD),
                  ('aggressive','Aggressive behaviour',MAROON),('serious','Serious incidents','#C1440E'),
                  ('intoxicated','Intoxicated persons','#3A6EA5'),('arrests','Arrests',GREEN)]:
    vals=[t.get(k,0) for t in sub]; ax.bar(sx,vals,bottom=bottom,label=lab,color=col,width=0.62); bottom=[b+v for b,v in zip(bottom,vals)]
ax.set_title('Detailed incidents handled — since tracking began (Mar 2026)',fontsize=13,color=NAVY,fontweight='bold',loc='left',pad=10)
ax.set_ylabel('Incidents / month'); ax.set_xticks(sx); ax.set_xticklabels(slab)
ax.legend(fontsize=8,frameon=False,ncol=2,loc='upper left'); ax.grid(axis='y',color='#EAEAEA',lw=0.7); ax.spines[['top','right']].set_visible(False)
for i,t in enumerate(sub):
    if t['ym'] in ('2026-07','2026-08','2026-09'): ax.axvspan(i-0.42,i+0.42,color=GOLD,alpha=0.10,zorder=0)
plt.tight_layout(); plt.savefig(f"{OUT}/fig4_detail_incidents.png",bbox_inches='tight'); plt.close()

# ============ Fig 5: TOTAL recorded activity (everything combined) ============
fig,ax=plt.subplots(figsize=(11,4.6),dpi=200)
# core total (full history, distinct measures, no double-count): calls + aggression + police + drink + assist
core=[t.get('calls',0)+t.get('aggressive',0)+t.get('police',0)+t.get('drinking',0)+t.get('assist',0) for t in TL]
ax.plot(x,core,color=NAVY,lw=0.9,alpha=0.28,marker='o',ms=2.5,zorder=2)
ax.plot(x,ma(core),color=NAVY,lw=2.6,zorder=3,label='Core total (calls + aggression + police + drink/drugs + assist)')
# fuller total from Mar 2026: add the detailed incident types (aggression already counted, so excluded here)
addl=['vagrants','theft','serious','intoxicated','arrests','injuries']
fx=[i for i,t in enumerate(TL) if 'vagrants' in t]
fy=[core[i]+sum(TL[i].get(k,0) for k in addl) for i in fx]
ax.plot(fx,fy,color=GOLD,lw=2.4,marker='o',ms=4.5,zorder=4,label='Total incl. detailed incidents (tracked from Mar 2026)')
clean_axis(ax,'Total recorded activity per month — all measures combined','Activity events / month')
ax.legend(loc='upper center',fontsize=8,frameon=True,facecolor='white',edgecolor='#DDDDDD')
ymin,ymax=ax.get_ylim()
ax.text(0.5,ymin+(ymax-ymin)*0.03,'Core line runs the full history. Gold adds vagrancy, theft, serious incidents, intoxication & arrests — only tracked since Mar 2026, so the step up is broader recording, not a real jump.',fontsize=6.8,color='#666')
plt.tight_layout(); plt.savefig(f"{OUT}/fig5_total_activity.png",bbox_inches='tight'); plt.close()

print("Saved cleaned charts to",OUT)
for f in sorted(os.listdir(OUT)): print("  ",f)
