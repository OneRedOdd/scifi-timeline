"""Build the static GitHub Pages site in docs/ (no build step is needed on GitHub: the output is committed).

Copies data, charts and the paper into docs/, writes every page, and renders paper/paper.md to docs/paper.html.
Run after changing data or charts:  python src/build_site.py   (needs the 'markdown' package)
All links are relative, so the site works at https://OneRedOdd.github.io/<repo>/.
"""
import os, re, json, shutil, html, csv
import markdown

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = lambda *a: os.path.join(REPO, *a)
D = RP('docs')
REPO_URL = 'https://github.com/OneRedOdd/scifi-timeline'  # replaced at push time if desired; only used in text
S = json.load(open(RP('data', 'derived', 'stats.json')))
T = json.load(open(RP('data', 'derived', 'tone.json')))

# ---------- copy assets ----------
COPY = {
    'data': ['data/films.csv', 'data/predictions.csv', 'data/alt_history_candidates.csv', 'data/rejected_candidates.csv',
             'data/series/series.csv', 'data/wythoff_leane/match_mine_vs_wl.csv', 'data/wythoff_leane/add_candidates_shortlist.csv',
             'data/README.md'],
    'charts': ['charts/' + f for f in sorted(os.listdir(RP('charts')))],
    'paper': ['paper/paper.md', 'paper/paper.docx', 'paper/paper.pdf'],
    'paper/figures': ['paper/figures/' + f for f in sorted(os.listdir(RP('paper', 'figures')))] if os.path.isdir(RP('paper', 'figures')) else [],
    'findings': ['findings/' + f for f in ['stats_summary.md', 'tone_analysis.md', 'audit_findings.md', 'audit_findings_v2.md', 'literature.md']] + ['findings/wythoff_leane/findings.md'],
}
for dst, files in COPY.items():
    os.makedirs(os.path.join(D, dst), exist_ok=True)
    for f in files:
        if not os.path.exists(RP(f)):
            continue
        name = 'wythoff_leane_findings.md' if f.endswith('wythoff_leane/findings.md') else os.path.basename(f)
        shutil.copy2(RP(f), os.path.join(D, dst, name))
open(os.path.join(D, '.nojekyll'), 'w').close()

# The site flattens data/ into docs/data/, so rewrite the codebook's paths to match what is published there.
GH_DATA = 'https://github.com/OneRedOdd/scifi-timeline/tree/main/data'
cb_path = os.path.join(D, 'data', 'README.md')
cb = open(cb_path, encoding='utf-8').read()
for a, b in [
    ("excerpts in `wythoff_leane/`", "excerpts in `match_mine_vs_wl.csv` and `add_candidates_shortlist.csv`"),
    ('`series/series.csv`', '`series.csv`'),
    ('`wythoff_leane/match_mine_vs_wl.csv`', '`match_mine_vs_wl.csv`'),
    ('`wythoff_leane/add_candidates_shortlist.csv`', '`add_candidates_shortlist.csv`'),
]:
    cb = cb.replace(a, b)
cb = re.sub(r'^(\| `(?:series/series_dropped\.md|wythoff_leane/my_films_snapshot\.csv|derived/[^`]+)` \|[^|]*\| )(.*) \|$',
            r'\1\2 (repository only, not on the site) |', cb, flags=re.M)
cb = cb.replace('| File | Rows | What it is |',
    f'On this site every published file sits directly in `data/`. Files marked "repository only" (including everything in `derived/`) are in the [GitHub repository]({GH_DATA}) but are not published on the site.\n\n| File | Rows | What it is |', 1)
open(cb_path, 'w', encoding='utf-8').write(cb)
HAVE_PAPER = os.path.exists(RP('paper', 'paper.md'))

NAV = [('index.html', 'Home'), ('films.html', 'Films'), ('predictions.html', 'Predictions'), ('series.html', 'TV series'),
       ('alt-history.html', 'Alt history'), ('comparison.html', 'Wythoff &amp; Leane'), ('methodology.html', 'Methodology'),
       ('paper.html', 'Paper'), ('downloads.html', 'Downloads')]

def page(fn, title, body, wide=False, js=False, scripts=(), desc='A sourced timeline of 233 science fiction films and the futures they predicted.'):
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == fn else ""}>{t}</a>' for h, t in NAV)
    out = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Roads? Where We&#x27;re Going</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="dark">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site"><div class="wrap"><a class="brand" href="index.html">Roads? Where We&#x27;re Going</a><nav>{nav}</nav></div></header>
