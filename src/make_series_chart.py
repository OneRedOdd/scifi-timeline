"""Draw the TV-series timeline (charts/series_timeline.png and .pdf) from data/series/series.csv."""
import os, sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
import csv, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
rows=sorted(csv.DictReader(open(RP('data','series','series.csv'),encoding='utf-8')),key=lambda r:(int(r['release_year']),int(r['setting_year'])))
BG='#0d1424'; FG='#e8ecf4'; MUTED='#8b97b0'; GRID='#1f2a40'; BAND='#121b30'
NEAR='#4fc3f7'; FAR='#ff8a65'; REL='#ffd54f'; AMB='#ce93d8'; DEC='#5c6b8a'; STREAM='#f06292'; BADGE='#26c6a6'
SPLIT=2125; NEARMIN=1950; FARMAX=4100
TX=0.245  # right edge of title column (figure fraction)
n=len(rows); RH=0.42
H=n*RH+4.8
fig=plt.figure(figsize=(24,H),dpi=100,facecolor=BG)
top=1-2.4/H; bot=2.3/H
axL=fig.add_axes([0.25,bot,0.49,top-bot],facecolor=BG)
axR=fig.add_axes([0.76,bot,0.215,top-bot],facecolor=BG,sharey=axL)
axL.set_xlim(NEARMIN,SPLIT+12); axR.set_xlim(SPLIT,FARMAX)
axL.set_ylim(n-0.4,-0.9)
for ax in (axL,axR):
    ax.tick_params(colors=MUTED,labelsize=13,labeltop=True,top=False)
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(axis='x',color=GRID,lw=1); ax.set_axisbelow(True)
    ax.tick_params(axis='y',left=False,labelleft=False)
axL.set_xticks(range(1960,2121,20)); axR.set_xticks([2500,3000,3500,4000])
axL.axvline(2026,color='#ffffff',lw=1.5,ls=(0,(4,4)),alpha=0.55)
axL.text(2028,-0.7,'Today (2026)',color=FG,ha='left',va='center',fontsize=12,alpha=0.9)
axL.set_title('Near future (to 2125)',color=NEAR,fontsize=16,pad=34,loc='left')
axR.set_title('Far future (compressed scale)',color=FAR,fontsize=16,pad=34,loc='left')
yfig=lambda i: axL.transData.transform((0,i))[1]/fig.bbox.height
ISO={'Japan':'JP','Canada':'CA','Germany':'DE','West Germany':'DE','France':'FR','Australia':'AU','Soviet Union':'SU','South Korea':'KR','Spain':'ES','Poland':'PL'}
UKUS=('United States','United Kingdom')
def badge_info(country):
    cs=[c.strip() for c in country.split(';')]
    base=[c for c in cs if not c.startswith(UKUS)]
    if not base: return None
    if len(base)==len(cs): return 'solid','/'.join(dict.fromkeys(ISO[c] for c in cs))
    if not cs[0].startswith(UKUS): return 'outline',ISO[cs[0]]
    return None
fig.canvas.draw(); RENDER=fig.canvas.get_renderer()
yl=lambda g: f'+{g:,} yr' if g==1 else f'+{g:,} yrs'
prev_dec=None
def tag(x,y,txt,kind):
    if kind=='solid': return fig.text(x,y,txt,color=BG,fontsize=11.5,fontweight='bold',ha='right',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BADGE,ec=BADGE))
    if kind=='outline': return fig.text(x,y,txt,color=BADGE,fontsize=11.5,fontweight='bold',ha='right',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BG,ec=BADGE,lw=1.5))
    return fig.text(x,y,txt,color=STREAM,fontsize=15,fontweight='bold',ha='right',va='center')
