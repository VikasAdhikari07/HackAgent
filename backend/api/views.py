from unicodedata import category
from django.shortcuts import render
from portia import Portia, PlanUUID
from .config import default_config
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Sector
from google import genai 
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)
from .sectorTools.marketingTool import register_marketing_tools
from .sectorTools.researchTools import register_research_tools
@api_view(['GET'])
def get_sector_names(request):
    """
    API endpoint to fetch all sector names.
    
    Returns:
        Response: JSON response containing a list of sector names
        
    Example response:
    {
        "success": true,
        "data": [
            {
                "id": 1,
                "name": "Technology",
                "slug": "technology",
                "category": "industry"
            },
            {
                "id": 2,
                "name": "Healthcare",
                "slug": "healthcare", 
                "category": "industry"
            }
        ],
        "count": 2
    }
    """
    try:
        # Fetch only active sectors, ordered by their order field and name
        sectors = Sector.objects.filter(is_active=True).values(
            'id', 'name', 'slug', 'category'
        )
        
        return Response({
            'success': True,
            'data': list(sectors),
            'count': len(sectors)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch sector names'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_enhanced_prompt(request):
    """
    API endpoint to get enhanced prompt.
    
    Returns:
        Response: JSON response containing the enhanced prompt
        
    Example response:
    {
        "success": true,
        "data": "Enhanced prompt text"
    }
    """

        # name = "marketing"
        # category = "SaaS product launch"
        # user_query = "I need to launch a product marketing campaign for a new SaaS tool. Please help me:"

    

    print(request.data,"request.data")
    category = request.data.get('category')
    name = request.data.get('name')
    user_query = request.data.get('user_query')
    try:
        contents = f"""
        Based on the sector name '{name}' and category '{category}', and the following user query:

        '{user_query}'

        Generate the 10 most important and sequential action steps required. 
        provide max upto 50 words and less than that. 
        Return the response in **valid JSON format** with this structure:

        
        "steps": [
            "Step 1 description",
            "Step 2 description",
            "Step 10 description"
        ]
       
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
        )
        print(response.text)
        return Response({
            'success': True,
            'data': response.text,
            'message': 'Enhanced prompt retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to get enhanced prompt'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_plan(request):
    """
    API endpoint to fetch a plan based on the request parameters.
    
    Expected request body:
    {
        "space": "sector_name",
        "original_prompt": "user's original prompt",
        "enhanced_prompts": ["enhanced prompt 1", "enhanced prompt 2"]
    }
    
    Returns:
        Response: JSON response containing the plan data
    """
    try:
        # Get the request data
        data = request.data
        print("Received plan request data:", data)  # Debug log
        
        # Get parameters from request data
        sector_name = data.get('space')
        original_prompt = data.get('original_prompt', '')
        enhanced_prompts = data.get('enhanced_prompts', [])
        
        if not sector_name or not original_prompt or not enhanced_prompts:
            error_msg = 'Missing required parameters: space, original_prompt, or enhanced_prompts'
            print(f"Validation error: {error_msg}")
            return Response({
                'success': False,
                'error': error_msg,
                'message': 'Please provide all required parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Combine original prompt with enhanced prompts
        combined_prompt = f"""Original Prompt: {original_prompt}
        
        Enhanced Prompts:
        """
        for i, prompt in enumerate(enhanced_prompts, 1):
            combined_prompt += f"{i}. {prompt}\n"
        
        print(f"Generated combined prompt: {combined_prompt}")  # Debug log
        
        # Get the appropriate tools based on the sector
        tools = None
        try:
            if sector_name.lower() == 'marketing':
                tools = register_marketing_tools()
            elif sector_name.lower() == 'research':
                tools = register_research_tools()
            print(f"Registered tools for {sector_name}")  # Debug log
        except Exception as e:
            print(f"Error registering tools: {e}")
            tools = None
        
        # Generate the plan using the combined prompt
        try:
            portia = Portia(config=default_config, tools=tools)
            
            # Add validation for the combined prompt
            if not combined_prompt or not isinstance(combined_prompt, str) or len(combined_prompt.strip()) == 0:
                return Response({
                    'success': False,
                    'error': 'Invalid or empty prompt provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Generating plan with prompt: {combined_prompt[:200]}...")  # Log first 200 chars of prompt
            
            # Get the plan with a timeout
            print("Generating plan with Portia...")
            try:
                plan = portia.plan(combined_prompt)
                print(f"Plan generated: {plan is not None}")
                
                if plan is None:
                    raise ValueError("Plan generation returned None")
                    
                # Convert the plan to a serializable format
                try:
                    plan_data = plan.model_dump()
                    print(f"Plan model dump successful. Keys: {list(plan_data.keys())}")
                except Exception as dump_error:
                    print(f"Error in model_dump(): {str(dump_error)}")
                    raise ValueError(f"Failed to serialize plan: {str(dump_error)}")
                
                if not plan_data or not isinstance(plan_data, dict):
                    raise ValueError("Invalid plan format: Expected a dictionary")
                    
                # Validate required fields in plan_data
                required_fields = ['id', 'steps']
                for field in required_fields:
                    if field not in plan_data:
                        raise ValueError(f"Missing required field in plan: {field}")
                        
            except Exception as plan_error:
                print(f"Error during plan generation: {str(plan_error)}")
                print(f"Plan object type: {type(plan) if 'plan' in locals() else 'N/A'}")
                if 'plan' in locals() and hasattr(plan, '__dict__'):
                    print(f"Plan object attributes: {vars(plan).keys()}")
                raise
            
            return Response({
                'success': True,
                'data': plan_data,
                'message': 'Plan generated successfully'
            }, status=status.HTTP_200_OK)
            
        except ValueError as ve:
            error_msg = f"Validation error: {str(ve)}"
            print(error_msg)
            return Response({
                'success': False,
                'error': error_msg,
                'type': 'validation_error'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            error_msg = f"Error generating plan: {str(e)}"
            print(error_msg)
            return Response({
                'success': False,
                'error': error_msg,
                'type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in get_plan: {error_trace}")
        return Response({
            'success': False,
            'error': str(e),
            'traceback': error_trace,
            'message': 'Failed to generate plan. Please check the server logs for more details.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
def run_plan(request):
    """
    API endpoint to run a plan based on the request parameters.
    """
    try:
        data = request.data
        print(data,"data;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
        plan_id = data.get('plan_id')
        sector_name = data.get('sector')
        if sector_name == 'marketing':
            tools = register_marketing_tools()
        elif sector_name == 'research':
            tools = register_research_tools()
        else:
            tools = None
        
        portia = Portia(config=default_config, tools=tools)
        
        run = portia.run_plan(plan=PlanUUID.from_string(plan_id))
        return Response({
            'success': True,
            'data': run.model_dump()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to run plan'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)