import gradio as gr
import requests
import json
from typing import List, Optional
import time

class StrategyBuilder:
    def __init__(self):
        self.api_base_url = "http://127.0.0.1:8000/api"
        self.spaces = []
        self.enhanced_prompts = []
        self.generated_plan = ""

    def fetch_spaces(self) -> List[str]:
        """Fetch available spaces/categories from API"""
        try:
            response = requests.get(f"{self.api_base_url}/spaces/")
            response.raise_for_status()
            data = response.json()
            self.spaces = [space['name'] for space in data] if isinstance(data, list) else data
            return self.spaces
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching spaces: {e}")
            return ["Marketing", "Sales", "SEO", "Content", "Product", "Custom"]

    def enhance_prompt(self, selected_space: str, user_prompt: str) -> tuple[Optional[List[str]], str]:
        """Call API to enhance user prompt and return list of enhanced suggestions"""
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

            # Clean the string and parse JSON
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
        """Generate plan based on selected enhanced prompts"""
        if not selected_enhanced_prompts:
            return None, "Please select at least one enhanced prompt to build a plan."
        
        try:
            payload = {
                "space": selected_space, 
                "original_prompt": original_prompt, 
                "enhanced_prompts": selected_enhanced_prompts
            }
            response = requests.post(f"{self.api_base_url}/generate-plan/", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

            plan = data.get("plan")
            if not plan:
                # Fallback for nested data structure
                if isinstance(data.get('data'), str):
                    plan_str = data['data'].replace('```json', '').replace('```', '').strip()
                    plan_data = json.loads(plan_str)
                    plan = plan_data.get('plan')

            if plan:
                self.generated_plan = plan
                return self.generated_plan, "Strategic plan generated successfully!"
            else:
                return None, "No valid plan was returned from the API."

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API server."
        except requests.exceptions.RequestException as e:
            return None, f"API request failed: {e}"
        except json.JSONDecodeError:
            return None, "Error: Could not parse the plan from the API response."
        except Exception as e:
            return None, f"An error occurred while generating the plan: {str(e)}"

    def execute_plan(self, plan_content: str) -> tuple[Optional[str], str]:
        """Execute the generated plan"""
        if not self.generated_plan:
             return None, "No valid plan to execute."
        
        try:
            payload = {"plan": self.generated_plan}
            response = requests.post(f"{self.api_base_url}/execute-plan/", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            result = data.get("execution_result", "")
            return result, "Plan executed successfully!"
        except requests.exceptions.RequestException as e:
            return None, f"API request failed during execution: {e}"
        except Exception as e:
            return None, f"An error occurred during plan execution: {str(e)}"

strategy_builder = StrategyBuilder()

css = """
/* (Your existing CSS is good, no changes needed here) */
body { background-color: #F8F9FA !important; } .gradio-container { max-width: 1200px !important; margin: auto; border-radius: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); } .step-header { font-size: 24px; font-weight: 600; color: #2c3e50; margin-bottom: 10px; display: flex; align-items: center; } .step-header span { margin-right: 12px; } .tab-item { font-size: 16px !important; } .gr-button-primary { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); } footer { display: none !important; } .feedback-info { font-style: italic; color: #576574; text-align: center; padding: 10px; }
"""

def create_ui():
    with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="blue", secondary_hue="sky")) as demo:
        gr.Markdown(
            """<div style="text-align: center; padding: 20px;"><h1 style="color: #182848; font-size: 3em;">🚀 AI Strategy Builder</h1><p style="color: #576574; font-size: 1.2em;">Your intelligent partner for building, enhancing, and executing powerful strategies.</p></div>"""
        )
        
        with gr.Tabs() as tabs:
            with gr.Tab("1. Ideate & Enhance", id=0):
                gr.Markdown("<h2 class='step-header'><span>💡</span>Define Your Core Idea</h2>")
                with gr.Row():
                    with gr.Column(scale=3):
                        space_dropdown = gr.Dropdown(choices=strategy_builder.fetch_spaces(), label="Select Domain / Space", interactive=True, info="Choose the area your idea belongs to.")
                    with gr.Column(scale=1, min_width=150):
                        refresh_spaces_btn = gr.Button("🔄 Refresh Spaces")
                user_prompt = gr.Textbox(label="Describe Your Goal or Initial Idea", placeholder="e.g., 'Launch a marketing campaign for a new sustainable coffee brand'", lines=4)
                enhance_btn = gr.Button("✨ Enhance My Idea", variant="primary", size="lg")
                
            with gr.Tab("2. Generate Plan", id=1):
                gr.Markdown("<h2 class='step-header'><span>📝</span>Build Your Strategic Plan</h2>")
                with gr.Accordion("🤖 AI-Enhanced Suggestions", open=True) as enhanced_section:
                    enhanced_prompts_checkbox = gr.CheckboxGroup(label="Select suggestions to include in your plan. The 'Generate' button will activate once you select at least one.", interactive=True)
                
                generate_plan_btn = gr.Button("📋 Generate Strategic Plan", variant="primary", size="lg", interactive=False)
                plan_output = gr.Markdown(value="*Your plan will appear here...*")

            with gr.Tab("3. Execute & Review", id=2):
                gr.Markdown("<h2 class='step-header'><span>⚡</span>Execute and See Results</h2>")
                gr.Markdown("The AI will now process the generated plan and produce the final output.")
                execute_btn = gr.Button("🚀 Execute Plan!", variant="primary", size="lg", interactive=False)
                execution_output = gr.Markdown(value="*Execution results will appear here...*")

        # Event Handlers
        def refresh_spaces():
            gr.Info("Fetching latest spaces...")
            new_spaces = strategy_builder.fetch_spaces()
            return gr.Dropdown(choices=new_spaces)

        def on_enhance_prompt(space, prompt):
            if not space or not prompt.strip():
                gr.Warning("Please select a space and describe your idea first!")
                return {enhanced_prompts_checkbox: gr.update(choices=[], value=[])}
            
            gr.Info("AI is thinking... Enhancing your prompt!")
            enhanced_prompts, message = strategy_builder.enhance_prompt(space, prompt)

            if enhanced_prompts:
                gr.Success(message)
                return {
                    enhanced_prompts_checkbox: gr.update(choices=enhanced_prompts, value=[], interactive=True),
                    tabs: gr.update(selected=1) # <<< CHANGE: Automatically switch to the plan generation tab
                }
            else:
                gr.Error(message)
                return {enhanced_prompts_checkbox: gr.update(choices=[], value=[])}

        def on_checkbox_change(selections):
            # Enable the generate button only if at least one checkbox is selected
            return gr.update(interactive=bool(selections))

        def on_generate_plan(space, original_prompt, selected_prompts):
            if not selected_prompts:
                gr.Warning("You must select at least one enhanced prompt.")
                return {}
            
            gr.Info("Generating your strategic plan... This might take a moment.")
            plan, message = strategy_builder.generate_plan(space, original_prompt, selected_prompts)
            
            if plan:
                gr.Success(message)
                return {
                    plan_output: gr.update(value=plan),
                    tabs: gr.update(selected=2),
                    execute_btn: gr.update(interactive=True)
                }
            else:
                gr.Error(message)
                return {plan_output: gr.update(value=f"### Generation Failed\n> {message}")}

        def on_execute_plan(plan):
            gr.Info("Executing the plan...")
            result, message = strategy_builder.execute_plan(plan)
            
            if result:
                gr.Success(message)
                return {execution_output: gr.update(value=result)}
            else:
                gr.Error(message)
                return {execution_output: gr.update(value=f"### Execution Failed\n> {message}")}

        # Wire up the events
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
        
        gr.Markdown("""<div class="feedback-info"><p>💡 **Tip:** Make sure your API server is running on `http://127.0.0.1:8000`</p></div>""")
    return demo

if __name__ == "__main__":
    app = create_ui()
    print("🚀 Starting AI Strategy Builder...")
    print("📡 Make sure your API server is running on http://127.0.0.1:8000")
    print("🌐 Gradio interface will be available at http://127.0.0.1:7860")
    app.launch(server_name="127.0.0.1", server_port=7860, show_error=True)