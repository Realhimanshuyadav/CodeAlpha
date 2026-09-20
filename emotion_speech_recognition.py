"""
TASK 2: EMOTION RECOGNITION FROM SPEECH
=======================================

Dataset: RAVDESS Speech Audio
Features: MFCCs (Mel-Frequency Cepstral Coefficients)
Models:
    1. CNN
    2. LSTM
Evaluation:
    Accuracy, Precision, Recall, F1-Score
    Confusion Matrix
    Classification Report

Expected dataset structure after extracting RAVDESS:

project_folder/
    emotion_speech_recognition.py
    ravdess/
        Actor_01/
            03-01-01-01-01-01-01.wav
            ...
        Actor_02/
            ...
        ...
        Actor_24/
            ...

The RAVDESS filename contains the emotion code:
01 = neutral
02 = calm
03 = happy
04 = sad
05 = angry
06 = fearful
07 = disgust
08 = surprised

The program uses an actor-wise split so the same speaker is not placed
in both training and test sets. This reduces speaker leakage.
"""

import os
import re
import random
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import librosa
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

import tensorflow as tf
from keras import layers, models, callbacks


# ============================================================
# 1. CONFIGURATION
# ============================================================

DATASET_DIR = "ravdess"
DATASET_CANDIDATES = (
    "ravdess",
    "Audio_Speech_Actors_01-24_16k",
    "Audio_Speech_Actors_01-24",
)

SAMPLE_RATE = 22050
N_MFCC = 40
MAX_DURATION = 4.0
MAX_PAD_LEN = int(np.ceil(MAX_DURATION * SAMPLE_RATE / 512))

TEST_ACTORS = [21, 22, 23, 24]
VALIDATION_ACTORS = [17, 18, 19, 20]

EPOCHS = 30
BATCH_SIZE = 32
RANDOM_SEED = 42

MODEL_CNN_FILE = "emotion_cnn.keras"
MODEL_LSTM_FILE = "emotion_lstm.keras"
FEATURE_CACHE_FILE = "ravdess_mfcc_features.npz"


# RAVDESS emotion labels
EMOTION_MAP = {
    1: "neutral",
    2: "calm",
    3: "happy",
    4: "sad",
    5: "angry",
    6: "fearful",
    7: "disgust",
    8: "surprised",
}

EMOTIONS = list(EMOTION_MAP.values())
LABEL_TO_ID = {emotion: i for i, emotion in enumerate(EMOTIONS)}
ID_TO_LABEL = {i: emotion for i, emotion in enumerate(EMOTIONS)}


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

os.environ["PYTHONHASHSEED"] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)


def resolve_dataset_dir():
    for candidate in DATASET_CANDIDATES:
        if os.path.isdir(candidate):
            return candidate

    for root, dirs, _ in os.walk("."):
        if "Actor_01" in dirs and "Actor_24" in dirs:
            return os.path.relpath(root)

    return DATASET_DIR


DATASET_DIR = resolve_dataset_dir()


# ============================================================
# 3. CHECK DATASET
# ============================================================

def check_dataset():
    if not os.path.isdir(DATASET_DIR):
        raise FileNotFoundError(
            f"\nDataset folder '{DATASET_DIR}' was not found.\n"
            "Download the RAVDESS Speech Audio ZIP, extract it, and "
            "rename the extracted folder to 'ravdess' or place the "
            "folder under the project root.\n"
            "The folder should contain Actor_01 ... Actor_24."
        )

    wav_files = []
    for root, _, files in os.walk(DATASET_DIR):
        for file in files:
            if file.lower().endswith(".wav"):
                wav_files.append(os.path.join(root, file))

    if not wav_files:
        raise FileNotFoundError(
            f"No .wav files were found inside '{DATASET_DIR}'."
        )

    print(f"Found {len(wav_files)} WAV files.")


# ============================================================
# 4. PARSE RAVDESS FILENAME
# ============================================================

def parse_ravdess_filename(file_path):
    """
    Example:
    03-01-05-02-02-01-12.wav

    Fields:
    1 modality
    2 vocal channel
    3 emotion
    4 emotional intensity
    5 statement
    6 repetition
    7 actor
    """

    filename = os.path.basename(file_path)
    stem = os.path.splitext(filename)[0]
    parts = stem.split("-")

    if len(parts) != 7:
        return None

    try:
        modality = int(parts[0])
        vocal_channel = int(parts[1])
        emotion_code = int(parts[2])
        actor = int(parts[6])
    except ValueError:
        return None

    # We only want audio-only speech.
    # RAVDESS audio-only speech uses modality 03 and vocal channel 01.
    if modality != 3 or vocal_channel != 1:
        return None

    if emotion_code not in EMOTION_MAP:
        return None

    return {
        "path": file_path,
        "emotion": EMOTION_MAP[emotion_code],
        "emotion_id": LABEL_TO_ID[EMOTION_MAP[emotion_code]],
        "actor": actor,
    }


