from pathlib import Path
import tkinter as tk
from tkinter import messagebox

import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_FILE = PROJECT_ROOT / "handwritten_digit_cnn.keras"


def load_model(model_path=MODEL_FILE):
    model_path = Path(model_path)
    if not model_path.exists():
        return None

    try:
        return tf.keras.models.load_model(str(model_path))
    except Exception:
        return None


def preprocess_image(image):
    bbox = image.getbbox()
    if bbox is None:
        raise ValueError("Canvas is empty")

    digit_image = image.crop(bbox)
    digit_image.thumbnail((20, 20))

    resized = Image.new("L", (28, 28), 0)
    x = (28 - digit_image.width) // 2
    y = (28 - digit_image.height) // 2
    resized.paste(digit_image, (x, y))

    array = np.array(resized, dtype="float32") / 255.0
    return array.reshape(1, 28, 28, 1)


def predict_digit(model_obj, image):
    if model_obj is None:
        raise ValueError("Model not found")

    array = preprocess_image(image)
    prediction = model_obj.predict(array, verbose=0)[0]
    digit = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100
    return digit, confidence


model = load_model()


class DigitRecognizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Digit Recognition")
        self.root.geometry("520x650")
        self.root.resizable(False, False)

        self.canvas_size = 400
        self.brush_size = 18

        title = tk.Label(
            root,
            text="Handwritten Digit Recognition",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        info = tk.Label(
            root,
            text="Draw a digit from 0 to 9",
            font=("Arial", 13)
        )
        info.pack()

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="black",
            cursor="cross"
        )
        self.canvas.pack(pady=15)

        self.image = Image.new("L", (self.canvas_size, self.canvas_size), 0)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        self.result = tk.Label(
            root,
            text="Prediction: -",
            font=("Arial", 18, "bold")
        )
        self.result.pack(pady=10)

        buttons = tk.Frame(root)
        buttons.pack()

        tk.Button(
            buttons,
            text="Predict",
            command=self.predict,
            width=12,
            height=2
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear,
            width=12,
            height=2
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            buttons,
            text="Exit",
            command=root.destroy,
            width=12,
            height=2
        ).grid(row=0, column=2, padx=8)

    def paint(self, event):
        x, y = event.x, event.y
        r = self.brush_size

        self.canvas.create_oval(
            x-r, y-r, x+r, y+r,
            fill="white",
            outline="white"
        )

        self.draw.ellipse(
            [x-r, y-r, x+r, y+r],
            fill=255
        )

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new(
            "L",
            (self.canvas_size, self.canvas_size),
            0
        )
        self.draw = ImageDraw.Draw(self.image)
        self.result.config(text="Prediction: -")

    def predict(self):
        if model is None:
            messagebox.showerror(
                "Model not found",
                "Please run train_model.py first."
            )
            return

        try:
            digit, confidence = predict_digit(model, self.image)
        except ValueError:
            messagebox.showwarning(
                "Empty Canvas",
                "Please draw a digit first."
            )
            return

        self.result.config(
            text=f"Prediction: {digit}  |  Confidence: {confidence:.2f}%"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizer(root)
    root.mainloop()
