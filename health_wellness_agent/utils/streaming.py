import os
import asyncio
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

async def stream_agent_response(user_input: str, *, placeholder=None) -> str:
    if not user_input or not user_input.strip():
        err = "❌ Empty input provided"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err

    try:
        def _generate():
            return model.generate_content(user_input.strip())

        response = await asyncio.to_thread(_generate)

        if not response or not hasattr(response, 'text'):
            err = "❌ No valid response from Gemini API"
            if placeholder:
                placeholder.error(err)
            else:
                print(err)
            return err

        text = response.text.strip()

        if placeholder:
            placeholder.markdown(textwrap.dedent(text))
        else:
            print(text)

        return text

    except Exception as e:
        err = f"❌ Unexpected error: {str(e)}"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err

def get_gemini_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        if not response or not hasattr(response, 'text'):
            return "❌ No valid response from Gemini API"
        return response.text
    except Exception as e:
        # Debug print for error details
        st.error(f"Gemini API error details: {e}")
        return f"❌ Gemini API error: {e}"

def test_gemini_connection():
    try:
        response = model.generate_content("Hello, just testing Gemini connection.")
        return True, "✅ Connection successful"
    except Exception as e:
        return False, f"❌ Connection failed: {str(e)}"