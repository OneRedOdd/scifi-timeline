# Roads? Where We're Going: the movies promised me flying cars, so I kept score

A hand-built, sourced dataset of **233 released science fiction films (1910–2026)** that set their story in a named future year on humanity's current calendar, with the gap between release and setting year for each, and a scored exploration of what the films whose future has already arrived actually got right.

I've been thinking about this since Back to the Future Part II's big day, 21 October 2015. It's a spare-time project: I built the dataset up over time in spreadsheets and moved it all here once it was ready to share.

By **Andi Sharkey**, October 2026. Browsable site: `https://OneRedOdd.github.io/scifi-timeline/` (served from [`docs/`](docs/)). Paper: [`paper/paper.pdf`](paper/paper.pdf) ([Markdown](paper/paper.md), [Word](paper/paper.docx)). Talk slides: [`slides/roads-where-were-going.pdf`](slides/roads-where-were-going.pdf) ([PowerPoint](slides/roads-where-were-going.pptx)).

![Top of the timeline infographic](charts/timeline.png)

## The question

When film-makers put a date on the future, how far ahead do they look? And once that year arrives, how much of what they showed on screen came true?

## Method in brief

- **Scope.** Released films only (cinema, streaming-first and streaming-only), set in a named future year **on humanity's current calendar**. Invented calendars and non-Earth timelines (for example *Star Wars*) are excluded, as are alternate histories. A handful of shorts and serials are kept only where they fill otherwise empty early release years.
- **Setting year.** Taken from on-screen dates, the film's Wikipedia plot or other cited sources (AFI Catalog, BFI, SFE, EOFFTV and others). Every row carries a `source_url`. Where the year is ambiguous, derived, or only in tie-in/official material rather than on screen, the title is **flagged with an asterisk** and explained in `notes`; years are never invented. 49 of the 233 titles are flagged.
- **Gap.** `gap_years = setting_year − release_year`.
- **Prediction scoring.** For the 81 films whose setting year is on or before 2026, the main on-screen technology and society forecasts were scored *came true*, *sort of* or *didn't*, **judged by the film's own setting year** (anything that arrived later counts as didn't). Technology that already existed at release, and plot devices (time travel, aliens, monsters, the supernatural, alternate history) are excluded rather than scored. Headline score counts *sort of* as half.
- **Checking my work.** I checked the scoring twice. The first round (audit v1) re-scored a random 40 predictions from scratch (39 agreed), re-checked every hit and partial, recomputed every number and tested the tone labels against a stricter on-screen rule; "about 1 in 5" held (21.5% after fixes). The second round (audit v2) went through all 44 predictions added in the 233-film expansion line by line (3 changed). See [`findings/audit_findings.md`](findings/audit_findings.md) and [`findings/audit_findings_v2.md`](findings/audit_findings_v2.md).

Full detail: [`docs/methodology.html`](docs/methodology.html) and the codebook in [`data/README.md`](data/README.md).

## Headline findings (12 October 2026)

| | |
|---|---|
| Films | **233** (217 theatrical, 15 streaming, 1 non-theatrical) |
| Median look-ahead | **34 years** (the mean is meaningless: *The Time Machine* is set 800,741 years ahead) |
| Set in a year that has already arrived (≤ 2026) | **81 films (35%)** |
| Scored predictions | **220** (from 75 films; 46 further rows excluded as premise devices or already existing) |
| Came true outright | **11.4%** (about 1 in 9) |
| Score with *sort of* = half | **20.2%** (about 1 in 5) |
| Communication tech (video calls, flat screens, voice control) | **57.5%**, far ahead of every other theme; society/politics lowest at 11% |
| Catastrophes (plagues, wars, collapses, police states) | **2 of 42** came true (both a second world war, foreseen in 1929 and 1933) |
| Tone vs accuracy | No significant link. Wikipedia labels: 20.2% vs 20.3%, Fisher p = 0.52. Strict labels: dystopian 18.6% vs 21.6%, p = 0.14 |

In short: **films are good at guessing our gadgets and bad at guessing our fate.**

### Caveats that should travel with these numbers

- These are **hopefully fairly well-known films that name a year**, not a random sample of science fiction. Nothing here means "science fiction gets X% right".
- **One scorer**, who checked the work twice; there's no second scorer, so there's no inter-rater reliability statistic.
- **Gap vs accuracy:** films set further ahead scored slightly better (audit v1, 164-film version: Spearman ρ = 0.21, p = 0.08; odds ratio 1.33 per e-fold of gap, p = 0.04), but the tendency **largely fades once the theme of the prediction is accounted for** (OR 1.20, p = 0.19). It is not "no link", and it is not evidence that looking further ahead makes a film more accurate. Not yet rerun on the 233-film version.
- **"Dystopias are rising"** only holds on Wikipedia's generous labels (OR 1.19 per decade, p = 0.012). On the stricter on-screen rule the trend is not significant (p = 0.24) and the 2010s peak falls from 86% to 63%.
- Most theme and tone cells hold fewer than 30 predictions.

Full numbers: [`findings/stats_summary.md`](findings/stats_summary.md) and [`findings/tone_analysis.md`](findings/tone_analysis.md).

## What was set aside

- **Alternate history.** Settings that break from real history (for example *2009: Lost Memories*, moved out after audit v1) are excluded from the 233 and parked to look at later: [`data/alt_history_candidates.csv`](data/alt_history_candidates.csv).
- **TV series.** 94 series set in a named future year were collected but kept out of the film analysis; they could be scored the same way later: [`data/series/series.csv`](data/series/series.csv) and [`charts/series_timeline.png`](charts/series_timeline.png).

## Repository layout

```
data/        films.csv, predictions.csv, alt_history_candidates.csv, series/, wythoff_leane/, derived/  (+ README.md codebook)
charts/      timeline.png/.pdf (main infographic), series_timeline.png/.pdf, tone_vs_accuracy.png, chart1-3 (W&L comparison)
src/         chart and statistics scripts (run from any directory)
findings/    stats_summary.md, tone_analysis.md, audit_findings*.md, literature.md, wythoff_leane/findings.md
paper/       research paper: paper.md, paper.docx, paper.pdf, figures/
docs/        GitHub Pages site (plain HTML/CSS/JS, no build step)
```

## How to reproduce

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python src/make_timeline_chart.py        # charts/timeline.png + .pdf (checks all 233 films are drawn)
python src/make_series_chart.py          # charts/series_timeline.png + .pdf
python src/headline_stats.py             # data/derived/stats.json (headline numbers)
python src/tone_stats.py                 # data/derived/tone.json (tone tests; needs statsmodels)
python src/make_tone_chart.py            # charts/tone_vs_accuracy.png
python src/wythoff_leane/make_wl_charts.py   # downloads W&L data to data/external/ (git-ignored), draws chart1-3
python src/make_paper_figs.py            # paper/figures/
python src/build_site.py                 # copies data/charts/paper into docs/ and rewrites the site pages
```

To preview the site: `cd docs && python -m http.server` and open http://localhost:8000/.

With the pinned versions in `requirements.txt` (Python 3.13), the PNGs reproduce byte for byte; PDFs differ only in their embedded creation date. If you edit the data, rerun `src/build_site.py` so the copies in `docs/` match.

## How to cite

See [`CITATION.cff`](CITATION.cff). Suggested form:

> Sharkey, A. (2026). *Roads? Where We're Going: the movies promised me flying cars, so I kept score* [Data set and code]. https://github.com/OneRedOdd/scifi-timeline

## Licence

- Data, charts and text: **CC BY 4.0** ([`LICENSE`](LICENSE)). Please credit Andi Sharkey.
- Code in `src/` and `docs/*.js`: **MIT** ([`LICENSE-CODE`](LICENSE-CODE)).
- The Wythoff & Leane *Futuristic Fiction* data is © its authors, published under CC BY 4.0 by the Post45 Data Collective. It is **not redistributed** here; the comparison files in `data/wythoff_leane/` contain matched excerpts (titles, years, notes and record ids) with attribution, and the script downloads the original from [their repository](https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction).

## Related work

- Wythoff, G. & Leane, T. (2025). *Time Horizons of Futuristic Fiction.* Post45 Data Collective. https://data.post45.org/posts/futuristic-fiction/ · doi:[10.18737/552626](https://doi.org/10.18737/552626). The gap measure at scale: 2,552 hand-checked works, 960 of them films. 146 of my original 163 films (90%) appear in their data; see [`findings/wythoff_leane/findings.md`](findings/wythoff_leane/findings.md).
- Xu, W., Kotecha, M. C., Padilla, D., Jimenez, J. & McAdams, D. A. (2021). *Quantifying the Predictive Abilities of Speculative Fiction: A Feasibility Study.* ASME IDETC/CIE 2021. doi:[10.1115/DETC2021-68723](https://doi.org/10.1115/DETC2021-68723). 45% of 3,095 technologies judged eventually realised (any time, not by the story's year).
- Chang, A. (2024). *Who killed the world?* The Pudding. https://pudding.cool/2024/07/scifi/. The rise of dystopia in sci-fi film and TV by decade.

A wider review of 20 items is in [`findings/literature.md`](findings/literature.md).
