import os
import csv
import time
import argparse
import numpy as np
from tensorflow.keras.models import load_model

from ..training.preprocess import load_data
from ..training.fuzzy import fuzzy_decision
from .capture import capture_packets


# =================================
# Load model
# =================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE, "models", "ids_model.h5")

model = load_model(MODEL_PATH)


# =================================
# Logger
# =================================
def log_decision(risk):
    with open("src/results/logs.csv", "a", newline="") as f:
        csv.writer(f).writerow([risk])


# =================================
# REPLAY MODE (dataset simulation)
# =================================
def run_replay():
    print("▶ Dataset Replay Mode\n")

    _, X_test, _, _ = load_data("data/")

    for x in X_test[:10000]:
        prob = model.predict(x.reshape(1, -1))[0][0]
        risk = fuzzy_decision(prob)

        print("Risk:", risk)
        log_decision(risk)

        time.sleep(0.05)


# =================================
# LIVE MODE (real packets)
# =================================
def process_packet(features):
    features = np.pad(features, (0, 77-len(features)))[:77]

    prob = model.predict(features.reshape(1, -1))[0][0]
    risk = fuzzy_decision(prob)

    print("Risk:", risk)
    log_decision(risk)


def run_live():
    print("▶ Live Capture Mode\n")
    capture_packets(process_packet)


# =================================
# CLI toggle
# =================================
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["replay", "live"], default="replay")
args = parser.parse_args()

if args.mode == "live":
    run_live()
else:
    run_replay()
