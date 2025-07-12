from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    input_guardrail,
    output_guardrail
)
from context import UserSessionContext


class GoalInputGuardrailOutput(BaseModel):
    is_valid: bool
    reason: str


goal_check_agent = Agent(
    name="Goal Validator",
    instructions="Check if the input goal is in valid format (e.g. 'lose 5kg in 2 months')",
    output_type=GoalInputGuardrailOutput,
)

@input_guardrail
async def validate_goal_input(
    ctx: RunContextWrapper[UserSessionContext],
    agent: Agent,
    input: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(goal_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_valid
    )
