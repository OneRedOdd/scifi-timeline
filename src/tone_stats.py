"""Tone vs accuracy tests (Fisher, Mann-Whitney, permutation, GEE) -> data/derived/tone.json. Needs statsmodels."""
import os, sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP=lambda *a: os.path.join(REPO,*a)
import pandas as pd, numpy as np, json, warnings
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
warnings.filterwarnings('ignore'); rng=np.random.default_rng(2026)
F=pd.read_csv(RP('data','films.csv'),keep_default_na=False); P=pd.read_csv(RP('data','predictions.csv'),keep_default_na=False)
P=P[(P.scored=='yes')&P.title.isin(F.title)].copy()
P['s']=P.verdict.map({'came true':1,'sort of':.5,"didn't":0})
ft=F.set_index('title'); P['wiki']=P.title.map(ft.tone)=='dystopian'; P['strict']=P.title.map(ft.tone_strict).str.startswith('dystopian')
thin=set(pd.read_csv(RP('data','predictions.csv'),keep_default_na=False).query("reason.str.contains('THIN')",engine='python').title)
heads=['2001: A Space Odyssey','Blade Runner','Back to the Future Part II']
O={}
def test(df,col):
    a=df[df[col]]; b=df[~df[col]]
    fl=df.groupby('title').agg(sc=('s','mean'),dy=(col,'first'))
    obs=fl[fl.dy].sc.mean()-fl[~fl.dy].sc.mean(); arr=fl.sc.values; lab=fl.dy.values
    perm=np.array([ (lambda l: arr[l].mean()-arr[~l].mean())(rng.permutation(lab)) for _ in range(10000)])
    t=[[(a.s==1).sum(),(a.s<1).sum()],[(b.s==1).sum(),(b.s<1).sum()]]; fo,fp=stats.fisher_exact(t)
    g=smf.gee(f's ~ dy + C(theme)',groups='title',data=df.assign(dy=df[col].astype(int)),family=sm.families.Binomial()).fit()
    return dict(dys_films=int(fl.dy.sum()),non_films=int((~fl.dy).sum()),dys_n=len(a),non_n=len(b),dys_true=100*(a.s==1).mean(),non_true=100*(b.s==1).mean(),
        dys=100*a.s.mean(),non=100*b.s.mean(),fisher_p=fp,OR=fo,film_dys=100*fl[fl.dy].sc.mean(),film_non=100*fl[~fl.dy].sc.mean(),
        mw_p=stats.mannwhitneyu(fl[fl.dy].sc,fl[~fl.dy].sc).pvalue,perm_p=float((np.abs(perm)>=abs(obs)).mean()),
        gee_OR=float(np.exp(g.params['dy'])),gee_p=float(g.pvalues['dy']))
for col in ['wiki','strict']:
    O[col]={'all':test(P,col),'ex_thin':test(P[~P.title.isin(thin)],col),'ex_headline':test(P[~P.title.isin(heads)],col)}
O['theme_strict']={t:dict(dys=100*g[g.strict].s.mean() if g.strict.any() else None,dn=int(g.strict.sum()),non=100*g[~g.strict].s.mean() if (~g.strict).any() else None,nn=int((~g.strict).sum()),all=100*g.s.mean(),n=len(g)) for t,g in P.groupby('theme')}
F['dec']=(F.release_year.astype(int)//10)*10
O['decade']={int(d):dict(n=len(g),wiki=int((g.tone=='dystopian').sum()),strict=int(g.tone_strict.str.startswith('dystopian').sum())) for d,g in F.groupby('dec')}
O['counts_wiki']=F.tone.value_counts().to_dict(); O['counts_strict']=F.tone_strict.value_counts().to_dict()
O['agree']=dict(both=int(((F.tone=='dystopian')&F.tone_strict.str.startswith('dyst')).sum()),wiki_only=int(((F.tone=='dystopian')&~F.tone_strict.str.startswith('dyst')).sum()),strict_only=int(((F.tone!='dystopian')&F.tone_strict.str.startswith('dyst')).sum()))
# trend test: share dystopian vs release year (logistic) for films released 1950+
for col,fn in [('wiki',lambda d:(d.tone=='dystopian')),('strict',lambda d:d.tone_strict.str.startswith('dyst'))]:
    d=F.assign(y=fn(F).astype(int),yr=F.release_year.astype(int)); d=d[d.yr>=1950]
    m=smf.logit('y ~ yr',d).fit(disp=0); O[f'trend_{col}']=dict(OR_per_decade=float(np.exp(10*m.params['yr'])),p=float(m.pvalues['yr']),n=len(d))
json.dump(O,open(RP('data','derived','tone.json'),'w'),indent=1,default=float)
print(json.dumps(O,indent=1,default=float))
