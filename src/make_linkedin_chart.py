"""Draw charts/timeline_eight.png: eight well-known films from data/films.csv, square-ish for LinkedIn.
Same colours as the main timeline. Run from anywhere: python src/make_linkedin_chart.py"""
# The full chart is too tall for a feed, so this is my eight-film taster for Post 1.
import os, csv, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; BAND='#121b30'
NEAR='#4fc3f7'; REL='#ffd54f'
PICK=['2001: A Space Odyssey','Soylent Green','Escape from New York','Blade Runner','Back to the Future Part II','Minority Report','Children of Men','Terminator: Dark Fate']
F={r['title'].rstrip('*'):r for r in csv.DictReader(open(RP('data','films.csv'),encoding='utf-8'))}
rows=sorted((F[t] for t in PICK),key=lambda r:int(r['release_year']))
fig=plt.figure(figsize=(12,15),dpi=100,facecolor=BG)
fig.text(0.05,0.95,'Eight films, eight futures',color=FG,fontsize=40,fontweight='bold')
fig.text(0.05,0.915,'Each line runs from the year a film came out to the year it\'s set in.\nSix of these eight futures are already in the past. I\'m still waiting for my flying car.',color=MUTED,fontsize=17,va='top',linespacing=1.4)
ax=fig.add_axes([0.05,0.1,0.9,0.73],facecolor=BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xlim(1955,2075); ax.set_ylim(len(rows)-0.4,-0.9)
ax.set_xticks(range(1960,2071,20)); ax.tick_params(colors=MUTED,labelsize=16,left=False,labelleft=False)
ax.grid(axis='x',color=GRID,lw=1); ax.set_axisbelow(True)
ax.axvline(2026,color='#ffffff',lw=2,ls=(0,(4,4)),alpha=0.45,zorder=1)
ax.text(2027,-0.75,'Today (2026)',color=FG,fontsize=15,va='center')
for i,r in enumerate(rows):
    ry,sy=int(r['release_year']),int(r['setting_year']); t=r['title'].rstrip('*')
    if i%2==0: ax.axhspan(i-0.5,i+0.5,color=BAND,zorder=0)
    ax.plot([ry,sy],[i+0.12]*2,color=NEAR,lw=6,solid_capstyle='round',zorder=2)
    ax.scatter([ry],[i+0.12],s=170,color=REL,zorder=3); ax.scatter([sy],[i+0.12],s=170,color=NEAR,zorder=3)
    ax.text(ry,i-0.2,t,color=FG,fontsize=20,fontweight='bold',va='center',ha='left')
    ax.text(ry-1.2,i+0.12,str(ry),color=REL,fontsize=15,va='center',ha='right')
    ax.text(sy+1.2,i+0.12,f'{sy}  (+{sy-ry} yr{"s" if sy-ry!=1 else ""})',color=FG,fontsize=15,va='center',ha='left')
for x,c,l in [(0.05,REL,'Release year'),(0.25,NEAR,'Setting year')]:
    fig.text(x,0.06,'\u25CF',color=c,fontsize=22,va='center'); fig.text(x+0.025,0.06,l,color=FG,fontsize=16,va='center')
fig.text(0.05,0.025,'From my hand-built timeline of 233 sci-fi films. Full chart: oneredodd.github.io/scifi-timeline',color=MUTED,fontsize=14)
fig.savefig(RP('charts','timeline_eight.png'),facecolor=BG); print('saved', [ (r['title'],r['release_year'],r['setting_year']) for r in rows])
