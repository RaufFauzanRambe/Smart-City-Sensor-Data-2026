import pandas as pd
from functools import reduce
from typing import Dict
import logging

try:
    import swifter  # optional for faster apply
    SWIFTER_AVAILABLE = True
except ImportError:
    SWIFTER_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def preprocess_timestamp(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
    """
    Convert timestamp column to datetime, drop invalids, and sort.
    Auto-detect timestamp if not found.
    """
    if timestamp_col not in df.columns:
        # Try to find a datetime-like column automatically
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                timestamp_col = col
                logging.info(f"Auto-detected timestamp column: {col}")
                break
    if timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
        df = df.dropna(subset=[timestamp_col])
        df = df.sort_values(timestamp_col).reset_index(drop=True)
    else:
        logging.warning(f"Timestamp column '{timestamp_col}' not found.")
    return df

def clean_numeric(df: pd.DataFrame, force_convert: bool = True) -> pd.DataFrame:
    """
    Convert numeric-like columns to float. Use swifter if available for large datasets.
    """
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
    if force_convert:
        for col in df.select_dtypes(include=['object']).columns:
            try:
                sample = df[col].dropna().sample(min(10, len(df[col].dropna())))
                if sample.apply(lambda x: pd.to_numeric(x, errors='coerce')).notna().all():
                    numeric_cols.append(col)
            except ValueError:
                continue
    for col in numeric_cols:
        if SWIFTER_AVAILABLE:
            df[col] = df[col].swifter.apply(pd.to_numeric, errors='coerce')
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def merge_datasets(datasets: Dict[str, pd.DataFrame], on: list = None, how: str = 'outer') -> pd.DataFrame:
    """
    Merge multiple datasets dynamically. Automatically uses ['timestamp','location'] if on=None.
    Skips empty datasets.
    """
    if not datasets:
        logging.warning("No datasets provided for merging.")
        return pd.DataFrame()
    if on is None:
        on = ['timestamp','location']
    valid_dfs = [df for df in datasets.values() if not df.empty]
    if not valid_dfs:
        logging.warning("All datasets are empty.")
        return pd.DataFrame()
    merged = reduce(lambda left, right: pd.merge(left, right, on=on, how=how), valid_dfs)
    logging.info(f"Merged {len(valid_dfs)} datasets on {on} with '{how}' join.")
    return merged

def preprocess_all(datasets: Dict[str, pd.DataFrame], timestamp_col='timestamp') -> Dict[str, pd.DataFrame]:
    """
    Preprocess all datasets: timestamp + numeric conversion.
    """
    processed = {}
    for name, df in datasets.items():
        logging.info(f"Processing dataset: {name}")
        df = preprocess_timestamp(df, timestamp_col)
        df = clean_numeric(df)
        processed[name] = df
    return processed
