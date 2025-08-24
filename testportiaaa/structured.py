from portia.plan import PlanBuilder
from pydantic import BaseModel
from dotenv import load_dotenv
from portia import (
    Portia,
    default_config,
    example_tool_registry,
)

load_dotenv()
portia = Portia(tools=example_tool_registry)

# Final Output schema type to coerce to
class FinalPlanOutput(BaseModel):
    result: float # result here is an integer output from calculator tool, but will be converted to a float via structured output

# Example via plan builder, attach to the plan at top level
plan = PlanBuilder(
  "Add 1 + 1", structured_output_schema=FinalPlanOutput
).step(
  "Add 1 + 1", tool_id='calculator_tool'
).build()

# Example via plan interface
plan2 = portia.plan("Add 1 + 1", structured_output_schema=FinalPlanOutput)