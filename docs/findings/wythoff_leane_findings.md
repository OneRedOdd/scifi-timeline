# Exploring Wythoff & Leane (2025): Time Horizons of Futuristic Fiction

Analysis date: 11 October 2026. I worked these numbers out from W&L's `futuristic_fiction.csv` and a read-only snapshot of my `films.csv` (`my_films_snapshot.csv`, 163 films, taken at 23:58 on 11 October 2026).

## 1. The dataset

**Source.** Grant Wythoff and Theodore Leane, *Time Horizons of Futuristic Fiction*, Post45 Data Collective, 24 June 2025. Article and codebook: https://data.post45.org/posts/futuristic-fiction/. Data: https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction (a single file, `futuristic_fiction.csv`, with no separate README in the folder. The codebook is the "Dataset Description" section of the article, saved here as `article.html`.)

**Licence.** The article page says "This work is licensed under CC BY 4.0". The GitHub repo itself has no LICENSE file (GitHub's API reports no licence), so CC BY 4.0 from the article is the licence to cite. Reuse is allowed, including commercially, as long as it's credited.

**How to cite** (their own suggested form):
> Wythoff, Grant, and Theodore Leane. 2025. "Time Horizons of Futuristic Fiction." Post45 Data Collective, June 24. https://doi.org/10.18737/552626.

A short credit for charts: "Data: Wythoff & Leane (2025), Post45 Data Collective, doi:10.18737/552626, CC BY 4.0".

**Size and coverage.** There are 2,552 works, released from 1733 to 2024 (94% after 1945). Settings run from 1840 to 100 trillion AD. Ten works have no setting year (NaN). One work has a gap of 0 (The Lake House, 2006). The data was last scraped in February 2025, so nothing from 2025 or 2026 is included, and 2023 and 2024 are thin (only 4 films from 2024).

| Medium | Works |
|---|---|
| Film | 960 (959 with a year) |
| Prose fiction (novels and stories) | 761 |
| Television (series and episodes) | 377 |
| Video games | 325 |
| Comics | 75 |
| Radio | 36 |
| Tabletop games | 9 |
| Drama | 6 |
| Theme-park rides | 2 |
| Illustration | 1 |

**Columns.** `record_id` (surname_firstword_year), `wikidata_work_qid`, `title`, `creator` (director for film), `released` (year), `year_set`, `years_distant` (= year_set − released, which I checked and it holds for every row), `multiyears` (all years shown, with commas for jumps and hyphens for spans, filled for 242 rows), `medium`, `genre` (the first Wikidata genre only, so a lot of SF films are tagged "action" or "horror"), `wikipedia_pg`, `verify_yr` (an outside source, used when Wikipedia or Wikidata was unclear, filled for 212 rows), `notes`, `is_series` (the Wikidata ID of the parent series, filled for 446 rows), `predictions` (text taken from Wikipedia's "List of stories set in a future now past"), and `source` (wikicategory, wikifilm, wikipast, wikitext or wikidata). There's also an unnamed index column.

**How they define the setting year and gap.**
- Selection: any narrative work set at least one year after its release, whatever its genre. That means superhero films, romcoms and slashers set a year or two ahead are all included. Only about 37% of the films have "science fiction" as their first genre.
- Sources: English Wikipedia and Wikidata only (the "set in period" property P2408, the "future now past" list, the "list of films set in the future", the "Films set in YYYY" category pages, and the phrase "set in the year" in article text). About 10% of years were refined with IMDb, fan wikis, jacket copy and so on (the `verify_yr` column).
- Multi-year works: they use the main year where the plot makes it obvious (for example Terminator 2 = 1995). Otherwise they take the median of the years shown (Bicentennial Man = 2048). Two-year spans round down. Five past/future works use the farthest future year instead (Cloud Atlas = 2321).
- Placeholder years: "20XX" becomes 2050 and "200-" becomes 2005. Fan conversions of in-universe calendars are accepted (Dune, Ender, The Expanse).
- Franchises: Star Trek is cut down to 12 series and 13 films. Doctor Who episodes stay in (about 100).
- Republished books keep the year from the first edition.
- This is my "main setting year" rule plus a median fallback. That's the main reason my years disagree with theirs (section 3).

## 2. Their films

| | W&L films | W&L novels | W&L all media |
|---|---|---|---|
| n (with year) | 959 | 755 | 2,542 |
| Median gap | **25 years** | 65 | 37 |
| Mean gap | 1,870 (skewed by outliers) | 30.5 million | 39 billion |
| 5% trimmed mean | 81 | 261 | 143 |
| Interquartile range | 6 to 87.5 | 21 to 262.5 | 11 to 151 |
| Within 10 years | **34.6%** | 14.4% | 24.3% |
| Within 50 years | **67.3%** | 43.7% | 57.7% |
| Within 100 years | **77.7%** | 59.7% | 70.0% |
| More than 1,000 years | 3.3% | 11.1% | 7.6% |

(The article's "a quarter within a decade, 58% within fifty, 69% within a century" is the all-media figure. I get 24.3%, 57.7% and 70.0%.)

- Film distribution: 226 films at 0 to 5 years, 105 at 6 to 10, 151 at 11 to 25, 162 at 26 to 50, 100 at 51 to 100, 85 at 101 to 250, 97 at 251 to 1,000, 26 at 1,001 to 10,000 and 6 above 10,000. 130 films (14%) are set only 0 to 2 years ahead.
- Longest film gaps: The Time Machine (1960) at +800,741 and The Time Machine (2002) at +800,699, then Dune (2021) at +21,331 (a fan-converted calendar), Mortal Engines at +10,989, Vampire Hunter D at +10,105 and Bloodlust at +10,090. Shortest: The Lake House at 0, then a group at +1 (Made for Each Other, Bushy Hare, Geordie and others).
- **Films compared with novels:** films look much nearer ahead. Their median is 25 years against 65, and 35% of films are set within 10 years against 14% of novels (Mann–Whitney p ≈ 7×10⁻²⁹). Even the films whose first genre is SF have a median of 42, still well below novels.

### Trend: does screen SF look nearer over time? (Hollinger 2006)

Median gap by release decade (decades with at least 5 works):

| Decade | Films n | Films median | Films within 10 yrs | Novels median | All media median |
|---|---|---|---|---|---|
| 1950s | 18 | 22 | 33% | 76 | 51 |
| 1960s | 43 | 50 | 19% | 100 | 63.5 |
| 1970s | 53 | 40 | 25% | 46 | 49 |
| 1980s | 119 | 32 | 28% | 52.5 | 38 |
| 1990s | 180 | 30.5 | 31% | 53 | 38 |
| 2000s | 221 | 27 | 35% | 68 | 30 |
| 2010s | 239 | 17 | 41% | 59.5 | 25 |
| 2020s (2020 to 2024) | 64 | 10.5 | 50% | 28 (n=21) | 24 |

Hollinger test: the last 20 years (2005 to 2024) against 1950 to 2004.
- **Films: supported.** The median falls from 32 to 18, and the share within 10 years rises from 29% to 41% (n 517 vs 420, Mann–Whitney p ≈ 6×10⁻⁶). The Spearman correlation between release year and gap (from 1950) is ρ = −0.18, p ≈ 10⁻⁸.
- **All media: supported.** 41 falls to 26 (p ≈ 2×10⁻⁹).
- **Novels: not supported.** 56 *rises* to 62 (p = 0.49). Television: 46 to 40, not significant (p = 0.38).
- **Robustness:** the result holds without series entries (30 to 15, p ≈ 3×10⁻⁷). It gets stronger without the "future now past" list source (49 to 19, p ≈ 3×10⁻⁷), which matters because that list can only include old works whose future has already arrived. **But it weakens a lot for films whose first Wikidata genre is SF-type: 49 to 32.5, p = 0.053.** A good part of the film trend comes from the mix changing. Recent decades have many more superhero, horror and comedy films set 1 to 3 years ahead (non-SF-tagged films have a median of 14.5 years, with 45% within 10 years).
- **My list shows no clear trend.** Its decade medians are 27.5 (1980s), 38 (1990s), 50 (2000s), 20 (2010s) and 37.5 (2020s, n=26), all small samples.
- **Overall:** Hollinger's near-future claim holds for films (and for all media together) but not for novels. For films, part of the effect is the incidental near future of franchise films rather than SF writers imagining less far ahead.

Caveats: this is English Wikipedia's view (editors are mostly male and white, as the authors note). Recent works may be under-catalogued. Star Trek is deliberately thinned. Genre is the first Wikidata tag only.

## 3. Comparison with my films.csv

**Overlap.** Fuzzy matching on normalised title plus release year within ±1 (rapidfuzz ratio ≥85, with two manual matches: "2010" for 2010: The Year We Make Contact, and Warriors of Future) matches **146 of my 163 films (90%)**. All the matches were reviewed. Three matched films have a different release year in W&L: Cherry 2000 (mine 1988, W&L 1987), Fortress (mine 1992, W&L 1993) and Warriors of Future (mine 2022, W&L 2019).

**Setting years: 132 of 146 agree (90%), and 14 disagree.**

| Film | Release | Mine | W&L | Why they differ |
|---|---|---|---|---|
| High Treason* | 1929 | 1940 | 1950 | Sound version 1940, silent version 1950 (W&L's note says so). I follow the sound version. |
| Things to Come* | 1936 | 2036 | 1967 | W&L take the median of 1940/1966-67/1970/2036. I use the final, main setting. |
| Thunderbirds Are Go* | 1966 | 2065 | 2066 | W&L median of 2065 and 2067 |
| The Running Man | 1987 | 2017 | 2019 | W&L say "majority set in 2019". Wikipedia's plot says "In 2017". |
| Judge Dredd | 1995 | 2139 | 2110 | W&L median of 2080-2139. Wikipedia's plot says "In 2139". |
| Star Trek: First Contact* | 1996 | 2063 | 2373 | W&L say the majority is in 2373 (Memory Alpha). I use the main Earth action in 2063. A real judgement call. |
| The Fifth Element* | 1997 | 2263 | 2259 | A known source conflict (alarm clock 2263, DVD notes 2257, Besson's book 2259). W&L follow Besson. |
| Bicentennial Man* | 1999 | 2005 | 2048 | W&L median of five eras. I use the opening year. |
| Titan A.E. | 2000 | 3028 | 3043 | W&L say "majority set in 3043". Wikipedia's plot opens "In 3028 A.D.". |
| Code 46 | 2003 | 2077 | 2050 | W&L give no note. Current Wikipedia says "In the year 2077", which supports mine. |
| Death Race | 2008 | 2020 | 2012 | W&L appear to use the backstory year (economy fails in 2012). The main action is "In 2020" (Wikipedia). |
| Bigbug | 2022 | 2045 | 2050 | W&L give no note. Wikipedia says "In 2045", which supports mine. |
| Avatar: The Way of Water* | 2022 | 2170 | 2168 | Derived from "sixteen years after" Avatar. Sources differ. |
| The Creator* | 2023 | 2065 | 2067 | W&L median of 2065-2070. Wikipedia is internally inconsistent (2065 in the plot, 2070 in the lead). |

So 6 of the 14 come from method (their median against my main year), 5 are source conflicts that I'd already flagged with *, and 3 (Code 46, Bigbug, Death Race) look like W&L errors when checked against current Wikipedia. **I wouldn't change any of my values on the strength of W&L alone.** Star Trek: First Contact and Bicentennial Man are the two worth looking at again, because the main year is debatable for both.

**My films that W&L don't have (17).** Two came out after their cut-off (Mickey 17, 2025; Mercy, 2026). Seven are from 2023 to 2024, after or near their scrape (The Wandering Earth 2, Psycho-Pass Providence, Jung_E, Mars Express, Atlas, 2073, Kalki 2898 AD). Five are early or obscure (Looking Forward 1910, Die Große Wette 1916, The Shining Future 1944, THX 1138 4EB 1967, Libra 1978). Three are post-2017 titles they missed (Upgrade 2018, Cosmoball 2020, Voyagers 2021). (Timecop is in W&L as "Time Cop".)

**Their films that I don't have: 813.** I screened them. I kept the SF-relevant ones (an SF-type first genre, or an SF film hand-picked from a generic genre) with a gap of at least 5 years, which leaves 377 in `add_candidates.csv`. For each, the script checked whether the W&L year appears in the current English Wikipedia article text (207 do, though a few of those hits are unrelated mentions) or only in a "Films set in YYYY" category (35). I ranked them by English Wikipedia pageviews from Sep 2025 to Aug 2026, as a sourced measure of fame. The curated shortlist of 118 is in `add_candidates_shortlist.csv`. **Every row is marked "from W&L, to verify".** Highlights:

*Tier A: strong. SF premise, on humanity's current calendar, and the year is stated in the Wikipedia plot (50 films; W&L year shown):*
Star Trek II: The Wrath of Khan (1982 → 2285), Star Trek IV (1986 → 2286), Star Trek VI (1991 → 2293), Star Trek Generations (1994 → 2371, prologue 2293), Planet of the Apes (2001 → 5021), The Time Machine (2002 → 802,701, a second extreme outlier), Ghosts of Mars (2001 → 2176), What Happened to Monday (2017 → 2073), Repo! The Genetic Opera (2008 → 2056), Heavy Metal (1981 → 2031, one segment), Gamer (2009 → 2034), Autómata (2014 → 2044, ES), Screamers (1995 → 2078), Hotel Artemis (2018 → 2028), Cowboy Bebop: The Movie (2001 → 2071, JP), Highlander II (1991 → 2024), 2067 (2020 → 2067, AU), Ganapath (2023 → 2070, IN), Lockout (2012 → 2079), Wing Commander (1999 → 2654), A Sound of Thunder (2005 → 2055), Split Second (1992 → 2008), Nemesis (1993 → 2027), Moonshot (2022 → 2049, streaming), Enemy Mine (1985 → 2092), Space Battleship Yamato (2010 → 2199, JP), Cargo (2009 → 2267, CH), Gunhed (1989 → 2038, JP), Sayonara Jupiter (1984 → 2125, JP), Moon Zero Two (1969 → 2021), Thunderbird 6 (1968 → 2068), Doppelgänger (1969 → 2069), The Time Travelers (1964 → 2071), Frankenstein Unbound (1990 → 2031), First Spaceship on Venus (1960 → 1985, East Germany/Poland), Futureworld (1976 → 1985), Rise of the Planet of the Apes (2011 → 2016), The Purge (2013 → 2022), The Purge: Anarchy (2014 → 2023), and more in the CSV.

*Tier G: fills release years that are currently empty on my chart (to verify):* The Great Air Robbery (1919 → 1925), Algol (1920 → 1940, Germany), The Tunnel (1935 → 1940; Wikipedia calls the setting an "unspecified near-future" but notes a year), The House of Tomorrow (1949 → 2050, Tex Avery short), Pirates of 1920 (1911 → 1920, IMDb only). **W&L have nothing for 1954 or 1957 either.**

*Tier B: famous, but the W&L year isn't in Wikipedia's article text, so it needs another source (47):* Alien (2122), Aliens (2179), Interstellar (2067; Wikipedia only has the category "Films set in 2067") and Forbidden Planet (2200), all four of which **I excluded earlier for having no stated year**. Also Alien 3 and Alien Resurrection, Passengers (2313), the Hunger Games films (2092/2093, and 2248 for Ballad; fan-derived), Starship Troopers (2197, W&L cite IMDb), RoboCop 1987 (2043), A Clockwork Orange (1995), V for Vendetta (2022, the median of 2015-2028 via Screen Rant), Mad Max: Fury Road (2060), Vanilla Sky (2151), the Matrix sequels, Big Hero 6 (2032), Ad Astra (2105), Kingdom of the Planet of the Apes (2328), Dredd (2134), Star Trek: The Motion Picture (2271), Ender's Game (2198), the Riddick films, Valérian (2713), THX 1138 (2400; **I date the 1967 short at 2187**, worth reconciling), Barbarella (4000) and others.

*Tier C: rule conflicts, probably exclude:* The Terminator (main action is in 1984; 2029 appears only in flash-forwards, and W&L's own rule would give 1984, as they did for T2), The Adam Project (main action in 2022), X-Men: Days of Future Past (main action 1973), A.I. (median year), Cloud Atlas, Battle for the Planet of the Apes and Bill & Ted (framing years), Star Trek Into Darkness and Beyond (Kelvin alternate timeline), Dune 1984 and 2021, Divergent and Mortal Engines (fan-converted calendars), and Your Name and Weathering with You (+5, incidental).

**Median gap: mine compared with theirs.**
- Mine: **32 years** (n=163), with 14.1% within 10 years, 65.0% within 50 and 78.5% within 100.
- W&L films: **25 years** (n=959), with 34.6%, 67.3% and 77.7%. The difference is significant (Mann–Whitney p = 0.0013).
- **On the 146 films we both have, the medians are almost identical: 30.5 (mine) and 31 (W&L).** So the gap comes from selection, not from dating. W&L include lots of films set a year or two ahead that I leave out as not really "future" SF. Without those, as in W&L's SF-genre films (median 42, 20% within 10 years), their distribution looks like mine or slightly further out. My 17 films that W&L don't have run further out (median 49).

## 4. Charts (dark timeline palette from `src/make_timeline_chart.py`, each checked visually)
- `chart1_median_gap_by_decade.png`: median gap by release decade for W&L films, W&L novels, W&L all media and my timeline.
- `chart2_gap_distribution_mine_vs_wl.png`: gap distribution (% of films per band), mine against W&L films.
- `chart3_near_future_share_by_decade.png`: Hollinger test, the share set within 10 years of release by decade, for films, novels and TV.

## 5. Things I might look at later
- A third of "future" films are set less than 10 years ahead, and half of the 2020s ones are. I'd like to see how much of that is franchise films nudged a year ahead.
- Films look about 25 years ahead and novels about 65. I'm curious why.
- Where W&L and I both date the same 146 films we agree 90% of the time, and most of the gaps come down to one rule (main year vs median year). If we used the same rule, the two lists would be easier to join up.

## Files in this repository
- `data/wythoff_leane/my_films_snapshot.csv`: a read-only copy of my films.csv (163 films) used for the comparison.
- `data/wythoff_leane/match_mine_vs_wl.csv`: all 163 of my films with their W&L match, both setting years, W&L multiyears and notes.
- `data/wythoff_leane/add_candidates_shortlist.csv`: the 118 W&L films I shortlisted to check, in tiers A, G, B and C, all marked "from W&L, to verify".
- `src/wythoff_leane/make_wl_charts.py`: draws charts 1–3. W&L's own data (`futuristic_fiction.csv`, CC BY 4.0) isn't included here; the script downloads it to `data/external/`.
