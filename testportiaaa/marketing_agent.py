from dotenv import load_dotenv
import os
from portia import (
    Portia,
    open_source_tool_registry,
    PortiaToolRegistry,
    ToolRegistry,
    Config,
    LogLevel,
    LLMProvider,
    StorageClass,
)

load_dotenv()

def create_marketing_agent():
    """Create a focused marketing agent with selected tools."""
    
    # Check for required environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    portia_api_key = os.getenv("PORTIA_API_KEY")
    
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    if not portia_api_key:
        raise ValueError("PORTIA_API_KEY not found in environment variables")
    
    print(f"✅ Google API Key: {google_api_key[:10]}...")
    print(f"✅ Portia API Key: {portia_api_key[:10]}...")
    
    # Configure Portia with proper credentials
    config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model="google/gemini-2.0-flash",
        planning_model="google/gemini-2.0-flash", 
        execution_model="google/gemini-2.0-flash",
        introspection_model="google/gemini-2.0-flash",
        summarizer_model="google/gemini-2.0-flash",
        temperature=0.7,
        google_api_key=google_api_key,
        portia_api_key=portia_api_key,
        storage_class=StorageClass.CLOUD,
        default_log_level=LogLevel.DEBUG,
    )
    
    try:
        # Get Portia cloud tools
        print("🔍 Loading Portia cloud tools...")
        portia_cloud_registry = PortiaToolRegistry(config=config)
        print(f"✅ Loaded {len(portia_cloud_registry)} cloud tools")
        
        # Extract specific local tools from open source registry
        local_tools = []
        desired_local_tools = [
            "search_tool",
            "crawl_tool", 
            "extract_tool",
            "image_understanding_tool"
        ]
        
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
        marketing_registry = ToolRegistry(local_tools + cloud_tools)
        print(f"✅ Created marketing registry with {len(marketing_registry)} tools")
        
        # Create the marketing agent
        marketing_agent = Portia(
            config=config,
            tools=marketing_registry
        )
        
        return marketing_agent, marketing_registry
        
    except Exception as e:
        print(f"❌ Error creating marketing agent: {str(e)}")
        print("💡 This might be due to API connectivity or authentication issues")
        raise

def main():
    """Demonstrate the marketing agent capabilities."""
    
    print("🚀 Initializing Marketing Agent...")
    
    try:
        marketing_agent, marketing_registry = create_marketing_agent()
        
        print(f"\n✅ Marketing Agent ready with {len(marketing_registry)} tools:")
        
        # List available tools
        for tool in marketing_registry.get_tools():
            print(f"  - {tool.id}: {tool.name}")
        
        print("\n" + "="*50)
        print("Marketing Agent is ready for campaigns!")
        print("="*50)
        test_query = input("Enter your query: ")
        # Simple test query first
        # test_query = """
        # I need to launch a product marketing campaign for a new SaaS tool. Please help me:
        # 1. Research our top 3 competitors and their messaging
        # 2. Draft an email announcement for our customer list
        # 3. Schedule a campaign launch meeting for next Tuesday at 2 PM
        # 4. Create a plan to track email engagement
        # """
        print(f"\n📋 Test Query: {test_query}")
        
        # Run a simple test
        result = marketing_agent.run(test_query)
        print("\n📊 Test Results:")
        print(result.model_dump_json(indent=2))
        print("="*60)
        
        # Extract and display key information from the result
        print(f"🆔 Run ID: {result.id}")
        print(f"📋 Plan ID: {result.plan_id}")
        print(f"✅ Status: {result.state}")
        print(f"👤 User ID: {result.end_user_id}")
        
        # print("\n🔍 Research Summary:")
        # print("-" * 40)
        # final_summary = result.outputs.final_output.get('summary', 'No summary available')
        # print(final_summary)
        
        # print("\n📚 Detailed Research Results:")
        # print("-" * 40)
        
        # # Parse and display the research data
        # import json
        # try:
        #     research_data = json.loads(result.outputs.final_output.get('value', '[]'))
            
        #     for i, source in enumerate(research_data, 1):
        #         print(f"\n{i}. {source.get('title', 'No title')}")
        #         print(f"   🔗 URL: {source.get('url', 'No URL')}")
        #         print(f"   📊 Relevance Score: {source.get('score', 'N/A'):.2f}")
        #         print(f"   📄 Content Preview:")
        #         content = source.get('content', 'No content')
        #         # Truncate content for readability
        #         if len(content) > 200:
        #             content = content[:200] + "..."
        #         print(f"      {content}")
                
        # except json.JSONDecodeError:
        #     print("Error parsing research data")
        #     print(result.outputs.final_output.get('value', 'No data available'))
        
        # print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has valid API keys")
        print("2. Ensure internet connectivity")
        print("3. Verify API keys have proper permissions")
        raise

if __name__ == "__main__":
    main()
