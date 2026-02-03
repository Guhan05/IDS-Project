import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from .preprocess import load_data

# load data
X_train, X_test, y_train, y_test = load_data("data/")

# simple ANN
model = Sequential([
    Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])

model.fit(X_train, y_train, epochs=5, batch_size=256)

# save model
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE, "models", "ids_model.h5")

model.save(MODEL_PATH)

print("✅ Model saved at:", MODEL_PATH)
