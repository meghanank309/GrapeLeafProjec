
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg16_preprocess
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet50_preprocess


# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Class order confirmed in your MobileNetV2 notebook.
CLASS_NAMES = [
    "Grape Black Measles",
    "Grape Black rot",
    "Grape Healthy",
    "Grape Isariopsis Leaf Spot",
]

# Model file paths
MODEL_PATHS = {
    "MobileNetV2": BASE_DIR / "models/incoming/MobileNetV2/mobilenetv2_best.keras",
    "VGG16": BASE_DIR / "models/incoming/VGG16/grape_vgg16_best_continued.keras",
    "ResNet50": BASE_DIR / "models/incoming/ResNet50/best_resnet50.keras",
    "EfficientNetB3": BASE_DIR / "models/incoming/EfficientNetB3/efficientnetb3_grape_leaf_best.keras",
}


@st.cache_resource
def load_models():
    """Load and cache the trained models."""
    loaded = {}

    for name, path in MODEL_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(
                f"{name} model file was not found:\n{path}"
            )

        loaded[name] = tf.keras.models.load_model(
            path,
            compile=False,
        )

    return loaded


def prepare_image(image: Image.Image, model_name: str):
    """Resize and preprocess an image for a model."""
    size = (300, 300) if model_name == "EfficientNetB3" else (224, 224)

    image = image.convert("RGB").resize(size)
    array = np.asarray(image, dtype=np.float32)

    if model_name == "MobileNetV2":
        array = array / 255.0
    elif model_name == "VGG16":
        array = vgg16_preprocess(array)
    elif model_name == "ResNet50":
        array = resnet50_preprocess(array)
    elif model_name == "EfficientNetB3":
        # Confirm this scaling against the EfficientNet training pipeline.
        pass

    return np.expand_dims(array, axis=0)


def predict_all(image: Image.Image):
    """Return the top prediction and four scores for each model."""
    models = load_models()
    results = {}

    for name, model in models.items():
        batch = prepare_image(image, name)
        scores = np.asarray(model.predict(batch, verbose=0))[0]

        if len(scores) != len(CLASS_NAMES):
            raise ValueError(
                f"{name} returned {len(scores)} scores, expected 4."
            )

        best_index = int(np.argmax(scores))

        results[name] = {
            "predicted_class": CLASS_NAMES[best_index],
            "confidence": float(scores[best_index]) * 100,
            "scores": {
                CLASS_NAMES[i]: float(scores[i]) * 100
                for i in range(len(CLASS_NAMES))
            },
        }

    return results