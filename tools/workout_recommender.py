from pydantic import BaseModel
from typing import List
from agents import function_tool, RunContextWrapper
from context import UserSessionContext


class WorkoutPlanOutput(BaseModel):
    plan: List[str]

@function_tool
async def recommend_workout(ctx: RunContextWrapper[UserSessionContext]) -> WorkoutPlanOutput:
    goal = ctx.context.goal or {}
    experience = goal.get("experience_level", "beginner")

    if experience == "beginner":
        workouts = [
            "Day 1: Full body stretching",
            "Day 2: Light cardio (15 mins)",
            "Day 3: Bodyweight strength (squats, pushups)",
            "Day 4: Rest day",
            "Day 5: Light yoga",
            "Day 6: Walking (30 mins)",
            "Day 7: Rest day"
        ]
    else:
        workouts = [
            "Day 1: Upper body strength",
            "Day 2: HIIT cardio",
            "Day 3: Lower body strength",
            "Day 4: Core workout",
            "Day 5: Yoga or mobility",
            "Day 6: Full body circuit",
            "Day 7: Active recovery"
        ]

    ctx.context.workout_plan = {"level": experience, "schedule": workouts}
    return WorkoutPlanOutput(plan=workouts)
