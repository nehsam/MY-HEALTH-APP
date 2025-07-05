import os
import asyncio
import textwrap
from groq import Groq
from groq import GroqError


def initialize_groq_client():
    """Initialize Groq client with proper error handling"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return Groq(api_key=api_key)


# Initialize client with error handling
try:
    client = initialize_groq_client()
except ValueError as e:
    print(f"❌ Error initializing Groq client: {e}")
    client = None

MODEL_NAME = "llama3-8b-8192"         # free & fast
# MODEL_NAME = "llama3-70b-8192"      # bigger, slower


async def stream_agent_response(user_input: str, *, placeholder=None) -> str:
    """
    Simple helper: blocking Groq completion ko background thread me run karta hai.
    Streaming API bhi possible hai, but yahan ek‑shot response enough hai.
    """
    # Check if client is initialized
    if client is None:
        err = "❌ Groq client not initialized. Please check your GROQ_API_KEY."
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err
    
    # Validate input
    if not user_input or not user_input.strip():
        err = "❌ Empty input provided"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err
    
    try:
        def _generate():
            return client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_input.strip()}],
                max_tokens=1024,  # Add reasonable limit
                temperature=0.7,  # Add temperature for better responses
            )

        response = await asyncio.to_thread(_generate)
        
        # Better error handling for response
        if not response.choices:
            err = "❌ No response received from Groq API"
            if placeholder:
                placeholder.error(err)
            else:
                print(err)
            return err
        
        text = response.choices[0].message.content
        if not text:
            err = "❌ Empty response from Groq API"
            if placeholder:
                placeholder.error(err)
            else:
                print(err)
            return err
        
        text = text.strip()

        if placeholder:
            placeholder.markdown(textwrap.dedent(text))
        else:
            print(text)

        return text

    except GroqError as e:
        err = f"❌ Groq API error: {str(e)}"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err
    
    except Exception as e:
        err = f"❌ Unexpected error: {str(e)}"
        if placeholder:
            placeholder.error(err)
        else:
            print(err)
        return err


# Synchronous version for non-async contexts
def get_groq_response(user_input: str) -> str:
    """
    Synchronous version of the response function
    """
    if client is None:
        return "❌ Groq client not initialized. Please check your GROQ_API_KEY."
    
    if not user_input or not user_input.strip():
        return "❌ Empty input provided"
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_input.strip()}],
            max_tokens=1024,
            temperature=0.7,
        )
        
        if not response.choices:
            return "❌ No response received from Groq API"
        
        text = response.choices[0].message.content
        if not text:
            return "❌ Empty response from Groq API"
        
        return text.strip()
        
    except GroqError as e:
        return f"❌ Groq API error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


# Test function
def test_groq_connection():
    """Test if Groq connection is working"""
    try:
        if client is None:
            return False, "Client not initialized"
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Hello, just testing the connection."}],
            max_tokens=50,
        )
        
        return True, "Connection successful"
        
    except Exception as e:
        return False, f"Connection failed: {str(e)}"