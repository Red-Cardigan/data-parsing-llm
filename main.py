import os
from dotenv import load_dotenv
from string import Template
import re
import json
import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

load_dotenv(dotenv_path='.env')
# OPENAI_API_KEY=print(os.getenv('OPENAI_API_KEY'))
# OpenAI.set_key(OPENAI_API_KEY)

from esg_llm.schema_processor import process_input

OPENAI_API_KEY='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'

# Expected input structure
# {
#     "field-name": "",
#     "description": "",
#     "llm": "",
#     "instruction": "",
#     "target-unit": ""
# }

# Example usage [name, value, {type}], also test data (end of file):
# inputs = [
#     {'field-name':'diverse_csuite', 'description': 'C-suite individuals over 50 in DEI prog', 'llm':tesla, 'instruction':str, 'target-unit':'%'},
#     {'field-name':'workforce_count_start', 'description':'year workforce counting policy began', 'llm':tesla, 'instruction':str, 'target-unit':'year'},
#     {'field-name':'num_hispanic_managers', 'description':'total hispanic managers', 'llm':tesla, 'instruction':str, 'target-unit':'int'},
#     {'field-name':'dynamics_measures', 'description':'measures to improve workforce dynamics', 'llm':tesla, 'instruction':str, 'target-unit':'int'}
# ]


# - Needs GPT-4 to get concise strings as responses. Presumably will apply to generative answers when we do these
# - Applying regex validation rather than a manager prompt works consistently for int and float.

# unit_template = Template("Determine the most appropriate unit to store the data point described below.\
#                          This might be an int, %, year, str, or something else.\nfield name: $field_name\nfield description: $description\n return your answer as 'unit:<>'")

# questions_template = Template("Provide subcomponents to search for in a corpus of documents to find the value for this field.\nfield name: $field_name\ndescription: $description\nYanswer with a list of questions and nothing else'")

# search_template = Template("Search the context below for information relevant to the questions, and return only relevant information in bullet points.\nQuestions: $questions\nContext: $context")

# meta_template = Template("Find an final answer in the context below.\nfield name: $field_name\ndescription: $description\ncontext: $context\nunit: $target_unit\n return your answer as 'final answer:<>'")

# meta_template_string = Template("Use the information provided to return your final answer in 5 words or less.\nfield name: $field_name\ndescription: $description\ncontext: $context\nunit: $target_unit\nreturn your answer as 'final answer:<>'")

# def phrase_prompt(prompt, api_key, max_tokens):
#     try:
#         openai.api_key = api_key
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",  
#             messages=[
#                 {"role": "system", "content": "You are an ESG analyst with a strong grasp of the language used in your field. {context from Jan}"},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=max_tokens,  # adjust as needed
#             n=1,
#             stop=None,
#             temperature=0  # adjust for creativity
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"Error during question generation: {e}")
#         return prompt  # Fallback to original prompt in case of error
    
# def create_json_schema(inputs):
#     json_data = {"items": {}}

#     # Mapping variable types to their corresponding units and validation regex
#     type_mappings = {
#         "%": {"unit": "%", "validation": "\\b\\d*\\.?\\d+\\b"},
#         "year": {"unit": "year", "validation": "\\b(?:19|20)\\d{2}\\b"},
#         "int": {"unit": "int", "validation": "\\b\\d+\\b"},
#         "integer": {"unit": "int", "validation": "\\b\\d+\\b"},
#         "count": {"unit": "int", "validation": "\\b\\d+\\b"},
#         "str": {"unit": "str", "validation": "5w_or_less"} ,
#     }

#     for item in inputs:
#         description = item['description']
#         field_name = item["field-name"]
#         context = item["llm"]
#         filled_questions_template = questions_template.substitute(description = description, field_name = field_name) 
#         target_unit_raw = unit_template.substitute(description = description, field_name = field_name)

#         ## Construct the generative/extractive prompts separately (we may want this later)
#         #Generative
#         # if target_unit == "%" or target_unit == 'int' or target_unit == 'year':  
#             # filled_questions_template = questions_template.substitute(description = description)      
#         #Extractive
#         # elif target_unit == "str":    
#         #     filled_questions_template = questions_template.substitute(description = description)

