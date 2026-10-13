# Audit of sci-fi timeline findings (11 Oct 2026)

My first check of my own scoring.
Files: `audit_findings.md` and `audit/` (scripts `recompute.py` and `audit_analysis.py`, plus `sample40_raw.csv` and `sample40_rescore_audit.csv`).
Scoring: came true = 1, sort of = 0.5, didn't = 0. The random seed is 2026 throughout.

## 1. Recomputation: every published number reproduces
| Claim | Recomputed | Status |
|---|---|---|
| 164 films; 69 (42.1%) set ≤2026 | 164; 69 (42.1%) | OK |
| Median gap ~31 | 31.5 (mean 5,062; distorted by The Time Machine) | OK. Say "about 31", or "31.5" |
| gap_years = setting − release | 0 mismatches | OK |
| 224 predictions: 30 true / 38 sort of / 156 didn't = 13.4 / 17.0 / 69.6%; score 21.9% | identical | OK |
| Excluding 19 THIN films: 182 predictions, 25.3% | identical | OK |
| Dystopian 41 films / 135 predictions vs non-dystopian 28 / 89, both 21.9%; Fisher p = 0.69 | 21.85% vs 21.91%; p = 0.69 | OK |
| Theme scores 62 / 35 / 23 / 18 / 16 / 11 / 10 / 5% | identical | OK |
| Dystopian share by decade: 87% (2010s), 54% (2020s) | 20/23, 14/26 | OK (Wikipedia labels; the 2020s covers 2020–26 only) |
| 2001 35%, Blade Runner 39%, BTTF II 50% | identical | OK |

The arithmetic is clean. The problems are in definitions and judgement, covered below.

## 2. Re-scoring
### Random sample (40 predictions, seed 2026; see `audit/sample40_rescore_audit.csv`)
Rows: 5, 12, 15, 24, 34, 37, 42, 46, 52, 56, 65, 71, 76, 80, 82, 93, 94, 100, 110, 114, 115, 119, 122, 126, 132, 136, 143, 153, 164, 170, 175, 186, 193, 194, 206, 207, 211, 214, 217, 218.
- **Verdict agreement: 39 of 40 (97.5%).** The one change is row 12 (High Treason, "United States of Europe" by 1940): sort of becomes didn't, because no federal Europe existed by 1940.
- I'd also take 3 rows out of scoring altogether, because they depend on the premise rather than forecasting anything: rows 82, 193 and 194. Counting those as disagreements, agreement is 36 of 40 (90%).
- Caveat: 36 of the 40 sampled items were "didn't", and most of those are obvious (dragons, alien invasions and the like). A random sample flatters agreement, so I also reviewed **all 68 "came true" and "sort of" rows** by hand.

### Targeted review of every "came true" and "sort of" row
**Verdict changes (5):**
- 12 High Treason, federal Europe by 1940: sort of → didn't.
- 39 1984, home telescreens by 1984: sort of → didn't. The reason given cites today's smart devices, not 1984.
- 53 Battle in Outer Space, UN-led space effort by 1965: sort of → didn't. Its own reason says this came later (ISS, 1998).
- 155 BTTF II, self-lacing shoes: sort of → didn't. They arrived in 2016, a year late, and the stated rule says late counts as didn't.
- 13 High Treason, world war by 1940: sort of → came true. Men Must Fight row 18 gets came true for the same claim.

**Not predictions at all: the thing already existed when the film came out (9 rows).**
- 1: a woman mayor, already real in 1887 (Susanna Salter).
- 49: nuclear submarines (USS Nautilus, 1954).
- 77: archive documentaries on TV.
- 106: a crewed space station. Salyut stations were crewed from 1971, before the 1977 film.
- 191: the ISS. It was under assembly from 1998 and the film came out in March 2000.
- 212: US medical debt, already widely documented before 2010.
- 221: drones on the US border. CBP has flown Predator B drones there since 2005.
- 169 and 202: private prisons, which already existed (CCA was founded in 1983). Both are "sort of".

**7 of the 30 "came true" hits (23%) are these.**

**Premise items (33 rows).** These depend on time travel, aliens or alien life, monsters, the supernatural or psychic powers, or alternate history. All are scored "didn't". They aren't forecasts of the real world, and they drag down the scores of fantasy-premise films. See `flag_premise` in `predictions_audit.csv`.

**Bias check:**
- **Late arrivals:** I wasn't too harsh on "arrived after the setting year". If anything I was inconsistent in the lenient direction: rows 12, 39, 53 and 155 got "sort of" despite arriving late. The rule itself is strict by design, though. Counting anything that came true by 2026, the cleaned score rises to **about 27%** (Moon landing, Channel Tunnel, tablets, space stations and so on).
- **"Sort of":** this is the main source of subjectivity. It covers 17% of predictions, and my reason text sometimes cites evidence dated after the setting year (rows 39, 102 and 198; row 198 cites Neuralink in 2024 for a film set in 2019, although BrainGate implants from 2004 would support the same verdict).
- **Missing reliability check:** there is only one scorer, and no second-rater kappa has been calculated.

