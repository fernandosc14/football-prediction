from src.api_fetch import main as update_historical_data
from src.train import train_model
from src.predict import main as run_predictions

import argparse

"""
python main.py --mode train
python main.py --mode predict
python main.py --mode full
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "predict", "full"], required=True)
    args = parser.parse_args()

    if args.mode == "train":
        print("Updating historical data...")
        update_historical_data()
        print("Training model...")
        train_model()

    elif args.mode == "predict":
        print("Making predictions...")
        preds = run_predictions()
        print("Predictions: ", preds)

    elif args.mode == "full":
        print("Updating historical data...")
        update_historical_data()
        print("Training model...")
        train_model()
        print("Making predictions...")
        preds = run_predictions()
        print("Predictions: ", preds)
