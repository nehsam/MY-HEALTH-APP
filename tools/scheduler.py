from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def schedule_checkins(ctx: RunContextWrapper[UserSessionContext]) -> str:
    # Dummy logic to simulate scheduling
    log_entry = "Check-ins scheduled every Monday at 8 AM."
    ctx.context.progress_logs.append({"event": "checkin_scheduled", "message": log_entry})
    return log_entry
