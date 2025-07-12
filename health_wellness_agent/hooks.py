from agents import RunHooks

class CustomRunHooks(RunHooks):
   

    # Tool start
    async def on_tool_start(self, event):  # no type annotation needed
        try:
            tool_name = event.tool.name
        except AttributeError:
            tool_name = "unknown"
        print(f"[HOOK] Tool started: {tool_name}")

    # Tool end
    async def on_tool_end(self, event):
        try:
            tool_name = event.tool.name
        except AttributeError:
            tool_name = "unknown"
        print(f"[HOOK] Tool finished: {tool_name}")

    # Handoff
    async def on_handoff(self, event):
        try:
            agent_name = event.handoff.agent.name
        except AttributeError:
            agent_name = "unknown"
        print(f"[HOOK] Handoff to: {agent_name}")
