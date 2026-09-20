from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "handwritten_digit_cnn.keras"


def build_model():
    model = models.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def train_and_save_model(model_path=MODEL_PATH):
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)

    model = build_model()
    model.summary()

    model.fit(
        x_train,
        y_train,
        epochs=5,
        batch_size=128,
        validation_split=0.1
    )

    _, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    model_path = Path(model_path)
    model.save(model_path)
    print(f"Model saved as {model_path.name}")
    return model


if __name__ == "__main__":
    train_and_save_model()
