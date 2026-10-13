"""Draw the main timeline infographic (charts/timeline.png and .pdf) from data/films.csv.
Run from anywhere: python src/make_timeline_chart.py"""
# I built this by hand — 233 films on humanity's current calendar. This script draws the poster chart.
import os, sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
import csv, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, textwrap, sys
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from panels import FOUND,METHOD,SOURCES
# Sort by release, then setting — so the 1980s (Blade Runner, BTTF II) sit together.
rows=sorted(csv.DictReader(open(RP('data','films.csv'),encoding='utf-8')),key=lambda r:(int(r['release_year']),int(r['setting_year'])))
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; BAND='#121b30'
NEAR='#4fc3f7'; FAR='#ff8a65'; REL='#ffd54f'; AMB='#ce93d8'; DEC='#5c6b8a'
# Near axis to 2125; anything further gets the compressed right-hand scale.
SPLIT=2125; NEARMIN=1900; FARMAX=5400; OFF=4850
n=len(rows); RH=0.42  # inches per row
WRAP=89; LH=0.285
import functools; textwrap.wrap=functools.partial(textwrap.wrap,break_on_hyphens=False)
def lines(items): return [textwrap.wrap(f'{a} {b}',WRAP) for a,b in items]
SL=len(textwrap.wrap(SOURCES,WRAP+4))
PH0=0.95+LH*max(sum(len(l)+0.45 for l in lines(FOUND)), sum(len(l)+0.45 for l in lines(METHOD))+SL+0.4)+0.35
PB=1.85  # panel bottom (in)
H=n*RH+4.4+PH0+0.6
fig=plt.figure(figsize=(24,H),dpi=100,facecolor=BG)
top=1-2.3/H; bot=(PB+PH0+0.95)/H
axL=fig.add_axes([0.205,bot,0.525,top-bot],facecolor=BG)
axR=fig.add_axes([0.75,bot,0.22,top-bot],facecolor=BG,sharey=axL)
axL.set_xlim(NEARMIN,SPLIT+12); axR.set_xlim(SPLIT,FARMAX)
axL.set_ylim(n-0.4,-0.9)
for ax in (axL,axR):
    ax.tick_params(colors=MUTED,labelsize=13,labeltop=True,top=False)
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(axis='x',color=GRID,lw=1); ax.set_axisbelow(True)
    ax.tick_params(axis='y',left=False,labelleft=False)
axL.set_xticks(range(1900,2121,20)); axR.set_xticks([2500,3000,3500,4000,4500,5000])
# "Today" line — 2026. 81 of the 233 futures are already behind it.
axL.axvline(2026,color='#ffffff',lw=1.5,ls=(0,(4,4)),alpha=0.55)
axL.text(2028,-0.7,'Today (2026)',color=FG,ha='left',va='center',fontsize=12,alpha=0.9)
axL.set_title('Near future (to 2125)',color=NEAR,fontsize=16,pad=34,loc='left')
axR.set_title('Far future (compressed scale)',color=FAR,fontsize=16,pad=34,loc='left')
yfig=lambda i: axL.transData.transform((0,i))[1]/fig.bbox.height
prev_dec=None
# Country badges: solid = made outside UK/US; outline = co-pro led by that country.
ISO={'Germany':'DE','West Germany (West Berlin)':'DE','West Germany':'DE','Austria':'AT','Czechoslovakia':'CS','Czech Republic':'CZ','Denmark':'DK','Italy':'IT','France':'FR','Finland':'FI','Canada':'CA','Japan':'JP','Hong Kong':'HK','South Korea':'KR','China':'CN','Australia':'AU','Ireland':'IE','Hungary':'HU','Jordan':'JO','Romania':'RO','Soviet Union':'SU','Poland':'PL','India':'IN','Belgium':'BE','Luxembourg':'LU','South Africa':'ZA','Russia':'RU','Slovakia':'SK','Serbia':'RS','East Germany':'DD','Spain':'ES','Bulgaria':'BG','Switzerland':'CH','Argentina':'AR','New Zealand':'NZ','Indonesia':'ID','Dominican Republic':'DO','Kenya':'KE'}
BADGE='#26c6a6'; STREAM='#ff6fae'
NOBADGE={'Terminator: Dark Fate'}
def badge_info(country):
    cs=[c.strip() for c in country.split(';')]
    base=[c for c in cs if not c.startswith(('United States','United Kingdom'))]
    if not base: return None
    if len(base)==len(cs): return 'solid','/'.join(dict.fromkeys(ISO[c] for c in cs))
    if not cs[0].startswith(('United States','United Kingdom')): return 'outline',ISO[cs[0]]
    return None
