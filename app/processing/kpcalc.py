import pandas as pd


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return basic descriptive statistics for all numeric columns.
    """
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return pd.DataFrame()
    summary = df[numeric_cols].describe().T  # rows = columns, stats as columns
    return summary


def category_summary(df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    For each categorical/text column, return top N most frequent values.
    """
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    result: dict[str, dict] = {}

    for col in cat_cols:
        vc = df[col].value_counts().head(top_n)
        result[col] = vc.to_dict()

    return result


def time_series_summary(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    If there is a datetime column, aggregate numeric columns by that date
    to build simple time-series stats for plotting.
    """
    datetime_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns

    if len(datetime_cols) == 0:
        return None

    # Use the first datetime-like column
    date_col = datetime_cols[0]

    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return None

    ts = df.groupby(date_col)[numeric_cols].sum().reset_index()
    return ts
