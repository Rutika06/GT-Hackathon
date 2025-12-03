import pandas as pd


def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Try to parse any column that looks like a date/time into datetime.
    Leaves other columns unchanged.
    """
    for col in df.columns:
        col_lower = col.lower()
        if "date" in col_lower or "time" in col_lower or "timestamp" in col_lower:
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                # If parsing fails, just skip that column
                pass
    return df


def merge_on_common_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Optional helper: if you later ingest multiple data sources,
    this can merge them on shared column names.
    """
    common_cols = list(set(df1.columns) & set(df2.columns))
    if not common_cols:
        # No common keys → just return first df for now
        return df1

    merged = df1.merge(df2, on=common_cols, how="left", suffixes=("", "_src2"))
    return merged