<main class="wrap{' wide' if wide else ''}">
{body}
</main>
<footer class="site"><div class="wrap">Andi Sharkey, 2026. Data and text <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; code MIT.
Comparison data: Wythoff &amp; Leane (2025), Post45 Data Collective, <a href="https://doi.org/10.18737/552626">doi:10.18737/552626</a> (CC BY 4.0).</div></footer>
{'<script src="assets/table.js"></script>' if js else ''}{''.join(f'<script src="assets/{x}"></script>' for x in scripts)}
</body>
</html>
'''
    open(os.path.join(D, fn), 'w', encoding='utf-8').write(out)

a = S['all']; pct = lambda x: f'{x:.1f}%'
comm = S['theme']['communication']['h']; tw = T['wiki']['all']; ts = T['strict']['all']
films = list(csv.DictReader(open(RP('data', 'films.csv'), encoding='utf-8')))
n_flag = sum(r['title'].endswith('*') for r in films); n_stream = sum(r['release_type'] == 'streaming' for r in films)

FLY = 'paper.html#82-wheres-my-flying-car-function-versus-form'

CAVEATS = f'''<div class="caveat"><strong>Before you quote any of this</strong>
<ul>
<li>These are well-known films that name a year, not a random sample of science fiction. So nothing here means "science fiction gets X% right".</li>
<li>I did the scoring myself and checked my work twice. There's no second scorer, though, so there's no inter-rater reliability statistic.</li>
<li>Gap vs accuracy: films set further ahead did score slightly better, but that largely fades once you account for the theme of the prediction (audit v1, 164-film version; I haven't rerun it on 233 yet). So it's not "no link", but it's not evidence that looking further ahead makes a film more accurate either.</li>
<li>"Dystopias are rising" only holds on Wikipedia's fairly generous labels (p = {T['trend_wiki']['p']:.3f}). On the stricter on-screen rule the trend isn't significant (p = {T['trend_strict']['p']:.2f}).</li>
<li>Most theme and tone groups have fewer than 30 predictions, so I wouldn't read much into the small ones.</li>
</ul></div>'''

# ---------- index ----------
page('index.html', 'Home', f'''
<h1>Roads? Where We&#x27;re Going: the movies promised me flying cars, so I kept score</h1>
<p class="lede">I built this timeline by hand. It covers {S['films']} released science fiction films (1910–2026) that set their story in a named future year on humanity's current calendar, each with a sourced setting year. Then, for the films whose future has already arrived, I checked what they actually got right. It's a personal project, by Andi Sharkey, October 2026.</p>
<p>A spare-time project I've been mulling since 2015, built up in spreadsheets and published here in 2026.</p>
<div class="cards">
<div class="card"><div class="num">{S['films']}</div><div class="lbl">films, all with a sourced setting year ({n_flag} flagged as ambiguous)</div></div>
<div class="card"><div class="num">{S['median_gap']:g} yrs</div><div class="lbl">is the median jump from release year to setting year</div></div>
<div class="card"><div class="num">{S['past']} ({S['past_pct']:.0f}%)</div><div class="lbl">are set in a year that's already arrived (2026 or earlier)</div></div>
<div class="card"><div class="num">{pct(a['h'])}</div><div class="lbl">of the {a['n']} predictions I scored came true, if near-misses count as half. About 1 in 5</div></div>
<div class="card"><div class="num">{pct(a['pt'])}</div><div class="lbl">came true outright. More like 1 in 9</div></div>
<div class="card"><div class="num">{comm:.1f}%</div><div class="lbl">for communication tech, like video calls, flat screens and voice control</div></div>
</div>
<h2>The question</h2>
<p>When film-makers put a date on the future, how far ahead do they look? And when that year finally turns up, how much of what they put on screen actually happened? That's really all I wanted to know.</p>
<h2>What I found</h2>
<p>The short version: about 1 in 5 predictions came true if you count near-misses as half ({pct(a['h'])} of {a['n']}). Only about 1 in 9 came true outright ({pct(a['pt'])}).</p>
<p>Communication tech was miles ahead of everything else, at {comm:.1f}%. Society and politics ({S['theme']['society/politics']['h']:.0f}%) and transport ({S['theme']['transport']['h']:.1f}%, from only {S['theme']['transport']['n']} forecasts) did worst.</p>
<p>Which brings me to the question everyone asks: where's my flying car? Every flying-car forecast I scored is a miss. To be fair, eVTOL air taxis do fly today, but they're still pre-production. It's a good example of a future turning up early as a demo and then stalling. There's more on that, and on films getting the function right but the form wrong, in the paper's <a href="{FLY}">"Where's my flying car?"</a> section.</p>
<p>Films did a fair bit better on gadgets than on catastrophes. Only 2 of 42 plagues, wars, collapses and police states actually happened, and both of those were a second world war, foreseen between the wars.</p>
<p>And the bleak futures weren't any better as guides. With Wikipedia's labels, dystopian films scored {tw['dys']:.1f}% against {tw['non']:.1f}% for the rest (Fisher p = {tw['fisher_p']:.2f}). With the stricter on-screen labels it's {ts['dys']:.1f}% against {ts['non']:.1f}% (p = {ts['fisher_p']:.2f}). No significant link either way.</p>
<p>So if I had to sum it up in one line: films are good at guessing our gadgets and bad at guessing our fate.</p>
{CAVEATS}
<h2>The timeline</h2>
<p>Hover over (or tap) a bar for the years, and click it, or press Enter, for the film's source note. You can filter by decade and sort by gap. The static version is still there if you'd rather have it.</p>
<p><a class="btn" href="charts/timeline.pdf">Open the full chart (PDF)</a><a class="btn" href="charts/timeline.png">Full-size PNG</a><a class="btn" href="films.html">Browse the films table</a></p>
<figure>
<div id="itl" class="itl" data-src="data/films.csv"><noscript><p>The interactive chart needs JavaScript. Here's the static one instead.</p></noscript></div>
<noscript><img src="charts/timeline.png" alt="Timeline infographic: one bar per film from release year to setting year, 233 films from 1910 to 2026, near futures on a linear scale and far futures on a compressed scale, with findings and method panels at the bottom." loading="lazy" width="2400" height="10948"></noscript>
<figcaption>Each bar runs from a film's release year (yellow) to the year it's set in. Blue is the near future, up to 2125. Orange is the far future, squashed onto a compressed scale. Lilac titles with an asterisk have an ambiguous or off-screen year. The badges mark films made outside the UK and US, and the pink diamonds are streaming releases.</figcaption></figure>
<h2>Related work</h2>
<p>I'm not the first to have a go at this. These are the three I'd point you to:</p>
<ul>
<li>Wythoff, G. &amp; Leane, T. (2025). <a href="https://data.post45.org/posts/futuristic-fiction/"><em>Time Horizons of Futuristic Fiction</em></a>. Post45 Data Collective. <a href="https://doi.org/10.18737/552626">doi:10.18737/552626</a>. I compare my list with theirs <a href="comparison.html">here</a>.</li>
<li>Xu, W. et al. (2021). Quantifying the Predictive Abilities of Speculative Fiction: A Feasibility Study. ASME IDETC/CIE 2021. <a href="https://doi.org/10.1115/DETC2021-68723">doi:10.1115/DETC2021-68723</a>.</li>
<li>Chang, A. (2024). <a href="https://pudding.cool/2024/07/scifi/">Who killed the world?</a> <em>The Pudding</em>.</li>
</ul>
<p>There's a longer list of 20 items in <a href="findings/literature.md">literature.md</a>.</p>
''', scripts=('timeline.js',))

# ---------- films ----------
page('films.html', 'Films', f'''
<h1>The {S['films']} films</h1>
<p class="lede">Here's every film, with its release year, setting year, gap and source. Click a column heading to sort, or use the search box and drop-downs to narrow it down. Lilac titles with an asterisk have a setting year that's ambiguous, derived or only given off screen. The notes say why.</p>
<p><a href="data/films.csv">Download films.csv</a> · <a href="data/README.md">Codebook</a></p>
<div class="csvtable" data-src="data/films.csv" data-cols="title,release_year,setting_year,gap_years,format,release_type,country,director,tone,tone_strict,source_url,notes"
 data-filters="format,release_type,tone,tone_strict" data-num="release_year,setting_year,gap_years" data-long="notes" data-sort="release_year"></div>
''', wide=True, js=True)

# ---------- predictions ----------
rows = ''.join(f'<tr><td>{html.escape(k)}</td><td class="num">{v["n"]}</td><td class="num">{S["theme_films"][k]}</td><td class="num">{v["pt"]:.0f}%</td><td class="num">{v["h"]:.1f}%</td></tr>' for k, v in S['theme'].items())
hl = ''.join(f'<tr><td>{html.escape(k)}</td><td class="num">{v["t"]}</td><td class="num">{v["s"]}</td><td class="num">{v["d"]}</td><td class="num">{v["h"]:.0f}%</td></tr>' for k, v in S['headline'].items())
page('predictions.html', 'Predictions', f'''
<h1>Predictions: what came true?</h1>
<p class="lede">For the {S['past']} films whose setting year has already come round, I picked out the main on-screen technology and society forecasts. Each one is scored <span class="v-true">came true</span>, <span class="v-sort">sort of</span> or <span class="v-no">didn't</span>, judged by the film's own year. That's {S['raw_rows']} rows, and {a['n']} of them are scored. The rest are left out because they're plot devices, or because the thing already existed when the film came out.</p>
<div class="cards">
<div class="card"><div class="num">{a['t']}</div><div class="lbl">came true ({pct(a['pt'])})</div></div>
<div class="card"><div class="num">{a['s']}</div><div class="lbl">sort of ({pct(a['ps'])})</div></div>
<div class="card"><div class="num">{a['d']}</div><div class="lbl">didn't ({100*a['d']/a['n']:.1f}%)</div></div>
<div class="card"><div class="num">{pct(a['h'])}</div><div class="lbl">score, with sort of counting as half</div></div>
</div>
<h2>By theme</h2>
<table><thead><tr><th>Theme</th><th>Predictions</th><th>Films</th><th>Came true</th><th>Score (sort of = half)</th></tr></thead><tbody>{rows}</tbody></table>
<p class="count">Only communication stands out once you correct for multiple comparisons. Below that the ranking is mostly noise, so I wouldn't lean on it.</p>
<p>And if you're wondering where your flying car is: every flying-car forecast I scored is a miss. There's a bit more on that in the paper's <a href="{FLY}">"Where's my flying car?"</a> section.</p>
<h2>Headline films</h2>
<table><thead><tr><th>Film</th><th>Came true</th><th>Sort of</th><th>Didn't</th><th>Score</th></tr></thead><tbody>{hl}</tbody></table>
<h2>Did a bleak future make a better guess?</h2>
<figure><img src="charts/tone_vs_accuracy.png" alt="Chart comparing prediction scores of dystopian and non-dystopian films under Wikipedia and strict labels, and the dystopian share by decade." loading="lazy"><figcaption>Not really. Tone made no significant difference to accuracy under either labelling rule. The details are in <a href="findings/tone_analysis.md">tone_analysis.md</a>.</figcaption></figure>
{CAVEATS}
<h2>Every prediction row</h2>
<p><a href="data/predictions.csv">Download predictions.csv</a></p>
<div class="csvtable" data-src="data/predictions.csv" data-cols="title,release_year,setting_year,theme,prediction,verdict,scored,exclusion_reason,reason,audit_note,source_url"
 data-filters="theme,verdict,scored" data-num="release_year,setting_year" data-long="prediction,reason" data-sort="release_year"></div>
''', wide=True, js=True)

# ---------- series ----------
page('series.html', 'TV series', '''
<h1>TV series (set aside)</h1>
<p class="lede">I collected 94 television series set in a named future year alongside the films, but kept them out of the film analysis. I haven't scored them. They could be scored the same way later, if I get round to it.</p>
<p><a class="btn" href="charts/series_timeline.pdf">Series chart (PDF)</a><a class="btn" href="data/series.csv">Download series.csv</a></p>
<figure><img src="charts/series_timeline.png" alt="Timeline chart of 94 TV series from premiere year to setting year." loading="lazy"></figure>
<div class="csvtable" data-src="data/series.csv" data-cols="title,release_year,setting_year,gap_years,country,network_platform,release_type,source_url,notes"
 data-filters="release_type" data-num="release_year,setting_year,gap_years" data-long="notes" data-sort="release_year"></div>
''', wide=True, js=True)

# ---------- alt history ----------
page('alt-history.html', 'Alternate history', '''
<h1>Alternate history (set aside)</h1>
<p class="lede">Films whose world breaks away from real history before they came out fail my "real timeline" rule. So they're not in the 233. I've parked them to look at later.</p>
<p>So far only one film has been moved out: <em>2009: Lost Memories</em> (2002), where Korea is still under Imperial Japanese rule in 2009 after a 1909 assassination goes differently. It came out when I first checked my work. Its two prediction rows are still in <code>predictions.csv</code>, marked unscored. The plan for the follow-on is a chart of the real year each story breaks from history.</p>
<p><a href="data/alt_history_candidates.csv">Download alt_history_candidates.csv</a></p>
<div class="csvtable" data-src="data/alt_history_candidates.csv" data-cols="title,release_year,setting_year,gap_years,country,director,source_url,notes,reason_moved"
 data-num="release_year,setting_year,gap_years" data-long="notes,reason_moved"></div>
<h2>Other rejected candidates</h2>
<p>I also turned down 25 candidates for the 233-film expansion under the inclusion rules, for example because the year isn't reliably sourced.</p>
<div class="csvtable" data-src="data/rejected_candidates.csv" data-num="release_year,candidate_setting" data-long="reason"></div>
''', wide=True, js=True)

# ---------- comparison ----------
page('comparison.html', 'Comparison with Wythoff & Leane', '''
<h1>Comparison with Wythoff &amp; Leane (2025)</h1>
<p class="lede">Wythoff and Leane's <a href="https://data.post45.org/posts/futuristic-fiction/"><em>Time Horizons of Futuristic Fiction</em></a> hand-checked 2,552 works set in the future, 960 of them films. It's the closest thing to my project I've found, so I checked my list against it. This was when my list stood at 163 films (11 October 2026), before it grew to 233.</p>
<p>Mine turns out to be mostly a subset of theirs: 146 of my 163 films (90%) are in their data. The 17 they don't have are mostly 2023–26 releases (their data stops in early 2025), plus a few obscure early titles.</p>
<p>W&amp;L and I agree on the setting year for 132 of the 146 shared films. Of the 14 disagreements, 6 come from their method (they take the median of a multi-year story where I use the main year), 5 are source conflicts I'd already flagged, and 3 look like errors in their data when checked against current Wikipedia.</p>
<p>On look-ahead, their 960 films (959 with a year) have a median gap of 25 years against my 32. But on the shared films both datings give about 31, so the difference is down to which films each list picked. Theirs includes lots of superhero, horror and comedy films set a year or two ahead.</p>
<p>Their films do show a trend. The median look-ahead falls from about 50 years in the 1960s to 17 in the 2010s and about 10 in the early 2020s. Novels don't show this, and my own list shows no clear trend. Part of the effect is the incidental near future of franchise films, rather than film-makers imagining less far ahead.</p>
<p>Their data also turned up films I'd missed. 51 of them were checked and added when the list grew to 233.</p>
<figure><img src="charts/chart1_median_gap_by_decade.png" alt="Median gap by release decade, Wythoff and Leane films, novels and my films." loading="lazy"></figure>
<figure><img src="charts/chart2_gap_distribution_mine_vs_wl.png" alt="Distribution of gaps, my 163 films against Wythoff and Leane's films." loading="lazy"></figure>
<figure><img src="charts/chart3_near_future_share_by_decade.png" alt="Share of works set within 10 years of release, by decade." loading="lazy"></figure>
<p>The full write-up is in <a href="findings/wythoff_leane_findings.md">findings.md</a>. The matched table is <a href="data/match_mine_vs_wl.csv">match_mine_vs_wl.csv</a>, and the shortlist is <a href="data/add_candidates_shortlist.csv">add_candidates_shortlist.csv</a>.</p>
<p class="note">Their raw data isn't redistributed here. You can get <code>futuristic_fiction.csv</code> from the <a href="https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction">Post45 Data Collective repository</a> (CC BY 4.0).</p>
''')

# ---------- methodology ----------
page('methodology.html', 'Methodology', f'''
<h1>Methodology</h1>
<h2>Which films count</h2>
<p>I set the rules early and stuck to them for every film I added.</p>
<ul>
<li>Earth's timeline and humanity's current calendar only. A film has to be set in a named future year on humanity's current calendar, so galaxy-far-away settings like <em>Star Wars</em> are out, and so are invented calendars.</li>
<li>Released films only. Streaming-first and streaming-only releases count ({n_stream} films, flagged). Unreleased and festival-only titles don't.</li>
<li>Shorts and serials only get in where they fill an otherwise empty early release year.</li>
<li>No alternate history (parked <a href="alt-history.html">for later</a>) and no television (<a href="series.html">94 series set aside</a>).</li>
<li>A sourced year, not a decade. Decades, centuries and years that only turn up in a Wikipedia category don't count.</li>
</ul>
<h2>Setting year and gap</h2>
<p>Setting years come from on-screen dates, the film's Wikipedia plot, or other cited sources (AFI Catalog, BFI, SFE, EOFFTV, DEFA and press coverage). Every row has a <code>source_url</code> and a quote in <code>notes</code>. Sometimes the year is ambiguous, derived, or comes from tie-in or official material rather than the screen (<em>Alien</em>'s 2122, for example). Then I've flagged the title with an asterisk rather than guess. {n_flag} of {S['films']} are flagged.</p>
<p>The gap is simply setting year minus release year. I report the median, because a few far-future films make the mean meaningless. <em>The Time Machine</em>, for one, is set 800,741 years ahead.</p>
<h2>Scoring predictions</h2>
<p>I only scored films whose setting year is 2026 or earlier ({S['past']} films). For each one I took the main on-screen technology and society forecasts, wrote each as a claim about the setting year and gave it a theme. Then it's came true, sort of or didn't, judged by the film's own setting year. If something turned up later than that, it counts as didn't.</p>
<p>Some things I left out rather than scored. That means anything that already existed when the film came out, and plot devices (time travel, aliens, monsters, the supernatural, alternate history). The headline score counts sort of as half. Films I only know from synopses are marked THIN, and I also give the results without them.</p>
<h2>Tone labels</h2>
<p>Each film has two labels. One is rule-based, from Wikipedia's short description, lead and categories. The other is a stricter on-screen label: a film only counts as dystopian if society itself is oppressive or collapsed for most of the runtime. For the tests I used Fisher's exact test, film-level Mann–Whitney and permutation tests, and a theme-adjusted GEE model clustered by film.</p>
<h2>Checking my work</h2>
<p>I didn't want to take my own scoring on trust, so I went back and checked my work twice.</p>
<ul>
<li>First round of checks (audit v1, 164-film version): I re-scored a random 40 predictions from scratch (39 agreed), re-checked every hit and partial, recomputed every published number, re-labelled tone with the strict rule and tested gap vs accuracy. That showed some hits weren't real forecasts, moved <em>2009: Lost Memories</em> to alternate history, and knocked <em>Back to the Future Part II</em> down from 50% to 45%. "About 1 in 5" held up (21.5% after fixes). <a href="findings/audit_findings.md">audit_findings.md</a></li>
<li>Second round (audit v2): I went through all 44 predictions added when the list grew to 233 films, line by line. 3 changed, and the headline moved by a tenth of a point. <a href="findings/audit_findings_v2.md">audit_findings_v2.md</a></li>
</ul>
{CAVEATS}
<p>All the numbers are in <a href="findings/stats_summary.md">stats_summary.md</a>, and the column definitions are in the <a href="data/README.md">codebook</a>.</p>
''')

# ---------- paper ----------
if HAVE_PAPER:
    md = open(RP('paper', 'paper.md'), encoding='utf-8').read()
    meta = {}
    m = re.match(r'^---\n(.*?)\n---\n', md, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(':'); meta[k.strip()] = v.strip().strip('"')
        md = md[m.end():]
    def fig(mm):
        cap, src = mm.group(1), mm.group(2)
        src = 'paper/' + src if src.startswith('figures/') else src.replace('../charts/', 'charts/')
        cap_html = markdown.markdown(cap).removeprefix('<p>').removesuffix('</p>')
        alt = html.escape(re.sub(r'[`*_]', '', cap))
        return f'\n<figure><img src="{src}" alt="{alt}" loading="lazy"><figcaption>{cap_html}</figcaption></figure>\n'
    md = re.sub(r'^!\[(.*?)\]\(([^)]+)\)(\{[^}]*\})?\s*$', fig, md, flags=re.M)
    body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'toc', 'sane_lists'], output_format='html5')
    body = re.sub(r'(https?://[^\s<]+[^\s<.,;)])(?![^<]*</a>)(?![^<>]*>)', r'<a href="\1">\1</a>', body)
    page('paper.html', 'Paper', f'''
