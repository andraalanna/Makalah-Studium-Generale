import pandas as pd
from .bps_reader import extract_export_hs84_85


def build_export_table(paths: list[str]) -> pd.DataFrame:
    frames = [extract_export_hs84_85(p) for p in paths]
    data = pd.concat(frames, ignore_index=True)

    # Hindari duplikat (kalau ada overlap tahun)
    data = data.drop_duplicates(subset=["year", "hs_code"], keep="last")

    # Pivot jadi kolom HS84 & HS85
    detail = (
        data.groupby(["year", "hs_code"], as_index=False)["value_usd"]
        .sum()
        .sort_values(["year", "hs_code"])
    )

    pivot = detail.pivot(index="year", columns="hs_code", values="value_usd").reset_index()
    pivot = pivot.rename(columns={
        "84": "export_hs84_usd",
        "85": "export_hs85_usd",
    })

    pivot["export_hs84_85_usd"] = pivot["export_hs84_usd"].fillna(0) + pivot["export_hs85_usd"].fillna(0)
    pivot = pivot.sort_values("year").reset_index(drop=True)

    return pivot
