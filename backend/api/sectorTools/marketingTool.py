from portia import tool
from typing import Dict, Any, List
from typing import Annotated
from pydantic import Field
import os, base64, uuid
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image

from backend.api.config import model, response_modalities, save_dir, image_format, return_base64
from dotenv import load_dotenv

load_dotenv()


@tool
def image_generator(
    prompt: Annotated[str, Field(description="Text description of the image to generate")]
) -> Dict[str, Any]:
    """
    Generate one or more images using Google's Gemini image model.
    Saves images to disk and returns file paths; optionally returns base64 data.
    Expects GOOGLE_API_KEY to be available to the client (env or default config).
    Return the path to the image.
    """

    client = genai.Client()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=response_modalities
        )
    )

    os.makedirs(save_dir, exist_ok=True)

    texts: List[str] = []
    images_meta: List[Dict[str, Any]] = []
    images_b64: List[str] = []

    candidate = response.candidates[0]
    for part in candidate.content.parts:
        if getattr(part, "text", None):
            texts.append(part.text)
        elif getattr(part, "inline_data", None):
            data: bytes = part.inline_data.data
            # Infer extension from mime or requested image_format
            mime: str = getattr(part.inline_data, "mime_type", f"image/{image_format.lower()}")
            ext = "png" if "png" in mime.lower() or image_format.upper() == "PNG" else "jpg"

            filename = f"{uuid.uuid4().hex}.{ext}"
            path = os.path.join(save_dir, filename)

            Image.open(BytesIO(data)).save(path, format=image_format.upper())

            images_meta.append({
                "path": path,
                "mime_type": mime,
                "size_bytes": len(data)
            })

            if return_base64:
                images_b64.append(base64.b64encode(data).decode("utf-8"))

    return path
