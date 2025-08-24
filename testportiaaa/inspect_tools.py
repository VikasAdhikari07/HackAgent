from portia import (
    Portia,
    example_tool_registry,
    open_source_tool_registry,
    Config,
    LogLevel,
    PortiaToolRegistry,
    LLMProvider
)
from pydantic import BaseModel
import inspect
import os

def get_tool_details(tool) -> dict:
    """Extract detailed information about a tool."""
    details = {
        "id": getattr(tool, "id", "Unknown"),
        "name": getattr(tool, "name", "Unknown"),
        "description": tool.__doc__.strip() if tool.__doc__ else "No description",
        "input_schema": None,
        "output_schema": None,
    }
    
    # # Get input schema
    # if hasattr(tool, "args_schema"):
    #     schema = tool.args_schema
    #     if inspect.isclass(schema) and issubclass(schema, BaseModel):
    #         details["input_schema"] = {
    #             name: (field.annotation, field.field_info.description)
    #             for name, field in schema.model_fields.items()
    #         }
    
    # # Get output schema
    # if hasattr(tool, "output_schema"):
    #     details["output_schema"] = tool.output_schema
    
    return details

def print_detailed_tool_info(registry_name: str, registry) -> None:
    """Print comprehensive information about tools in a registry."""
    print(f"\n{'='*20} {registry_name} {'='*20}")
    print(f"Total tools: {len(registry)}\n")
    
    for tool in registry.get_tools():
        # details = get_tool_details(tool)
        
        # print(f"\nTool ID: {details['id']}")
        # print(f"Name: {details['name']}")
        # print("\nDescription:")
        # print(details['description'])
        
        # if details['input_schema']:
        #     print("\nInput Parameters:")
        #     for param_name, (param_type, param_desc) in details['input_schema'].items():
        #         print(f"- {param_name}: {param_type}")
        #         print(f"  Description: {param_desc}")
        
        # if details['output_schema']:
        #     print("\nOutput Schema:")
        #     print(f"Type: {details['output_schema'][0]}")
        #     print(f"Description: {details['output_schema'][1]}")
        print(tool)
        
        print("-" * 60)

def print_portia_tools():
    """Print tools from Portia's cloud registry."""
    print("\n=== Portia Cloud Tools ===")
    
    # Create config with necessary credentials
    config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        portia_api_key=os.getenv("PORTIA_API_KEY")
    )
    
    try:
        # Initialize PortiaToolRegistry with config
        portia_registry = PortiaToolRegistry(config=config)
        
        # Get and print all tools
        print(f"\nTotal Portia Cloud Tools: {len(portia_registry)}")
        
        for tool in portia_registry.get_tools():
            print("\n" + "="*40)
            print(f"Tool ID: {tool.id}")
            print(f"Name: {tool.name}")
            print("\nDescription:")
            print(tool.__doc__ if tool.__doc__ else "No description")
            
            # Print schema information if available
            if hasattr(tool, "args_schema"):
                print("\nInput Schema:")
                print(tool.args_schema.model_json_schema())
            
            if hasattr(tool, "output_schema"):
                print("\nOutput Schema:")
                print(tool.output_schema)
            
            print("="*40)
    except Exception as e:
        print(f"Error accessing Portia Cloud Tools: {str(e)}")

def main():
    # Print detailed information about example tools
    print_detailed_tool_info("Example Tool Registry", example_tool_registry)
    
    # Print detailed information about open source tools
    print_detailed_tool_info("Open Source Tool Registry", open_source_tool_registry)
    
    # Print Portia cloud tools
    print_portia_tools()
    
    # Print information about conditional tools
    print("\nConditional Tools (Require Extra Dependencies):")
    print("1. BrowserTool")
    print("   - Requires: tools-browser-local")
    print("   - Purpose: Web browser automation and interaction")
    
    print("\n2. PDFReaderTool")
    print("   - Requires: tools-pdf-reader and MISTRAL_API_KEY")
    print("   - Purpose: PDF document reading and extraction")

if __name__ == "__main__":
    main()