fig.canvas.draw(); RENDER=fig.canvas.get_renderer()
DRAWN=[]
# One bar per film: release year → setting year, gap labelled beside the setting blob.
for i,r in enumerate(rows):
    ry,sy,g=int(r['release_year']),int(r['setting_year']),int(r['gap_years'])
    title=r['title']; amb=title.endswith('*'); fmt=r.get('format','feature')
    # Shorten the THX short — the full Electronic Labyrinth title eats the label.
    title={'Electronic Labyrinth: THX 1138 4EB*':'THX 1138 4EB*'}.get(title,title)
    if fmt in ('short','serial'): title=title+f' ({fmt})'
    yl=lambda g: f'+{g:,} yr' if g==1 else f'+{g:,} yrs'
    dec=ry//10*10
    # Decade banding so you can skim the 80s without getting lost in 233 rows.
    if dec!=prev_dec:
        if prev_dec is not None:
            for ax in (axL,axR): ax.axhline(i-0.5,color=DEC,lw=1.2,alpha=0.8)
        fig.text(0.006,yfig(i),f'{dec}s',color=DEC,fontsize=17,fontweight='bold',va='center',ha='left')
        prev_dec=dec
    if i%2==0:
        for ax in (axL,axR): ax.axhspan(i-0.5,i+0.5,color=BAND,zorder=0)
    far=sy>SPLIT; col=FAR if far else NEAR
    # Far futures hop the split; The Time Machine (802,701) runs off with an arrow.
    if far:
        axL.plot([ry,SPLIT+12],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
        if sy>FARMAX:
            axR.plot([SPLIT,OFF],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
            axR.annotate('',xy=(OFF+260,i),xytext=(OFF-5,i),arrowprops=dict(arrowstyle='-|>',color=col,lw=2.5,mutation_scale=22))
            axR.text(2200,i-0.02,f'{sy:,} AD (off scale)   {yl(g)}',color=FG,fontsize=12.5,va='center',ha='left',
                     bbox=dict(boxstyle='round,pad=0.2',fc=BG,ec='none',alpha=0.9))
        else:
            axR.plot([SPLIT,sy],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
            axR.scatter([sy],[i],s=120,color=col,zorder=3,edgecolor=BG,lw=2)
            if sy>4600: axR.text(sy-60,i,f'{sy}  {yl(g)}',color=FG,fontsize=12.5,va='center',ha='right',zorder=4,bbox=dict(boxstyle='square,pad=0.1',fc=BAND if i%2==0 else BG,ec='none'))
            else: axR.text(sy+45,i,f'{sy}  {yl(g)}',color=FG,fontsize=12.5,va='center',ha='left')
    else:
        # The usual case — most films look about 34 years ahead (the median).
        axL.plot([ry,sy],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
        axL.scatter([sy],[i],s=120,color=col,zorder=3,edgecolor=BG,lw=2)
        lx,ha=(sy-3.5,'right') if sy>2100 else (sy+2.5,'left')
        axL.text(lx,i,f'{sy}  {yl(g)}',color=FG,fontsize=12.5,va='center',ha=ha,zorder=4,bbox=dict(boxstyle='square,pad=0.1',fc=BAND if i%2==0 else BG,ec='none'))
    # Fifteen streaming titles in the 233 — pink diamond, not a gold cinema dot.
    if r['release_type']=='streaming':
        axL.scatter([ry],[i],s=110,marker='D',facecolor=BG,edgecolor=STREAM,lw=2.2,zorder=3)
        axL.text(ry-14,i,'STREAM',color=BG,fontsize=10,fontweight='bold',va='center',ha='right',zorder=4,bbox=dict(boxstyle='round,pad=0.2',fc=STREAM,ec=STREAM))
    else: axL.scatter([ry],[i],s=100,color=REL,zorder=3,edgecolor=BG,lw=2)
    axL.text(ry-2,i,f'{ry}',color=STREAM if r['release_type']=='streaming' else REL,fontsize=12,va='center',ha='right')
    DRAWN.append(r['title'])
    tt=fig.text(0.2,yfig(i),title,color=AMB if amb else FG,fontsize=14,ha='right',va='center',fontweight='bold')
    b=None if r['title'].rstrip('*') in NOBADGE else badge_info(r['country'])
    if b:
        x0=tt.get_window_extent(RENDER).x0/fig.bbox.width-0.004
        if b[0]=='solid': fig.text(x0,yfig(i),b[1],color=BG,fontsize=11.5,fontweight='bold',ha='right',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BADGE,ec=BADGE))
        else: fig.text(x0,yfig(i),b[1],color=BADGE,fontsize=11.5,fontweight='bold',ha='right',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BG,ec=BADGE,lw=1.5))
fig.text(0.74,bot-0.32/H,'//',color=MUTED,fontsize=20,ha='center',va='center',fontweight='bold')
# Title and lede.
fig.text(0.03,1-0.65/H,"Roads? Where We're Going: the movies promised me flying cars, so I kept score",color=FG,fontsize=32,fontweight='bold')
fig.text(0.03,1-1.1/H,f'{n} films, at least one per release year where a sourced example exists. Each bar runs from release year to the year the film is set in, on humanity\'s current calendar.',color=MUTED,fontsize=16)
ly=0.5/H; x=0.03
for c,t in [(REL,'Release year'),(NEAR,'Setting year (near future)'),(FAR,'Setting year (far future)'),(AMB,'Title colour: year ambiguous*')]:
    fig.text(x,ly,'\u25CF',color=c,fontsize=18,va='center'); fig.text(x+0.012,ly,t,color=FG,fontsize=13,va='center'); x+=0.115
fig.text(0.03,ly+0.42/H,'JP',color=BG,fontsize=11.5,fontweight='bold',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BADGE,ec=BADGE))
fig.text(0.05,ly+0.42/H,'Made outside the UK/US (ISO country code; CS = Czechoslovakia, DD = East Germany, SU = Soviet Union)',color=FG,fontsize=13,va='center')
fig.text(0.485,ly+0.42/H,'KR',color=BADGE,fontsize=11.5,fontweight='bold',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BG,ec=BADGE,lw=1.5))
fig.text(0.505,ly+0.42/H,'Co-production with the UK/US, led by the country shown (first-listed)',color=FG,fontsize=13,va='center')
fig.text(0.03,ly+0.84/H,'STREAM',color=BG,fontsize=10,fontweight='bold',va='center',bbox=dict(boxstyle='round,pad=0.2',fc=STREAM,ec=STREAM))
fig.text(0.068,ly+0.84/H,'\u25C7',color=STREAM,fontsize=16,va='center',fontweight='bold')
fig.text(0.08,ly+0.84/H,'Streaming-first or streaming-only release (Netflix, Prime Video, digital/VOD); release marker drawn as a hollow diamond',color=FG,fontsize=13,va='center')
fig.text(0.97,ly,'* Ambiguous, derived, or not stated on screen; see films.csv notes. (short)/(serial) = not a single feature.\nSources: Wikipedia, AFI Catalog, BFI, SFE, EOFFTV, DEFA, Screen Rant, Smithsonian. October 2026.',
         color=MUTED,fontsize=12,ha='right',va='center')

