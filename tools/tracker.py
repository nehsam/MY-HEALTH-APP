from pydantic import BaseModel
from typing import Dict
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

class ProgressUpdateInput(BaseModel):
    update: str

@function_tool
async def track_progress(ctx: RunContextWrapper[UserSessionContext], input: ProgressUpdateInput) -> str:
    ctx.context.progress_logs.append({
        "event": "user_update",
        "message": input.update
    })
    return f"Progress update recorded: {input.update}"