### Corrected overall rates
| Version | n | Came true | Score (sort of = ½) |
|---|---|---|---|
| A. As published | 224 | 13.4% | 21.9% |
| B. Audit verdict fixes | 224 | 13.8% | 21.2% |
| C. B, minus premise items | 191 | 16.2% | 24.6% |
| **D. C, minus things that already existed** | **182** | **13.2%** | **21.4%** |
| E. D, minus THIN films | 154 | 15.6% | 24.0% |
| D, counting things that came true by 2026 | 182 | ~19% | ~27% |
| Film-equal weighting (A / D) | 69 / 62 films | – | 18.5% / 17.7% |

The two corrections pull in opposite directions and roughly cancel, so **"about 1 in 5"** is robust. The exact range is 18–27% depending on definitions.

Headline films after the fixes:
- 2001: 35% (45% counting things that came true by 2026, because tablets arrived in 2010).
- Blade Runner: 39%, unchanged.
- **BTTF II: 45%** (50% as published, and 55% counting things that came true by 2026). Don't quote "50%" without saying "counting near-misses as half".

## 3. Tone labels and "no correlation"
**Stricter rule:** a film counts as dystopian only if the society it depicts is itself oppressive or collapsed for most of the runtime (`tone_strict` in `films_audit.csv`). Under this rule, 9 of the 41 Wikipedia "dystopian" films drop out: The Last Man on Earth (1924), BTTF II, Escape from the Planet of the Apes, Westworld, Terminator 2, Strange Days, Pacific Rim, Terminator: Dark Fate and Avengers: Endgame. The Apple is added. That gives **33 dystopian and 36 not**.
Borderline calls: Repo Men, On the Beach, Rollerball and The Apple (all D); Strange Days and Time of Roses (both N).

| Specification | Dystopian | Not | Tests |
|---|---|---|---|
| Wikipedia labels, pooled | 21.9% | 21.9% | Fisher 0.69; perm 0.54 |
| **Strict labels, pooled** | **20.3%** | **23.3%** | Fisher 0.24; MW 0.80; perm 0.66 |
| Strict, film-equal weighting | 17.5% | 19.4% | perm 0.66 |
| Strict, excluding THIN films | 22.0% | 28.7% | perm 0.13 |
| Strict, excluding the 3 headline films | 18.6% | 19.4% | perm 0.78 |
| Strict, audit verdicts, excluding premise and existed rows | 19.4% | 23.4% | perm 0.65 |
| Theme-adjusted logistic (GEE, clustered by film), strict | OR 0.75 | – | p = 0.28 |
| Most-trimmed subset, theme-adjusted | OR 0.43 | – | p = 0.03 (see below) |

**Verdict:** "no significant correlation" survives. "Exactly equal" doesn't: the 21.9% vs 21.9% tie is an artefact of Wikipedia's labels. With stricter labels, dystopias score slightly *lower* in every specification (by 1–7 points), and the theme-adjusted odds ratio is below 1 every time (0.4–0.75). That only reaches p < 0.05 in the most heavily trimmed subsets, after about 24 tests, so it is forking paths, not a finding.
Honest wording: "No detectable link. If anything, bleak films did slightly worse, but the sample is far too small to say."
Power: with about 30 hits, only a gap of roughly 15 points or more could be detected.

## 4. Confounds
- **Theme mix (the big one).** 43 of the 45 space predictions come from non-dystopian films, and 22 of the 26 medicine predictions come from dystopian ones. Any tone comparison is mostly a comparison of themes. Theme adjustment was used above.
- **The theme table.** The overall chi-square is p = 5e-5. After a Holm correction for 8 comparisons, **only communication stands out (62% vs the rest; Holm p = 2e-6)**. Computing/AI at 35% doesn't survive (Holm p = 0.22), and the rankings from environment down to transport are noise. Communication is also small and concentrated: 21 predictions from 11 films, **52% of them from the 3 headline films**. After the audit it is still 57.5% (n = 20).
- **Gap length.** Near-future films do **not** score better, and the trend runs the other way. Scores by gap:

| Gap | Score |
|---|---|
| 1–10 years | 15% (58 predictions, 22 films) |
| 11–20 years | 18% |
| 21–30 years | 29% |
| 31+ years | 26% |

  Film-level Spearman ρ = 0.21 (p = 0.08). Unadjusted GEE OR = 1.33 per e-fold of gap (p = 0.04), but it drops to 1.20 (p = 0.19) after adjusting for theme. Likely reason: very-near-future films are mostly premise thrillers (Predator 2, Alien Nation, Strange Days, T2) with few technology forecasts, while longer-gap films make more gadget forecasts. Note too that the scored films are capped at a 100-year gap (median 17, against 31.5 for all 164), because only films whose year has passed can be scored.
