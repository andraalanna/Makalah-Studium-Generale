import re
import pandas as pd
from pathlib import Path
from .bps_reader import extract_import_totals_per_year_file


def _extract_year_from_filename(name: str) -> int | None:
    m = re.search(r"(19|20)\d{2}", name)
    return int(m.group()) if m else None


def build_import_table_from_year_files(data_raw_dir: Path) -> pd.DataFrame:
    files = sorted(data_raw_dir.glob("exim_impor_*.xlsx"))
    frames = []

    for f in files:
        y = _extract_year_from_filename(f.name)
        if y is None:
            continue

        df = extract_import_totals_per_year_file(str(f))  # hs_code, value_usd
        df["year"] = y

        pivot = df.pivot(index="year", columns="hs_code", values="value_usd").reset_index()

        if "84" not in pivot.columns:
            pivot["84"] = 0
        if "85" not in pivot.columns:
            pivot["85"] = 0

        pivot = pivot.rename(columns={"84": "import_hs84_usd", "85": "import_hs85_usd"})
        pivot["import_hs84_85_usd"] = pivot["import_hs84_usd"] + pivot["import_hs85_usd"]

        frames.append(pivot)

    if not frames:
        raise FileNotFoundError("Tidak nemu file exim_impor_YYYY.xlsx di data/raw")

    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset=["year"], keep="last").sort_values("year").reset_index(drop=True)
    return out
