# Destination entropy — findings and questions for Esteban

March 2025 MITMA data, 3,742 district-level origins.

## Where we are

Computed per-origin destination entropy `H_i = -Σ p_ij ln p_ij`, where
`p_ij` is origin *i*'s share of outgoing trips going to *j*.

Raw destination counts are unusable: Madrid Centro "reaches" 3,572 districts but
50 of them carry 91% of its trips. Count correlates +0.71 with log trip volume,
so it largely measures how much data MITMA recorded.

H fixes this — correlation with log trips is −0.004, with population +0.046.

## Chose H over normalised S

`S_i = H_i / ln N_i` reintroduces a volume dependence through the denominator
(S vs log trips: −0.277; H: −0.004). This matters because income itself
correlates +0.357 with trip volume, so S's artifact works directly against the
relationship we're testing: H vs log income is +0.165, S vs log income +0.057.

Also tried normalising by *available* destinations (zones within 25 km, geometry
only). Broken as specified — numerator counts all destinations, denominator only
local ones, so values exceed 1. Would need H restricted to the same radius.

## Regression results

`H ~ ln(income) + ln(pop)`, n = 3,740, R² = 0.028
- ln(income) 0.444 (se 0.045, p < 0.001)
- ln(pop) 0.010 (se 0.011, p = 0.36)

`H ~ u + ln(income) + ln(pop)`, n = 3,269, R² = 0.031
- unemployment rate −1.056 (se 0.322, p = 0.001)
- ln(income) 0.363 (se 0.053, p < 0.001)
- ln(pop) 0.020 (se 0.012, p = 0.095)

Both predictors are the expected sign and statistically clear, but explain ~3%
of H's variation. Within-decile spread in H is more than twice the gap between
income deciles 1 and 10.

## The main finding: geography dominates

Adding district area and counts of zones within 25 km / 50 km:

| model | R² |
|---|---|
| income + population | 0.028 |
| zones within 25 km alone | 0.143 |
| district area alone | 0.018 |
| all three geographic | 0.409 |
| geographic + income + population | 0.415 |

Geography alone reaches 41%; income and population add 0.6 points on top.
Income's coefficient halves (0.444 → 0.205) and its t-statistic falls from 9.9
to 5.7 once geography is controlled.

Mechanism: H can only be high if there are many places to go. Dense metro
districts have hundreds of nearby zones and necessarily spread trips across
them; rural districts have few, so H stays low regardless of how their residents
behave. Income correlates with metro location, so part of the apparent income
effect was really urban location.

This looks like the same point as *Diversity Beyond Density* — that opportunity
structure is first-order and socioeconomic factors are second-order.

## Questions

**1. What is `N_i` in `S_i = H_i / ln N_i` — observed or available destinations?**
Observed destinations carry the volume artifact. If `N_i` is meant as available
destinations (geographic opportunity), the confound disappears, but then the
numerator needs restricting to the same set or the ratio exceeds 1.

**2. Is `P_i` in `S_i ~ I_i + P_i` population or paro?**
Assumed population. Empirically it does nothing here (coef 0.010, p = 0.36) —
because H is independent of population to begin with. It would be load-bearing
under S, which correlates −0.236 with population.

**3. Should geographic opportunity be a control or the framing?**
Options: control for zone counts and read the income coefficient; or reframe as
"given equal opportunity, does the richer district use it more diversely." The
second seems closer to the *Diversity Beyond Density* approach. Normalising by
available destinations is a third route to the same correction.

**4. Should within-district trips be included?**
The current matrix has zero self-loops, so H describes outbound travel only. A
district where most people stay put looks identical to one where everyone
commutes out. This likely drives part of the rural/urban difference. Need to
check whether the source files contain self-flows before deciding — not yet
verified.

**5. Zone size varies enormously and district area has t = 30.**
MITMA zones hold roughly equal population, so rural zones are geographically
huge and urban ones tiny. A 20 km trip crosses many zones in Madrid and stays
inside one in Soria, so "one destination" is not comparable across the country.
Standard MAUP problem, but it acts directly on the outcome variable. Is there a
preferred correction — distance-based measures, or restriction to comparable
zone types?

**6. Income is residence-based, mobility is behaviour-based.**
District mean income describes residents; trips are made by whoever is present.
Probably fine for residential origins, questionable for central business
districts.

## Data notes

- Income and population: section-level, aggregate cleanly to MITMA districts.
  Coverage 3,740 of 3,742.
- Paro: municipality-level only, and the two geographies don't nest — 925
  districts span multiple municipalities, 423 municipalities split across
  districts. Allocated municipal paro to sections by working-age share, then
  summed to districts. Rate uses working-age population as denominator.
- Paro missing for 1,555 of 8,135 municipalities. Districts touching any
  municipality with missing paro were dropped: n = 3,269 of 3,742.
- The allocation assumes uniform unemployment within municipalities, which will
  attenuate the coefficient. −1.056 is likely a floor.
- Self-loops: absent from the cached OD matrix. Source-file check pending.
