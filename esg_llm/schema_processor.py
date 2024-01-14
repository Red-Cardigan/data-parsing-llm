from typing import List, Dict, Any
import re
from .llm_utils import phrase_prompt
from string import Template
import os
from dotenv import load_dotenv
from string import Template
import re
import json
import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
# from app import MozartMistral
from .templates import unit_template, questions_template, search_template, meta_template, meta_template_string
from esg_llm.llm_utils import find_answer

load_dotenv(dotenv_path='./.env')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

# Expected input structure
# {
#     "field-name": "",
#     "description": "",
#     "llm": "",
#     "instruction": "",
#     "target-unit": ""
# }

# Example usage [name, value, {type}], also test data (see main):
# inputs = [
#     {'field-name':'diverse_csuite', 'description': 'C-suite individuals over 50 in DEI prog', 'llm':tesla, 'instruction':str, 'target-unit':'%'},
#     {'field-name':'workforce_count_start', 'description':'year workforce counting policy began', 'llm':tesla, 'instruction':str, 'target-unit':'year'},
#     {'field-name':'num_hispanic_managers', 'description':'total hispanic managers', 'llm':tesla, 'instruction':str, 'target-unit':'int'},
#     {'field-name':'dynamics_measures', 'description':'measures to improve workforce dynamics', 'llm':tesla, 'instruction':str, 'target-unit':'int'}
# ]

# - Applying regex validation rather than a manager prompt works consistently for int and float.

def create_json_schema(inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates a JSON schema based on the provided inputs.

    Args:
        inputs (List[Dict[str, Any]]): A list of input dictionaries.

    Returns:
        Dict[str, Any]: The generated JSON schema.
    """
    json_data = {"items": {}}

    # Mapping variable types to their corresponding units and validation regex
    type_mappings = {
        "%": {"unit": "%", "validation": "\\b\\d*\\.?\\d+\\b"},
        "year": {"unit": "year", "validation": "\\b(?:19|20)\\d{2}\\b"},
        "int": {"unit": "int", "validation": "\\b\\d+\\b"},
        "integer": {"unit": "int", "validation": "\\b\\d+\\b"},
        "count": {"unit": "int", "validation": "\\b\\d+\\b"},
        "str": {"unit": "str", "validation": "5w_or_less"} ,
    }

    for item in inputs:
        field_name = item["field-name"]
        description = item['description']
        context = item["llm"]
        filled_questions_template = questions_template.substitute(description = description, field_name = field_name) 
        target_unit_raw = unit_template.substitute(description = description, field_name = field_name)
        model = "gpt4" #or azure, mozart, gpt3.5
        # - process_json_schema() needs GPT-4 to get concise strings as responses. 
        # Presumably this will apply to generative answers when we do these


        ## Construct the generative/extractive prompts separately (we may want this later)
        #Generative
        # if target_unit == "%" or target_unit == 'int' or target_unit == 'year':  
            # filled_questions_template = questions_template.substitute(description = description)      
        #Extractive
        # elif target_unit == "str":    
        #     filled_questions_template = questions_template.substitute(description = description)


        # Generate questions to ask based on the description using GPT-3
        generated_questions = phrase_prompt(model, filled_questions_template, OPENAI_API_KEY, max_tokens=250)
        #Find relevant content in the input based on generated questions
        retrieved_context = search_template.substitute(questions = generated_questions, description = description, context = context)
        #Find a good target unit with GPT-3
        target_unit = re.findall(r'unit:\s*([^.\s]+)', phrase_prompt(target_unit_raw, OPENAI_API_KEY, max_tokens=20))
        
        # type_mappings.get(variable_type, {"unit": "", "validation": ""})

        ##Append retrieved_context to a doc to use as context for stuffing

        json_data["items"][field_name] = {
            "field_name":field_name,
            "generated_questions": generated_questions,
            "relevant_context": phrase_prompt(f"{generated_questions}\n{retrieved_context}", OPENAI_API_KEY, max_tokens = 500),
            "unit": target_unit[0].replace("<", "").replace(">", "") if target_unit else "str",
            "validation": type_mappings[target_unit[0]]["validation"] if target_unit and target_unit[0] in type_mappings else "5w_or_less",
            "output": {"value": None}
        }
        # "context":context,

    return json_data


def process_json_schema(inputs: List[Dict[str, Any]], json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the JSON schema with given inputs.

    Args:
        inputs (List[Dict[str, Any]]): The original input data.
        json_data (Dict[str, Any]): The pre-filled JSON template.

    Returns:
        Dict[str, Any]: The processed JSON schema (final output).
    """
    for item in inputs:
            field_name = item["field-name"]
            unit_info = json_data["items"][field_name]
            target_unit = unit_info['unit']
            validation = unit_info['validation']
            relevant_context = unit_info['relevant_context']
            # prompt = unit_info['filled_prompt_template']
            # search_findings = phrase_prompt(prompt, OPENAI_API_KEY)
            json_data = find_answer(target_unit, field_name, item, relevant_context, validation, json_data)

            # if target_unit == 'str':
            #     model = "gpt4"
            #     final_answer_raw = model.invoke(meta_template_string.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))
            # else:
            #     model = MozartMistral()
            #     # previous: gpt3
            #     # model = OpenAI(max_tokens=30), 
            #     final_answer_raw = model.invoke(meta_template.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))
            # # print(final_answer_raw)
            # final_answer = re.findall(r'answer:\s*([^.]+)', str(final_answer_raw))

            # # Validate and extract the relevant information
            # if final_answer and validation != '5w_or_less':
            #     #If string/ generative answer
            #     match = re.search(validation, final_answer[0])
            #     json_data["items"][field_name]["output"]["value"] = match.group() if match else "No answer in context"
            # elif final_answer:
            #     #Most answers are extractive and can be done with MozartMistral (prev: gpt3)
            #     json_data["items"][field_name]["output"]["value"] = final_answer
            # else:
            #     json_data["items"][field_name]["output"]["value"] = "No answer in context"

    return json_data

def process_input(inputs):
    # Find relevant context and preload JSON structure
    json_data = create_json_schema(inputs)
    # print(json.dumps(json_data, indent=4))

    # Fill output structures and return final answer
    output_json = process_json_schema(inputs, json_data)
    # print(json.dumps(output_json, indent=4))
    return output_json