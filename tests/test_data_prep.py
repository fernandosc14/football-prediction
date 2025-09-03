from src import data_prep

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_preprocess_data_runs():
    """Test if preprocess_data runs without errors and returns expected outputs."""
    df, features, scaler, le_league = data_prep.preprocess_data()
    assert not df.empty
    assert isinstance(features, list)
    assert all(col in df.columns for col in features)
    assert scaler is not None
    assert le_league is not None


def test_preprocess_data_returns_scaler_encoder():
    """Test if preprocess_data returns scaler and encoder when cleanup_models is False."""
    df, features, scaler, le_league = data_prep.preprocess_data()
    assert scaler is not None
    assert le_league is not None