# ============================================================
# 5. BUILD DATAFRAME
# ============================================================

def build_metadata():
    rows = []

    for root, _, files in os.walk(DATASET_DIR):
        for file in files:
            if not file.lower().endswith(".wav"):
                continue

            path = os.path.join(root, file)
            parsed = parse_ravdess_filename(path)

            if parsed is not None:
                rows.append(parsed)

    metadata = pd.DataFrame(rows)

    if metadata.empty:
        raise RuntimeError(
            "No valid RAVDESS audio-only speech files were found."
        )

    metadata = metadata.sort_values(
        ["actor", "emotion", "path"]
    ).reset_index(drop=True)

    print("\nSpeech samples by emotion:")
    print(metadata["emotion"].value_counts().sort_index())

    print("\nSpeech samples by actor:")
    print(metadata["actor"].value_counts().sort_index())

    metadata.to_csv("ravdess_metadata.csv", index=False)

    return metadata


# ============================================================
# 6. EXTRACT MFCC FEATURES
# ============================================================

def extract_mfcc(file_path):
    """
    Returns an MFCC matrix with shape:
        (N_MFCC, MAX_PAD_LEN)

    The matrix is padded/truncated to a fixed length.
    """

    audio, _ = librosa.load(
        file_path,
        sr=SAMPLE_RATE,
        duration=MAX_DURATION,
        mono=True,
    )

    # Normalize audio amplitude.
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=N_MFCC,
        n_fft=1024,
        hop_length=512,
    )

    # Pad or truncate time axis.
    if mfcc.shape[1] < MAX_PAD_LEN:
        pad_width = MAX_PAD_LEN - mfcc.shape[1]
        mfcc = np.pad(
            mfcc,
            ((0, 0), (0, pad_width)),
            mode="constant",
        )
    else:
        mfcc = mfcc[:, :MAX_PAD_LEN]

    return mfcc.astype(np.float32)


def extract_all_features(metadata):
    X = []
    y = []
    actors = []

    total = len(metadata)

    for i, row in metadata.iterrows():
        try:
            feature = extract_mfcc(row["path"])
            X.append(feature)
            y.append(row["emotion_id"])
            actors.append(row["actor"])
        except Exception as error:
            print(
                f"Could not process {row['path']}: {error}"
            )

        if (i + 1) % 100 == 0 or (i + 1) == total:
            print(
                f"Feature extraction: {i + 1}/{total}"
            )

    if not X:
        raise RuntimeError("No features were extracted from the dataset.")

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int64)
    actors = np.array(actors, dtype=np.int64)

    np.savez_compressed(
        FEATURE_CACHE_FILE,
        X=X,
        y=y,
        actors=actors,
    )

    print("\nFeature array shape:", X.shape)
    print("Label array shape:", y.shape)

    return X, y, actors


def load_or_extract_features(metadata):
    if os.path.exists(FEATURE_CACHE_FILE):
        print(
            f"\nLoading cached MFCC features from "
            f"'{FEATURE_CACHE_FILE}'..."
        )

        data = np.load(FEATURE_CACHE_FILE)

        return (
            data["X"],
            data["y"],
            data["actors"],
        )

    print("\nExtracting MFCC features...")
    return extract_all_features(metadata)


# ============================================================
# 7. ACTOR-WISE TRAIN / VALIDATION / TEST SPLIT
# ============================================================

def split_data(X, y, actors):
    train_mask = ~np.isin(
        actors,
        TEST_ACTORS + VALIDATION_ACTORS
    )

    validation_mask = np.isin(
        actors,
        VALIDATION_ACTORS
    )

    test_mask = np.isin(
        actors,
        TEST_ACTORS
    )

    X_train = X[train_mask]
    y_train = y[train_mask]

    X_val = X[validation_mask]
    y_val = y[validation_mask]

    X_test = X[test_mask]
    y_test = y[test_mask]

    print("\nDataset split:")
    print("Training   :", len(X_train))
    print("Validation :", len(X_val))
    print("Testing    :", len(X_test))

    return (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test,
    )


# ============================================================
# 8. NORMALIZE MFCC FEATURES
# ============================================================

def normalize_features(
    X_train,
    X_val,
    X_test,
):
    """
    Normalize using only training data statistics.
    """

    mean = X_train.mean()
    std = X_train.std() + 1e-8

    X_train = (X_train - mean) / std
    X_val = (X_val - mean) / std
    X_test = (X_test - mean) / std

    return X_train, X_val, X_test


# ============================================================
# 9. CNN MODEL
# ============================================================

