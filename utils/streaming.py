
import os, asyncio, textwrap
from groq import Groq
from groq import GroqError


client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama3-8b-8192"         # free & fast
# MODEL_NAME = "llama3-70b-8192"      # bigger, slower


async def stream_agent_response(user_input: str, *, placeholder=None) -> str:
    """
    Simple helper: blocking Groq completion ko background thread me run karta hai.
    Streaming API bhi possible hai, but yahan ek‑shot response enough hai.
    """
    try:
        def _generate():
            return client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_input}],
            )

        response = await asyncio.to_thread(_generate)
        text = response.choices[0].message.content.strip()

        if placeholder:
            placeholder.markdown(textwrap.dedent(text))
        else:
            print(text)

        return text

    except GroqError as e:
        err = f"❌ Groq API error: {e}"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err
