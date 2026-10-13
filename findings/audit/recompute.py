import pandas as pd, numpy as np
from scipy import stats
f=pd.read_csv('films.csv'); p=pd.read_csv('predictions.csv')
S={'came true':1,'sort of':0.5,"didn't":0}
p['s']=p.verdict.map(S); assert p.s.notna().all()
print('films',len(f),'preds',len(p),'pred films',p.title.nunique())
f['gap_calc']=f.setting_year-f.release_year
print('gap mismatches',(f.gap_calc!=f.gap_years).sum())
print('median gap',f.gap_years.median(),'mean',f.gap_years.mean())
print('min',f.loc[f.gap_years.idxmin(),['title','gap_years']].tolist(),'max',f.loc[f.gap_years.idxmax(),['title','gap_years']].tolist())
past=f[f.setting_year<=2026]; print('past',len(past),len(past)/len(f))
print('past titles not in preds',set(past.title)-set(p.title),'pred titles not past',set(p.title)-set(past.title))
print(p.verdict.value_counts(), p.verdict.value_counts(normalize=True).round(4))
print('score',p.s.sum(),p.s.mean())
thinfilms=set(p[p.reason.str.contains('THIN',na=False)].title); print('thin films',len(thinfilms))
q=p[~p.title.isin(thinfilms)]; print('ex thin',len(q),q.verdict.value_counts().to_dict(),q.s.mean())
tone=f.set_index('title').tone; p['tone']=p.title.map(tone)
print(p.groupby('title').tone.first().value_counts())
p['dys']=p.tone=='dystopian'
for k,g in p.groupby('dys'): print('dys',k,g.title.nunique(),len(g),g.s.mean(), (g.s==1).sum())
a=p[p.dys]; b=p[~p.dys]
t=[[ (a.s==1).sum(), (a.s<1).sum()],[(b.s==1).sum(),(b.s<1).sum()]]
print('fisher true',stats.fisher_exact(t))
t2=[[ (a.s>0).sum(), (a.s==0).sum()],[(b.s>0).sum(),(b.s==0).sum()]]
print('fisher any',stats.fisher_exact(t2))
print(p.groupby('theme').s.agg(['mean','size']).sort_values('mean',ascending=False))
for t_ in ['2001: A Space Odyssey','Blade Runner','Back to the Future Part II']:
    g=p[p.title==t_]; print(t_,g.verdict.value_counts().to_dict(),g.s.mean())
f['dec']=(f.release_year//10)*10
d=f.groupby('dec').apply(lambda g:((g.tone=='dystopian').sum(),len(g)))
print(d)
fs=p.groupby('title').s.mean(); print('films at 0%',(fs==0).sum()); print(fs.sort_values(ascending=False).head(10))
