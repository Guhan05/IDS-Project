import os
import csv
import time
import argparse
import numpy as np
from datetime import datetime
from tensorflow.keras.models import load_model

from ..training.preprocess import load_data
from ..training.fuzzy import fuzzy_decision
from .capture import capture_packets


# =================================================
# PATHS
# =================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE, "models", "ids_model.h5")
LOG_PATH = os.path.join(BASE, "results", "logs.csv")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


# =================================================
# LOAD MODEL
# =================================================
print("🔹 Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded\n")


# =================================================
# LOGGER  ⭐ FULL DETAILS
# =================================================
def log_event(src, dst, proto, prob, risk, mode):
    write_header = not os.path.exists(LOG_PATH)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "time",
                "mode",
                "src_ip",
                "dst_ip",
                "protocol",
                "probability",
                "risk"
            ])

        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            mode,
            src,
            dst,
            proto,
            round(float(prob), 4),
            risk
        ])


# =================================================
# REPLAY MODE (fake IPs for simulation)
# =================================================
def run_replay():
    print("▶ Dataset Replay Mode\n")

    _, X_test, _, _ = load_data("data/")

    for i, x in enumerate(X_test[:10000]):

        prob = model.predict(x.reshape(1, -1), verbose=0)[0][0]
        risk = fuzzy_decision(prob)

        # fake info for demo
        src = f"192.168.1.{i%255}"
        dst = "10.0.0.1"
        proto = "TCP"

        print(f"[REPLAY] {risk} ({prob:.3f})")

        log_event(src, dst, proto, prob, risk, "replay")

        time.sleep(0.05)


# =================================================
# LIVE MODE (real packet capture)
# =================================================
def process_packet(features, src_ip, dst_ip, proto):
    features = np.pad(features, (0, 77 - len(features)))[:77]

    prob = model.predict(features.reshape(1, -1), verbose=0)[0][0]
    risk = fuzzy_decision(prob)

    print(f"[LIVE] {src_ip} → {dst_ip} | {risk}")

    log_event(src_ip, dst_ip, proto, prob, risk, "live")


def run_live():
    print("▶ Live Capture Mode\n")
    capture_packets(process_packet)


# =================================================
# CLI
# =================================================
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["replay", "live"], default="replay")
args = parser.parse_args()

if args.mode == "live":
    run_live()
else:
    run_replay()
