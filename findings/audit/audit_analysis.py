import pandas as pd, numpy as np, warnings
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
warnings.filterwarnings('ignore')
rng=np.random.default_rng(2026)
f=pd.read_csv('films.csv'); p=pd.read_csv('predictions.csv')
S={'came true':1,'sort of':0.5,"didn't":0}
p['row']=p.index
# ---------- audit verdict changes (rule: judge vs setting year; consistency) ----------
changes={12:("didn't","Federal Europe did not exist by 1940 (EU later); 'arriving later = didn't' rule"),
         39:("didn't","Judged vs 1984: no home telescreens in 1984; reason cites later smart devices"),
         53:("didn't","Reason itself says it came later (ISS 1998) than 1965; rule says didn't"),
         155:("didn't","Self-lacing shoes arrived 2016, after 2015; rule says didn't (or score every 'a bit late' item sort of, consistently)"),
         13:("came true","Consistency with Men Must Fight row 18: a world war did break out by 1940")}
p['verdict_audit']=p.verdict
for k,(v,_) in changes.items(): p.loc[k,'verdict_audit']=v
p['audit_change_reason']=''
for k,(_,r) in changes.items(): p.loc[k,'audit_change_reason']=r
# premise items: depend on time travel, aliens/ET life, monsters/supernatural/psychic, alt-history
premise=[37,44,47,54,57,63,64,81,82,88,104,108,132,133,138,144,147,159,164,165,173,174,192,193,194,195,196,208,213,217,219,222,223]
# already existed / in use at release -> not a forecast
existed={1:"First US woman mayor 1887 (Susanna Salter) - before the 1910 film",
 49:"USS Nautilus 1954, before 1959 film (reason already says so)",
 77:"Archive-compilation TV documentaries existed by 1969",
 106:"Crewed Salyut stations from 1971, before the 1977 film",
 191:"ISS assembly began 1998; first crew Nov 2000, months after the film",
 212:"US medical debt/bankruptcy widely documented before 2010 (e.g. Himmelstein et al. 2009)",
 221:"CBP has flown Predator B drones on the border since 2005; film released 2019 set 2020",
 169:"Private prisons (CCA, 1983) existed before 1992",
 202:"Private prisons existed before 2008"}
