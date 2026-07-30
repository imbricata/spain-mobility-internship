---
title: "Research Project: Understanding Mobility Patterns in Spain"
author: "Esteban Moro"
project_type: "Student research onboarding"
topic: "Origin-destination matrix modeling in Spain"
country: "Spain"
duration_weeks: 9
status: "draft"
primary_language: "Python"
primary_dataset: "MITMA OpenData Movilidad"
maintainer: "Emoro"
last_updated: "2026-03-24"
---

# Research Project: Understanding Mobility Patterns in Spain

Research project using real large-scale mobility data from Spain provided by the Spanish Ministry of Transport.

This project will introduce you to:

- Urban mobility analysis
- Network science
- Spatial interaction modeling
- Data-driven research

You are **not expected to know anything about mobility data beforehand**.  
The goal is to learn step by step.

---

# 1. The Data We Will Use

## Official Data Source

The main data we will use is the Spanish Ministry of Transport mobility dataset:

- **MITMA OpenData Movilidad**  
  https://www.transportes.gob.es/ministerio/proyectos-singulares/estudios-de-movilidad-con-big-data/opendata-movilidad

This dataset provides anonymized origin-destination mobility flows derived from mobile phone data.

You can also explore related methodological documentation here: [Daily Study Documentation](https://www.transportes.gob.es/ministerio/proyectos-singulares/estudios-de-movilidad-con-big-data/estudio-basico-diario)

We will also use other datasets:

- INE (National Statistics Institute) demographic data: https://www.ine.es/ (population and socioeconomic indicators)
- Geospatial data for Spanish municipalities (e.g., from the Spanish Geographic Institute): https://www.ign.es/ (mapping and distance calculations)
- Optional: OpenStreetMap data for additional geographic information: https://www.openstreetmap.org/
- Optional: FourSquare OS Places: https://opensource.foursquare.com/os-places/

---

# 2. The Main Tool You Will Use

We will use Python to analyze the data.

We will access the data using the Python package:

- **pySpainMobility**  
  https://github.com/pySpainMobility/pySpainMobility

This package allows structured downloading, cleaning, and manipulation of the Spanish mobility datasets.

Related documentation or preprint: pySpainMobility preprint https://arxiv.org/abs/2506.13385

---

# 3. Other Python Libraries You Will Use

You will work in Python using these libraries. Don't worry if you don't know them yet; we will learn them as needed.

- pandas - https://pandas.pydata.org/
- numpy - https://numpy.org/
- geopandas - https://geopandas.org/
- matplotlib - https://matplotlib.org/
- seaborn - https://seaborn.pydata.org/
- networkx - https://networkx.org/
- scipy - https://scipy.org/

Optional (if needed):

- statsmodels - https://www.statsmodels.org/
- scikit-learn - https://scikit-learn.org/

---

# 4. Research Background (Examples of Studies Using This Data)

These data have already been used in research:

- Ponce-de-Leon et al. (2021) - COVID-19 Flow-Maps  
  https://www.nature.com/articles/s41597-021-01093-5
- Ventura-Fernandez (2025) - Inter-city mobility flows in Spain  
  https://link.springer.com/article/10.1007/s11205-025-03580-3
- Extreme heat and mobility (arXiv preprint)  
  https://arxiv.org/abs/2501.03978

You will not replicate these fully, but you will build simplified versions of similar analyses.

---

# 5. Project Roadmap

## Phase 0 - Understanding Mobility (Week 1)

Before coding, let's get familiar with the concepts and dataset. Read:

- MITMA OpenData Movilidad documentation: https://www.transportes.gob.es/ministerio/proyectos-singulares/estudio-de-movilidad-con-big-data
- Related research papers (e.g., Ponce-de-Leon et al. 2021, Ventura-Fernandez 2025)
- General concepts in mobility analysis:
  - Mobile positioning data: https://en.wikipedia.org/wiki/Mobile_positioning_data
  - Origin-destination matrices: https://www.sciencedirect.com/topics/computer-science/origin-destination-matrix
  - Gravity models: https://en.wikipedia.org/wiki/Gravity_model_of_trade (although framed for trade, it explains the core idea used in mobility)

Goal:  
Build intuition before touching the data.

---

## Phase 1 - Exploring the Data (Weeks 2-3)

You will:

- Download mobility data for one region (e.g., Madrid or Catalonia)
- Extract origin-destination flows, $T_{ij}$
- Compute:
  - Total trips
  - Top origins
  - Top destinations
- Create simple maps and bar charts

Questions:

- Which municipalities send the most trips?
- Which receive the most?
- Is mobility evenly distributed?

Deliverable:

- Clean exploratory notebook with figures

Goal:  
Become comfortable with real large-scale data.

---

## Phase 2 - Building a Mobility Network (Weeks 4-5)

Think of mobility as a network:

- Municipalities = nodes
- Trips = edges

Using `networkx`:

- Compute in-strength (attractiveness)
- Compute out-strength (emission)
- Identify top hubs
- Identify peripheral areas

Questions:

- Is Spanish mobility dominated by a few large cities?
- How central is Madrid?
- Are there regional clusters?

Deliverable:

- 4-5 page report describing network structure

Goal:  
Understand mobility as a system.

---

## Phase 3 - Fitting a Constrained Gravity Model (Weeks 6-7)

Concept:

Trips increase with population and decrease with distance, while preserving trip totals through constraints.

Baseline formula:

$$Trips_{ij} \sim \frac{Population_i \times Population_j}{Distance_{ij}^{gamma}}$$

Origin-constrained formulation (recommended for simulation):

$$T_{ij} = O_i \frac{D_j^{beta} f(c_{ij})}{\sum_k D_k^{beta} f(c_{ik})}$$

You will:

- Compute distances between municipalities
- Fit and compare:
  - Unconstrained gravity baseline (log-log model)
  - Origin-constrained gravity model (fixed origin totals)
- Estimate the distance decay parameter
- Validate model fit (predicted vs observed flows)
- Optional extension: doubly-constrained model (fixed origin and destination totals)

Questions:

- How strongly does distance limit mobility?
- Does the constrained model improve realism?
- How does imposing constraints change flow allocation?

Deliverable:

- Notebook + interpretation (including unconstrained vs constrained comparison)

Goal:  
Move from description to explanation.

---

## Phase 4 - A Simple Simulation (Weeks 8-9)

You will simulate a policy change.

Example:  
"What happens if travel between Madrid and Barcelona becomes 20% easier?"

You will:

- Modify the distance/cost matrix for a policy scenario
- Recompute predicted flows with the constrained model
- Compare before vs after
- Identify municipalities that gain or lose
- Quantify redistribution effects on non-target OD flows

Questions:

- Does mobility become more centralized?
- Do peripheral areas benefit?
- Which OD pairs lose trips when targeted corridors improve?

Deliverable:

- Visual comparison + interpretation (including spillover analysis)

Goal:  
Understand how models allow simulation of policy changes.

---

# 6. Final Research Question (Choose One)

Option A:  
How strongly does distance limit mobility in Spain?

Option B:  
Is Spanish mobility highly centralized in a few hubs?

Option C:  
How would improving connectivity between major cities reshape flows?

We will choose together based on your interests.

---

# Final Note

This project is meant to:

- Teach you how real urban data works
- Introduce you to research
- Help you think quantitatively about cities

You are not expected to know everything.

You are expected to learn.

Welcome to computational urban science.

