import os
from dotenv import load_dotenv
from portia import (
    StorageClass,
    Config,
    LogLevel,
    LLMProvider,
)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PORTIA_API_KEY = os.getenv("PORTIA_API_KEY")
default_model = os.getenv("DEFAULT_MODEL")

model = os.getenv("IMAGE_GENERATION_MODEL")
response_modalities = ["TEXT", "IMAGE"]
save_dir = "generated_images"
image_format = "PNG"
return_base64 = False

default_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE,
    default_model=default_model,
    planning_model=default_model,
    execution_model=default_model,
    introspection_model=default_model,
    summarizer_model=default_model,
    google_api_key=GOOGLE_API_KEY,
    storage_class=StorageClass.DISK,
    portia_api_key=PORTIA_API_KEY,
    default_log_level=LogLevel.DEBUG,
)