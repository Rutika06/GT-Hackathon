import pandas as pd
from io import BytesIO


def load_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Load a CSV file from raw bytes into a pandas DataFrame.
    Used by the /generate-report endpoint.
    """
    df = pd.read_csv(BytesIO(file_bytes))
    return df
