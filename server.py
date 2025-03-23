from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import pickle
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.applications import DenseNet201
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import pad_sequences
from tensorflow.keras.models import Model, load_model
import io
from PIL import Image
import logging

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and supporting files
try:
    logger.info("Loading model...")
    caption_model = load_model("model.keras")
    logger.info("Model loaded successfully.")

    with open("tokenizer.pkl", "rb") as file:
        tokenizer = pickle.load(file)

    with open("max_length.pkl", "rb") as file:
        max_length = pickle.load(file)

    # Load DenseNet201 for feature extraction
    base_model = DenseNet201(weights="imagenet", include_top=False, pooling="avg")
    feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)

except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise RuntimeError(f"Failed to load model: {e}")


# Define response model
class CaptionResponse(BaseModel):
    caption: str


def extract_image_feature(image_bytes: bytes) -> np.ndarray:
    """Extracts feature vector from an image."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((224, 224))  # Resize to model input size
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)  # Normalize

        feature = feature_extractor.predict(image, verbose=0)
        feature = feature.flatten()

        resized_feature = np.resize(feature, (1920,))
        return resized_feature
    except Exception as e:
        logger.error(f"Error extracting image features: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image")


def generate_caption(model, tokenizer, image_feature, max_length):
    """Generates a caption for a given image feature vector."""
    in_text = "startseq"
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)

        y_pred = model.predict([np.expand_dims(image_feature, axis=0), sequence], verbose=0)
        word_index = np.argmax(y_pred)

        word = tokenizer.index_word.get(word_index, None)
        if word is None or word == "endseq":
            break
        in_text += " " + word

    return in_text.replace("startseq", "").replace("endseq", "").strip()


@app.post("/predict/", response_model=CaptionResponse)
async def predict(file: UploadFile = File(...)):
    """API endpoint to generate an image caption."""
    try:
        logger.info(f"Received file: {file.filename}")

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file received")

        image_feature = extract_image_feature(image_bytes)
        generated_caption = generate_caption(caption_model, tokenizer, image_feature, max_length)

        logger.info(f"Generated Caption: {generated_caption}")

        return {"caption": generated_caption}

    except HTTPException as http_error:
        return JSONResponse(content={"error": str(http_error.detail)}, status_code=http_error.status_code)
    except Exception as e:
        logger.error(f"Server error: {e}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
