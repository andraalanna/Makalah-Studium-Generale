import pandas as pd

def build_trade_balance(export_df: pd.DataFrame, import_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        export_df,
        import_df,
        on="year",
        how="inner"
    )

    # Neraca perdagangan
    df["trade_balance_hs84_85_usd"] = (
        df["export_hs84_85_usd"] - df["import_hs84_85_usd"]
    )

    return df.sort_values("year").reset_index(drop=True)
