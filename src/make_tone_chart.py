"""Draw charts/tone_vs_accuracy.png from data/derived/tone.json (made by src/tone_stats.py)."""
import os, sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
import json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np
S=json.load(open(RP('data','derived','tone.json')))
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; NEAR='#4fc3f7'; FAR='#ff8a65'; REL='#ffd54f'; AMB='#ce93d8'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':FG,'axes.labelcolor':FG,'xtick.color':MUTED,'ytick.color':MUTED})
fig=plt.figure(figsize=(24,15),dpi=100,facecolor=BG)
gs=fig.add_gridspec(2,2,left=0.05,right=0.98,top=0.86,bottom=0.11,hspace=0.62,wspace=0.16)
def style(ax):
    ax.set_facecolor(BG); [s.set_visible(False) for s in ax.spines.values()]; ax.grid(axis='y',color=GRID,lw=1); ax.set_axisbelow(True); ax.tick_params(labelsize=14)
# A: accuracy by tone, both label sets
ax=fig.add_subplot(gs[0,0]); style(ax)
groups=[('wiki','dys','Wikipedia:\ndystopian'),('wiki','non','Wikipedia:\nnot dystopian'),('strict','dys','Strict:\ndystopian'),('strict','non','Strict:\nnot dystopian')]
x=np.array([0,1,2.4,3.4]); w=0.36
ct=[S[l]['all'][f'{k}_true'] for l,k,_ in groups]; hc=[S[l]['all'][k] for l,k,_ in groups]
b1=ax.bar(x-w/2,ct,w,color=NEAR,label='% came true'); b2=ax.bar(x+w/2,hc,w,color=REL,label="Score ('sort of' = half)")
for b,v in list(zip(b1,ct))+list(zip(b2,hc)): ax.text(b.get_x()+b.get_width()/2,v+0.6,f'{v:.1f}%',ha='center',color=FG,fontsize=14,fontweight='bold')
labs=[f"{t}\n{S[l]['all'][k+'_films']} films · {S[l]['all'][k+'_n']} preds" for l,k,t in groups]
ax.set_xticks(x); ax.set_xticklabels(labs,fontsize=12.5,color=FG)
ax.set_ylim(0,32); ax.set_ylabel('% of scored predictions',fontsize=14)
ax.set_title('A. Prediction accuracy by tone (75 films whose year has arrived)',loc='left',fontsize=19,color=FG,pad=14,fontweight='bold')
ax.legend(frameon=False,fontsize=13,loc='upper right',labelcolor=FG)
wa,sa=S['wiki']['all'],S['strict']['all']
ax.text(0.0,-0.33,f"Came true vs not, Fisher's exact: Wikipedia p = {wa['fisher_p']:.2f}; strict p = {sa['fisher_p']:.2f} (OR {sa['OR']:.2f}). Film-level permutation p = {wa['perm_p']:.2f} / {sa['perm_p']:.2f};\ntheme-adjusted model p = {wa['gee_p']:.2f} / {sa['gee_p']:.2f}. No significant difference: if anything, strictly dystopian films do slightly worse.",transform=ax.transAxes,color=MUTED,fontsize=12.5)
# B: theme x strict tone
ax=fig.add_subplot(gs[0,1]); style(ax)
th=['communication','computing/AI','society/politics','medicine/biotech','space','environment','transport','other']
x=np.arange(len(th)); T=S['theme_strict']
dv=[T[t]['dys'] or 0 for t in th]; nv=[T[t]['non'] or 0 for t in th]; dn=[T[t]['dn'] for t in th]; nn=[T[t]['nn'] for t in th]
b1=ax.bar(x-w/2,dv,w,color=FAR,label='Strictly dystopian'); b2=ax.bar(x+w/2,nv,w,color=NEAR,label='Not dystopian')
for b,v,n in list(zip(b1,dv,dn))+list(zip(b2,nv,nn)):
    ax.text(b.get_x()+b.get_width()/2,v+1.5,f'{v:.0f}%',ha='center',color=FG,fontsize=12,fontweight='bold')
    ax.text(b.get_x()+b.get_width()/2,-7,f'{n}',ha='center',color=MUTED,fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(['comms','computing\n/AI','society\n/politics','medicine\n/biotech','space','environ-\nment','transport','other'],fontsize=13,color=FG); ax.tick_params(axis='x',pad=26)
ax.set_ylim(-10,85); ax.set_yticks(range(0,81,20)); ax.set_ylabel("Score ('sort of' = half), %",fontsize=14)
ax.set_title('B. Accuracy by theme and strict tone',loc='left',fontsize=19,color=FG,pad=14,fontweight='bold')
ax.legend(frameon=False,fontsize=13,loc='upper right',labelcolor=FG)
ax.text(0.0,-0.33,'Grey numbers = predictions per bar; most bars are small (space and transport have only 2 dystopian predictions each).\nTheme, not tone, drives accuracy: communication scores highest; society/politics, transport and space lowest.',transform=ax.transAxes,color=MUTED,fontsize=12.5)
# C: decade share, wiki vs strict
ax=fig.add_subplot(gs[1,:]); style(ax)
dec=sorted(S['decade'].items(),key=lambda kv:int(kv[0])); ks=[f"{k}s" for k,_ in dec]; tot=[v['n'] for _,v in dec]
wv=[100*v['wiki']/v['n'] for _,v in dec]; sv=[100*v['strict']/v['n'] for _,v in dec]
x=np.arange(len(ks)); w2=0.38
c1=[FAR if t>=10 else '#7a4a3c' for t in tot]; c2=[AMB if t>=10 else '#5e4466' for t in tot]
bA=ax.bar(x-w2/2,wv,w2,color=c1,label='Wikipedia label'); bB=ax.bar(x+w2/2,sv,w2,color=c2,label='Strict on-screen label')
for b,v in list(zip(bA,wv))+list(zip(bB,sv)): ax.text(b.get_x()+b.get_width()/2,v+2,f'{v:.0f}%',ha='center',color=FG,fontsize=12.5,fontweight='bold')
for i,(k,v) in enumerate(dec): ax.text(i,-10,f"{v['n']} films",ha='center',color=MUTED,fontsize=12)
ax.set_xticks(x); ax.set_xticklabels(ks,fontsize=14,color=FG); ax.tick_params(axis='x',pad=26); ax.set_ylim(-14,100); ax.set_yticks(range(0,101,25)); ax.set_ylabel('% dystopian',fontsize=14)
ax.set_title('C. Share of dystopian films by release decade (all 233 films)',loc='left',fontsize=19,color=FG,pad=14,fontweight='bold')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=FAR,label='Wikipedia label'),Patch(color=AMB,label='Strict on-screen label')],frameon=False,fontsize=13,loc='upper left',labelcolor=FG)
tw,ts=S['trend_wiki'],S['trend_strict']
ax.text(0.0,-0.26,f"Darker bars: fewer than 10 films in the decade. 2020s = 2020-2026 only. Trend since 1950 (logistic): Wikipedia labels rise significantly (OR {tw['OR_per_decade']:.2f} per decade, p = {tw['p']:.2f});\nstrict labels show no significant trend (OR {ts['OR_per_decade']:.2f}, p = {ts['p']:.2f}). The 2010s peak (86%) is largely a Wikipedia labelling effect: 63% on the strict rule.",transform=ax.transAxes,color=MUTED,fontsize=12.5)
fig.text(0.05,0.955,'Do dark futures predict better? Tone vs prediction accuracy',color=FG,fontsize=30,fontweight='bold')
fig.text(0.05,0.918,"Wikipedia tone = dystopian/post-apocalyptic wording or categories. Strict tone = the society on screen is oppressive or collapsed for most of the runtime. Scored against each film's setting year.",color=MUTED,fontsize=14.5)
fig.text(0.98,0.02,'Sources: films.csv (tone, tone_strict), predictions.csv (220 scored predictions, audit v2). October 2026.',color=MUTED,fontsize=12,ha='right')
fig.savefig(RP('charts','tone_vs_accuracy.png'),facecolor=BG); print('ok')
