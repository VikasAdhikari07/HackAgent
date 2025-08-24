from portia import PortiaToolRegistry, ToolRegistry, open_source_tool_registry, config, tool
from typing import Dict, Any, List
from typing import Annotated
from pydantic import Field
import os, base64, uuid
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image

from ..config import model, response_modalities, save_dir, image_format, return_base64, default_config
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

def register_marketing_tools():
    # Get Portia cloud tools
    print("🔍 Loading Portia cloud tools...")
    portia_cloud_registry = PortiaToolRegistry(config=default_config)
    print(f"✅ Loaded {len(portia_cloud_registry)} cloud tools")
    
    # Extract specific local tools from open source registry
    local_tools = []
    desired_local_tools = [
        "search_tool",
        "crawl_tool", 
        "extract_tool",
        "image_understanding_tool"
    ]
    
    image_generator_tool = ToolRegistry([image_generator()])
    
    for tool in open_source_tool_registry.get_tools():
        if tool.id in desired_local_tools:
            local_tools.append(tool)
            print(f"✅ Added local tool: {tool.id}")
    
    # Extract specific Portia cloud tools
    cloud_tools = []
    desired_cloud_tools = [
        "portia:google:gmail:send_email",
        "portia:google:gmail:draft_email", 
        "portia:google:gmail:search_email",
        "portia:google:sheets:get_spreadsheet",
        "portia:google:gcalendar:create_event"
    ]
    
    for tool in portia_cloud_registry.get_tools():
        if tool.id in desired_cloud_tools:
            cloud_tools.append(tool)
            print(f"✅ Added cloud tool: {tool.id}")
    
    # Create marketing-focused tool registry
    marketing_registry = ToolRegistry(local_tools + cloud_tools + image_generator_tool)
    print(f"✅ Created marketing registry with {len(marketing_registry)} tools")
    return marketing_registry