"""Comparison charts with Wythoff & Leane (2025) -> charts/chart1..3_*.png.

Their raw data is NOT redistributed in this repo. On first run this script downloads
futuristic_fiction.csv (CC BY 4.0, Post45 Data Collective, doi:10.18737/552626) into
data/external/ (git-ignored). My side uses the 163-film snapshot taken on 11 Oct 2026
(data/wythoff_leane/my_films_snapshot.csv), which is what these charts were drawn from.
"""
import os, urllib.request
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RP=lambda *a: os.path.join(REPO,*a)
WL_URL='https://raw.githubusercontent.com/Post45-Data-Collective/data/main/futuristic_fiction/futuristic_fiction.csv'
WL_MD5='6e5df3843416cebd0bf766509ed4ccda'  # version used in this analysis (fetched 11 Oct 2026)
WL=RP('data','external','futuristic_fiction.csv')
if not os.path.exists(WL):
    os.makedirs(os.path.dirname(WL),exist_ok=True); print('Downloading',WL_URL); urllib.request.urlretrieve(WL_URL,WL)
import hashlib
if hashlib.md5(open(WL,'rb').read()).hexdigest()!=WL_MD5: print('WARNING: futuristic_fiction.csv differs from the version used in this analysis; results may change.')
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; BAND='#121b30'
NEAR='#4fc3f7'; FAR='#ff8a65'; REL='#ffd54f'; AMB='#ce93d8'; BADGE='#26c6a6'; STREAM='#ff6fae'
w=pd.read_csv(WL).dropna(subset=['year_set']); w['dec']=w.released//10*10
o=pd.read_csv(RP('data','wythoff_leane','my_films_snapshot.csv')); o['dec']=o.release_year//10*10
SRC='Data: Wythoff & Leane (2025), Time Horizons of Futuristic Fiction, Post45 Data Collective, doi:10.18737/552626 (CC BY 4.0); my timeline: films.csv (163 films).'
def style(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=MUTED,labelsize=13)
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(axis='y',color=GRID,lw=1); ax.set_axisbelow(True)
def head(fig,t,sub):
    fig.text(0.05,0.94,t,color=FG,fontsize=24,fontweight='bold'); fig.text(0.05,0.895,sub,color=MUTED,fontsize=14)
    fig.text(0.05,0.03,SRC,color=MUTED,fontsize=10.5)
MINN=5; decs=list(range(1950,2030,10))
# Chart 1 median gap by decade
fig=plt.figure(figsize=(16,9),dpi=110,facecolor=BG); ax=fig.add_axes([0.07,0.13,0.88,0.7]); style(ax)
series=[('W&L films',w[w.medium=='film'],'released','years_distant',NEAR,'o'),('W&L novels & stories',w[w.medium=='prose fiction'],'released','years_distant',FAR,'s'),
        ('W&L all media',w,'released','years_distant',MUTED,'D'),('My timeline (films)',o,'release_year','gap_years',REL,'^')]
for lab,d,rc,gc,col,mk in series:
    g=d.groupby('dec')[gc].agg(['count','median']).reindex(decs)
    g=g[g['count']>=MINN]
    ax.plot(g.index+5,g['median'],color=col,lw=3 if 'W&L films'==lab or 'My' in lab else 2,marker=mk,ms=9,label=lab,ls='-' if lab!='W&L all media' else '--')
    for x,(c,m) in zip(g.index+5,g.values):
        if lab=='W&L films':
            om=o.groupby('dec').gap_years.median().get(x-5,0); up=om<m
            ax.text(x,m+(3 if up else -3.5),f'{m:g}',color=col,fontsize=12,ha='center',va='bottom' if up else 'top',fontweight='bold',zorder=5,bbox=dict(boxstyle='round,pad=0.15',fc=BG,ec='none'))
