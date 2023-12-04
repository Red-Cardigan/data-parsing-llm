import os
# from dotenv import load_dotenv
from string import Template
import re
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.chat_models.base import BaseChatModel, SimpleChatModel
from app import MozartMistral
from .templates import meta_template, meta_template_string

# load_dotenv(dotenv_path='..env')
# OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
# # OpenAI.set_key(OPENAI_API_KEY)
# OPENAI_API_KEY='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'

# Call the LLM with prefilled prompt templates
def get_prefilled_prompt(json_data, field_key):
    return json_data["items"].get(field_key)

def get_llm(provider):
    if provider == 'azure':
        return AzureChatOpenAI(
            deployment_name="mozart-ai-gpt-35",
            openai_api_version="2023-07-01-preview",
            temperature=0,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1.0,
        )
    elif provider == 'gpt3':
        return ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1.0,
        )
    elif provider == 'mozart':
        return MozartMistral(
            model_dir="/model",
            template='''<s>[INST] <<SYS>>
                {system}
                <</SYS>>

                {user} [/INST] ''',
            temperature=0.1,
            top_p=0.95,
            presence_penalty=1.15,
            max_tokens=50
        )
    else:
        return ChatOpenAI(
            model_name="gpt-4-1106-preview",
            temperature=0,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1.0,
        )

def phrase_prompt(provider: str, prompt: str, api_key: str, max_tokens: int) -> str:
    """
    Generates questions to ask the docs based on the description.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (str): OpenAI API key for authentication.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The content of the model's response.
    """
    model = get_llm(provider)
    try:
        response = model.generate(prompt, max_tokens=max_tokens)
        return response
    except Exception as e:
        print(f"Error during question generation: {e}")
        return prompt

def find_answer(target_unit, field_name, item, relevant_context, validation, json_data):

    if target_unit == 'str':
        model = "gpt4"
        final_answer_raw = model.invoke(meta_template_string.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))
    else:
        model = MozartMistral()
        final_answer_raw = model.invoke(meta_template.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))

    final_answer = re.findall(r'answer:\s*([^.]+)', str(final_answer_raw))

    if final_answer and validation != '5w_or_less':
        match = re.search(validation, final_answer[0])
        json_data["items"][field_name]["output"]["value"] = match.group() if match else "No answer in context"
    elif final_answer:
        json_data["items"][field_name]["output"]["value"] = final_answer
    else:
        json_data["items"][field_name]["output"]["value"] = "No answer in context"

    return json_data