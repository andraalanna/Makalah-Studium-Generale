from pathlib import Path
import pandas as pd

from .config import DATA_RAW, OUT_TABLES, PROJECT_ROOT
from .export_pipeline import build_export_table
from .import_pipeline import build_import_table_from_year_files
from .trade_balance import build_trade_balance
from .plot_trade import plot_export_import, plot_trade_balance


def _is_missing_or_empty_csv(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        df = pd.read_csv(path)
        return df.empty or (len(df.columns) == 0)
    except Exception:
        return True


def _ensure_exports():
    out_csv = OUT_TABLES / "ekspor_ringkas_hs84_85_2020_2025.csv"
    out_xlsx = OUT_TABLES / "ekspor_ringkas_hs84_85_2020_2025.xlsx"

    # kalau sudah ada & tidak kosong → skip
    if not _is_missing_or_empty_csv(out_csv) and out_xlsx.exists():
        print("↪️ [EKSPOR] output sudah ada, skip")
        return

    print("🛠️ [EKSPOR] membangun ulang output...")

    # input ekspor (sesuaikan nama file kamu)
    f_2020_2024 = DATA_RAW / "exim_ekspor_2020_2024.xlsx"
    f_2025 = DATA_RAW / "exim_ekspor_2025.xlsx"

    if not f_2020_2024.exists() or not f_2025.exists():
        raise FileNotFoundError(
            f"File ekspor tidak lengkap. Pastikan ada:\n"
            f"- {f_2020_2024}\n- {f_2025}"
        )

    ekspor_df = build_export_table([str(f_2020_2024), str(f_2025)])

    if ekspor_df.empty:
        raise ValueError("[EKSPOR] hasil kosong. Cek reader/format file ekspor.")

    ekspor_df.to_csv(out_csv, index=False)
    ekspor_df.to_excel(out_xlsx, index=False)
    print("✅ [EKSPOR] tersimpan:", out_xlsx.name)


def _ensure_imports():
    out_csv = OUT_TABLES / "impor_ringkas_hs84_85_2020_2025.csv"
    out_xlsx = OUT_TABLES / "impor_ringkas_hs84_85_2020_2025.xlsx"

    if not _is_missing_or_empty_csv(out_csv) and out_xlsx.exists():
        print("↪️ [IMPOR] output sudah ada, skip")
        return

    print("🛠️ [IMPOR] membangun ulang output...")

    # impor per tahun: exim_impor_YYYY.xlsx ada di data/raw
    impor_files = sorted(DATA_RAW.glob("exim_impor_*.xlsx"))
    if len(impor_files) == 0:
        raise FileNotFoundError(
            "Tidak ketemu file impor per tahun. Pastikan file ada di data/raw "
            "dengan format nama: exim_impor_2020.xlsx, exim_impor_2021.xlsx, dst."
        )

    impor_df = build_import_table_from_year_files(DATA_RAW)

    if impor_df.empty:
        raise ValueError("[IMPOR] hasil kosong. Cek reader/format file impor.")

    impor_df.to_csv(out_csv, index=False)
    impor_df.to_excel(out_xlsx, index=False)
    print(" [IMPOR] tersimpan:", out_xlsx.name)


def main():
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    print("=== RUN src.main ===")
    print("DATA_RAW:", DATA_RAW)
    print("OUT_TABLES:", OUT_TABLES)

    # 1) pastikan ekspor & impor sudah ada
    _ensure_exports()
    _ensure_imports()

    # 2) load ekspor & impor
    export_df = pd.read_csv(OUT_TABLES / "ekspor_ringkas_hs84_85_2020_2025.csv")
    import_df = pd.read_csv(OUT_TABLES / "impor_ringkas_hs84_85_2020_2025.csv")

    if export_df.empty or import_df.empty:
        raise ValueError("Ekspor/Impor kosong setelah diproses. Cek output di outputs/tables/")

    # 3) build neraca
    trade_df = build_trade_balance(export_df, import_df)

    out_trade_csv = OUT_TABLES / "neraca_hs84_85_2020_2025.csv"
    out_trade_xlsx = OUT_TABLES / "neraca_hs84_85_2020_2025.xlsx"
    trade_df.to_csv(out_trade_csv, index=False)
    trade_df.to_excel(out_trade_xlsx, index=False)

    print(" Neraca perdagangan selesai:", out_trade_xlsx.name)
    print(trade_df[["year", "export_hs84_85_usd", "import_hs84_85_usd", "trade_balance_hs84_85_usd"]])

    # 4) plots
    fig_dir = PROJECT_ROOT / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    plot_export_import(trade_df, fig_dir)
    plot_trade_balance(trade_df, fig_dir)
    print(" Grafik disimpan di:", fig_dir)


if __name__ == "__main__":
    main()
