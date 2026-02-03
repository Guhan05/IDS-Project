import time
import os
import csv
from tensorflow.keras.models import load_model
from ..training.preprocess import load_data
from ..training.fuzzy import fuzzy_decision

# load model
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE, "models", "ids_model.h5")

model = load_model(MODEL_PATH)

# load test data for replay
_, X_test, _, y_test = load_data("data/")

print("🚀 Starting realtime replay...\n")

for x in X_test[:500]:

    prob = model.predict(x.reshape(1, -1))[0][0]
    decision = fuzzy_decision(prob)

    print("Decision:", decision)

    # save logs
    with open("src/results/logs.csv", "a", newline="") as f:
        csv.writer(f).writerow([decision])

    time.sleep(0.3)
