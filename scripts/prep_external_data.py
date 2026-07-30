"""Clean the externally-downloaded INE (renta, population) and SEPE (paro) files
into tidy per-area tables that phase05 can load directly.

Run from data/ after the raw downloads complete:
    python prep_external_data.py

Outputs (all in data/):
    renta/renta_seccion_2023.csv   seccion_ine, renta_persona   (net income EUR/person/yr, 2023)
    demo/pop_seccion_2023.csv      seccion_ine, poblacion        (persons, 2023)
    paro/paro_municipios_2025-03.csv  municipio_ine, total_paro  (registered unemployed, Mar 2025)
"""
import glob
import pandas as pd

DATA = "/Users/theocoronges/Documents/internship2026/data"


def _int_es(s):
    """INE 'Total' strings use '.' as thousands sep ('20.516' -> 20516). Blank/'.'/'-' -> NaN."""
    return pd.to_numeric(s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                         errors="coerce")


def prep_renta():
    frames = []
    for f in glob.glob(f"{DATA}/renta/raw/*.csv"):
        frames.append(pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str))
    r = pd.concat(frames, ignore_index=True)
    r.columns = [c.strip() for c in r.columns]
    ind = "Indicadores de renta media y mediana"
    r = r[(r[ind] == "Renta neta media por persona") &
          (r["Periodo"] == "2023") &
          r["Secciones"].notna() & (r["Secciones"].str.strip() != "")].copy()
    r["seccion_ine"] = r["Secciones"].str.split().str[0]
    r["renta_persona"] = _int_es(r["Total"])
    out = (r[["seccion_ine", "renta_persona"]]
           .dropna(subset=["seccion_ine"]).drop_duplicates("seccion_ine")
           .sort_values("seccion_ine"))
    out.to_csv(f"{DATA}/renta/renta_seccion_2023.csv", index=False)
    print(f"renta: {len(out):,} sections  "
          f"({out['renta_persona'].notna().sum():,} with a value, "
          f"{out['renta_persona'].isna().sum():,} suppressed)")


def prep_pop():
    frames = []
    for f in glob.glob(f"{DATA}/demo/raw/*.csv"):
        frames.append(pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str))
    d = pd.concat(frames, ignore_index=True)
    d.columns = [c.strip() for c in d.columns]
    ind = "Indicadores demográficos"
    d = d[(d[ind] == "Población") &
          (d["Periodo"] == "2023") &
          d["Secciones"].notna() & (d["Secciones"].str.strip() != "")].copy()
    d["seccion_ine"] = d["Secciones"].str.split().str[0]
    d["poblacion"] = _int_es(d["Total"])
    out = (d[["seccion_ine", "poblacion"]]
           .dropna(subset=["seccion_ine"]).drop_duplicates("seccion_ine")
           .sort_values("seccion_ine"))
    out.to_csv(f"{DATA}/demo/pop_seccion_2023.csv", index=False)
    print(f"pop:   {len(out):,} sections  "
          f"(total pop {out['poblacion'].sum():,.0f})")


def prep_workingage():
    """Working-age (18-64) population per section = pop * (1 - %under18 - %65+).
    Gives a proper unemployment-rate denominator instead of total population."""
    frames = []
    for f in glob.glob(f"{DATA}/demo/raw/*.csv"):
        frames.append(pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str))
    d = pd.concat(frames, ignore_index=True)
    d.columns = [c.strip() for c in d.columns]
    ind = "Indicadores demográficos"
    d = d[(d["Periodo"] == "2023") &
          d["Secciones"].notna() & (d["Secciones"].str.strip() != "")].copy()
    d["seccion_ine"] = d["Secciones"].str.split().str[0]
    keep = {"Población": "pob", "Porcentaje de población menor de 18 años": "p_u18",
            "Porcentaje de población de 65 y más años": "p_o65"}
    d = d[d[ind].isin(keep)].copy()
    d["val"] = d["Total"]
    wide = d.pivot_table(index="seccion_ine", columns=ind, values="val", aggfunc="first")
    wide = wide.rename(columns=keep)
    wide["pob"] = _int_es(wide["pob"])
    for c in ["p_u18", "p_o65"]:
        wide[c] = pd.to_numeric(wide[c].str.replace(",", ".", regex=False), errors="coerce")
    wide["wa_share"] = (100 - wide["p_u18"] - wide["p_o65"]).clip(lower=0) / 100
    wide["working_age_pop"] = wide["pob"] * wide["wa_share"]
    out = wide[["working_age_pop"]].dropna().reset_index().sort_values("seccion_ine")
    out.to_csv(f"{DATA}/demo/workingage_seccion_2023.csv", index=False)
    print(f"work-age: {len(out):,} sections  (18-64 pop {out['working_age_pop'].sum():,.0f})")


def prep_paro():
    p = pd.read_csv(f"{DATA}/paro/Paro_por_municipios_2025_csv.csv",
                    sep=";", encoding="latin1", skiprows=1, dtype=str)
    p.columns = [c.strip() for c in p.columns]
    p = p[p["Código mes"] == "202503"].copy()
    p["municipio_ine"] = p["Codigo Municipio"].str.strip()
    p["total_paro"] = pd.to_numeric(p["total Paro Registrado"], errors="coerce")
    out = (p[["municipio_ine", "total_paro"]]
           .dropna(subset=["municipio_ine"]).drop_duplicates("municipio_ine")
           .sort_values("municipio_ine"))
    out.to_csv(f"{DATA}/paro/paro_municipios_2025-03.csv", index=False)
    print(f"paro:  {len(out):,} municipios  (total unemployed {out['total_paro'].sum():,.0f})")


if __name__ == "__main__":
    prep_renta()
    prep_pop()
    prep_workingage()
    prep_paro()
