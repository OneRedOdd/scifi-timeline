# Tone vs prediction accuracy (after my second check; 12 Oct 2026)

Files: `films.csv` (columns `tone`, `tone_source`, `tone_strict` and `tone_strict_basis`), `predictions.csv` (220 scored rows), chart `tone_vs_accuracy.png` (script `src/make_tone_chart.py`), stats `data/derived/tone.json` (script `src/tone_stats.py`).

## Labels
- **Wikipedia tone** (all 233 films): the film's Wikipedia short description, lead and categories are scanned for dystopian, post-apocalyptic, totalitarian or utopian wording. dystopian 131, neutral 95, unclear 3, mixed 3, utopian 1.
- **Strict tone** (now all 233): a film counts as dystopian only if the society on screen is itself oppressive or collapsed for most of the runtime. Dystopian 116, not dystopian 117. Sources of the labels: audit v1 for 68 films; my own labels for the 13 films from the 233-film update whose year has arrived (re-checked at audit v2; all 13 kept); and my own judgement for the remaining 152 films, which are not scored and are used only for the decade shares. Borderline calls are noted in `tone_strict_basis`.
- The two label sets agree on 105 films as dystopian. 26 films are dystopian only by Wikipedia's labels (e.g. Back to the Future Part II, Pacific Rim, Logan, 12 Monkeys) and 11 only by the strict rule (e.g. The Purge, The Apple, Buck Rogers). One Hundred Years Ahead sits in a Wikipedia dystopian category, but its 2124 is a bright future, so it is not dystopian on the strict rule.

## Accuracy by tone (75 films whose year has arrived, 220 scored predictions)
Columns: dystopian films / predictions / % came true / score with sort of = half, then the same for the rest. Then Fisher's exact test (came true vs not), film-level means (Mann–Whitney and a 10,000-shuffle permutation test, seed 2026), and a theme-adjusted GEE logistic model clustered by film.

| Labels and subset | Dystopian | Not dystopian | Fisher p | Film-level | Theme-adjusted |
|---|---|---|---|---|---|
| Wikipedia, all | 43 / 129 / 10.1% / **20.2%** | 32 / 91 / 13.2% / **20.3%** | 0.52 (OR 0.74) | 15.6% vs 18.5% (MW 0.47, perm 0.48) | OR 0.66, p 0.16 |
| Wikipedia, excl. THIN films | 37 / 117 / 11.1% / **21.8%** | 24 / 73 / 15.1% / **21.9%** | 0.50 (OR 0.70) | 17.7% vs 20.0% (MW 0.62, perm 0.63) | OR 0.65, p 0.17 |
| Wikipedia, excl. 3 headline films | 41 / 110 / 5.5% / **16.4%** | 31 / 81 / 12.3% / **18.5%** | 0.11 (OR 0.41) | 14.3% vs 18.0% (MW 0.37, perm 0.39) | OR 0.60, p 0.17 |
| Strict, all | 35 / 102 / 7.8% / **18.6%** | 40 / 118 / 14.4% / **21.6%** | 0.14 (OR 0.51) | 15.7% vs 17.9% (MW 0.64, perm 0.61) | OR 0.74, p 0.28 |
| Strict, excl. THIN films | 30 / 92 / 8.7% / **19.6%** | 31 / 98 / 16.3% / **24.0%** | 0.13 (OR 0.49) | 16.9% vs 20.2% (MW 0.49, perm 0.47) | OR 0.63, p 0.10 |
| Strict, excl. 3 headline films | 34 / 93 / 5.4% / **16.7%** | 38 / 98 / 11.2% / **17.9%** | 0.19 (OR 0.45) | 15.0% vs 16.7% (MW 0.72, perm 0.68) | OR 0.75, p 0.43 |

**Result: no significant link between tone and accuracy** in any specification (all p ≥ 0.10). With Wikipedia labels the two groups score almost the same (20.2% vs 20.3%). With strict labels, dystopian films do slightly worse (18.6% vs 21.6%; 7.8% vs 14.4% came true outright). Every odds ratio is below 1, but none is significant. Power is low: there are only 25 outright hits, so only a gap of roughly 15 points or more could be detected.

## Accuracy by theme × strict tone (score, sort of = half; n = predictions)
| Theme | All | Dystopian | Not dystopian |
|---|---|---|---|
| communication | 57.5% (20) | 64% (11) | 50% (9) |
| computing/AI | 30.3% (33) | 27% (15) | 33% (18) |
| other | 30.0% (5) | 0% (1) | 38% (4) |
| environment | 17.6% (17) | 14% (11) | 25% (6) |
| medicine/biotech | 14.8% (27) | 15% (17) | 15% (10) |
| space | 14.3% (42) | 0% (2) | 15% (40) |
| transport | 12.5% (12) | 25% (2) | 10% (10) |
| society/politics | 10.9% (64) | 8% (43) | 17% (21) |

Theme matters more than tone, and the two are tangled together. Non-dystopian films make 40 of the 42 space predictions, and dystopian films make 43 of the 64 society/politics predictions, both low-scoring themes. Most cells are small. The only theme that stands out after a multiple-comparison correction (audit v1) is communication.

## Dystopian share by release decade (all 233 films)
| Decade | Films | Wikipedia dystopian | Strict dystopian |
|---|---|---|---|
| 1910s | 4 | 0 (0%) | 0 (0%) |
| 1920s | 3 | 2 (67%) | 1 (33%) |
| 1930s | 5 | 0 (0%) | 1 (20%) |
| 1940s | 3 | 0 (0%) | 0 (0%) |
| 1950s | 9 | 3 (33%) | 3 (33%) |
| 1960s | 18 | 6 (33%) | 8 (44%) |
| 1970s | 18 | 13 (72%) | 11 (61%) |
| 1980s | 21 | 8 (38%) | 9 (43%) |
| 1990s | 33 | 18 (55%) | 14 (42%) |
| 2000s | 36 | 25 (69%) | 22 (61%) |
| 2010s | 35 | 30 (86%) | 22 (63%) |
| 2020s | 48 | 26 (54%) | 25 (52%) |

Trend since 1950 (logistic, 218 films): Wikipedia labels rise significantly (OR 1.19 per decade, p = 0.012). Strict labels show no significant trend (OR 1.08, p = 0.24).
The previously reported 2010s peak (87% of 164 films; now 86% of 233) is largely a labelling effect: Wikipedia's categories are generous with recent films. On the strict rule, the 1970s, 2000s and 2010s are all about 61–63%, and the 2020s (2020–26, 48 films) are 52–54% on either rule. Decades before 1950 have too few films to read anything into.

## What this supports
- Bleak films were no better and no worse at predicting. On the stricter label they are, if anything, slightly worse, but the difference isn't significant.
- What came true was mostly incidental technology (communication 57.5%, computing/AI 30%). The catastrophes that make a film dystopian almost never happened: 2 of 42 plague, war, collapse and police-state forecasts came true, both of them a second world war foreseen between the wars.
- "Dystopias are on the rise" holds only with Wikipedia's labels. Don't headline it without that caveat.

## Caveats
- Strict labels are my own judgement. 152 of them cover films with no scored predictions, and nobody else has checked them.
- The films are well-known titles that name a year, not a random sample. There is one scorer for the predictions.
- Many tests on small groups: treat any single theme or decade cell as anecdote.
