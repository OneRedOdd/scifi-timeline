# Data codebook

All files are UTF-8 CSV with a header row. Years are integers on the Gregorian (Common Era) calendar. Licence: CC BY 4.0 (Andi Sharkey, 2026), except the attributed Wythoff & Leane excerpts in `match_mine_vs_wl.csv` and `add_candidates_shortlist.csv` (CC BY 4.0, Wythoff & Leane 2025).

On this site every published file sits directly in `data/`. Files marked "repository only" (including everything in `derived/`) are in the [GitHub repository](https://github.com/OneRedOdd/scifi-timeline/tree/main/data) but are not published on the site.

| File | Rows | What it is |
|---|---|---|
| `films.csv` | 233 | The main dataset: one row per released film |
| `predictions.csv` | 268 | One row per on-screen prediction for films whose setting year has arrived (266 for listed films, 220 scored; plus 2 excluded rows for *2009: Lost Memories*, now in `alt_history_candidates.csv`) |
| `alt_history_candidates.csv` | 1 | Alternate-history films set aside for now; I might look at them later |
| `rejected_candidates.csv` | 25 | Candidate films considered for the 233-film expansion and rejected, with reasons |
| `series.csv` | 94 | TV series set in a named future year (set aside; not scored) |
| `series/series_dropped.md` | – | Series considered and dropped, with reasons (repository only, not on the site) |
| `match_mine_vs_wl.csv` | 163 | My 163-film list (11 Oct 2026 snapshot) matched to Wythoff & Leane |
| `add_candidates_shortlist.csv` | 118 | Films in W&L's data missing from my 163, shortlisted for checking |
| `wythoff_leane/my_films_snapshot.csv` | 163 | Read-only snapshot of my `films.csv` used for the W&L comparison (same columns as `films.csv` at that date) (repository only, not on the site) |
| `derived/stats.json` | – | Headline statistics from `src/headline_stats.py` (repository only, not on the site) |
| `derived/tone.json` | – | Tone tests from `src/tone_stats.py`, read by `src/make_tone_chart.py` (repository only, not on the site) |
| `derived/catastrophes.json` | – | Keyword list defining the 42 "catastrophe" predictions (repository only, not on the site) |

Wythoff & Leane's raw `futuristic_fiction.csv` is **not** included. Get it from https://github.com/Post45-Data-Collective/data/tree/main/futuristic_fiction (or run `src/wythoff_leane/make_wl_charts.py`, which downloads it to `data/external/`).

## Conventions

- **Asterisk.** A trailing `*` on a title means the setting year is ambiguous, derived (for example counted from an on-screen interval), or comes from tie-in/official material rather than the screen. The reason is in `notes` (look for `FLAG:` or `AMBIGUOUS:`). 49 films are flagged. The asterisk is part of the `title` string, and joins between files use the title exactly as written.
- **Humanity's current calendar only.** Every setting year is a year on humanity's current calendar. Invented calendars, non-Earth timelines and alternate histories are excluded.
- **Multi-year settings** use the main year of the action (or the starting year where the film moves through time); see `notes`.

## `films.csv`

| Column | Type / values | Description |
|---|---|---|
| `title` | text | Film title, with a trailing `*` if the setting year is flagged |
| `release_year` | integer | Year of first release (premiere or first general release) |
| `setting_year` | integer | Main future year in which the action takes place |
| `gap_years` | integer | `setting_year − release_year` (always ≥ 1) |
| `format` | `feature` / `short` / `serial` | Shorts and serials are kept only to fill otherwise empty early release years |
| `release_type` | `theatrical` / `streaming` / `non-theatrical` | First release route. `streaming` = streaming-first or streaming-only (Netflix, Prime Video, digital/VOD) |
| `country` | text, `;`-separated | Production countries, first-listed first |
| `director` | text | Director(s), from the film's Wikipedia page or the cited source |
| `source_url` | URL | Main source for the setting year |
| `notes` | text | Sourcing evidence, usually a short quote. Explains any flag |
| `prediction_notes` | text | Summary of the film's scored predictions (counts by verdict) if its year has arrived; otherwise blank or a note |
| `tone` | `dystopian` / `neutral` / `mixed` / `utopian` / `unclear` | Rule-based label from the film's Wikipedia short description, lead and categories |
| `tone_source` | text | Evidence for `tone`, with link |
| `tone_strict` | `dystopian` / `not dystopian (strict)` | Stricter rule: dystopian only if the society on screen is itself oppressive or collapsed for most of the runtime |
| `tone_strict_basis` | text | Where the strict label came from (all labels are mine): `audit v1 (11 Oct 2026)` (68 films), `my label; re-checked at audit v2` (13), or `my label at audit v2 …` (152, unscored films; borderline calls marked `b:`) |

## `predictions.csv`

| Column | Type / values | Description |
|---|---|---|
| `title`, `release_year`, `setting_year` | as in `films.csv` | Join keys to `films.csv` |
| `theme` | `communication`, `computing/AI`, `environment`, `medicine/biotech`, `space`, `transport`, `society/politics`, `other` | Theme of the prediction |
| `prediction` | text | The on-screen element, phrased as a claim about the setting year |
| `verdict` | `came true` / `sort of` / `didn't` | Final verdict (after my checks), judged by the film's own setting year; arriving later counts as `didn't` |
| `verdict_original` | as above | Scorer's verdict before the audits |
| `scored` | `yes` / `no` | Whether the row counts towards the scores |
| `exclusion_reason` | text | Why a row is not scored: `premise device (time travel/aliens/monsters/supernatural/alt-history), not a forecast` or `already existed at release: …` |
| `audit_note` | text | Changes or notes from my two checks (audit v1 / v2); rows added in the 233-film update say so |
| `reason` | text | Evidence for the verdict. `THIN` marks films known only from synopses (for example lost films) |
| `source_url` | URL | Source for the on-screen element |

**Score** = (came true + 0.5 × sort of) / scored rows.

## `alt_history_candidates.csv`

Same columns as `films.csv` up to `tone_source` (no `tone_strict*`), plus `reason_moved`: why the film was taken out of the main list.

## `rejected_candidates.csv`

| Column | Description |
|---|---|
| `title`, `release_year` | Candidate film |
| `candidate_setting` | Setting year proposed by the source list |
| `source_list` | Where the candidate came from (for example `W&L tier A`, recent-release sweep) |
| `reason` | Why it was rejected (year not reliably sourced, rule conflict, etc.) |

## `series.csv`

| Column | Description |
|---|---|
| `title` | Series title (`*` = flagged year, as for films) |
| `release_year` | Year the series premiered |
| `setting_year` | Main (or starting) future year of the series |
| `gap_years` | `setting_year − release_year` |
| `country` | Production countries, `;`-separated |
| `network_platform` | Original broadcaster or streaming platform |
| `release_type` | `broadcast` / `streaming` |
| `source_url` | Main source for the setting year |
| `notes` | Sourcing evidence and flags |

## `match_mine_vs_wl.csv`

Built from my 163-film snapshot (11 Oct 2026, before the expansion to 233). Columns prefixed `wl_` are excerpts from Wythoff & Leane (2025), CC BY 4.0.

| Column | Description |
|---|---|
| `my_title`, `my_release`, `my_setting`, `my_gap` | My film and years |
| `match` | `yes` / `none` |
| `wl_other_medium` | Same-title W&L records in another medium or year (not matched) |
| `score` | Fuzzy-match score (rapidfuzz ratio, ≥ 85), or `manual` |
| `wl_title`, `wl_release`, `wl_setting`, `wl_gap` | W&L's title and years for the matched record |
| `wl_multiyears` | W&L's list of years where a work spans several |
| `wl_verify` | W&L's verification source |
| `wl_notes` | W&L's notes |
| `wl_record` | W&L `record_id` |

## `add_candidates_shortlist.csv`

Shortlist of W&L films missing from my 163, as drawn up **before** verification. 51 of them were later verified and added (see `findings/stats_summary.md`); the `status` column still shows the pre-verification state.

| Column | Description |
|---|---|
| `tier` | `A` strong (year in Wikipedia plot text), `B` famous but year not in Wikipedia text, `C` rule conflict / probably exclude, `G` fills an empty release year |
| `title`, `release_year` | Film |
| `wl_setting_year`, `gap`, `wl_multiyears` | W&L's setting year, the gap, and multi-year list |
| `note` | My note |
| `wikipedia` | Wikipedia URL |
| `wl_verify_source` | W&L's verification source |
| `wiki_year_context` | Sentence from the Wikipedia plot containing the year |
| `pageviews_12m` | English Wikipedia page views over 12 months (popularity proxy) |
| `status` | Pre-verification status |
| `wl_record_id` | W&L `record_id` |
