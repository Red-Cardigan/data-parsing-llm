import os
from dotenv import load_dotenv
from string import Template
import re
import json
import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from typing import Optional

load_dotenv(dotenv_path='..env')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
# OpenAI.set_key(OPENAI_API_KEY)
OPENAI_API_KEY='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'

# Call the LLM with prefilled prompt templates
def get_prefilled_prompt(json_data, field_key):
    return json_data["items"].get(field_key)

def phrase_prompt(prompt: str, api_key: str, max_tokens: int) -> str:
    """
    Generates a completion using OpenAI's chat model based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (str): OpenAI API key for authentication.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The content of the model's response.
    """
    try:
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are an ESG analyst with a strong grasp of the language used in your field. {context from Jan}"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during question generation: {e}")
        return prompt