- **Release decade.** No trend (ρ = −0.01). Decades with fewer than 5 films are unreadable.
- **Selection bias.** The 69 films are those that (a) name a year, (b) have a year that has passed, and (c) are well known enough to have been found. They skew towards the 1950s–80s and short gaps. They are not "science fiction" as a whole, so don't generalise to "sci-fi gets X% right".
- **Unit of analysis.** Films contribute 1–10 predictions each (mean 3.25). The well-documented films (2001, Blade Runner, BTTF II) contribute the most, and the most hits. Pooled percentages over-weight famous films, and film-equal weighting lowers the score to about 18%.
- **Scorer subjectivity.** There is one scorer, with no blinding or second rater. Choosing *which* on-screen details count as "predictions" is itself subjective and matters more than the verdicts: the 33 premise rows and 9 already-existed rows show this.
- **Multiple comparisons.** About 8 theme cells × 2 tones × several decade cells. Treat any single cell as anecdote.

## 5. "Came true" highlights: accuracy and fair framing
| Highlight | Holds? | Fair framing |
|---|---|---|
| Running Man: faked face/death, set 2017 | Yes, on screen. The broadcaster digitally maps the leads' faces onto stunt doubles and airs their "deaths" (Cinemablend, befores & afters, The Conversation). | "Deepfakes" got their name on Reddit in late 2017, which is a neat coincidence. Digital face replacement existed before 2017, and no broadcaster faked a death. Say "imagined broadcast deepfakes; the tech arrived on cue". |
| Akira: Tokyo 2020 Olympics | Yes. The 2019-set film shows a "147 days until the Games" sign with "Just cancel it" graffiti (Bloomberg/Japan Times, Feb 2020). Tokyo won the bid in 2013, and the Games were postponed to 2021. | It's a coincidence, not foresight. Tokyo had hosted in 1964 and bid repeatedly. PolitiFact debunked the viral claim that it "predicted the pandemic". Don't imply it did. |
| Fortress: body scanners at borders | Mostly. Karen wears a magnetic vest to fool border scanners that would reveal her pregnancy (Wikipedia). | Backscatter body scanners were developed in the early 1990s (CRS report). US Customs used them at airports from 1999, and TSA rolled them out from 2007. The technology was already being developed in 1992, and real scanners don't police pregnancies. Say "sort of" or "extrapolation". |
| Johnny Mnemonic: society runs on a global internet | Yes by 2021. | The internet was already growing fast in 1995. That's a trend extrapolation from a Gibson story, not a leap. |
| Death Race: pay-per-view livestreaming | Yes by 2020. The film shows the race livestreamed for profit (Wikipedia). | Pay-per-view TV long predated 2008, and livestreaming sites existed (Justin.tv, 2007). It's an extrapolation of an existing trend. |
| Repo Men: crushing medical debt | It was already true in 2010. | **Not a prediction.** Drop it from the hits, or label it "already true". |
| Terminator: Dark Fate: border drones and surveillance | It was already true in 2019 (CBP Predator B drones since 2005). | **Not a prediction**: the film is set one year ahead and shows the present. Drop it. |

Of the seven highlights, two aren't predictions and three are coincidences or extrapolations of existing trends. Only the Running Man one is a genuinely striking hit, and it still needs the caveat.

## Strongest defensible headline claims
1. Of 164 well-known films set in a named future year, 69 (42%) are set in a year that has already passed. The median film looks about 31 years ahead.
2. Across about 180–220 on-screen predictions from those 69 films, about **1 in 5** came true, counting near-misses as half. Only about **1 in 8 came true outright** by the film's own date.
3. **Communication tech is the clear standout** (about 60% vs about 20% overall). It is the only theme that survives a multiple-comparison correction. Flying cars and other transport scored worst (1 of 10 got even half credit), but n = 10.
4. **There is no evidence that bleak films predicted better or worse.** If anything, strict dystopias did slightly worse, but the difference isn't significant.
5. Films get the background gadgets right and the big catastrophes wrong. Almost every plague, nuclear war and police-state premise scored "didn't".

## Required caveats
- These are curated, well-known films that name a year. That is not a random sample of sci-fi.
- There is a single scorer. Choosing what counts as a "prediction" is subjective. Late arrivals count as misses.
- The tone labels are coarse. The exact 21.9% vs 21.9% tie depends on the labelling and shouldn't be quoted as "identical".
- Remove or relabel non-predictions (Repo Men medical debt, Dark Fate drones, the 1910 woman mayor, On the Beach submarines, the ISS and Salyut rows) before quoting hit lists.
- Akira and Running Man are coincidences with good stories behind them, not evidence of foresight.
- Small numbers: most theme and decade cells have fewer than 30 predictions.
- Inclusion: 2009: Lost Memories is alternate history and arguably breaks the "real timeline" rule. Consider moving it to the alt-history set.
