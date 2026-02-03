import numpy as np
from tensorflow.keras.models import load_model

model = load_model("../../models/ids_model.h5")

def predict(features):
    x = np.array(features).reshape(1, -1)
    prob = model.predict(x)[0][0]
    return prob
