# Spain Mobility & Socioeconomic Segregation

Empirical analysis of Spanish origin–destination mobility flows (MITMA OpenData Movilidad, 3.11B trips across 3,792 districts and 3.36M directed OD pairs), linked with census-section income & demographics (INE), registered unemployment (SEPE), and points of interest (Foursquare OS Places).

Research internship at Northeastern University (supervised by Prof. Esteban Moro). Original brief: [`docs/project.md`](docs/project.md).

## Key Findings

1. **Experienced income diversity vs. segregation:** Higher-income destinations exhibit *more* balanced visitor income distributions and lower divergence from the national baseline (Jensen–Shannon divergence $\rho \approx -0.37$); lower-income and peripheral districts are the most socioeconomically selective.
2. **Distance-decayed income assortativity:** Mobility is strongly income-assortative at short range ($r \approx 0.49$ under 25 km, representing ~90% of trips) and decays toward zero beyond 100 km. Both log-OLS and Poisson Pseudo-Maximum Likelihood (PPML) gravity specifications confirm significant friction in cross-income travel controlling for physical distance.
3. **Destination entropy & unemployment:** Higher Shannon entropy and Pielou evenness of outgoing resident mobility fluxes correlate with lower working-age unemployment ($\rho \approx -0.15$), independent of district income.

## Repository Layout

| Path | Description |
|---|---|
| `notebooks/` | `phase01`–`phase05` and `entropy.ipynb` (spatial entropy, JSD, and gravity decompositions) |
| `scripts/` | `prep_external_data.py` (INE/SEPE ingestion), `gravity_income.py` (OLS & PPML gravity models with income distance), `eda_plots.py`, `build_phase05.py`, `build_pptx.py` |
| `results/` | Self-contained HTML presentation decks (`phase05_results_v2.html` is the latest) |
| `docs/` | Project brief and research questions |
| `data/` | Git-ignored (~7.8 GB of derived MITMA parquet, geometries, POI, and INE/SEPE tables) |

## Notebooks

| Notebook | Scope |
|---|---|
| `phase01` | MITMA OD ingestion, top corridors, Madrid spatial structure, temporal profiles, baseline gravity model |
| `phase02` | Weekday vs. weekend dynamics and trip purpose decomposition |
| `phase03` | v1 (2020) vs. v2 (2023) zone harmonization, common-unit crosswalks, district-level gravity, POI scaling |
| `phase04` | POI category breakdown and 4×3 age × income stratified gravity elasticities |
| `phase05` | Census-section income deciles, experienced income diversity (Shannon entropy & JSD), assortativity, unemployment |
| `entropy` | Normalized spatial entropy within reachable radius ($S_{50}$), destination selectivity, and robustness checks |

## Environment & Reproducibility

```bash
conda env create -f environment.yml   # creates env: spain-mobility
conda activate spain-mobility
python scripts/prep_external_data.py
```

### Data Layout (`data/`, git-ignored)

| Directory | Contents |
|---|---|
| `recent_2025-03/` | March 2025 district OD parquet, age × income tables, and OD-pair cache |
| `early_2022-01/` | January 2022 district OD parquet |
| `od/` | October benchmark weeks across 2022–2025 (activity & sociodemographic parquet) |
| `covid_comparison/` | Pre-COVID (Feb–Mar 2020, v1) and post-COVID (Feb–Mar 2023, v2) OD parquet |
| `geometries/` | MITMA district polygons, INE↔MITMA crosswalks, and population weights |
| `poi/` | Foursquare OS Places extracts for Spain |
| `renta/`, `demo/`, `paro/` | INE census-section income & age structure (2023), SEPE municipal unemployment (Mar 2025) |
