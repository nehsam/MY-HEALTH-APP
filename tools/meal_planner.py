from pydantic import BaseModel
from typing import List
from agents import function_tool, RunContextWrapper
from context import UserSessionContext


class MealPlanOutput(BaseModel):
    days: List[str]

@function_tool
async def plan_meals(ctx: RunContextWrapper[UserSessionContext]) -> MealPlanOutput:
    preference = ctx.context.diet_preferences or "balanced"

    if "vegetarian" in preference.lower():
        plan = [
            "Day 1: Veggie stir-fry with tofu",
            "Day 2: Lentil soup with whole grain bread",
            "Day 3: Grilled paneer with quinoa",
            "Day 4: Chickpea curry with rice",
            "Day 5: Stuffed bell peppers",
            "Day 6: Mixed veggie pasta",
            "Day 7: Spinach and mushroom pizza"
        ]
    else:
        plan = [
            "Day 1: Grilled chicken with broccoli",
            "Day 2: Fish curry with rice",
            "Day 3: Turkey sandwich",
            "Day 4: Egg salad",
            "Day 5: Beef stir-fry",
            "Day 6: Chicken soup",
            "Day 7: Tuna pasta"
        ]

    ctx.context.meal_plan = plan
    return MealPlanOutput(days=plan)
