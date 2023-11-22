from esg_llm import process_json_schema
from esg_llm import create_json_schema
from esg_llm import process_input

file_path = '/Users/cardigan/Documents/esg-llm/tesla.md'
with open(file_path, 'r') as file:
    tesla = file.read()

#The module expects a list of JSON dictionaries with field-name, description, and llm (any other fields are ignored)
# input = process_input([{ 
#     'field-name':"name of the field",
#     'description':"description of the field - should contain an indication of the target unit",
#     "llm": this is the data, parsed as text
# }])

#Here's a sample input
input_list = [
        {'field-name':'diverse_csuite', 'description': 'C-suite individuals over 50 in DEI prog', 'llm':tesla, 'instruction':str, 'target-unit':'%'},
        {'field-name':'workforce_count_start', 'description':'year workforce counting policy began', 'llm':tesla, 'instruction':str, 'target-unit':'year'},
        {'field-name':'num_hispanic_managers', 'description':'total hispanic managers', 'llm':tesla, 'instruction':str, 'target-unit':'int'},
        {'field-name':'dynamics_measures', 'description':'measures to improve workforce dynamics', 'llm':tesla, 'instruction':str, 'target-unit':'int'}
    ]

#This will do the LLM magic to extract the target unit and validated type answer from the text
# #in format {, output:{value:[answer]}}
response = process_input(input_list)

#This is composed of two primary stages: 
# 1) create_json_schema to break the description into subquestions, and find the target_unit and relevant context
# 2) process_json_schema to find the answer in relevant context 
json_schema = create_json_schema(input_list)
final = process_json_schema(input_list, json_schema)

# print(json_schema)

print(final) #same as print(response)