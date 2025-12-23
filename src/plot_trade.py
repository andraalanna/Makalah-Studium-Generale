import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def plot_export_import(df: pd.DataFrame, out_dir: Path):
    plt.figure()
    plt.plot(df["year"], df["export_hs84_85_usd"])
    plt.plot(df["year"], df["import_hs84_85_usd"])
    plt.xlabel("Year")
    plt.ylabel("Value (USD)")
    plt.title("Export vs Import of Electronics (HS 84–85)")
    plt.legend(["Export", "Import"])
    plt.grid(True)

    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / "export_vs_import_hs84_85.png", dpi=300)
    plt.close()


def plot_trade_balance(df: pd.DataFrame, out_dir: Path):
    plt.figure()
    plt.plot(df["year"], df["trade_balance_hs84_85_usd"])
    plt.xlabel("Year")
    plt.ylabel("Value (USD)")
    plt.title("Trade Balance of Electronics (HS 84–85)")
    plt.grid(True)

    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / "trade_balance_hs84_85.png", dpi=300)
    plt.close()
