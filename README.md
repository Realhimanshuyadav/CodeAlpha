# Task 3: Handwritten Character Recognition

## Objective
Identify handwritten digits using image processing and a Convolutional Neural Network (CNN).

## Dataset
MNIST handwritten digit dataset.

## Technologies
- Python
- TensorFlow/Keras
- NumPy
- Pillow
- Tkinter
- CNN

## Project Structure

```text
Task_3_Handwritten_Character_Recognition/
│
├── train_model.py
├── app.py
├── requirements.txt
└── README.md
```

## Installation

Open the terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## Step 1: Train the CNN

```bash
python train_model.py
```

This downloads the MNIST dataset, trains the CNN and creates:

```text
handwritten_digit_cnn.keras
```

## Step 2: Run the Application

```bash
python app.py
```

Draw a digit on the black canvas and click Predict.

## Workflow

Input handwritten digit
        ↓
Image preprocessing
        ↓
Resize to 28 × 28
        ↓
Normalization
        ↓
CNN model
        ↓
Prediction
        ↓
Predicted digit + confidence

## Expected Result

The trained model should normally achieve high test accuracy on MNIST. Actual accuracy depends on the training environment and settings.

## Important

Run `train_model.py` before running `app.py`, because the application needs the saved CNN model.
