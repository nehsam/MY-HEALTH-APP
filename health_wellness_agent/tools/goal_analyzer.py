from pydantic import BaseModel
from typing import Optional
from agents import function_tool, RunContextWrapper
from context import UserSessionContext


class GoalOutput(BaseModel):
    quantity: float
    metric: str
    duration: str
    description: Optional[str] = None


@function_tool  # decorator hi tool bana deta hai
async def analyze_goal(
    ctx: RunContextWrapper[UserSessionContext],
    input: str
) -> GoalOutput:
    """
    Very simple goal parser (demo purposes).
    """
    if "lose" in input.lower() and "kg" in input.lower():
        return GoalOutput(
            quantity=5,
            metric="kg",
            duration="2 months",
            description="Weight‑loss goal"
        )

    # fallback
    return GoalOutput(
        quantity=0,
        metric="",
        duration="",
        description="Unable to parse goal"
    )
