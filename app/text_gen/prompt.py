import pandas as pd
import json
from typing import Optional


def build_summary_for_llm(
    df: pd.DataFrame,
    num_summary: pd.DataFrame,
    cat_summary: dict,
    ts_summary: Optional[pd.DataFrame] = None,
) -> str:
    """
    Build a compact textual summary of the dataset for the LLM.
    """
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    sample_rows = df.head(5).to_dict(orient="records")

    parts = []

    parts.append("Dataset schema (column: dtype):")
    parts.append(json.dumps(schema, indent=2))

    parts.append("\nNumeric column summary:")
    if num_summary is not None and not num_summary.empty:
        parts.append(num_summary.to_string())
    else:
        parts.append("No numeric columns found.")

    parts.append("\nCategorical column top values:")
    if cat_summary:
        parts.append(json.dumps(cat_summary, indent=2))
    else:
        parts.append("No categorical columns found.")

    if ts_summary is not None and not ts_summary.empty:
        parts.append("\nTime series aggregate (first 10 rows):")
        parts.append(ts_summary.head(10).to_string())
    else:
        parts.append("\nNo time-series detected.")

    parts.append("\nSample rows (up to 5):")
    parts.append(json.dumps(sample_rows, indent=2))

    return "\n".join(parts)


def build_llm_prompt(summary_text: str) -> str:
    """
    Wrap structured dataset summary into a natural language request for insights.
    """
    prompt = (
        "You are a senior data analyst.\n\n"
        "You are given a dataset description including column types, numeric summaries, "
        "categorical distributions and sample rows.\n\n"
        "Dataset Summary:\n"
        f"{summary_text}\n\n"
        "Your tasks:\n"
        "1. Write a concise executive summary (3–5 bullet points).\n"
        "2. Highlight trends, patterns and anomalies.\n"
        "3. Identify any data quality issues visible.\n"
        "4. Suggest 3–5 business questions or next analytical steps.\n\n"
        "Write clearly for business stakeholders, no jargon, max 400 words."
    )
    return prompt
