# Findings

| File | What it is | Status |
|---|---|---|
| `stats_summary.md` | Headline numbers for the 233-film dataset | **Current (12 Oct 2026)** |
| `tone_analysis.md` | Tone vs accuracy, dystopia share by decade | **Current** |
| `audit_findings_v2.md` | Audit v2: line-by-line check of the 44 predictions added in the 233-film update | **Current** |
| `audit_findings.md` | Audit v1: my first check, on the 164-film version (re-score sample, recomputation, tone labels, gap vs accuracy) | Historical numbers (164 films); conclusions still hold |
| `audit/` | Audit v1 sample and scripts | Supporting |
| `wythoff_leane/findings.md` | Comparison with Wythoff & Leane (2025) | Based on the 163-film snapshot, before the expansion |
| `literature.md` | Review of 20 related studies, sites and datasets | Compares with the current 20.2% score |

Where each file mentioned in these documents sits in this repository:

| Name used in the documents | Location here |
|---|---|
| `films.csv`, `predictions.csv`, `alt_history_candidates.csv` | `data/` |
| `timeline.png` / `.pdf`, `tone_vs_accuracy.png` | `charts/` |
| `tone.json`, `stats.json`, `catastrophes.json` | `data/derived/` |
| `series/series.csv`, `series/series_timeline.png` | `data/series/`, `charts/` |
| `wythoff_leane/*.csv`, `wythoff_leane/chart*.png` | `data/wythoff_leane/`, `charts/` |
| `wythoff_leane/futuristic_fiction.csv` | Not redistributed; downloaded to `data/external/` by `src/wythoff_leane/make_wl_charts.py` |
