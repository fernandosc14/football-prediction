import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from .data_prep import preprocess_data

def train_model():

    df = pd.read_csv('data/processed/matches.csv')

    return