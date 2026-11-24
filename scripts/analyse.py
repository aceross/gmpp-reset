"""Which 2025-26 GMPP projects stayed in the April 2026 portfolio, by rating, category and cost.

Usage: python3 -I scripts/analyse.py data/raw/gmpp_2025_26.csv data/raw/gmpp_apr_2026.ods data > data/analysis_output.txt
Writes data/gmpp_matched.csv and prints the tables used in the draft.
"""
import sys
from pathlib import Path

import pandas as pd


def clean(s):
    return s.astype(str).str.replace("​", "", regex=False).str.strip()


def rating(v):
    v = str(v).strip().upper()
    if v.startswith("EXEMPT"):
        return "Exempt"
    if v in ("NAN", "", "NONE"):
        return "Not given"
    return v.title()


def parse_wlc(s):
    mid = s.astype(str).str.extract(r"Mid:\s*([\d,]+(?:\.\d+)?)", expand=False)
    raw = mid.fillna(s.astype(str))
    return pd.to_numeric(raw.str.replace(",", "", regex=False).str.strip(), errors="coerce")


def main(annual_csv, april_ods, outdir):
    a = pd.read_csv(annual_csv, encoding="utf-8-sig")
    a.columns = [c.replace("Â", "").strip() for c in a.columns]
    apr = pd.read_excel(april_ods, engine="odf")
    apr["GMPP ID"] = clean(apr["GMPP ID"])
    apr["Department"] = clean(apr["Department"])

    a["id"] = clean(a["Major Projects ID"])
    a["retained"] = a["id"].isin(set(apr["GMPP ID"]))
    # Two 2025-26 rows lack an ID; match rows without an ID on normalised name instead.
    norm = lambda s: s.astype(str).str.lower().str.replace(r"\(.*?\)", "", regex=True).str.replace(r"[^a-z0-9]", "", regex=True)
    no_id = a["Major Projects ID"].isna() | a["id"].isin(["nan", ""])
    name_hit = norm(a["Project Name"]).isin(set(norm(apr["GMPP Project Name"])))
    a.loc[no_id & name_hit, "retained"] = True
    matched_by_name = apr[norm(apr["GMPP Project Name"]).isin(set(norm(a.loc[no_id & name_hit, "Project Name"])))]
    apr_lookup = apr.set_index("GMPP ID")["GMPP Project Name"].to_dict()
    apr.loc[matched_by_name.index, "GMPP ID"] = "matched-by-name"
    print("Matched by name (no ID in 2025-26 data):", list(a.loc[no_id & name_hit, "Project Name"]))
    a["nista_dca"] = a["IPA Delivery Confidence Assessment"].map(rating)
    a["sro_dca"] = a["SRO Delivery Confidence Assessment"].map(rating)
    colours = {"Red", "Amber", "Green"}
    a["rating"] = a["nista_dca"].where(a["nista_dca"].isin(colours), a["sro_dca"])
    a["rating_source"] = "NISTA"
    a.loc[~a["nista_dca"].isin(colours), "rating_source"] = "SRO only"
    a.loc[~a["rating"].isin(colours), "rating_source"] = "No rating published"
    wlc_col = [c for c in a.columns if c.startswith("Whole Life Cost")][0]
    a["wlc_m"] = parse_wlc(a[wlc_col])
    a["any_exempt"] = a.apply(lambda r: any(str(v).startswith("Exempt") for v in r.values), axis=1)
    a["category"] = a["Annual Report Category"].str.strip()

    new_in_april = sorted(set(apr["GMPP ID"]) - set(a["id"]) - {"matched-by-name"})
    print(f"2025-26 projects: {len(a)}; April 2026 projects: {len(apr)}")
    print(f"Retained from 2025-26: {a['retained'].sum()}; new in April list: {len(new_in_april)}")
    print(apr[apr["GMPP ID"].isin(new_in_april)].to_string(index=False))

    print("\n== Missing-ID rows in 2025-26 data")
    print(a.loc[no_id, ["Project Name", "Department", "rating", "rating_source", "wlc_m", "retained"]].to_string(index=False))

    print("\n== Retained IDs with materially changed or colliding April project names")
    id_matched = a[a["id"].isin(apr_lookup)].copy()
    id_matched["april_name"] = id_matched["id"].map(apr_lookup)
    diff_mask = norm(id_matched["Project Name"]) != norm(id_matched["april_name"])
    print(id_matched.loc[diff_mask, ["id", "Project Name", "april_name"]].to_string(index=False))

    dropped_name_hits = a[(~a["retained"]) & name_hit]
    if len(dropped_name_hits):
        print("\n== Dropped 2025-26 rows whose normalised name appears in April list under another ID")
        for _, r in dropped_name_hits.iterrows():
            hits = apr[norm(apr["GMPP Project Name"]) == norm(pd.Series([r["Project Name"]])).iloc[0]]
            for _, h in hits.iterrows():
                print(f"  2025-26 {r['id']} ({r['Project Name'].strip()}) <-> April {h['GMPP ID']} ({h['GMPP Project Name']})")

    end_dt = pd.to_datetime(a["End Date"], format="%d/%m/%Y", errors="coerce")
    ended_mar26 = a[(~a["retained"]) & (end_dt <= "2026-03-31")]
    print(f"\n== Dropped projects with scheduled End Date <= 2026-03-31 ({len(ended_mar26)})")
    print(ended_mar26[["id", "Project Name", "Department", "End Date", "rating"]].to_string(index=False))

    def tab(col):
        t = pd.crosstab(a[col], a["retained"]).rename(columns={True: "kept", False: "dropped"})
        t["total"] = t.sum(axis=1)
        t["kept_pct"] = (100 * t["kept"] / t["total"]).round(0)
        return t.sort_values("total", ascending=False)

    print("\n== rating source x rating x kept")
    print(pd.crosstab([a["rating_source"], a["rating"]], a["retained"], margins=True).to_string())

    for col in ["nista_dca", "sro_dca", "rating", "rating_source", "category", "Department", "any_exempt"]:
        print(f"\n== {col}\n{tab(col).to_string()}")

    print("\n== whole-life cost (£m, rows with a number)")
    print(a.groupby("retained")["wlc_m"].describe().round(0).to_string())
    print("Sum of whole-life cost by status (£bn):")
    print((a.groupby("retained")["wlc_m"].sum() / 1000).round(1).to_string())

    red = a[a["nista_dca"] == "Red"].sort_values("wlc_m", ascending=False)
    print("\n== Red-rated projects")
    print(red[["Project Name", "Department", "category", "wlc_m", "retained"]].to_string(index=False))

    out = Path(outdir)
    a["over_1bn"] = pd.cut(a["wlc_m"], [-1, 1000, float("inf")], labels=["£1bn or less", "over £1bn"])
    a["over_1bn"] = a["over_1bn"].cat.add_categories("cost not published").fillna("cost not published")
    print("\n== cost band x kept")
    print(pd.crosstab(a["over_1bn"], a["retained"], margins=True).to_string())
    print("\n== red-rated (either source) and dropped")
    print(a[(a["rating"] == "Red") & ~a["retained"]][["Project Name", "Department", "rating_source", "wlc_m"]]
          .sort_values("wlc_m", ascending=False).to_string(index=False))
    print("\n== dropped projects with the largest whole-life cost")
    top = a[~a["retained"]].sort_values("wlc_m", ascending=False).head(12)
    print(top[["Project Name", "Department", "category", "rating", "rating_source", "wlc_m"]].to_string(index=False))
    print("\nWhole-life cost not published (dropped / kept):",
          a[~a["retained"]]["wlc_m"].isna().sum(), "/", a[a["retained"]]["wlc_m"].isna().sum())

    cols = ["id", "Project Name", "Department", "category", "nista_dca", "sro_dca", "rating", "rating_source",
            "wlc_m", "any_exempt", "retained"]
    a[cols].to_csv(
        out / "gmpp_matched.csv", index=False
    )


if __name__ == "__main__":
    main(*sys.argv[1:4])
