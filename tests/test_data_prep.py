from src import data_prep

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_preprocess_data_runs():
    """Test that data preprocessing runs and returns expected outputs."""
    df, features = data_prep.preprocess_data()
    assert not df.empty
    assert isinstance(features, list)
    assert all(col in df.columns for col in features)