def build_cnn(input_shape, num_classes):
    model = models.Sequential(
        [
            layers.Input(shape=input_shape),

            layers.Conv2D(
                32,
                kernel_size=(3, 3),
                padding="same",
                activation="relu",
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),
            layers.Dropout(0.25),

            layers.Conv2D(
                64,
                kernel_size=(3, 3),
                padding="same",
                activation="relu",
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),
            layers.Dropout(0.25),

            layers.Conv2D(
                128,
                kernel_size=(3, 3),
                padding="same",
                activation="relu",
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D(
                pool_size=(2, 2)
            ),
            layers.Dropout(0.30),

            layers.GlobalAveragePooling2D(),

            layers.Dense(
                128,
                activation="relu",
            ),
            layers.Dropout(0.35),

            layers.Dense(
                num_classes,
                activation="softmax",
            ),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# ============================================================
# 10. LSTM MODEL
# ============================================================

def build_lstm(input_shape, num_classes):
    model = models.Sequential(
        [
            layers.Input(shape=input_shape),

            layers.Bidirectional(
                layers.LSTM(
                    128,
                    return_sequences=True
                )
            ),
            layers.Dropout(0.30),

            layers.Bidirectional(
                layers.LSTM(64)
            ),
            layers.Dropout(0.30),

            layers.Dense(
                64,
                activation="relu"
            ),

            layers.Dropout(0.30),

            layers.Dense(
                num_classes,
                activation="softmax"
            ),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# ============================================================
# 11. TRAINING CALLBACKS
# ============================================================

def get_callbacks(model_name):
    return [
        callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1,
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
        callbacks.ModelCheckpoint(
            model_name,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]


# ============================================================
# 12. PLOT TRAINING HISTORY
# ============================================================

def plot_history(history, title):
    plt.figure(figsize=(8, 5))

    plt.plot(
        history.history["accuracy"],
        label="Training Accuracy"
    )
    plt.plot(
        history.history["val_accuracy"],
        label="Validation Accuracy"
    )

    plt.title(title)
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))

    plt.plot(
        history.history["loss"],
        label="Training Loss"
    )
    plt.plot(
        history.history["val_loss"],
        label="Validation Loss"
    )

    plt.title(title + " - Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# 13. EVALUATION
# ============================================================

def evaluate_model(model, X_test, y_test, model_name):
    probabilities = model.predict(
        X_test,
        verbose=0
    )

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("\n" + "=" * 70)
    print(f"{model_name} - TEST RESULTS")
    print("=" * 70)

    print(f"Accuracy : {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall   : {recall:.4f} ({recall * 100:.2f}%)")
    print(f"F1-Score : {f1:.4f} ({f1 * 100:.2f}%)")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=EMOTIONS,
            zero_division=0,
        )
    )

    cm = confusion_matrix(
        y_test,
        predictions,
    )

    plt.figure(figsize=(9, 7))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=EMOTIONS,
        yticklabels=EMOTIONS,
    )

    plt.title(
        f"{model_name} - Confusion Matrix"
    )
    plt.xlabel("Predicted Emotion")
    plt.ylabel("Actual Emotion")
    plt.tight_layout()
    plt.show()

    return {
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "Predictions": predictions,
        "Probabilities": probabilities,
    }


# ============================================================
# 14. PREDICT ONE AUDIO FILE
# ============================================================

def predict_audio(
    model,
    audio_path,
    model_name="Model"
):
    if not os.path.exists(audio_path):
        print(
            f"\nAudio file not found: {audio_path}"
        )
        return

    mfcc = extract_mfcc(audio_path)

    # Use the same normalization strategy as the dataset.
    # The training normalization values are not saved separately
    # in this simple educational version, so we normalize the sample
    # by its own MFCC statistics.
    mfcc = (
        mfcc - mfcc.mean()
    ) / (mfcc.std() + 1e-8)

    if model_name == "CNN":
        sample = mfcc[np.newaxis, ..., np.newaxis]
    else:
        sample = mfcc.T[np.newaxis, ...]

    probabilities = model.predict(
        sample,
        verbose=0
    )[0]

    predicted_id = int(
        np.argmax(probabilities)
    )

    predicted_emotion = ID_TO_LABEL[
        predicted_id
    ]

    print("\n" + "=" * 70)
    print("AUDIO PREDICTION")
    print("=" * 70)
    print("Audio:", audio_path)
    print("Model:", model_name)
    print(
        "Predicted emotion:",
        predicted_emotion.upper()
    )

    print("\nEmotion probabilities:")

    probability_table = pd.DataFrame(
        {
            "Emotion": EMOTIONS,
            "Probability": probabilities,
        }
    ).sort_values(
        "Probability",
        ascending=False
    )

    probability_table["Probability"] = (
        probability_table["Probability"] * 100
    ).round(2)

    print(probability_table.to_string(index=False))


# ============================================================
# 15. MAIN PROGRAM
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("TASK 2: EMOTION RECOGNITION FROM SPEECH")
    print("=" * 70)

    print("\nGoal:")
    print(
        "Recognize human emotions from speech audio "
        "using MFCC features and deep learning."
    )

    # Check dataset
    check_dataset()

    # Metadata
    metadata = build_metadata()

    # Extract/load MFCC features
    X, y, actors = load_or_extract_features(
        metadata
    )

    # Split
    (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test,
    ) = split_data(
        X,
        y,
        actors
    )

    # Normalize
    (
        X_train,
        X_val,
        X_test,
    ) = normalize_features(
        X_train,
        X_val,
        X_test
    )

    # ========================================================
    # CNN
    # ========================================================

    print("\n" + "=" * 70)
    print("BUILDING CNN")
    print("=" * 70)

    X_train_cnn = X_train[..., np.newaxis]
    X_val_cnn = X_val[..., np.newaxis]
    X_test_cnn = X_test[..., np.newaxis]

    cnn = build_cnn(
        input_shape=X_train_cnn.shape[1:],
        num_classes=len(EMOTIONS)
    )

    cnn.summary()

    cnn_history = cnn.fit(
        X_train_cnn,
        y_train,
        validation_data=(
            X_val_cnn,
            y_val
        ),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=get_callbacks(
            MODEL_CNN_FILE
        ),
        verbose=1,
    )

    plot_history(
        cnn_history,
        "CNN Training"
    )

    cnn_results = evaluate_model(
        cnn,
        X_test_cnn,
        y_test,
        "CNN"
    )

    # ========================================================
    # LSTM
    # ========================================================

    print("\n" + "=" * 70)
    print("BUILDING LSTM")
    print("=" * 70)

    # CNN MFCC shape:
    # (samples, 40 MFCC, time)
    #
    # LSTM expects:
    # (samples, time, MFCC)
    X_train_lstm = np.transpose(
        X_train,
        (0, 2, 1)
    )

    X_val_lstm = np.transpose(
        X_val,
        (0, 2, 1)
    )

    X_test_lstm = np.transpose(
        X_test,
        (0, 2, 1)
    )

    lstm = build_lstm(
        input_shape=X_train_lstm.shape[1:],
        num_classes=len(EMOTIONS)
    )

    lstm.summary()

    lstm_history = lstm.fit(
        X_train_lstm,
        y_train,
        validation_data=(
            X_val_lstm,
            y_val
        ),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=get_callbacks(
            MODEL_LSTM_FILE
        ),
        verbose=1,
    )

    plot_history(
        lstm_history,
        "LSTM Training"
    )

    lstm_results = evaluate_model(
        lstm,
        X_test_lstm,
        y_test,
        "LSTM"
    )

    # ========================================================
    # MODEL COMPARISON
    # ========================================================

    comparison = pd.DataFrame(
        [
            {
                "Model": "CNN",
                "Accuracy": cnn_results["Accuracy"],
                "Precision": cnn_results["Precision"],
                "Recall": cnn_results["Recall"],
                "F1-Score": cnn_results["F1-Score"],
            },
            {
                "Model": "LSTM",
                "Accuracy": lstm_results["Accuracy"],
                "Precision": lstm_results["Precision"],
                "Recall": lstm_results["Recall"],
                "F1-Score": lstm_results["F1-Score"],
            },
        ]
    )

    print("\n" + "=" * 70)
    print("CNN vs LSTM")
    print("=" * 70)

    print(
        comparison.to_string(
            index=False,
            float_format=lambda value:
                f"{value:.4f}"
        )
    )

    comparison.to_csv(
        "emotion_model_comparison.csv",
        index=False
    )

    # ========================================================
    # SAMPLE PREDICTION
    # ========================================================

    sample_files = metadata["path"].tolist()

    if sample_files:

        sample_audio = sample_files[0]

        print("\nTesting a sample audio file:")
        print(sample_audio)

        predict_audio(
            cnn,
            sample_audio,
            model_name="CNN"
        )

        predict_audio(
            lstm,
            sample_audio,
            model_name="LSTM"
        )

    # ========================================================
    # FINISHED
    # ========================================================

    print("\n" + "=" * 70)
    print("TASK 2 COMPLETED")
    print("=" * 70)

    print(
        """
Generated files:
    ravdess_metadata.csv
    ravdess_mfcc_features.npz
    emotion_cnn.keras
    emotion_lstm.keras
    emotion_model_comparison.csv

Main outputs:
    - MFCC features
    - CNN model
    - LSTM model
    - Training/validation accuracy graphs
    - Training/validation loss graphs
    - Confusion matrices
    - Classification reports
    - Accuracy
    - Precision
    - Recall
    - F1-score
    - CNN vs LSTM comparison
    """
    )


if __name__ == "__main__":
    main()
