# Audit v2: checking the 233-film update (12 Oct 2026)

Scope: the 44 prediction rows I added in the 233-film update for 13 newly added films whose year has arrived (rows 224–267 of `predictions.csv`), plus their `tone_strict` labels. The rules are the same as audit v1: judge each prediction by the film's setting year; exclude tech that already existed at release and plot devices; apply "sort of" consistently.
I kept a copy of the data before changing anything, and every change is noted in the `audit_note` column of `predictions.csv`.

## Result
- **41 of 44 verdicts or scoring decisions agreed.** 3 changed (2 verdicts, 1 scored → excluded). 4 more rows had only their reason text corrected or a THIN marker added.
- **13 of 13 `tone_strict` labels agreed.** The "not yet checked" tag is removed, and `tone_strict_basis` records the check.
- The exclusions in the update (5 premise devices; Zeppelin passenger airships from 1910; US Air Mail from 1918) are all correct.

## Changes (each logged in `audit_note` as "Audit v2: …")
| Row | Film | Prediction | Change | Reason / source |
|---|---|---|---|---|
| 233 | The Silent Star* (1960→1970) | Robot companion Omega | sort of → **didn't** | Omega is an autonomous robot crewmate. Lunokhod 1 (Nov 1970) was a teleoperated rover driven from Earth, so the core function did not exist. This is the same bar as the Westworld/Futureworld androids. |
| 252 | Rise of the Planet of the Apes* (2011→2016) | Viral gene-therapy drug tested for Alzheimer's | scored → **excluded (already existed)** | The original reason ("no viral gene therapy for it reached human trials") was wrong. AAV2-NGF (CERE-110) was in human trials from 2004 (phase 1) and 2009–15 (phase 2): Alzforum; ClinicalTrials.gov NCT00876863; Rafii et al., JAMA Neurol 2018. Testing pre-dated the 2011 release, and there is still no cure. |
| 258 | The 6th Day* (2000→2015) | Lifelike talking AI dolls (SimPal) | didn't → **sort of** | Conversational AI dolls were on sale by 2015: My Friend Cayla (2014) and Hello Barbie (Nov 2015; speech recognition plus cloud AI; BBC, TechRepublic). They were not lifelike or autonomous. This matches the "sort of" for Bicentennial Man's expressive robots. |
| 248 | Highlander II (1991→2024) | Ozone layer recovering by 2024 | reason only; **sort of kept** | The reason cited 2066 as the recovery date, but that is the Antarctic figure. The WMO/UNEP 2022 Assessment gives a return to 1980 levels around 2040 near-globally, 2045 in the Arctic and 2066 in the Antarctic. Recovery is under way, not complete. |
| 227–229 | The Great Air Robbery (1919→1925) | all 3 rows | **THIN added** | Lost film (Wikipedia; no Library of Congress holdings), known from its synopsis and a 1920 NYT review. This matches how Die Große Wette and The Last Man on Earth (1924) were treated. The night air-mail hit stays "came true": regular transcontinental night flying began on 1 July 1924, and the first experimental night mail flight was in Feb 1921, after release. |

Notes only, with no change: 244 (Split Second's flooded Underground) is a consequence of row 243 and double-counts one flooding forecast; it is kept for consistency with audit v1. 257 (The 6th Day's cloned food animals): livestock cloning already existed (Dolly, 1996), so it scores "sort of" only for the food-use part (FDA, 2008). 255 (The 6th Day's pet cloning) is a genuine forecast: no pet had been cloned at release, and the first commercial cloned cat came in 2004.

Rows agreed without change: 224–226, 230–232, 234–247, 249–251, 253–257, 259–267.
Checked in particular:
- 224: airships bombing ships at sea, sort of. Aircraft and occasionally Zeppelins attacked shipping in WWI.
- 241: private commercial spaceflight by May 2021, sort of. SpaceX had been flying NASA crews since 2020; the Blue Origin and Virgin Galactic tourist flights only came in July 2021.
- 251: eye-scan identity checks at airports, sort of. Iris checks were in use at some airports (CLEAR; UAE borders), but not as a standard checkpoint, and none were deployed in 1996.
- 260: Purge unemployment at 1%, didn't. US unemployment was about 3.6% in 2022.

## tone_strict, 13 films from the update (rule: the society on screen is oppressive or collapsed for most of the runtime)
All agreed:
- **Dystopian:** Highlander II (shield world under a corporation), Barb Wire (civil war, fascist Directorate), The Purge and The Purge: Anarchy (state-sanctioned killing; consistent with Repo Men = dystopian).
- **Not dystopian:** Pirates of 1920, The Great Air Robbery, The Silent Star, Futureworld, Moon Zero Two, Split Second (borderline: flooded but functioning London; consistent with Strange Days), Rise of the Planet of the Apes, The 6th Day, The Door into Summer.

Additionally, so that the decade analysis can use strict tone across all 233 films, I labelled the 152 films that had no strict label (all set after 2026, none scored). Borderline calls are flagged "b:" in `tone_strict_basis`. One Wikipedia label looks wrong: One Hundred Years Ahead (2024) is in a "dystopian films" category, but it shows a bright 2124.

## Effect on headline numbers
| Measure | Before this check | After this check |
|---|---|---|
| Scored predictions | 221 | **220** |
| Came true | 25 (11.3%) | 25 (**11.4%**) |
| Sort of | 39 | 39 (one out, one in) |
| Score, sort of = half | 20.1% | **20.2%** |
| Excluding THIN films | 22.0% (19 films, 193 predictions) | **21.8%** (20 films, 190 predictions) |
| Film-equal weighting | 16.9% | 16.9% |
| Medicine/biotech score | 14.3% (28) | 14.8% (27) |
| Strict tone: dystopian vs rest | 18.6% vs 21.4%, p = 0.14 | 18.6% vs **21.6%**, p = 0.14 |
| Wikipedia tone | 20.0% vs 20.3%, p = 0.52 | 20.2% vs 20.3%, p = 0.52 |
| Catastrophes that came true | "2 of 35" (no definition recorded) | **2 of 42**, reproducible keyword list in `data/derived/catastrophes.json` |
| Headline films | 2001 35%, Blade Runner 39%, BTTF II 45% | unchanged |
| Films / set by 2026 / median gap | 233 / 81 (35%) / 34 | unchanged |

## Infographic
The "What I found" panel numbers changed (20.1%→20.2%, 221→220, 11.3%→11.4%, strict non-dystopian 21%→22%, catastrophes 2 of 35→2 of 42). The method note also said the new rows hadn't been checked yet. I updated the panels (`src/panels.py`) and redrew **`timeline.png` / `timeline.pdf`** with `src/make_timeline_chart.py`. All 233 films in the CSV are drawn, none are missing, and the header says 233. I also looked over the header, the timeline and both panels by eye.

## Remaining caveats
- I did the scoring and the checking myself, so there's no second-rater reliability statistic.
- The 152 new strict labels rest on my own knowledge of the films and published plot summaries. They feed only the decade-share chart.
- The "catastrophes" figure depends on a keyword definition. The earlier 35 couldn't be reproduced.
