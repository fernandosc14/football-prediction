import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import data_prep


def test_preprocess_data_runs():
    df, features = data_prep.preprocess_data()
    assert not df.empty
    assert isinstance(features, list)
    assert all(col in df.columns for col in features)