for i,r in enumerate(rows):
    ry,sy,g=int(r['release_year']),int(r['setting_year']),int(r['gap_years'])
    title=r['title']; amb=title.endswith('*')
    dec=ry//10*10
    if dec!=prev_dec:
        if prev_dec is not None:
            for ax in (axL,axR): ax.axhline(i-0.5,color=DEC,lw=1.2,alpha=0.8)
        fig.text(0.006,yfig(i),f'{dec}s',color=DEC,fontsize=17,fontweight='bold',va='center',ha='left')
        prev_dec=dec
    rowbg=BAND if i%2==0 else BG
    if i%2==0:
        for ax in (axL,axR): ax.axhspan(i-0.5,i+0.5,color=BAND,zorder=0)
    far=sy>SPLIT; col=FAR if far else NEAR
    if far:
        axL.plot([ry,SPLIT+12],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
        axR.plot([SPLIT,sy],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
        axR.scatter([sy],[i],s=120,color=col,zorder=3,edgecolor=BG,lw=2)
        lab=f'{sy}  {yl(g)}'
        if sy>3700: axR.text(sy-45,i,lab,color=FG,fontsize=12.5,va='center',ha='right',zorder=4,bbox=dict(boxstyle='square,pad=0.1',fc=rowbg,ec='none'))
        else: axR.text(sy+45,i,lab,color=FG,fontsize=12.5,va='center',ha='left')
    else:
        axL.plot([ry,sy],[i,i],color=col,lw=5,solid_capstyle='butt',alpha=0.9)
        axL.scatter([sy],[i],s=120,color=col,zorder=3,edgecolor=BG,lw=2)
        lab=f'{sy}  {yl(g)}'
        if sy>2100: axL.text(sy-2.5,i-0.33,lab,color=FG,fontsize=11,va='center',ha='right',zorder=4)
        else: axL.text(sy+2.5,i,lab,color=FG,fontsize=12.5,va='center',ha='left',zorder=4,bbox=dict(boxstyle='square,pad=0.1',fc=rowbg,ec='none'))
    axL.scatter([ry],[i],s=100,color=REL,zorder=3,edgecolor=BG,lw=2)
    axL.text(ry-1.2,i,f'{ry}',color=REL,fontsize=12,va='center',ha='right')
    tt=fig.text(TX,yfig(i),title,color=AMB if amb else FG,fontsize=14,ha='right',va='center',fontweight='bold')
    x0=tt.get_window_extent(RENDER).x0/fig.bbox.width-0.004
    b=badge_info(r['country'])
    if b:
        bt=tag(x0,yfig(i),b[1],b[0]); x0=bt.get_window_extent(RENDER).x0/fig.bbox.width-0.006
    if r['release_type']=='streaming':
        tag(x0,yfig(i),'\u25B6','stream')
fig.text(0.75,bot-0.32/H,'//',color=MUTED,fontsize=20,ha='center',va='center',fontweight='bold')
fig.text(0.03,1-0.65/H,'Tomorrow, on the small screen: sci-fi series and the futures they imagined',color=FG,fontsize=32,fontweight='bold')
fig.text(0.03,1-1.1/H,f'{n} TV and streaming series, 1962 to 2026. Each bar runs from the year a series (or the season shown) first aired to the year it is set in, on humanity\'s current calendar.',color=MUTED,fontsize=16)
ly=0.85/H; x=0.03
for c,t in [(REL,'First aired'),(NEAR,'Setting year (near future)'),(FAR,'Setting year (far future)'),(AMB,'Title colour: year ambiguous*')]:
    fig.text(x,ly,'\u25CF',color=c,fontsize=18,va='center'); fig.text(x+0.012,ly,t,color=FG,fontsize=13,va='center'); x+=0.115
x+=0.03; fig.text(x,ly,'\u25B6',color=STREAM,fontsize=15,fontweight='bold',va='center'); fig.text(x+0.012,ly,'Streaming-first release',color=FG,fontsize=13,va='center')
fig.text(0.03,ly+0.45/H,'JP',color=BG,fontsize=11.5,fontweight='bold',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BADGE,ec=BADGE))
fig.text(0.05,ly+0.45/H,'Made outside the UK/US (ISO country code; SU = Soviet Union)',color=FG,fontsize=13,va='center')
fig.text(0.36,ly+0.45/H,'CA',color=BADGE,fontsize=11.5,fontweight='bold',va='center',bbox=dict(boxstyle='round,pad=0.25',fc=BG,ec=BADGE,lw=1.5))
fig.text(0.38,ly+0.45/H,'Co-production with the UK/US, led by the country shown (first-listed)',color=FG,fontsize=13,va='center')
fig.text(0.03,0.3/H,'* Ambiguous, derived, framing-story only, or not stated on screen; see series.csv notes. Multi-year settings use the starting year.   Sources: Wikipedia (EN/JA/ES), SFE, Netflix Tudum, Collider, Business Insider and others.   Draft v1, October 2026.',
         color=MUTED,fontsize=12,ha='left',va='center')
fig.savefig(RP('charts','series_timeline.png'),facecolor=BG)
fig.savefig(RP('charts','series_timeline.pdf'),facecolor=BG)
print(fig.get_size_inches()*100)