<article class="paper">
<p><a class="btn" href="paper/paper.pdf">PDF</a><a class="btn" href="paper/paper.docx">Word (.docx)</a><a class="btn" href="paper/paper.md">Markdown source</a></p>
<h1>{html.escape(meta.get('title', 'Paper'))}</h1>
<p class="lede">{html.escape(meta.get('author', 'Andi Sharkey'))}, {html.escape(meta.get('date', '2026'))}.</p>
<p class="note">On this site, the data files are on the <a href="downloads.html">Downloads</a> page.</p>
{body}
</article>''', desc='Roads? Where We\'re Going: the movies promised me flying cars, so I kept score.')
else:
    page('paper.html', 'Paper', '<h1>Paper</h1><p class="lede">I\'m still writing up a paper on this project. It\'ll go here when it\'s done.</p>')

# ---------- downloads ----------
def size(p):
    b = os.path.getsize(os.path.join(D, p)); return f'{b/1048576:.1f} MB' if b > 1048576 else f'{b/1024:.0f} KB'
def li(p, desc): return f'<li><a href="{p}">{os.path.basename(p)}</a> ({size(p)}): {desc}</li>' if os.path.exists(os.path.join(D, p)) else ''
page('downloads.html', 'Downloads', f'''
<h1>Downloads</h1>
<p class="lede">It's all free to reuse: CC BY 4.0 for the data and text, MIT for the code. Just credit Andi Sharkey (2026). The full repository, scripts and all, is at <code>{REPO_URL}</code>.</p>
<h2>Data</h2><ul class="files">
{li('data/films.csv', f"{S['films']} films: release year, setting year, gap, format, release type, country, director, tone, source and notes")}
{li('data/predictions.csv', 'every prediction, scored or excluded, with its verdict, reason and source')}
{li('data/alt_history_candidates.csv', 'alternate-history films set aside')}
{li('data/rejected_candidates.csv', 'candidates rejected under the inclusion rules')}
{li('data/series.csv', '94 TV series set aside')}
{li('data/match_mine_vs_wl.csv', 'my 163-film snapshot matched to Wythoff &amp; Leane (attributed excerpts, CC BY 4.0)')}
{li('data/add_candidates_shortlist.csv', 'Wythoff &amp; Leane films missing from my 163, before I checked them')}
{li('data/README.md', 'codebook for every column')}
</ul>
<h2>Charts</h2><ul class="files">
{li('charts/timeline.pdf', 'main infographic (vector)')}{li('charts/timeline.png', 'main infographic')}
{li('charts/series_timeline.pdf', 'TV series chart (vector)')}{li('charts/series_timeline.png', 'TV series chart')}
{li('charts/tone_vs_accuracy.png', 'tone and accuracy')}
{li('charts/chart1_median_gap_by_decade.png', 'median gap by decade, with Wythoff &amp; Leane')}
{li('charts/chart2_gap_distribution_mine_vs_wl.png', 'gap distribution, mine vs Wythoff &amp; Leane')}
{li('charts/chart3_near_future_share_by_decade.png', 'near-future share by decade')}
</ul>
<h2>Paper</h2><ul class="files">
{li('paper/paper.pdf', 'PDF')}{li('paper/paper.docx', 'Word')}{li('paper/paper.md', 'Markdown source')}
</ul>
<h2>Findings</h2><ul class="files">
{li('findings/stats_summary.md', 'headline statistics (current)')}{li('findings/tone_analysis.md', 'tone vs accuracy (current)')}
{li('findings/audit_findings.md', 'audit v1 (164-film version)')}{li('findings/audit_findings_v2.md', 'audit v2')}
{li('findings/wythoff_leane_findings.md', 'comparison with Wythoff &amp; Leane (163-film snapshot)')}{li('findings/literature.md', 'related work, 20 items')}
</ul>
<p class="note">Wythoff &amp; Leane's own dataset isn't redistributed here. You can download it from the <a href="https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction">Post45 Data Collective</a>.</p>
''')
print('built', sorted(f for f in os.listdir(D) if f.endswith('.html')), 'paper:', HAVE_PAPER)
