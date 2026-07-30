# Spain Mobility — internship 2026

Analysis of Spanish origin–destination mobility flows (MITMA OpenData Movilidad),
combined with INE income/demographic data and Foursquare POIs.

Supervisor: Esteban Moro. Original brief: [`docs/project.md`](docs/project.md).

## Layout

| path | contents |
|---|---|
| `notebooks/` | `phase01`–`phase05`, run in order |
| `scripts/` | `prep_external_data.py` (INE raw → section-level CSVs), `build_phase05.py` (headless phase05 rerun), `build_pptx.py` (deck → pptx) |
| `results/` | keyboard-navigable HTML slide decks; `phase05_results_v2.html` is current |
| `docs/` | project brief |
| `data/` | not in git — see below |

## Notebooks

| | topic |
|---|---|
| `phase01` | download, load, top origins/destinations, Madrid, temporal, first gravity model |
| `phase02` | weekday vs weekend, trip purpose |
| `phase03` | common-unit map, fixed geometry, gravity overall + by district, POIs vs population |
| `phase04` | POIs by type, gravity by age × income (4×3 grid), common-OD-pair version |
| `phase05` | income deciles, experienced income diversity/selectivity, income assortativity, unemployment |

### Current findings (phase05, March 2025: 3,792 districts, 3.36M directed OD pairs, 3.11B trips)

1. Higher-income destinations are *less* segregated — visitor mix is more balanced and closer
   to the national mix (JSD ρ≈−0.37, the stronger signal); poorer/peripheral places are the
   selective ones.
2. Mobility is income-assortative but only locally (r≈0.47 overall, ≈0.49 under 25 km,
   ≈0 beyond 100 km).
3. Evener mobility fluxes ↔ lower working-age unemployment, independent of income.

## Environment

```
conda env create -f environment.yml   # env name: spain-mobility
```

## Data

`data/` is gitignored (7.8 GB). It holds derived parquet plus small geometry/POI/INE extracts:

| dir | contents |
|---|---|
| `recent_2025-03/` | March 2025 OD parquet, plus age×income variant and OD-pair cache |
| `early_2022-01/` | January 2022 OD parquet |
| `od/` | four October weeks, 2022–2025 (activity + social parquet) |
| `covid_comparison/` | pre (Feb–Mar 2020, v1) and post (Feb–Mar 2023, v2) parquet |
| `geometries/` | MITMA district shapes, INE↔MITMA crosswalks, population |
| `poi/` | Foursquare OS Places, Spain |
| `renta/`, `demo/`, `paro/` | INE income, population/working-age, unemployment |

The raw MITMA `.csv.gz` downloads and INE `raw/` CSVs were deleted after being converted —
every one is reproducible from the parquet build steps in the notebooks and
`scripts/prep_external_data.py`.
