# Beyond Forecast Skill

**Data and code accompanying _Beyond Forecast Skill: Two Decades of Data-Driven Prediction of Weather and Climate Extremes (2006–2025)_.**

**Journal:** companion materials for submission to [Atmospheric Research](https://www.sciencedirect.com/journal/atmospheric-research).

This repository supports inspection of the review's bibliometric results and task-level evidence synthesis. It provides the English manuscript, Supplementary Information, processed analysis inputs and three executable scripts.

The review follows data-driven prediction of weather and climate extremes, including heavy precipitation, heatwaves, drought and storms/cyclones, together with linked hydrological, marine and impact applications. Evidence is organized by forecast target, input availability, target interval and validation design. Reported predictive skill can therefore be assessed alongside the conditions under which it was evaluated.

**Version:** manuscript and supplement archived on 18 November 2026; WoS search and citation snapshot dated 13 October 2026; companion deposit prepared on 19 November 2026.

## Start here

- **Read the study:** [`paper/manuscript.pdf`](paper/manuscript.pdf) and [`paper/supplementary.pdf`](paper/supplementary.pdf).
- **Check the numerical results:** run `python3 code/recompute.py`; this requires only Python's standard library.
- **Inspect individual evidence:** `data/cases.csv` links 30 selected studies to their DOI, source availability, section/table locators, validation design, input availability and reported results.
- **Inspect native analyses:** `code/native.R` reruns Bibliometrix thematic analyses and R co-citation calculations and exports the preserved VOSviewer inputs.

## Data and code availability

The processed bibliometric data, task-level evidence tables and network inputs supporting this review are publicly available in [`data/`](data/). The analysis scripts and software requirements are provided in [`code/`](code/) and [`requirements.txt`](requirements.txt). Source studies are identified by DOI and evidence locators in the released tables. The scripts reproduce the analyses specified below from the frozen processed inputs.

The source literature was retrieved from the Web of Science Core Collection on 13 October 2026. Third-party full-record/cited-reference exports and article full texts are outside this deposit; access to those original materials remains subject to the respective providers' access and reuse terms. The search query, retrieval date, identifiers and evidence locators supplied here document how to locate the source material. Database contents and citation counts may change after the frozen retrieval date.

**Fixed submission snapshot:** [data](https://github.com/xiashupei4-sketch/extreme-weather-prediction-review/tree/8b81fc3763b9442580d6b2a5515412df139f3bb1/data), [code](https://github.com/xiashupei4-sketch/extreme-weather-prediction-review/tree/8b81fc3763b9442580d6b2a5515412df139f3bb1/code) and [manuscript/supplement](https://github.com/xiashupei4-sketch/extreme-weather-prediction-review/tree/8b81fc3763b9442580d6b2a5515412df139f3bb1/paper). These links identify the exact deposited research materials independently of later README updates. The full commit identifier is `8b81fc3763b9442580d6b2a5515412df139f3bb1`. File integrity can be checked against `SHA256SUMS` in that snapshot.

## Reproduce the core results

From the repository directory, using Python 3.9 or later:

```sh
python3 code/recompute.py
```

The script first verifies `SHA256SUMS`, then rebuilds the tables below in `results/`. Its summary should report **4,690 broad-corpus units, 1,344 strict candidates, 30 purposive cases, 9 cases with chronological holdout and 17 records with numeric target intervals**. The four period totals are **34, 98, 676 and 3,882**. Reconciled local citations sum to **17,114**.

| Evidence to inspect | Released input | Rebuilt output or entry point |
|---|---|---|
| Publication and citation patterns | `data/corpus.csv` | `results/annual-reconciled.csv` |
| Method-family attention across periods | `data/corpus.csv` | `results/method-family-period.csv` |
| Hazard-specific method mentions in strict candidates | `data/corpus.csv` | `results/strict-hazard-method.csv`; `results/strict-hazard-method-by-period.csv` |
| Validation designs in the task dossier | `data/cases.csv` | `results/figure10-source.csv` |
| Reported target intervals and conditional targets | `data/target-intervals.csv` | `code/figures.py` |
| Method mentions versus implemented model roles | `data/model-roles.csv` | 26 source-checked model entries across eight purposively selected cases |
| Thematic organization and evolution | Cleaned keywords in `data/corpus.csv` | `code/native.R` |
| Citation and keyword networks | `data/networks.json` | `code/native.R`; preserved VOSviewer map/network inputs |

For optional numerical redraws:

```sh
python3 -m pip install -r requirements.txt
python3 code/figures.py
```

This produces four PDF panels for method-period shares, hazard-method shares, case validation and target intervals. These are data-driven inspection plots. The manuscript PDFs preserve the final native layouts and assembled figures. Generated outputs are excluded from version control.

### Native R and VOSviewer analysis

The verified environment used **R 4.5.3, Bibliometrix 5.5.0, igraph 2.3.4 and jsonlite**. With these packages installed:

```sh
Rscript code/native.R
```

Outputs in `results/native/` include four period-specific thematic maps, thematic-evolution nodes/edges, co-citation community assignments and coordinates, the preserved VOSviewer input pairs, and the R session information.

- **Bibliometrix:** cleaned author keywords (`DE`); four five-year periods; thematic maps use `n=100`, minimum frequency 2 for periods with fewer than 100 documents and 5 otherwise; seed 1234. Thematic evolution uses boundaries 2010/2015/2020, `n=100`, `minFreq=2` and seed 1234.
- **Co-citation calculation in R:** all 60 reference labels; association-strength edge weights; Louvain clustering and Fruchterman–Reingold layout with seed 20261112, using 3,000 layout iterations.
- **Native rendering in VOSviewer 1.6.21:** open the paired `keyword-map.txt` / `keyword-network.txt` or `cocitation-map.txt` / `cocitation-network.txt` exported by the R script. Archived exports used scale 1.15, label-size variation 0.25, maximum label length 80 and at most 160 keyword or 42 co-citation lines. VOSviewer handled native rendering and label-overlap suppression; the co-citation communities and initial coordinates came from R.

### Verification against the frozen research archive

Before deposition, the five rebuilt numerical tables were compared with their archived counterparts and agreed in every cell. The native rerun reproduced all four archived thematic-map cluster tables, all **19 thematic-evolution nodes and 38 links**, and the co-citation communities and coordinates. The full co-citation network contains **1,399 edges**, with communities of **18, 21 and 21 references** and modularity **0.3182**. The coupling display retains **40 nodes and 80 edges**; 31 node titles contain “susceptibility” or “susceptible”.

## Data provenance and study units

The study searched **SCI-EXPANDED, Web of Science Core Collection, on 13 October 2026**, for English-language articles published in 2006–2025:

```text
TS=((CNN OR LSTM OR GRU OR Transformer OR Mamba OR "state space model" OR ConvLSTM OR "Random Forest" OR XGBoost OR "Support Vector Machine" OR SVM OR ARIMA OR SARIMA) AND ("extreme weather" OR "extreme climate event*" OR "heavy precipitation" OR "heavy rainfall" OR heatwave* OR "heat wave" OR drought* OR flood* OR wildfire* OR storm* OR cyclone*) AND (forecast* OR prediction OR regression)) AND PY=(2006-2025) AND LA=(English) AND DT=(Article)
```

The frozen export contains 5,085 unique accession numbers. Screening and exact normalized-DOI consolidation yielded the **4,690-unit broad bibliometric corpus**: 4,669 DOI groups and 21 UT-only units. The retained representative supplies the metadata and citation counts for each DOI group. Eligibility follows exported publication year (`PY`); early-access dates are treated separately in sensitivity analysis.

The **1,344-unit strict forward-forecasting subset**, the **61-paper high-citation sensitivity benchmark**, and the **30-case purposive dossier** answer different questions. Their denominators are kept separate. External representative methodological studies discussed in the manuscript are not added to the frozen corpus. Full screening, consolidation and sensitivity methods are described in the Supplementary Information.

### Reading the released data

| Field or file | Interpretation |
|---|---|
| `ut`, `doi`, `year`, `period` | Retained WoS accession, DOI where available, exported publication year and five-year period |
| `global_citations`, `local_citations` | Frozen WoS global citations and reconciled within-corpus local citations; neither is a live citation count |
| `strict_candidate` | Binary membership in the strict candidate subset |
| Four method-family columns | Binary title/abstract mention flags; several families may occur in one paper |
| Six hazard columns | Overlapping hazard flags populated for strict candidates |
| `keywords_clean` | Frozen normalized author-keyword strings used by the native thematic analyses |
| `AU`, `TI`, `SO`, `SR`, `DB` | Bibliographic fields required by native Bibliometrix functions: authors, title, journal, document label and database |
| Case `validation_code` | C: chronological holdout; R: random/shuffled; P: other partition with unclear order; X: cross-validation as the main test; U: allocation unreported; V: source not verified |
| Target-interval `hours`, `kind` | Semicolon-separated reported intervals; `conditional` identifies simulated/supplied future conditions; `one-step` identifies next-frame prediction |
| `data/networks.json` | Co-citation matrix/settings, native VOSviewer inputs, displayed coupling nodes/edges, country collaboration links and entity rankings |

Method mentions measure research attention. Actual model roles are checked separately in `model-roles.csv`; predictive comparisons require matching the task, inputs, lead time and validation conditions. Reported target intervals do not by themselves establish operational warning time, and range endpoints do not establish testing at every intermediate lead. Country collaboration links describe author-affiliation locations, rather than study locations.

## Evidence status and reproduction boundary

The screening procedures, audit design, verification status and unresolved decisions are documented in the manuscript’s Materials and Methods and the Supplementary Information. The audit and purposive case dossier support traceable evidence checks but do not estimate population screening accuracy. The incomplete control-query archive supports the reported within-archive comparisons; it does not establish full-query omission rates or temporal trend robustness.

The executable release begins at the **frozen processed coding layer**. It reproduces the numerical summaries and native analyses described above. Raw-record screening, primary-paper reading, title/abstract term extraction, cited-reference reconciliation and the complete sensitivity audit are upstream procedures documented in the paper and supplement; they are not rerun by these three scripts.

Raw WoS full-record/cited-reference exports and downloaded article full texts are omitted from this deposit. Source studies can be located using the supplied DOIs and evidence locators; repeating the database search requires access through Web of Science. A live search or citation lookup may differ from the frozen snapshot. Additional licensing terms have not been assigned to this deposit.

The repository intentionally contains only the manuscript, supplement, five processed input files, three scripts and essential repository metadata. It excludes drafts, private screening tables, local logs and installed software.
