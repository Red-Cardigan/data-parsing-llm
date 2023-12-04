from string import Template

unit_template = Template("""
    Determine the most appropriate data type for storing a given data point.

    Parameters:
    field_name (str): The name of the field.
    description (str): The description of the data to be stored in the field.

    Returns:
    str: A template string with the recommended data type for the field.
                         
    Data:
    field_name: $field_name
    description: $description
    """)
                         
#  Find the most appropriate unit to store the data point described below.\
#  For example, int, %, year, str etc.\nfield name: $field_name\nfield description: $description\
#  \n return your answer as 'unit:<>'")

questions_template = Template("""
    Generate questions to help an ESG analyst find information matching the description in a corpus of documents.

    Parameters:
    field_name (str): The name of the field.
    description (str): The description of the information to be found.

    Returns:
    str: A list of questions formatted as a string to guide the ESG analyst.
                              
    Data:
    field_name: $field_name
    description: $description         
    """)
    
    # "Provide questions to help a trainee ESG analyst find information which matches the description in\
    #                            a corpus of documents.\nfield name: $field_name\ndescription: $description\nphrase your answer as a\
    #                            list of questions'")

search_template = Template("""
    Use the provided questions and description to extract relevant information from a given context.

    Parameters:
    questions (str): The questions to guide the search.
    description (str): The description of the information sought.
    context (str): The context or corpus from which the information is to be extracted.

    Returns:
    str: A string with relevant information extracted from the context, formatted as bullet points.
                           
    Data:
    questions: $questions
    description: $description
    context: $context
    """)
    
    # "Use these questions and description to return relevant information from the context below. \
    #                        Return only relevant information in bullet points.\nQuestions: $questions\ndescription: $description\
    #                        \nContext: $context")

meta_template = Template("""
    Use the provided context to find a value that matches the description in a specified unit.

    Parameters:
    target_unit (str): The unit in which the matching value is to be found.
    field_name (str): The name of the field.
    description (str): The description of the information sought.
    context (str): The context or corpus from which the information is to be extracted.

    Returns:
    str: A string representing the final answer in the specified target unit.

    Data:
    target_unit: $target_unit
    field_name: $field_name
    description: $description
    context: $context
    """)
    
    # "Use the context below to find a $target_unit which matches the description\nfield name: $field_name\
    #                      \ndescription: $description\ncontext: $context\nunit: $target_unit\n return your answer as 'final answer:<>'")

meta_template_string = Template("""
    Use the provided context to find a value that matches the description in a specified unit.

    Parameters:
    target_unit (str): The unit in which the matching value is to be found.
    field_name (str): The name of the field.
    description (str): The description of the information sought.
    context (str): The context or corpus from which the information is to be extracted.

    Returns:
    str: A string representing the final answer in the specified target unit.

    Data:
    target_unit: $target_unit
    field_name: $field_name
    description: $description
    context: $context
    """)
    
    # "Use the information provided to return an which matches the description in $target_unit.\n\
    #                             field name: $field_name\ndescription: $description\ncontext: $context\nunit: $target_unit\n\
    #                             return your answer as 'final answer:<>'")
