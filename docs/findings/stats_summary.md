# Sci-fi timeline: stats summary (after my second check; recomputed 12 Oct 2026)

Source data: `films.csv` (233 released films, humanity's current calendar) and `predictions.csv` (266 prediction rows for films in the list, 220 of them scored).
Infographic: `timeline.png` / `timeline.pdf`. Audit log: `audit_findings_v2.md`.

## What changed after my second check (audit v2)
- I re-checked all 44 prediction rows added in the 233-film update (13 films) line by line and stuck with 41 of the 44 verdicts or scoring decisions. Changes: Silent Star's robot Omega, sort of -> didn't. The 6th Day's AI dolls, didn't -> sort of (Hello Barbie, 2015). Rise of the Planet of the Apes' viral gene therapy for Alzheimer's is now excluded: it was already in human trials before 2011. The Great Air Robbery is marked THIN (lost film). The Highlander II ozone reason was corrected. Details in `audit_findings_v2.md`.
- I re-checked my `tone_strict` labels for the 13 new films whose year has arrived and kept all 13. I also labelled the other 152 films (`tone_strict_basis` gives the basis), so strict tone now covers all 233.
- Earlier history: the 233-film update added 70 films (163 -> 233).

## Films
| Scope | Count |
|---|---|
| All films | **233** (217 theatrical, 15 streaming, 1 non-theatrical) |
| Features only | 226 |
| Features, unflagged | 180 |
| Flagged (asterisk) | 49 |

## Gap between release and setting year (years)
| Scope | n | Mean | Median | Shortest | Longest |
|---|---|---|---|---|---|
| All films | 233 | 7,037.9 | 34 | 1 (Terminator: Dark Fate) | 800,741 (The Time Machine*) |
| All, excl. the 3 extreme outliers (both Time Machines, Vampire Hunter D) | 230 | 123.0 | 33 | 1 (Terminator: Dark Fate) | 3,020 (Planet of the Apes (2001)) |
| Features only | 226 | 7,251.6 | 33.5 | 1 (Terminator: Dark Fate) | 800,741 (The Time Machine*) |
| Features, unflagged | 180 | 182.4 | 31 | 1 (Terminator: Dark Fate) | 10,105 (Vampire Hunter D) |

The median is the robust figure: films look **about 34 years ahead**.

## Films whose future has arrived
- Setting year ≤ 2026: **81 of 233 (35%)**. The share fell from 42% because many of the added films are set further ahead.
- 75 of these have at least one scored prediction. Those with only premise items: Escape from the Planet of the Apes, The Transformers: The Movie, Alien Nation, Timecop, Reign of Fire, Avengers: Endgame*.

## Prediction scoring
Each prediction is judged by the film's own setting year (anything arriving later counts as didn't). Technology that already existed at release, and plot devices, are excluded.

| Verdict | Count | % |
|---|---|---|
| Came true | 25 | **11.4%** (about 1 in 9) |
| Sort of | 39 | 17.7% |
| Didn't | 156 | 70.9% |
| **Score, sort of = half** | 44.5 / 220 | **20.2%** (about 1 in 5) |
| Excluding the 20 thin-evidence films (190 predictions) | 24 / 35 / 131 | 21.8% |
| Film-equal weighting (75 films) | – | 16.9% |

Before my second check: 221 scored, 11.3% came true, score 20.1%. The 164-film version after my first check: 184 scored, 12.5%, 21.5%.

### By theme
| Theme | n (films) | Came true | Score |
|---|---|---|---|
| communication | 20 (10) | 45% | 57.5% |
| computing/AI | 33 (21) | 15% | 30.3% |
| other | 5 (5) | 0% | 30.0% |
| environment | 17 (13) | 6% | 17.6% |
| medicine/biotech | 27 (21) | 4% | 14.8% |
| space | 42 (18) | 10% | 14.3% |
| transport | 12 (10) | 8% | 12.5% |
| society/politics | 64 (42) | 6% | 10.9% |

Communication is still far ahead of every other theme. The lowest are society/politics (11%) and transport (12.5%, from only 12 predictions). Transport is no longer the very lowest: The Great Air Robbery's night air-mail forecast came true.
Gadgets (communication plus computing/AI): 40.6% (n = 53). Catastrophes (plagues, wars, collapses, police states; keyword-defined list of 42 rows in `data/derived/catastrophes.json`, replacing the undocumented 35): 2 of 42 came true. Both are interwar films foreseeing a second world war.

### By tone
| Labels | Dystopian: films / predictions / score | Not dystopian | Fisher (came true vs not) |
|---|---|---|---|
| Wikipedia labels | 43 / 129 / 20.2% | 32 / 91 / 20.3% | p = 0.52 |
| Strict labels | 35 / 102 / 18.6% | 40 / 118 / 21.6% | p = 0.14 (OR 0.51) |

There is no significant link between tone and accuracy. Strictly dystopian films score slightly lower, which is consistent with the audit.

### Headline films
| Film | Came true | Sort of | Didn't | Score |
|---|---|---|---|---|
| 2001: A Space Odyssey | 2 | 3 | 5 | 35% |
| Blade Runner | 3 | 1 | 5 | 39% |
| Back to the Future Part II | 4 | 1 | 5 | 45% |

33 films score 0%.

## Caveats
- These are well-known films that name a year, not a random sample.
- It's just me: I did the scoring and both checks. Coverage: audit v1 re-scored a random 40 of the original rows and re-checked every hit and partial; audit v2 checked all 44 rows from the 233-film update line by line. There is no second-rater reliability statistic.
- Most theme and tone cells have fewer than 30 predictions.
