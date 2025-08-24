import os
from dotenv import load_dotenv
from portia import (
    Config,
    LLMProvider,
    Portia,
    example_tool_registry,
    StorageClass
)
from portia.plan import PlanUUID

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE,
    default_model="google/gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    storage_class=StorageClass.CLOUD,  # Add storage configuration
    portia_api_key=os.getenv('PORTIA_API_KEY')  # Add your Portia API key
)

# Instantiate a Portia instance. Load it with the config and with the example tools.
portia = Portia(config=google_config, tools=example_tool_registry)

def print_plan_by_id(plan_id_string: str):
    """
    Print a plan using its plan ID string.
    
    Args:
        plan_id_string: Plan ID in format "plan-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    """
    try:
        # Convert string to PlanUUID
        plan_uuid = PlanUUID.from_string(plan_id_string)
        
        # Retrieve plan from storage using the portia instance
        plan = portia.storage.get_plan(plan_uuid)  # Use the instance, not the class
        
        # Print the plan in JSON format
        print("Plan Details:")
        print("=" * 50)
        print(plan.model_dump_json(indent=2))
        
        return plan
        
    except Exception as e:
        print(f"Error retrieving plan {plan_id_string}: {e}")
        return None

# Example usage
plan_id = "plan-9d0f4bea-f554-4699-983e-33d6064af8dd"  # Your actual plan ID
print_plan_by_id(plan_id)

# # Run the test query and print the output!
# plan_run = portia.run('add 1 + 2')
# print(plan_run.model_dump_json(indent=2))