#         # Generate questions to ask based on the description using GPT-3
#         generated_questions = phrase_prompt(filled_questions_template, OPENAI_API_KEY, max_tokens=250)
#         #Find relevant content in the input based on generated questions
#         retrieved_context = search_template.substitute(questions = generated_questions, context = context)
#         #Find a good target unit with GPT-3
#         target_unit = re.findall(r'unit:\s*([^.]+)', phrase_prompt(target_unit_raw, OPENAI_API_KEY, max_tokens=20))
        
#         # type_mappings.get(variable_type, {"unit": "", "validation": ""})

#         ##Append retrieved_context to a doc to use as context for stuffing

#         json_data["items"][field_name] = {
#             "field_name":field_name,
#             "generated_questions": generated_questions,
#             "relevant_context": phrase_prompt(f"{generated_questions}\n{retrieved_context}", OPENAI_API_KEY, max_tokens = 500),
#             "unit": target_unit[0].replace("<", "").replace(">", "") if target_unit else "str",
#             "validation": type_mappings[target_unit[0]]["validation"] if target_unit and target_unit[0] in type_mappings else "5w_or_less",
#             "output": {"value": None}
#         }
#         # "context":context,

#     return json_data

# # Call the LLM with prefilled prompt templates
# def get_prefilled_prompt(json_data, field_key):
#     return json_data["items"].get(field_key)

# def process_json_schema(inputs, json_data):
#     """
#     Takes original inputs and filled json template dict. You may want to play with templates and num tokens. 
#     Takes both original data and new json object
#     Ready for messing with for generative answer validation
#     """
#     for item in inputs:
#         field_name = item["field-name"]
#         unit_info = json_data["items"][field_name]
        
#         if unit_info['unit'] == "str":
#             model = ChatOpenAI(model_name="gpt-4", max_tokens=50)
#         else:
#             model = OpenAI(max_tokens=30)
#         target_unit = unit_info['unit']
#         validation = unit_info['validation']
#         relevant_context = unit_info['relevant_context']
#         # prompt = unit_info['filled_prompt_template']
#         # search_findings = phrase_prompt(prompt, OPENAI_API_KEY)
#         if target_unit == 'str':
#             final_answer_raw = model.invoke(meta_template_string.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))
#         else:
#             final_answer_raw = model.invoke(meta_template.substitute(field_name=field_name, description=item['description'], context=relevant_context, target_unit=target_unit))
#         # print(final_answer_raw)
#         final_answer = re.findall(r'answer:\s*([^.]+)', str(final_answer_raw))

#         # Validate and extract the relevant information
#         if final_answer and validation != '5w_or_less':
#             #If string/ generative answer
#             match = re.search(validation, final_answer[0])
#             json_data["items"][field_name]["output"]["value"] = match.group() if match else "No answer in context"
#         elif final_answer:
#             #Most (extractive) answers
#             json_data["items"][field_name]["output"]["value"] = final_answer
#         else:
#             json_data["items"][field_name]["output"]["value"] = "No answer in context"

#     return json_data

# #             model = OpenAI()
# #             final_answer = re.findall(r'final answer:\s*([^.]+)', model.invoke(meta_template.substitute(field_name=field_name, description=field_name['description'], target_unit=field_name['target_unit'])))
# #             print("response:", final_answer)
# #             match = re.search(field_name['validation'], final_answer)
# #             if match:
# #                 json_data["items"][field_name]["output"]["value"] = match.group()
# #             else:
# #                 json_data["items"][field_name]["output"]["value"] = "Null"
    
# #             ## validation using manager prompt (for which responses?)
# #             # full_validation = f"{validation_prompt} \n{response}"
# #             # # Validate and store the response using the third prompt
# #             # final_output = model.invoke(full_validation)
# #             # print("final_output:", final_output)

# # def process_input(inputs):
# #     # Find relevant context and preload JSON structure
# #     json_data = create_json_schema(inputs)
# #     # print(json.dumps(json_data, indent=4))

