import modal
from esg_llm.schema_processor import process_input
from app import MozartMistral

stub = modal.Stub()

#   https://jedijoni--embedding-main.modal.run
# "https://doctorslimm--embedding-main.modal.run" 

# Create a MozartMistral object
# mistral = MozartMistral(api_url=mistral_api_url)

def get_tesla() -> str:
    # Test the module functionality
    file_path = './tests/data/tesla.md'
    with open(file_path, 'r') as file:
        return file.read()
    
@stub.function()
def hello_world():
    print("Hello, World!")

# Define a local entrypoint to call the function
@stub.local_entrypoint()
def main():
    hello_world.remote()

if __name__ == "__main__":
    # Example usage [name, value, {type}]
    tesla = get_tesla()
    test_inputs = {
        "json_objects": [
        {'field-name':'diverse_csuite', 'description': 'C-suite individuals over 50 in DEI prog', 'llm':tesla, 'instruction':"string", 'target-unit':'%'},
        {'field-name':'workforce_count_start', 'description':'year workforce counting policy began', 'llm':tesla, 'instruction':"string", 'target-unit':'year'},
        {'field-name':'num_hispanic_managers', 'description':'total hispanic managers', 'llm':tesla, 'instruction':"string", 'target-unit':'int'},
        {'field-name':'dynamics_measures', 'description':'measures to improve workforce dynamics', 'llm':tesla, 'instruction':"string", 'target-unit':'int'}
    ]}
    
    with stub.run():
        main()


    #Sample response:
    #     {'items': {'diverse_csuite': {'field_name': 'diverse_csuite', 'generated_questions': '1. Are there any mentions of C-suite executives in the corpus of documents?\n2. Are there any mentions of individuals over 50 in the C-suite?\n3. Are there any references to diversity, equity, and inclusion (DEI) programs?\n4. Are there any discussions or references to the diversity of the C-suite?\n5. Are there any discussions or references to the age of C-suite executives?\n6. Are there any discussions or references to the involvement of C-suite executives in DEI programs?\n7. Are there any discussions or references to the value or importance of having a diverse C-suite?\n8. Are there any discussions or references to the challenges or benefits of having C-suite executives over 50 in DEI programs?\n9. Are there any discussions or references to the role of C-suite executives in driving diversity and inclusion initiatives?\n10. Are there any discussions or references to the representation of different demographic groups in the C-suite?', 'relevant_context': '1. Mentions of C-suite executives:\n   - "C-Suite" mentioned in the table data under the "Seniority" column.\n\n2. Mentions of individuals over 50 in the C-suite:\n   - "Perc (%) > 50 Years" mentioned in the table data under the "C-Suite" row.\n\n3. References to diversity, equity, and inclusion (DEI) programs:\n   - "Empowering People from All backgrounds to engage in our DEI programme" mentioned in the table data.\n\n4. Discussions or references to the diversity of the C-suite:\n   - "C-Suite" mentioned in the table data under the "Seniority" column.\n   - Numbers of Hispanic, Black, and Native American individuals mentioned in the table data under the "C-Suite" row.\n\n5. Discussions or references to the age of C-suite executives:\n   - "Perc (%) > 50 Years" mentioned in the table data under the "C-Suite" row.\n\n6. Discussions or references to the involvement of C-suite executives in DEI programs:\n   - "Empowering People from All backgrounds to engage in our DEI programme" mentioned in the table data.\n\n7. Discussions or references to the value or importance of having a diverse C-suite:\n   - No specific mention or discussion found in the provided context.\n\n8. Discussions or references to the challenges or benefits of having C-suite executives over 50 in DEI programs:\n   - No specific mention or discussion found in the provided context.\n\n9. Discussions or references to the role of C-suite executives in driving diversity and inclusion initiatives:\n   - No specific mention or discussion found in the provided context.\n\n10. Discussions or references to the representation of different demographic groups in the C-suite:\n    - Numbers of Hispanic, Black, and Native American individuals mentioned in the table data under the "C-Suite" row.', 'unit': 'str', 'validation': '5w_or_less', 'output': {'value': ["Over 50 C-Suite Individuals in DEI'"]}}, 'workforce_count_start': {'field_name': 'workforce_count_start', 'generated_questions': '1. When did the organization start counting its workforce?\n2. In which year was the workforce counting policy implemented?\n3. What is the initial year for workforce count?\n4. When was the workforce count first initiated?\n5. At what point in time did the organization begin tracking its workforce count?\n6. When did the organization start recording the number of employees?\n7. In which year did the organization begin measuring its workforce size?\n8. What is the starting point for workforce count?\n9. When was the workforce count first established?\n10. At what year did the organization start monitoring its workforce count?', 'relevant_context': 'Relevant information from the context:\n\n- The organization started counting its workforce in 2019.\n- The workforce counting policy was implemented in 2019.\n- The initial year for workforce count is 2019.\n- The workforce count was first initiated in 2019.\n- The organization began tracking its workforce count in 2019.\n- The organization started recording the number of employees in 2019.\n- The organization began measuring its workforce size in 2019.\n- The starting point for workforce count is 2019.\n- The workforce count was first established in 2019.\n- The organization started monitoring its workforce count in 2019.', 'unit': 'year', 'validation': '\\b(?:19|20)\\d{2}\\b', 'output': {'value': 'No answer in context'}}, 'num_hispanic_managers': {'field_name': 'num_hispanic_managers', 'generated_questions': '1. How many Hispanic managers are there in the organization?\n2. What is the total number of Hispanic individuals holding managerial positions?\n3. How many managers in the organization identify as Hispanic?\n4. What is the count of Hispanic individuals in managerial roles?\n5. How many individuals of Hispanic descent are currently in managerial positions?\n6. What is the total count of Hispanic managers in the organization?\n7. How many managers in the organization are of Hispanic origin?\n8. What is the number of Hispanic individuals holding managerial roles?\n9. How many individuals identifying as Hispanic are currently in managerial positions?\n10. What is the total count of managers who are Hispanic?', 'relevant_context': '- The organization has 20 Hispanic managers.\n- The total number of Hispanic individuals holding managerial positions is 20.\n- 20 managers in the organization identify as Hispanic.\n- There are 20 Hispanic individuals in managerial roles.\n- There are 20 individuals of Hispanic descent currently in managerial positions.\n- The total count of Hispanic managers in the organization is 20.\n- 20 managers in the organization are of Hispanic origin.\n- The number of Hispanic individuals holding managerial roles is 20.\n- There are 20 individuals identifying as Hispanic currently in managerial positions.\n- The total count of managers who are Hispanic is 20.', 'unit': 'int', 'validation': '\\b\\d+\\b', 'output': {'value': '20'}}, 'dynamics_measures': {'field_name': 'dynamics_measures', 'generated_questions': '1. What are the key indicators or metrics used to assess workforce dynamics?\n2. What are the specific measures or initiatives implemented to enhance workforce dynamics?\n3. How are employee engagement and satisfaction levels measured and improved?\n4. What strategies or programs are in place to promote diversity and inclusion within the workforce?\n5. Are there any specific measures to address and reduce employee turnover?\n6. How is the effectiveness of leadership and management assessed in relation to workforce dynamics?\n7. Are there any initiatives or policies in place to foster collaboration and teamwork among employees?\n8. What measures are taken to ensure a healthy work-life balance for employees?\n9. How are conflicts or issues within the workforce identified and resolved?\n10. Are there any specific measures to promote continuous learning and professional development among employees?', 'relevant_context': '- Employee Data Index (EDI) is used to assess workforce dynamics, measuring the total number of employees and their distribution across regions.\n- The implementation of social change policies is a specific measure to enhance workforce dynamics.\n- Employee engagement and satisfaction levels are measured and improved, although specific methods are not mentioned in the context.\n- Strategies and programs are in place to promote diversity and inclusion within the workforce, including the Empowering People from All backgrounds program.\n- No specific measures to address and reduce employee turnover are mentioned.\n- The effectiveness of leadership and management in relation to workforce dynamics is not addressed in the context.\n- There is no mention of specific initiatives or policies to foster collaboration and teamwork among employees.\n- No information is provided regarding measures taken to ensure a healthy work-life balance for employees.\n- No information is provided regarding how conflicts or issues within the workforce are identified and resolved.\n- The context does not mention any specific measures to promote continuous learning and professional development among employees.', 'unit': 'str', 'validation': '5w_or_less', 'output': {'value': ["Social change policies, diversity programs'"]}}}}
    # (esg-llm-py3.10) (base) cardigan@Jethros-Air esg-llm % 

# Expected input structure
# {
#     "field-name": "",
#     "description": "",
#     "llm": "",
#     "instruction": "",
#     "target-unit": ""
# }

# - Needs GPT-4 to get concise strings as responses. Presumably will apply to generative answers when we do these
# - Applying regex validation rather than a manager prompt works consistently for int and float.

# unit_template = Template("Determine the most appropriate unit to store the data point described below.\
#                          This might be an int, %, year, "string", or something else.\nfield name: $field_name\nfield description: $description\n return your answer as 'unit:<>'")

# questions_template = Template("Provide subcomponents to search for in a corpus of documents to find the value for this field.\nfield name: $field_name\ndescription: $description\nYanswer with a list of questions and nothing else'")

# search_template = Template("Search the context below for information relevant to the questions, and return only relevant information in bullet points.\nQuestions: $questions\nContext: $context")

# meta_template = Template("Find an final answer in the context below.\nfield name: $field_name\ndescription: $description\ncontext: $context\nunit: $target_unit\n return your answer as 'final answer:<>'")

# meta_template_string = Template("Use the information provided to return your final answer in 5 words or less.\nfield name: $field_name\ndescription: $description\ncontext: $context\nunit: $target_unit\nreturn your answer as 'final answer:<>'")