import gradio as gr
import requests
import json
from typing import List, Optional
import time

class StrategyBuilder:
    """
    A class to handle the business logic for the AI Strategy Builder application.
    It communicates with a backend API to fetch data, enhance prompts, and generate/execute plans.
    """
    def __init__(self):
        """Initializes the StrategyBuilder with the API base URL and empty state variables."""
        self.api_base_url = "http://127.0.0.1:8000/api"
        self.spaces = []
        self.enhanced_prompts = []
        self.generated_plan = ""

    def fetch_spaces(self) -> List[str]:
        """
        Fetches available spaces/categories from the API.
        Includes fallback options in case of an API error.
        """
        try:
            response = requests.get(f"{self.api_base_url}/sectors/")
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            
            # Handle different possible response formats from the API
            if isinstance(data, dict) and 'data' in data:
                spaces_data = data['data']
            else:
                spaces_data = data
                
            if isinstance(spaces_data, list):
                # Extract the 'name' from each dictionary in the list
                self.spaces = [space.get('name', 'Unknown') for space in spaces_data if isinstance(space, dict)]
            else:
                # Default fallback if the API response is not a list
                self.spaces = ["Marketing", "Research", "Sales", "Product", "Content", "Technology"]
                
            return self.spaces
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching spaces: {e}")
            return ["Marketing", "Research", "Sales", "Product", "Content", "Technology"] # Fallback options

    def enhance_prompt(self, selected_space: str, user_prompt: str) -> tuple[Optional[List[str]], str]:
        """
        Calls the API to enhance a user's prompt and returns a list of suggestions.
        Handles various potential errors like connection issues, invalid JSON, etc.
        """
        if not selected_space or not user_prompt.strip():
            return None, "Please select a space and enter a prompt."
        
        try:
            payload = {"space": selected_space, "user_prompt": user_prompt.strip()}
            response = requests.post(f"{self.api_base_url}/enhance-prompt/", json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            # Robustly handle API response which might be a string or a dict
            steps_data_str = data.get('data', '')
            if not steps_data_str:
                return None, "API returned an empty response."

            # Clean the string to remove code fences and parse JSON
            json_str = str(steps_data_str).replace('```json', '').replace('```', '').strip()
            steps_data = json.loads(json_str)
            
            enhanced_prompts = steps_data.get('steps', [])
            if not isinstance(enhanced_prompts, list):
                return None, "Invalid response format: 'steps' should be a list."

            self.enhanced_prompts = enhanced_prompts
            return enhanced_prompts, f"Successfully generated {len(enhanced_prompts)} prompts!"

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API server. Please ensure it's running."
        except requests.exceptions.RequestException as e:
            return None, f"API request failed: {e}"
        except json.JSONDecodeError:
            return None, "Error: Could not parse the response from the API."
        except Exception as e:
            return None, f"An unexpected error occurred: {str(e)}"

    def generate_plan(self, selected_space: str, original_prompt: str, selected_enhanced_prompts: List[str]) -> tuple[Optional[str], str]:
        """
        Generates a strategic plan based on the selected enhanced prompts.
        Formats the plan into a user-friendly HTML output.
        """
        if not selected_enhanced_prompts:
            return None, "Please select at least one enhanced prompt to build a plan."
        
        try:
            payload = {
                "space": selected_space, 
                "original_prompt": original_prompt, 
                "enhanced_prompts": selected_enhanced_prompts
            }
            response = requests.post(f"{self.api_base_url}/plan/", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            # Handle potential variations in the API response structure
            plan_data = data.get("data", {})
            if not plan_data and isinstance(data.get('plan'), dict):
                plan_data = data.get('plan', {})
            
            # Start building the HTML for the plan display
            formatted_plan = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
    <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.5em;">🎯</span>
        Strategic Plan Generated
    </h2>
</div>
"""
            
            # Add the original query to the plan display
            if 'plan_context' in plan_data and 'query' in plan_data['plan_context']:
                formatted_plan += f"""
<div style="background: #f8f9ff; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #667eea;">
    <h3 style="margin-top: 0; color: #4a5568; display: flex; align-items: center; gap: 8px;">
        <span>📝</span> Original Query
    </h3>
    <p style="margin-bottom: 0; color: #2d3748; font-style: italic;">{plan_data['plan_context']['query']}</p>
</div>
"""
            
            # Add the execution steps to the plan display
            if 'steps' in plan_data and plan_data['steps']:
                formatted_plan += """
<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    <h3 style="margin-top: 0; color: #2d3748; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
        <span>📋</span> Execution Steps
    </h3>
"""
                for i, step in enumerate(plan_data['steps'], 1):
                    task = step.get('task', 'No task description')
                    tool = step.get('tool_id', 'No tool specified')
                    formatted_plan += f"""
<div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #fafbfc;">
    <div style="display: flex; align-items: flex-start; gap: 10px;">
        <div style="background: #667eea; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9em; flex-shrink: 0;">{i}</div>
        <div style="flex: 1;">
            <h4 style="margin: 0 0 8px 0; color: #2d3748;">{task}</h4>
            <div style="display: flex; align-items: center; gap: 15px; font-size: 0.9em;">
                <div style="color: #4a5568; display: flex; align-items: center; gap: 5px;">
                    <span>🔧</span> <strong>Tool:</strong> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{tool}</code>
                </div>
"""
                    if 'output' in step and step['output']:
                        formatted_plan += f"""
                <div style="color: #4a5568; display: flex; align-items: center; gap: 5px;">
                    <span>📤</span> <strong>Output:</strong> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{step['output']}</code>
                </div>
"""
                    formatted_plan += """
            </div>
        </div>
    </div>
</div>
"""
                formatted_plan += "</div>"
            else:
                formatted_plan += """
<div style="background: #fff5f5; border: 1px solid #fed7d7; border-radius: 10px; padding: 20px; text-align: center;">
    <p style="margin: 0; color: #c53030;">⚠️ No steps were generated in the plan.</p>
</div>
"""
            
            # Store the full plan data for execution
            self.generated_plan = plan_data
            return formatted_plan, "Strategic plan generated successfully!"

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API server."
        except requests.exceptions.RequestException as e:
            return None, f"API request failed: {e}"
        except json.JSONDecodeError:
            return None, "Error: Could not parse the plan from the API response."
        except Exception as e:
            return None, f"An error occurred while generating the plan: {str(e)}"

    def format_step_output(self, step_key: str, step_data: dict) -> str:
        """Helper function to format a single step's output"""
        return f"""
        <div style="margin-bottom: 25px; border-left: 4px solid #4CAF50; padding-left: 15px;">
            <h3 style="margin-top: 0; color: #2d3748;">{step_key.replace('_', ' ').title()}</h3>
            <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #4a5568;">Value:</h4>
                <div style="white-space: pre-wrap; color: #2d3748;">{step_data.get('value', 'No value provided')}</div>
            </div>
            <div style="background: #f0fff4; padding: 12px; border-radius: 8px;">
                <h4 style="margin-top: 0; color: #2d3748; margin-bottom: 5px;">Summary:</h4>
                <div style="white-space: pre-wrap; color: #2d3748;">{step_data.get('summary', 'No summary available')}</div>
            </div>
        </div>
        """

    def execute_plan(self, plan_content: str) -> tuple[Optional[str], str]:
        """
        Executes the generated plan by sending it to the API's run_plan endpoint.
        Formats the execution result into a user-friendly HTML output.
        """
        if not self.generated_plan:
             return None, "No valid plan to execute."
        
        try:
            # Extract the plan ID from the generated plan
            plan_id = self.generated_plan.get('id')
            if not plan_id:
                return None, "No plan ID found in the generated plan."
                
            # Get the sector from the plan context if available
            sector = self.generated_plan.get('plan_context', {}).get('sector', 'marketing-advertising')
            
            # Prepare the payload with the required fields
            payload = {
                "plan_id": plan_id,
                "sector": sector
            }
            
            print(f"Sending payload to run_plan: {json.dumps(payload, indent=2)}")
            
            response = requests.post(f"{self.api_base_url}/run_plan/", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success', False):
                return None, data.get('error', 'Failed to execute plan')
                
            result_data = data.get('data', {})
            step_outputs = result_data.get('outputs', {}).get('step_outputs', {})
            final_output = result_data.get('outputs', {}).get('final_output', {})
            
            # Build the HTML content
            html_content = """
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1000px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                            padding: 25px; border-radius: 12px; color: white; margin-bottom: 30px;">
                    <h1 style="margin: 0 0 10px 0; font-size: 28px;">🎯 Plan Execution Results</h1>
                    <div style="display: flex; gap: 15px; font-size: 14px; opacity: 0.9;">
                        <span>Plan ID: {plan_id}</span>
                        <span>Status: {status}</span>
                    </div>
                </div>
            """.format(
                plan_id=result_data.get('plan_id', 'N/A'),
                status=result_data.get('state', 'UNKNOWN')
            )
            
            # Add each step's output
            for step_key, step_data in step_outputs.items():
                html_content += self.format_step_output(step_key, step_data)
            
            # Add final output
            if final_output:
                html_content += """
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e2e8f0;">
                    <h2 style="color: #2d3748; margin-bottom: 20px;">🎉 Final Output</h2>
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                        <h3 style="margin-top: 0; color: #4a5568;">Value:</h3>
                        <div style="white-space: pre-wrap; color: #2d3748; line-height: 1.6;">
                            {value}
                        </div>
                    </div>
                    <div style="background: #f0fff4; padding: 20px; border-radius: 8px;">
                        <h3 style="margin-top: 0; color: #4a5568;">Summary:</h3>
                        <div style="white-space: pre-wrap; color: #2d3748; line-height: 1.6;">
                            {summary}
                        </div>
                    </div>
                </div>
                """.format(
                    value=final_output.get('value', 'No value provided'),
                    summary=final_output.get('summary', 'No summary available')
                )
            
            # Close the main container
            html_content += "</div>"
            
            return html_content, "Plan executed successfully!"
            
            # Format execution result into an HTML block
            formatted_result = f"""
<div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
    <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.5em;">🎉</span>
        Plan Executed Successfully!
    </h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    <h3 style="margin-top: 0; color: #2d3748; display: flex; align-items: center; gap: 8px;">
        <span>📊</span> Execution Results
    </h3>
    <div style="background: #f7fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
        <pre style="margin: 0; white-space: pre-wrap; font-family: 'Courier New', monospace; color: #2d3748;">{result}</pre>
    </div>
</div>
"""
            
            return formatted_result, "Plan executed successfully!"
        except requests.exceptions.RequestException as e:
            return None, f"API request failed during execution: {e}"
        except Exception as e:
            return None, f"An error occurred during plan execution: {str(e)}"

# Instantiate the main application logic class
strategy_builder = StrategyBuilder()

# CSS for styling the Gradio interface
css = """
/* Global Styling */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 20px !important;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    min-height: 100vh;
}
/* Header Styling */
.main-header {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}
.main-header h1 {
    color: white !important;
    font-size: 3.2em !important;
    margin-bottom: 10px !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.main-header p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.3em !important;
    margin: 0 !important;
    font-weight: 300;
}
/* Tab Styling */
.tab-nav {
    background: white !important;
    border-radius: 15px !important;
    padding: 8px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    margin-bottom: 25px !important;
}
.tab-nav button {
    font-size: 1.1em !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    border: none !important;
    background: transparent !important;
    color: #4a5568 !important;
}
.tab-nav button.selected {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3) !important;
}
.tab-nav button:hover:not(.selected) {
    background: #f7fafc !important;
    color: #2d3748 !important;
}
/* Content Cards */
.content-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
    border: 1px solid rgba(102, 126, 234, 0.1);
}
/* Step Headers */
.step-header {
    font-size: 1.8em !important;
    font-weight: 700 !important;
    color: #2d3748 !important;
    margin-bottom: 20px !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding-bottom: 15px;
    border-bottom: 2px solid #e2e8f0;
}
.step-header span {
    font-size: 1.2em;
    padding: 8px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
/* Hide Gradio Footer */
footer {
    display: none !important;
}
"""

def create_ui():
    """Creates the Gradio user interface and wires up all the event handlers."""
    with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="blue", secondary_hue="sky"), title="AI Strategy Builder") as demo:
        
        # Main Header
        gr.HTML("""
        <div class="main-header">
            <h1>🚀 AI Strategy Builder</h1>
            <p>Transform your ideas into actionable strategies with AI-powered intelligence</p>
        </div>
        """)
        
        with gr.Tabs(elem_classes=["tab-nav"]) as tabs:
            # Tab 1: Ideate & Enhance
            with gr.Tab("💡 Ideate & Enhance", id=0):
                with gr.Column(elem_classes=["content-card"]):
                    gr.HTML('<div class="step-header"><span>💡</span>Define Your Vision</div>')
                    
                    with gr.Row():
                        space_dropdown = gr.Dropdown(
                            choices=strategy_builder.fetch_spaces(), 
                            label="🏢 Select Your Domain", 
                            interactive=True, 
                            info="Choose the area your idea belongs to"
                        )
                        refresh_spaces_btn = gr.Button("🔄 Refresh", size="sm")
                    
                    user_prompt = gr.Textbox(
                        label="📝 Describe Your Vision", 
                        placeholder="Example: 'Launch a sustainable marketing campaign for eco-friendly products...'",
                        lines=4
                    )
                    
                    enhance_btn = gr.Button("✨ Enhance My Idea", variant="primary", size="lg")

            # Tab 2: Generate Plan  
            with gr.Tab("📋 Generate Plan", id=1):
                with gr.Column(elem_classes=["content-card"]):
                    gr.HTML('<div class="step-header"><span>📋</span>Build Your Strategic Plan</div>')
                    
                    with gr.Accordion("🤖 AI-Enhanced Suggestions", open=True):
                        enhanced_prompts_checkbox = gr.CheckboxGroup(
                            label="Select suggestions to include in your strategic plan:",
                            interactive=True
                        )
                    
                    generate_plan_btn = gr.Button(
                        "🎯 Generate Strategic Plan", 
                        variant="primary", 
                        size="lg", 
                        interactive=False
                    )
                    
                    plan_output = gr.HTML(
                        value="<div style='text-align: center; padding: 40px; color: #a0aec0;'><h3>🎯 Your strategic plan will appear here</h3></div>"
                    )

            # Tab 3: Execute & Review
            with gr.Tab("⚡ Execute & Review", id=2):
                with gr.Column(elem_classes=["content-card"]):
                    gr.HTML('<div class="step-header"><span>⚡</span>Execute Your Strategy</div>')
                    
                    execute_btn = gr.Button(
                        "🚀 Execute Strategy Now!", 
                        variant="primary", 
                        size="lg", 
                        interactive=False
                    )
                    
                    execution_output = gr.HTML(
                        value="<div style='text-align: center; padding: 40px; color: #a0aec0;'><h3>⚡ Execution results will appear here</h3></div>"
                    )

        # --- Event Handlers ---
        # These functions are defined inside create_ui to have access to the UI components.

        def refresh_spaces():
            gr.Info("🔄 Fetching latest domains...")
            new_spaces = strategy_builder.fetch_spaces()
            return gr.Dropdown(choices=new_spaces)

        def on_enhance_prompt(space, prompt):
            if not space or not prompt.strip():
                gr.Warning("⚠️ Please select a domain and describe your idea first!")
                return {enhanced_prompts_checkbox: gr.update(choices=[], value=[])}
            
            gr.Info("🧠 AI is analyzing your idea...")
            enhanced_prompts, message = strategy_builder.enhance_prompt(space, prompt)

            if enhanced_prompts:
                gr.Success(f"✅ {message}")
                return {
                    enhanced_prompts_checkbox: gr.update(choices=enhanced_prompts, value=[], interactive=True),
                    tabs: gr.update(selected=1)
                }
            else:
                gr.Error(f"❌ {message}")
                return {enhanced_prompts_checkbox: gr.update(choices=[], value=[])}

        def on_checkbox_change(selections):
            is_active = bool(selections)
            button_text = f"🎯 Generate Strategic Plan ({len(selections)} selected)" if selections else "🎯 Generate Strategic Plan"
            return gr.update(interactive=is_active, value=button_text)

        def on_generate_plan(space, original_prompt, selected_prompts):
            if not selected_prompts:
                gr.Warning("⚠️ Please select at least one enhanced prompt.")
                return {}, gr.update(), gr.update()
            
            gr.Info(f"🏗️ Generating your strategic plan...")
            plan, message = strategy_builder.generate_plan(space, original_prompt, selected_prompts)
            
            if plan:
                gr.Success(f"✅ {message}")
                return {
                    plan_output: gr.update(value=plan),
                    tabs: gr.update(selected=2),
                    execute_btn: gr.update(interactive=True)
                }
            else:
                gr.Error(f"❌ {message}")
                error_html = f"""
                <div style="background: #fff5f5; border: 1px solid #fed7d7; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3 style="color: #c53030;">⚠️ Plan Generation Failed</h3>
                    <p style="color: #2d3748;">{message}</p>
                </div>
                """
                return {plan_output: gr.update(value=error_html), tabs: gr.update(), execute_btn: gr.update()}

        def on_execute_plan(plan):
            gr.Info("⚡ Executing your strategic plan...")
            result, message = strategy_builder.execute_plan(plan)
            
            if result:
                gr.Success(f"🎉 {message}")
                return {execution_output: gr.update(value=result)}
            else:
                gr.Error(f"❌ {message}")
                error_html = f"""
                <div style="background: #fff5f5; border: 1px solid #fed7d7; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3 style="color: #c53030;">⚠️ Execution Failed</h3>
                    <p style="color: #2d3748;">{message}</p>
                </div>
                """
                return {execution_output: gr.update(value=error_html)}

        # --- Wire up the events ---
        refresh_spaces_btn.click(fn=refresh_spaces, outputs=[space_dropdown])
        
        enhance_btn.click(
            fn=on_enhance_prompt,
            inputs=[space_dropdown, user_prompt],
            outputs=[enhanced_prompts_checkbox, tabs]
        )
        
        enhanced_prompts_checkbox.change(
            fn=on_checkbox_change,
            inputs=[enhanced_prompts_checkbox],
            outputs=[generate_plan_btn]
        )
        
        generate_plan_btn.click(
            fn=on_generate_plan,
            inputs=[space_dropdown, user_prompt, enhanced_prompts_checkbox],
            outputs=[plan_output, tabs, execute_btn]
        )
        
        execute_btn.click(
            fn=on_execute_plan,
            inputs=[plan_output],
            outputs=[execution_output]
        )
    
    return demo

def main():
    """Main function to create and launch the Gradio application."""
    try:
        print("=" * 60)
        print("🚀 AI STRATEGY BUILDER - STARTING UP")
        print("=" * 60)
        
        app = create_ui()
        
        print("✅ UI components loaded successfully")
        print("📡 Testing API connection...")
        
        # Test API connection on startup
        try:
            test_response = requests.get("http://127.0.0.1:8000/api/sectors/", timeout=5)
            if test_response.status_code == 200:
                print("✅ API server connection: SUCCESS")
            else:
                print(f"⚠️ API server responding with status: {test_response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ API server connection: FAILED")
            print("💡 Make sure your API server is running on http://127.0.0.1:8000")
        
        print("=" * 60)
        print("🌐 GRADIO INTERFACE LAUNCHING...")
        
        app.launch(
            server_name="127.0.0.1", 
            server_port=7860, 
            show_error=True,
            inbrowser=True
        )
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ STARTUP ERROR")
        print(f"An unexpected error occurred: {str(e)}")
        print("=" * 60)

if __name__ == "__main__":
    main()