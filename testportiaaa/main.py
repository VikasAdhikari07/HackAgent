from dotenv import load_dotenv
import os
from portia import (
    Portia,
    example_tool_registry,
    StorageClass,
    ToolRegistry,
    Config,
    LogLevel,
    LLMProvider,
)
from structureplan import image_generator

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PORTIA_API_KEY = os.getenv("PORTIA_API_KEY")
print(GOOGLE_API_KEY)
print(PORTIA_API_KEY)

# Strongly recommended: set provider + keys explicitly
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE,
    default_model="google/gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    storage_class=StorageClass.DISK,
    portia_api_key=PORTIA_API_KEY,
    default_log_level=LogLevel.DEBUG,
)

# Instantiate your tool (the @tool decorator creates a class)
my_tool_registry = ToolRegistry([
    image_generator(),
])

complete_tool_registry = example_tool_registry + my_tool_registry

portia = Portia(
    config=google_config,
    tools=complete_tool_registry,
)

plan_run = portia.run(
    "Create a beautiful image of a futuristic city with flying cars and green buildings for my social media campaign"
)

print(plan_run.model_dump_json(indent=2))