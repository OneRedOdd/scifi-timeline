# Extra figures for paper_v2 (dark palette matching wythoff_leane/charts.py)
"""Extra figures for the paper -> paper/figures/."""
import os
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)

import pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; BAND='#121b30'
NEAR='#4fc3f7'; FAR='#ff8a65'; REL='#ffd54f'; AMB='#ce93d8'
def style(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=MUTED,labelsize=13)
    for s in ax.spines.values(): s.set_color(GRID)
    ax.grid(axis='y',color=GRID); ax.set_axisbelow(True)
f=pd.read_csv(RP('data','films.csv')); p=pd.read_csv(RP('data','predictions.csv')); p=p[p.title.isin(f.title)]
# Fig: gap distribution, all 233
bins=[(0,5),(6,10),(11,25),(26,50),(51,100),(101,250),(251,1000),(1001,10**9)]
labs=['0-5','6-10','11-25','26-50','51-100','101-250','251-1,000','1,000+']
flag=f.title.str.contains(r'\*',regex=True)
cu=[((f.gap_years>=a)&(f.gap_years<=b)&~flag).sum() for a,b in bins]
cf=[((f.gap_years>=a)&(f.gap_years<=b)&flag).sum() for a,b in bins]
fig=plt.figure(figsize=(16,9),dpi=110,facecolor=BG); ax=fig.add_axes([0.07,0.13,0.88,0.68]); style(ax)
x=range(len(labs)); ax.bar(x,cu,color=NEAR,label=f'Year sourced, unflagged ({(~flag).sum()})')
ax.bar(x,cf,bottom=cu,color=AMB,label=f'Year flagged as ambiguous/derived* ({flag.sum()})')
for i,(u,c) in enumerate(zip(cu,cf)): ax.text(i,u+c+1,str(u+c),ha='center',color=FG,fontsize=14)
ax.set_xticks(list(x)); ax.set_xticklabels(labs); ax.set_xlabel('Years between release and setting',color=MUTED,fontsize=14)
ax.set_ylabel('Films',color=MUTED,fontsize=14)
ax.legend(facecolor=BAND,edgecolor=GRID,labelcolor=FG,fontsize=13,loc='upper right')
fig.text(0.05,0.92,'How far ahead do the 233 films look?',color=FG,fontsize=24,weight='bold')
fig.text(0.05,0.87,f'Median gap {f.gap_years.median():.0f} years; {(f.gap_years<=10).mean()*100:.0f}% within 10 years, {(f.gap_years<=50).mean()*100:.0f}% within 50, {(f.gap_years<=100).mean()*100:.0f}% within 100.',color=MUTED,fontsize=15)
fig.text(0.05,0.03,'Source: films.csv (233 films, October 2026). Gap = setting year minus release year.',color=MUTED,fontsize=11)
fig.savefig(RP('paper','figures','fig_gap_distribution_233.png'),facecolor=BG); plt.close(fig)
# Fig: score by theme
s=p[p.scored=='yes'].copy(); s['pts']=s.verdict.map({'came true':1,'sort of':.5,"didn't":0})
t=s.groupby('theme').agg(n=('pts','size'),films=('title','nunique'),score=('pts','mean'),true=('verdict',lambda v:(v=='came true').mean())).sort_values('score')
fig=plt.figure(figsize=(16,9),dpi=110,facecolor=BG); ax=fig.add_axes([0.2,0.13,0.75,0.68]); style(ax); ax.grid(axis='x',color=GRID); ax.grid(axis='y',visible=False)
y=range(len(t)); ax.barh([i+0.2 for i in y],t.score*100,height=0.4,color=REL,label="Score (sort of = half)")
ax.barh([i-0.2 for i in y],t.true*100,height=0.4,color=NEAR,label='% came true outright')
for i,(sc,tr,n,fi) in enumerate(zip(t.score,t.true,t.n,t.films)):
    ax.text(sc*100+0.8,i+0.2,f'{sc*100:.1f}%',va='center',color=FG,fontsize=12)
    ax.text(tr*100+0.8,i-0.2,f'{tr*100:.0f}%',va='center',color=MUTED,fontsize=11)
ax.set_yticks(list(y)); ax.set_yticklabels([f'{k}\n(n={n}, {fi} films)' for k,n,fi in zip(t.index,t.n,t.films)],color=FG,fontsize=12)
ax.axvline(s.pts.mean()*100,color=FAR,ls='--'); ax.text(s.pts.mean()*100+0.5,len(t)-0.45,f'all themes {s.pts.mean()*100:.1f}%',color=FAR,fontsize=12)
ax.set_xlabel('% of scored predictions',color=MUTED,fontsize=14)
ax.legend(facecolor=BAND,edgecolor=GRID,labelcolor=FG,fontsize=13,loc='lower right')
fig.text(0.05,0.92,'Which kinds of prediction came true?',color=FG,fontsize=24,weight='bold')
fig.text(0.05,0.87,'220 scored predictions from 75 films whose setting year has arrived, judged by each film\'s own year.',color=MUTED,fontsize=15)
fig.text(0.05,0.03,'Source: predictions.csv (audit v2). Most themes have fewer than 30 predictions; only communication survives a multiple-comparison correction (audit v1).',color=MUTED,fontsize=11)
fig.savefig(RP('paper','figures','fig_theme_scores.png'),facecolor=BG); plt.close(fig)
# Crops of the main infographic
im=Image.open(RP('charts','timeline.png')).convert('RGB')
im.crop((0,0,2400,2500)).save(RP('paper','figures','timeline_top.png'))
im.crop((0,10150,2400,10947)).save(RP('paper','figures','timeline_panels.png'))
print(t)
