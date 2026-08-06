from litellm import completion
import config
from google import genai
import streamlit as st

client = genai.Client(api_key=config.GEMINI_API_KEY)


class GeminiServiceError(Exception):
    """Raised when the Gemini API call fails."""
    pass

@st.cache_data(show_spinner="Asking Gemini...")
def ask_gemini(message_list, msg):
    """
    Calls Gemini LLM with given prompt, and history(optional)
    Returns a str that contains the reponse
    """
    # make a copy since msg is not going to be stored in session_state
    if not message_list:
        msg_list = []
    else:
        msg_list = [{"role": role, "content": content} for role, content in message_list]

    msg_list.append({"role": "user", "content": msg})

    try:
        response = completion(
            api_key=config.GEMINI_API_KEY,
            model=config.MODEL,
            messages=msg_list,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        # translate any underlying error (litellm, network, etc.) into our own type
        raise GeminiServiceError(f"Gemini API call failed: {e}") from e