def panel(x0,w,head,items,col,extra=None,mk='\u25CF'):
    # Bottom panels: findings and method. Copy lives in panels.py so the site can share it.
    y1=(PB+PH0)/H
    fig.patches.append(FancyBboxPatch((x0,PB/H),w,PH0/H,boxstyle='round,pad=0,rounding_size=0.004',transform=fig.transFigure,fc=BAND,ec=col,lw=1.6,zorder=0))
    fig.text(x0+0.012,y1-0.42/H,head,color=col,fontsize=20,fontweight='bold',va='center')
    y=y1-0.95/H
    for k,(a,b) in enumerate(items):
        L=textwrap.wrap(f'{a} {b}',WRAP)
        fig.text(x0+0.012,y,mk,color=col,fontsize=12,va='top')
        first=L[0]; bold=a if first.startswith(a) else ''
        t0=fig.text(x0+0.026,y,bold,color=FG,fontsize=15,fontweight='bold',va='top')
        wb=t0.get_window_extent(RENDER).width/fig.bbox.width if bold else 0
        fig.text(x0+0.026+wb,y,(' ' if bold else '')+first[len(bold):].lstrip(),color=FG,fontsize=15,va='top')
        for j,l in enumerate(L[1:]): fig.text(x0+0.026,y-(j+1)*LH/H,l,color=FG,fontsize=15,va='top')
        y-=(len(L)+0.45)*LH/H
    if extra:
        for j,l in enumerate(textwrap.wrap(extra,WRAP+4)): fig.text(x0+0.012,y-0.1/H-j*LH/H,l,color=MUTED,fontsize=13.5,va='top',style='italic')
panel(0.03,0.455,'What I found',FOUND,NEAR,'Headline films (near-misses as half): 2001: A Space Odyssey 35%, Blade Runner 39%, Back to the Future Part II 45% (unchanged). Full figures: stats_summary.md.')
panel(0.515,0.455,'How I did it',METHOD,REL,SOURCES,'\u25B8')
fig.savefig(RP('charts','timeline.png'),facecolor=BG); fig.savefig(RP('charts','timeline.pdf'),facecolor=BG)
print(fig.get_size_inches()*100)
import csv as _c
allt=[r['title'] for r in _c.DictReader(open(RP('data','films.csv'),encoding='utf-8'))]
# Quick sanity check — every CSV title should have been drawn.
print('csv rows',len(allt),'drawn',len(DRAWN),'missing',[t for t in allt if t not in DRAWN],'header n',n)
