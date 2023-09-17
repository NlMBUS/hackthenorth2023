import os
import openai
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_review(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt},],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.get("choices")[0].get("message").get("content")
