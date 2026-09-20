# Task 2 - Emotion Recognition from Speech

## 1. Dataset

Use the RAVDESS Speech Audio dataset.

Official dataset:
https://zenodo.org/records/1188976

Download:
Audio_Speech_Actors_01-24.zip

After extracting, arrange the project as:

project/
    emotion_speech_recognition.py
    requirements.txt
    ravdess/
        Actor_01/
        Actor_02/
        ...
        Actor_24/

The program uses audio-only speech and extracts MFCC features.

## 2. Install packages

Open a terminal in this folder and run:

pip install -r requirements.txt

If TensorFlow installation differs on your system, install a compatible
TensorFlow version for your Python version.

## 3. Run

python emotion_speech_recognition.py

## 4. What the program does

- Reads RAVDESS speech WAV files
- Decodes emotion labels from filenames
- Extracts 40 MFCC coefficients
- Uses actor-wise train/validation/test splitting
- Normalizes features
- Trains CNN
- Trains Bidirectional LSTM
- Calculates accuracy, precision, recall and F1-score
- Creates confusion matrices
- Creates training graphs
- Compares CNN and LSTM
- Saves trained models

## 5. RAVDESS emotion codes

01 neutral
02 calm
03 happy
04 sad
05 angry
06 fearful
07 disgust
08 surprised

## 6. Important academic note

RAVDESS is an acted emotional-speech dataset. It is appropriate for an
academic demonstration of speech emotion recognition, but results should
not be interpreted as a universal measure of real-world human emotion.
