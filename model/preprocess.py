"""Data preprocessing utilities."""
import logging
from typing import Optional

import pandas as pd

from .config import PREPROCESSING_CONFIG

logger = logging.getLogger(__name__)

DROP_COLS = PREPROCESSING_CONFIG["drop_columns"]
BINARY_MAP = PREPROCESSING_CONFIG["binary_map"]
ONEHOT_COL = PREPROCESSING_CONFIG["onehot_columns"]


def preprocess(
    df: pd.DataFrame,
    feature_columns: Optional[list[str]] = None,
) -> pd.DataFrame:
    """Preprocess airline satisfaction data.
    
    Args:
        df: Input dataframe
        feature_columns: Columns to align output with (for inference)
        
    Returns:
        Preprocessed dataframe with proper features
    """
    df = df.copy()
    
    # Drop unnecessary columns
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = df.drop(columns=[c for c in ["satisfaction"] if c in df.columns])
    
    # Binary encoding
    for col, true_value in BINARY_MAP.items():
        df[col] = (df[col] == true_value).astype(int)
    
    # One-hot encoding
    df = pd.get_dummies(df, columns=ONEHOT_COL, drop_first=True)
    
    # Convert boolean columns to int
    bool_cols = df.select_dtypes(include="bool").columns
    df[bool_cols] = df[bool_cols].astype(int)
    
    # Align with expected features (for prediction)
    if feature_columns is not None:
        df = df.reindex(columns=feature_columns, fill_value=0)
    
    return df
