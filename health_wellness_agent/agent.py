from agents import Agent, handoff

# local modules
from context import UserSessionContext
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import plan_meals
from tools.workout_recommender import recommend_workout
from tools.scheduler import schedule_checkins
from tools.tracker import track_progress
from guardrails import validate_goal_input


# specialised handoff agents
from special_agents.escalation_agent import escalation_agent
from special_agents.nutrition_expert_agent import nutrition_expert_agent
from special_agents.injury_support_agent import injury_support_agent

# ──────────────────────────────────────────────────────────────
# Main health & wellness planner agent
# ──────────────────────────────────────────────────────────────
agent = Agent(
    name="Health Wellness Planner",
    instructions=(
        "You are a helpful wellness planner. Collect the user's fitness and "
        "dietary goals, generate personalised meal & workout plans, track "
        "progress, and schedule reminders. Delegate to specialist agents when "
        "necessary (nutrition, injury, escalation)."
    ),
    tools=[
        analyze_goal,
        plan_meals,
        recommend_workout,
        schedule_checkins,
        track_progress,
    ],
    input_guardrails=[validate_goal_input],
    handoffs=[
        handoff(escalation_agent),
        handoff(nutrition_expert_agent),
        handoff(injury_support_agent),
    ],
    # ❌ run_hooks=CustomRunHooks(),  ← is line ko hata dein
)