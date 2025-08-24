from dotenv import load_dotenv
from portia import (
    Config,
    LogLevel,
    Portia,
    StorageClass,
    LLMProvider
)

config = Config.from_default(
                llm_provider=LLMProvider.GOOGLE,
                storage_class=StorageClass.DISK, 
                storage_dir='demo_runs', # Amend this based on where you'd like your plans and plan runs saved!
                default_log_level=LogLevel.DEBUG,
                llm_redis_cache_url="redis://localhost:6379"
            )