ax.set_xticks([d+5 for d in decs]); ax.set_xticklabels([f'{d}s' for d in decs]); ax.set_ylabel('Median years between release and setting',color=MUTED,fontsize=13)
ax.set_ylim(0,110)
ax.legend(facecolor=BAND,edgecolor=GRID,labelcolor=FG,fontsize=13,loc='upper right')
head(fig,'Is screen sci-fi looking nearer? Median gap by release decade','W&L films fall from 50 years (1960s) to 10.5 (2020s); novels hold at 50-70 until a small 2020s sample (n=21). Decades with <5 works omitted.')
fig.savefig(RP('charts','chart1_median_gap_by_decade.png'),facecolor=BG); plt.close(fig)
# Chart 2 distribution
bins=[0,5,10,25,50,100,250,1000,1e20]; lab=['0-5','6-10','11-25','26-50','51-100','101-250','251-1,000','1,000+']
wf=w[w.medium=='film'].years_distant; og=o.gap_years
pw=pd.cut(wf,bins,labels=lab,include_lowest=True).value_counts(normalize=True).reindex(lab)*100
po=pd.cut(og,bins,labels=lab,include_lowest=True).value_counts(normalize=True).reindex(lab)*100
fig=plt.figure(figsize=(16,9),dpi=110,facecolor=BG); ax=fig.add_axes([0.07,0.13,0.88,0.7]); style(ax)
x=np.arange(len(lab)); bw=0.38
b1=ax.bar(x-bw/2,pw,bw,color=NEAR,label=f'W&L films (n={len(wf)}, median {wf.median():g} yrs)')
b2=ax.bar(x+bw/2,po,bw,color=REL,label=f'My timeline (n={len(og)}, median {og.median():g} yrs)')
for bars,c in((b1,NEAR),(b2,REL)):
    for b in bars: ax.text(b.get_x()+b.get_width()/2,b.get_height()+0.4,f'{b.get_height():.0f}%',color=c,ha='center',fontsize=11.5)
ax.set_xticks(x); ax.set_xticklabels(lab); ax.set_xlabel('Years between release and setting',color=MUTED,fontsize=13); ax.set_ylabel('Share of films (%)',color=MUTED,fontsize=13)
ax.legend(facecolor=BAND,edgecolor=GRID,labelcolor=FG,fontsize=13,loc='upper right')
head(fig,'How far ahead? My films vs Wythoff & Leane\'s 960','W&L include many "next year" films (superhero, horror, comedy) that I leave out, so a third of theirs sit within 10 years against 14% of mine.')
fig.savefig(RP('charts','chart2_gap_distribution_mine_vs_wl.png'),facecolor=BG); plt.close(fig)
# Chart 3 share within 10 years by decade
fig=plt.figure(figsize=(16,9),dpi=110,facecolor=BG); ax=fig.add_axes([0.07,0.13,0.88,0.7]); style(ax)
for labx,m,col,mk in [('Films','film',NEAR,'o'),('Novels & stories','prose fiction',FAR,'s'),('Television','television',AMB,'D')]:
    d=w[w.medium==m]; g=d.groupby('dec').years_distant.agg(count='count',share=lambda s:(s<=10).mean()*100).reindex(decs); g=g[g['count']>=MINN]
    ax.plot(g.index+5,g['share'],color=col,lw=3 if m=='film' else 2,marker=mk,ms=9,label=labx)
    if m=='film':
        for xx,v in zip(g.index+5,g['share']): ax.text(xx,v+1.5,f'{v:.0f}%',color=col,fontsize=11,ha='center')
ax.set_xticks([d+5 for d in decs]); ax.set_xticklabels([f'{d}s' for d in decs]); ax.set_ylabel('% set within 10 years of release',color=MUTED,fontsize=13); ax.set_ylim(0,60)
ax.legend(facecolor=BAND,edgecolor=GRID,labelcolor=FG,fontsize=13,loc='upper left')
head(fig,'Testing Hollinger: the share of near-future stories','Half of W&L\'s 2020s films are set within a decade of release, up from under a fifth in the 1960s. Decades with fewer than 5 works omitted.')
fig.savefig(RP('charts','chart3_near_future_share_by_decade.png'),facecolor=BG); plt.close(fig)
print('ok')
