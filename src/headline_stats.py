"""Headline numbers (films, gaps, prediction scores, theme, tone) -> data/derived/stats.json."""
import os, sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
import csv,collections,statistics as st,json
from scipy.stats import fisher_exact
F=list(csv.DictReader(open(RP('data','films.csv'),encoding='utf-8'))); FT={r['title']:r for r in F}
P=[p for p in csv.DictReader(open(RP('data','predictions.csv'),encoding='utf-8')) if p['title'] in FT]
S=[p for p in P if p['scored']=='yes']
def sc(ps):
    n=len(ps); t=sum(p['verdict']=='came true' for p in ps); s=sum(p['verdict']=='sort of' for p in ps); return dict(n=n,t=t,s=s,d=n-t-s,pt=100*t/n if n else 0,ps=100*s/n if n else 0,h=100*(t+.5*s)/n if n else 0)
o={}
g=[int(r['gap_years']) for r in F]; past=[r for r in F if int(r['setting_year'])<=2026]
o['films']=len(F); o['past']=len(past); o['past_pct']=100*len(past)/len(F); o['median_gap']=st.median(g); o['mean_gap']=st.mean(g)
g2=[int(r['gap_years']) for r in F if r['title'] not in('The Time Machine*','Vampire Hunter D')]; o['median_gap_ex']=st.median(g2); o['mean_gap_ex']=st.mean(g2)
o['scored_films']=len({p['title'] for p in S}); o['all']=sc(S); o['raw_rows']=len(P); o['excluded']=collections.Counter(p['exclusion_reason'].split(':')[0].split(' (')[0] for p in P if p['scored']=='no')
thin={p['title'] for p in P if 'THIN' in p['reason']}; o['exthin']=sc([p for p in S if p['title'] not in thin]); o['thin_films']=len(thin)
th=collections.defaultdict(list)
for p in S: th[p['theme']].append(p)
o['theme']={k:sc(v) for k,v in sorted(th.items(),key=lambda kv:-sc(kv[1])['h'])}
o['theme_films']={k:len({p['title'] for p in v}) for k,v in th.items()}
for lab,fn in (('wiki',lambda t:FT[t]['tone']=='dystopian'),('strict',lambda t:FT[t]['tone_strict'].startswith('dystopian'))):
    d=[p for p in S if fn(p['title'])]; n=[p for p in S if not fn(p['title'])]
    tab=[[sum(p['verdict']=='came true' for p in d),sum(p['verdict']!='came true' for p in d)],[sum(p['verdict']=='came true' for p in n),sum(p['verdict']!='came true' for p in n)]]
    o['tone_'+lab]=dict(dys=sc(d),non=sc(n),dys_films=len({p['title'] for p in d}),non_films=len({p['title'] for p in n}),fisher_p=fisher_exact(tab)[1],OR=fisher_exact(tab)[0])
fs=collections.defaultdict(list)
for p in S: fs[p['title']].append(p)
o['film_equal']=st.mean(sc(v)['h'] for v in fs.values())
o['headline']={t:sc(fs[t]) for t in ['2001: A Space Odyssey','Blade Runner','Back to the Future Part II']}
rank=sorted(((sc(v)['h'],sc(v)['n'],t) for t,v in fs.items()),reverse=True); o['top']=rank[:8]; o['zero']=[t for h,n,t in rank if h==0]
o['nopreds_scored']=[r['title'] for r in past if r['title'] not in fs]
o['hits']=[(p['title'],p['prediction']) for p in S if p['verdict']=='came true']
o['tone_counts']=collections.Counter(r['tone'] for r in F); o['strict_counts']=collections.Counter(r['tone_strict'] for r in F)
print(json.dumps(o,indent=1,default=str)); json.dump(o,open(RP('data','derived','stats.json'),'w'),default=str)
