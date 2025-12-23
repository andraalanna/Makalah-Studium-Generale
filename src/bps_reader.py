import pandas as pd


def _find_total_column_export(df: pd.DataFrame) -> str:
    # Cari kolom yang baris 0-nya "Totals" (biasanya kolom grand total)
    for col in reversed(df.columns):
        if str(df.loc[0, col]).strip().lower() == "totals":
            return col
    return df.columns[-1]


def extract_export_hs84_85(excel_path: str) -> pd.DataFrame:

    df = pd.read_excel(excel_path)

    hs_col = df.columns[0]
    year_col = df.columns[1]
    total_col = _find_total_column_export(df)

    df["year"] = pd.to_numeric(df[year_col], errors="coerce")
    df["value_usd"] = pd.to_numeric(df[total_col], errors="coerce")

    # forward-fill HS desc supaya baris tahun 2021-2024 ikut kebaca
    df["hs_desc_ffill"] = df[hs_col].ffill()
    df["hs_code"] = df["hs_desc_ffill"].astype(str).str.extract(r"^\[(\d+)\]")

    out = df.dropna(subset=["year", "value_usd", "hs_code"]).copy()
    out["year"] = out["year"].astype(int)

    # Filter HS 84/85
    out = out[out["hs_code"].isin(["84", "85"])]

    return out[["year", "hs_code", "value_usd"]]

def _find_totals_column(df: pd.DataFrame) -> str:
    for col in df.columns:
        if str(df.loc[0, col]).strip().lower() == "totals":
            return col
    return df.columns[-1]
import pandas as pd

def extract_import_totals_per_year_file(excel_path: str) -> pd.DataFrame:
    """
    Untuk file impor 1 tahun (exim_impor_YYYY.xlsx) yang punya kolom 'Totals' di paling kanan.
    Output: hs_code | value_usd
    """
    df = pd.read_excel(excel_path)

    hs_col = df.columns[0]  # "Kode HS"
    totals_col = None

    # cari kolom yang baris 0-nya "Totals" (di file kamu ada di kolom terakhir)
    for c in df.columns:
        v = df.at[0, c]
        if isinstance(v, str) and v.strip().lower() == "totals":
            totals_col = c
            break

    if totals_col is None:
        raise ValueError("Kolom 'Totals' tidak ditemukan di baris header (row 0).")

    hs_str = df[hs_col].astype(str).fillna("").str.strip()

    rows = df[hs_str.str.startswith("[84]") | hs_str.str.startswith("[85]")].copy()
    if rows.empty:
        raise ValueError("Tidak ketemu baris [84] / [85].")

    rows["hs_code"] = rows[hs_col].astype(str).str.extract(r"^\[(\d+)\]")
    rows["value_usd"] = pd.to_numeric(rows[totals_col], errors="coerce")

    out = rows[["hs_code", "value_usd"]].dropna()
    out = out[out["hs_code"].isin(["84", "85"])].groupby("hs_code", as_index=False)["value_usd"].max()
    return out