# #     # Fill output structures and return final answer
# #     output_json = process_json_schema(inputs, json_data)
# #     # print(json.dumps(output_json, indent=4))
# #     return output_json

def get_tesla() -> str:
    # Test the module functionality
    file_path = './tests/data/tesla.md'
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    # Example usage [name, value, {type}]
    tesla = get_tesla()
    test_inputs = [
        {'field-name':'diverse_csuite', 'description': 'C-suite individuals over 50 in DEI prog', 'llm':tesla, 'instruction':str, 'target-unit':'%'},
        {'field-name':'workforce_count_start', 'description':'year workforce counting policy began', 'llm':tesla, 'instruction':str, 'target-unit':'year'},
        {'field-name':'num_hispanic_managers', 'description':'total hispanic managers', 'llm':tesla, 'instruction':str, 'target-unit':'int'},
        {'field-name':'dynamics_measures', 'description':'measures to improve workforce dynamics', 'llm':tesla, 'instruction':str, 'target-unit':'int'}
    ]
    print(process_input(test_inputs))
    #Sample response:
    #     {'items': {'diverse_csuite': {'field_name': 'diverse_csuite', 'generated_questions': '1. Are there any mentions of C-suite executives in the corpus of documents?\n2. Are there any mentions of individuals over 50 in the C-suite?\n3. Are there any references to diversity, equity, and inclusion (DEI) programs?\n4. Are there any discussions or references to the diversity of the C-suite?\n5. Are there any discussions or references to the age of C-suite executives?\n6. Are there any discussions or references to the involvement of C-suite executives in DEI programs?\n7. Are there any discussions or references to the value or importance of having a diverse C-suite?\n8. Are there any discussions or references to the challenges or benefits of having C-suite executives over 50 in DEI programs?\n9. Are there any discussions or references to the role of C-suite executives in driving diversity and inclusion initiatives?\n10. Are there any discussions or references to the representation of different demographic groups in the C-suite?', 'relevant_context': '1. Mentions of C-suite executives:\n   - "C-Suite" mentioned in the table data under the "Seniority" column.\n\n2. Mentions of individuals over 50 in the C-suite:\n   - "Perc (%) > 50 Years" mentioned in the table data under the "C-Suite" row.\n\n3. References to diversity, equity, and inclusion (DEI) programs:\n   - "Empowering People from All backgrounds to engage in our DEI programme" mentioned in the table data.\n\n4. Discussions or references to the diversity of the C-suite:\n   - "C-Suite" mentioned in the table data under the "Seniority" column.\n   - Numbers of Hispanic, Black, and Native American individuals mentioned in the table data under the "C-Suite" row.\n\n5. Discussions or references to the age of C-suite executives:\n   - "Perc (%) > 50 Years" mentioned in the table data under the "C-Suite" row.\n\n6. Discussions or references to the involvement of C-suite executives in DEI programs:\n   - "Empowering People from All backgrounds to engage in our DEI programme" mentioned in the table data.\n\n7. Discussions or references to the value or importance of having a diverse C-suite:\n   - No specific mention or discussion found in the provided context.\n\n8. Discussions or references to the challenges or benefits of having C-suite executives over 50 in DEI programs:\n   - No specific mention or discussion found in the provided context.\n\n9. Discussions or references to the role of C-suite executives in driving diversity and inclusion initiatives:\n   - No specific mention or discussion found in the provided context.\n\n10. Discussions or references to the representation of different demographic groups in the C-suite:\n    - Numbers of Hispanic, Black, and Native American individuals mentioned in the table data under the "C-Suite" row.', 'unit': 'str', 'validation': '5w_or_less', 'output': {'value': ["Over 50 C-Suite Individuals in DEI'"]}}, 'workforce_count_start': {'field_name': 'workforce_count_start', 'generated_questions': '1. When did the organization start counting its workforce?\n2. In which year was the workforce counting policy implemented?\n3. What is the initial year for workforce count?\n4. When was the workforce count first initiated?\n5. At what point in time did the organization begin tracking its workforce count?\n6. When did the organization start recording the number of employees?\n7. In which year did the organization begin measuring its workforce size?\n8. What is the starting point for workforce count?\n9. When was the workforce count first established?\n10. At what year did the organization start monitoring its workforce count?', 'relevant_context': 'Relevant information from the context:\n\n- The organization started counting its workforce in 2019.\n- The workforce counting policy was implemented in 2019.\n- The initial year for workforce count is 2019.\n- The workforce count was first initiated in 2019.\n- The organization began tracking its workforce count in 2019.\n- The organization started recording the number of employees in 2019.\n- The organization began measuring its workforce size in 2019.\n- The starting point for workforce count is 2019.\n- The workforce count was first established in 2019.\n- The organization started monitoring its workforce count in 2019.', 'unit': 'year', 'validation': '\\b(?:19|20)\\d{2}\\b', 'output': {'value': 'No answer in context'}}, 'num_hispanic_managers': {'field_name': 'num_hispanic_managers', 'generated_questions': '1. How many Hispanic managers are there in the organization?\n2. What is the total number of Hispanic individuals holding managerial positions?\n3. How many managers in the organization identify as Hispanic?\n4. What is the count of Hispanic individuals in managerial roles?\n5. How many individuals of Hispanic descent are currently in managerial positions?\n6. What is the total count of Hispanic managers in the organization?\n7. How many managers in the organization are of Hispanic origin?\n8. What is the number of Hispanic individuals holding managerial roles?\n9. How many individuals identifying as Hispanic are currently in managerial positions?\n10. What is the total count of managers who are Hispanic?', 'relevant_context': '- The organization has 20 Hispanic managers.\n- The total number of Hispanic individuals holding managerial positions is 20.\n- 20 managers in the organization identify as Hispanic.\n- There are 20 Hispanic individuals in managerial roles.\n- There are 20 individuals of Hispanic descent currently in managerial positions.\n- The total count of Hispanic managers in the organization is 20.\n- 20 managers in the organization are of Hispanic origin.\n- The number of Hispanic individuals holding managerial roles is 20.\n- There are 20 individuals identifying as Hispanic currently in managerial positions.\n- The total count of managers who are Hispanic is 20.', 'unit': 'int', 'validation': '\\b\\d+\\b', 'output': {'value': '20'}}, 'dynamics_measures': {'field_name': 'dynamics_measures', 'generated_questions': '1. What are the key indicators or metrics used to assess workforce dynamics?\n2. What are the specific measures or initiatives implemented to enhance workforce dynamics?\n3. How are employee engagement and satisfaction levels measured and improved?\n4. What strategies or programs are in place to promote diversity and inclusion within the workforce?\n5. Are there any specific measures to address and reduce employee turnover?\n6. How is the effectiveness of leadership and management assessed in relation to workforce dynamics?\n7. Are there any initiatives or policies in place to foster collaboration and teamwork among employees?\n8. What measures are taken to ensure a healthy work-life balance for employees?\n9. How are conflicts or issues within the workforce identified and resolved?\n10. Are there any specific measures to promote continuous learning and professional development among employees?', 'relevant_context': '- Employee Data Index (EDI) is used to assess workforce dynamics, measuring the total number of employees and their distribution across regions.\n- The implementation of social change policies is a specific measure to enhance workforce dynamics.\n- Employee engagement and satisfaction levels are measured and improved, although specific methods are not mentioned in the context.\n- Strategies and programs are in place to promote diversity and inclusion within the workforce, including the Empowering People from All backgrounds program.\n- No specific measures to address and reduce employee turnover are mentioned.\n- The effectiveness of leadership and management in relation to workforce dynamics is not addressed in the context.\n- There is no mention of specific initiatives or policies to foster collaboration and teamwork among employees.\n- No information is provided regarding measures taken to ensure a healthy work-life balance for employees.\n- No information is provided regarding how conflicts or issues within the workforce are identified and resolved.\n- The context does not mention any specific measures to promote continuous learning and professional development among employees.', 'unit': 'str', 'validation': '5w_or_less', 'output': {'value': ["Social change policies, diversity programs'"]}}}}
    # (esg-llm-py3.10) (base) cardigan@Jethros-Air esg-llm % 