from litellm import completion
import config
from google import genai

client = genai.Client(api_key=config.GEMINI_API_KEY)
# message = [{"role": "user", "content": "tell me a short joke"}]
# sample_msg = prompts.generate_system_prompt("I love reading harry potter books. I also enjoy books from the author JRR Tolkien")
# print(sample_msg)
def ask_gemini(message_list, msg):
    # make a copy since msg is not going to be stored in session_state
    msg_list = message_list.copy()
    msg_list.append({"role": "user", "content": msg})

    response = completion(
        api_key=config.GEMINI_API_KEY,
        model=config.MODEL,
        messages=msg_list,
        stream=False
    )
    return response.choices[0].message.content