p['flag_premise']=p.row.isin(premise)
p['flag_existed_at_release']=p.row.isin(existed.keys())
p['existed_note']=p.row.map(existed).fillna('')
p['thin_film']=p.title.isin(set(p[p.reason.str.contains('THIN',na=False)].title))
p['s']=p.verdict.map(S); p['sa']=p.verdict_audit.map(S)
f2=f.set_index('title')
p['gap']=p.setting_year-p.release_year
p['decade']=(p.release_year//10)*10
p['tone_wiki']=p.title.map(f2.tone)
strict_D={'Metropolis*','1984','On the Beach','Beyond the Time Barrier','The Last Man on Earth','Crimes of the Future',
 'The Omega Man','Conquest of the Planet of the Apes','Soylent Green','Death Race 2000','Rollerball*','A Boy and His Dog',
 'The Apple','Escape from New York','Blade Runner','2019, After the Fall of New York','The Running Man','Cherry 2000','Akira',
 'Freejack','Fortress','Johnny Mnemonic','Escape from L.A.','The Postman','2009: Lost Memories','Reign of Fire','The Island',
 'I Am Legend','Death Race','Terminator Salvation','Daybreakers','Repo Men','Dawn of the Planet of the Apes'}
borderline={'Strange Days':'N','Repo Men':'D','On the Beach':'D','The Apple':'D','Rollerball*':'D','Time of Roses':'N'}
p['dys_wiki']=p.tone_wiki=='dystopian'
p['dys_strict']=p.title.isin(strict_D)
p.drop(columns=['s','sa']).to_csv('predictions_audit.csv',index=False)
fa=f.copy(); fa['tone_strict']=np.where(fa.title.isin(strict_D),'dystopian',np.where(fa.title.isin(p.title),'not dystopian (strict)',''))
fa['tone_strict_borderline']=fa.title.map(borderline).fillna('')
fa.to_csv('films_audit.csv',index=False)

out=[]
def P(*a): s=' '.join(str(x) for x in a); print(s); out.append(s)
def rate(d,col='s'): return f"{d[col].mean()*100:.1f}% (n={len(d)}; true {(d[col]==1).sum()}, sort {(d[col]==0.5).sum()})"
P('## Overall variants')
P('A as published:',rate(p))
P('B audit verdicts:',rate(p,'sa'))
c=p[~p.flag_premise]; P('C B minus premise items:',rate(c,'sa'))
d=c[~c.flag_existed_at_release]; P('D C minus already-existed:',rate(d,'sa'))
P('E D minus thin films:',rate(d[~d.thin_film],'sa'))
P('strict came-true only (D):',f"{(d.sa==1).mean()*100:.1f}%")
P('Film-equal-weight mean, A:',f"{p.groupby('title').s.mean().mean()*100:.1f}%",' D:',f"{d.groupby('title').sa.mean().mean()*100:.1f}%")

def tone_tests(df,col,dys,label):
    a=df[df[dys]]; b=df[~df[dys]]
    fl=df.groupby('title').agg(sc=(col,'mean'),dy=(dys,'first'))
    # permutation on film-level difference
    obs=fl[fl.dy].sc.mean()-fl[~fl.dy].sc.mean()
    perm=[]; arr=fl.sc.values; lab=fl.dy.values
    for _ in range(10000):
        l=rng.permutation(lab); perm.append(arr[l].mean()-arr[~l].mean())
    pp=(np.abs(perm)>=abs(obs)).mean()
    t=[[(a[col]==1).sum(),(a[col]<1).sum()],[(b[col]==1).sum(),(b[col]<1).sum()]]
    fp=stats.fisher_exact(t)[1]
    mw=stats.mannwhitneyu(fl[fl.dy].sc,fl[~fl.dy].sc).pvalue
    # GEE binomial on fractional score, clustered by film, with theme FE
    try:
        g=smf.gee(f'{col} ~ C({dys}) + C(theme)',groups='title',data=df.assign(**{dys:df[dys].astype(int)}),family=sm.families.Binomial()).fit()
        k=[x for x in g.params.index if dys in x][0]; gee=f"OR {np.exp(g.params[k]):.2f}, p={g.pvalues[k]:.2f}"
    except Exception as e: gee=f'err {e}'
    P(f"{label}: dys films {fl.dy.sum()} / preds {len(a)} score {a[col].mean()*100:.1f}% | non {(~fl.dy).sum()} / {len(b)} {b[col].mean()*100:.1f}% | Fisher(true) p={fp:.2f} | film-level means {fl[fl.dy].sc.mean()*100:.1f}% vs {fl[~fl.dy].sc.mean()*100:.1f}%, MW p={mw:.2f}, perm p={pp:.2f} | GEE theme-adjusted dys {gee}")
P('\n## Tone vs accuracy')
heads=['2001: A Space Odyssey','Blade Runner','Back to the Future Part II']
for dys in ['dys_wiki','dys_strict']:
    tone_tests(p,'s',dys,f'{dys} published verdicts, all')
    tone_tests(p,'sa',dys,f'{dys} audit verdicts, all')
    tone_tests(d,'sa',dys,f'{dys} audit, ex premise+existed')
    tone_tests(p[~p.thin_film],'s',dys,f'{dys} published, ex THIN films')
    tone_tests(p[~p.title.isin(heads)],'s',dys,f'{dys} published, ex 3 headline films')
    tone_tests(d[~d.thin_film & ~d.title.isin(heads)],'sa',dys,f'{dys} audit, ex premise/existed/THIN/headline')
P('\n## Theme table (published) + omnibus + Holm')
th=p.groupby('theme').s.agg(['mean','size'])
P(th.sort_values('mean',ascending=False).round(3).to_string())
ct=pd.crosstab(p.theme,p.verdict); chi=stats.chi2_contingency(ct); P('chi2 theme x verdict p=',f"{chi[1]:.2g}")
pv=[]
for t_ in th.index:
    x=p[p.theme==t_]; y=p[p.theme!=t_]
    pv.append((t_,stats.mannwhitneyu(x.s,y.s).pvalue))
from statsmodels.stats.multitest import multipletests
rej,adj,_,_=multipletests([v for _,v in pv],method='holm')
for (t_,v),a_,r in zip(pv,adj,rej): P(f"{t_}: raw p={v:.3g}, Holm p={a_:.3g}, {'sig' if r else 'ns'}")
P('Theme table after audit (D set):'); P(d.groupby('theme').sa.agg(['mean','size']).sort_values('mean',ascending=False).round(3).to_string())
P('communication films:',p[p.theme=='communication'].title.nunique(),'| share of comm preds from 3 headline films:',(p[p.theme=='communication'].title.isin(heads)).mean().round(2))
P('\n## Gap length / decade vs accuracy')
fl=p.groupby('title').agg(sc=('s','mean'),gap=('gap','first'),rel=('release_year','first'),n=('s','size'))
r=stats.spearmanr(fl.gap,fl.sc); P(f"film-level Spearman gap vs score rho={r.statistic:.2f} p={r.pvalue:.2f} (n={len(fl)})")
r=stats.spearmanr(fl.rel,fl.sc); P(f"film-level Spearman release year vs score rho={r.statistic:.2f} p={r.pvalue:.2f}")
fl['gb']=pd.cut(fl.gap,[0,10,20,30,200],labels=['1-10','11-20','21-30','31+'])
P(fl.groupby('gb').agg(films=('sc','size'),mean_score=('sc','mean')).round(3).to_string())
p['gb']=pd.cut(p.gap,[0,10,20,30,200],labels=['1-10','11-20','21-30','31+'])
P('prediction-level by gap band (published):'); P(p.groupby('gb').s.agg(['mean','size']).round(3).to_string())
dd=d.copy(); dd['gb']=pd.cut(dd.gap,[0,10,20,30,200],labels=['1-10','11-20','21-30','31+'])
P('prediction-level by gap band (audit D):'); P(dd.groupby('gb').sa.agg(['mean','size']).round(3).to_string())
g=smf.gee('s ~ np.log(gap) + C(theme)',groups='title',data=p,family=sm.families.Binomial()).fit()
P(f"GEE s ~ log(gap)+theme: OR per e-fold gap {np.exp(g.params['np.log(gap)']):.2f}, p={g.pvalues['np.log(gap)']:.2f}")
g=smf.gee('s ~ np.log(gap)',groups='title',data=p,family=sm.families.Binomial()).fit()
P(f"GEE s ~ log(gap): OR {np.exp(g.params['np.log(gap)']):.2f}, p={g.pvalues['np.log(gap)']:.2f}")
P('max gap among scored films:',p.gap.max(),'| median gap scored films:',fl.gap.median(),'vs all 164:',f.gap_years.median())
P('decade (published):'); P(p.groupby('decade').agg(films=('title','nunique'),preds=('s','size'),score=('s','mean')).round(3).to_string())
P('theme mix by strict tone:'); P(pd.crosstab(p.theme,p.dys_strict).to_string())
P('preds per film: mean',fl.n.mean().round(2),'min',fl.n.min(),'max',fl.n.max())
open('audit/analysis_output.txt','w').write('\n'.join(out))
