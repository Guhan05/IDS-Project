import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from .preprocess import load_data

print("🚀 Starting model training...\n")

# =========================
# Load dataset
# =========================
X_train, X_test, y_train, y_test = load_data("data/")

print("Dataset loaded")
print("Train shape:", X_train.shape)


# =========================
# Build ANN
# =========================
model = Sequential([
    Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid")   # binary output
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# =========================
# Train
# =========================
model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=256,
    validation_data=(X_test, y_test)
)


# =========================
# Save model
# =========================
os.makedirs("src/models", exist_ok=True)
model.save("src/models/ids_model.h5")

print("\n✅ Training complete")
print("✅ Model saved to src/models/ids_model.h5")
