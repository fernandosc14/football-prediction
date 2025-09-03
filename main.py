from src.api_fetch import fetch_upcoming_matches
from src.train import train_model
from src.predict import main

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
        print("Training model...")
        train_model()

    elif args.mode == "predict":
        print("Fetching upcoming matches...")
        fetch_upcoming_matches()
        print("Making predictions...")
        preds = main()
        print("Predictions: ", preds)

    elif args.mode == "full":
        print("Fetching upcoming matches...")
        fetch_upcoming_matches()
        print("Training model...")
        train_model()
        print("Making predictions...")
        preds = main()
        print("Predictions: ", preds)
