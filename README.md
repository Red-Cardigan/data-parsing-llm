# ESG LLM Data Entry Analyst Module (esg-llm)


### Goals
`Formatted Question Answering`

A module that uses an LLM to fill out forms from unstructured text data for ESG reporting.
As well as providing contextualized comments where necessary on additional information that may be relevant.


The Issue is that GPT is deaf, blind, and cannot read very well either.
With extensive prompt engineer, input parsing, and output parsing we are confident that we can change this.
Mozart ETL Data Extraction gives LLMs the eyes they need to see by breaking down the page components into purely readable format, now we must make them read good and respond good :D

### Requirements
* must have data type parsing and sanity checking across many target units
* must use A Replaceable LLM Call Under the Hood
  * Azure OpenAi gpt-35-turbo (For Now) https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.azure_openai.AzureChatOpenAI.html
  * Completely replaceable with any Remote Call with `system` prompt, and `user / task` prompt
  * Traceable Calls using LangSmith, Phoenix LLM Tracing, or Weights and Bias LLM Tracing (Or Some other Local Implementation of Tracking I/O)


```python
from usemozart.llm import ESG_LLM_Analyst

The module expects a list of JSON dictionaries with field-name, description, and llm (text to be analysed)
- any other fields are ignored

#Here's the structure template:

input = process_input([{ 
    'field-name':"name of the field",
    'description':"description of the field - should contain an indication of the target unit",
    "llm": "pass the the context in as text"
}])

# Here's a sample input:

input = process_input([{ 
    'field-name':'diverse_csuite', 
    'description': 'C-suite individuals over 50 in DEI prog', 
    'llm':tesla
}])

#The ouput returns the answer, unit, and questions asked:

items = {'diverse_csuite': 
    {
      'field_name': 'diverse_csuite', 'generated_questions': "1. What is the percentage of C-suite individuals over 50 in the company's diversity, equity, and inclusion (DEI) program?\n2. How does the company define its C-suite positions?\n3. Are there any specific targets or goals set by the company regarding the representation of individuals over 50 in its C-suite?\n4. What initiatives or programs does the company have in place to promote diversity and inclusion in its C-suite, particularly for individuals over 50?\n5. Are there any policies or practices in the company that may hinder or support the representation of individuals over 50 in its C-suite?\n6. Has the company made any public commitments or statements regarding the importance of age diversity in its C-suite?\n7. Are there any notable case studies or success stories of individuals over 50 who have held C-suite positions within the company?\n8. How does the company compare to industry peers in terms of the percentage of C-suite individuals over 50 in their DEI programs?\n9. Are there any external benchmarks or standards that the company uses to assess its progress in promoting age diversity in its C-suite?\n10. What metrics or data does the company track to measure the representation of individuals over 50 in its C-suite within", 'relevant_context': "- The percentage of C-suite individuals over 50 in the company's DEI program is 72.4%.\n- The company defines its C-suite positions as senior leadership roles within the organization.\n- There is no specific mention of targets or goals regarding the representation of individuals over 50 in the C-suite.\n- The company does not provide specific information about initiatives or programs to promote diversity and inclusion in the C-suite for individuals over 50.\n- There is no information provided about policies or practices that may hinder or support the representation of individuals over 50 in the C-suite.\n- There is no mention of any public commitments or statements regarding the importance of age diversity in the C-suite.\n- There is no information provided about notable case studies or success stories of individuals over 50 in C-suite positions.\n- There is no comparison provided to industry peers in terms of the percentage of C-suite individuals over 50 in their DEI programs.\n- There is no mention of external benchmarks or standards used by the company to assess progress in promoting age diversity in the C-suite.\n- There is no information provided about specific metrics or data tracked by the company to measure the representation of individuals over 50 in the C-suite.", 
      'unit': '%', 
      'validation': '\\b\\d*\\.?\\d+\\b', 
      'output': {'value': '72.4'}
    }
  }

### Example Usage in test_script.py###

# Client Agency Methodology Text (Optional):
#   - Can be summarized / augmented into a system_prompt
#   - Can be augmented into guardrails (https://github.com/NVIDIA/NeMo-Guardrails)
# eg: https://www.fitchratings.com/search?filter.sector=Corporate%20Finance&filter.language=English&filter.reportType=Rating%20Criteria&sort=recency)


```


***


### Input Data

| Parameter Name            | required | type                   | description                                                                       | example                                                                                                                                              | example                                                                                                                   |
|---------------------------|----------|------------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `Field_Name`              | true     | `string`               | A brief Title or Name of the field topic which requires populating from the data. | "Total Number of Employees"                                                                                                                          | "Gender Pay Gap Analysis"                                                                                                 |
| `Field_Description`       | true     | `string`               | A Concise description of the field topic which requires populating from the data. | "The total number of full-time employees in the organization"                                                                                        | "Wether the organization has conducted a pay equity analysis in the last three years."                                    |
| `Collection_Instructions` | optional | `string`               | More detailed additional information on how the data should be collected.         | "Only take employees in the United States, if not present then use Europe. Often confused with part time and seasonal, only use full time employees" | "If the not (0), if self reported then (1), if audited by by 3rd party such as KPMG or other regulatory organization (3)" |
| `Target_Unit`             | true     | `string`               | The unit of measurement required to be returned (Note: LLMs Cannot do Math...)    | "Hundreds"                                                                                                                                           | 0, 1, or 2                                                                                                                |
| `Sources`                 | true     | `array Source Objects` | An array of sources to be used to populate the field.                             | See Below                                                                                                                                            | See Below                                                                                                                 |


#### Source Object
Each Sources Object in the list will contain the following data:

| Parameter Name         | type     | description                                                                                                                                                                                      | example                              | example                                     |
|------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|---------------------------------------------|
| `Source_Name_Filename` | `string` | A brief Title or Filename Name of the source.                                                                                                                                                    | "Apple 2019 Corporate Social Report" | "tesla-annual-investor-highlights-2021.pdf" |
| `Page_Number`          | `int`    | The page number of the source.                                                                                                                                                                   | 34                                   | 12                                          |
| `LLM_Layout`           | `string` | The Extracted Markdown Layout of the relevant page in reading order. This Includes tables, and tables from charts which have been converted to tables, in order to make it readable for the LLM. | See Below                            | See Below                                   |


`LLM_Layout` Example (text string):

```text
### Tesla_2021_Annual_Report.pdf (Page 12)

#Our Workforce
Since 2019 we have been improving all of our workforce dynamics by implementing social change policies across the entire organization.
By doing so we can focus on our climate change goals and ensure that we are doing our part to help the world.

# Extracted Chart Data

## Employee Data Index (EDI)
Since we have implemented a new policy for counting our workforce, the amount of employees has increased by 100% since 2017 YoY.
| Year | Total Employees | Total Employees in US | Total Employees in Europe |
|------|-----------------|-----------------------|---------------------------|
| 2019 | 100             | 50                    | 50                        |
| 2020 | 200             | 100                   | 100                       |

# Extracted Table Data

## Empowering People from All backgrounds to engage in our DEI programme to foster an equitable future for our organization.
| Seniority | Total Hispanic | Total Black | Total Native American | Perc (%) > 50 Years | Perc (%) < 35 Years |
|-----------|----------------|-------------|-----------------------|----------------------|----------------------|
| C-Suite   | 2              | 3           | 0                     | 72.4                    | 5.3                    |
| VP       | 5              | 2           | 1                     | 12.4                    | 2.3                    |
| Director  | 10             | 5           | 0                     | 2.4                    | 1.3                    |
| Manager   | 20             | 10          | 1                     | 1.4                    | 0.3                    |

By engaging directly with suppliers from a diverse backgrounds we make sure to support the communities in which we operate.
```


`Sources` Example (array of Source Objects):
```json
[
  {
    "LLM_Layout": "### Page 34\n\n#Our Workforce\nSince 2014 we have ...",
    "Page_Number": 34,
    "Source_Name_Filename": "Apple 2019 Corporate Social Report",
  }, ...
]
```
***

### Output Data

| Parameter Name    | type                   | description                                                            | example                                  | example                                                    |
|-------------------|------------------------|------------------------------------------------------------------------|------------------------------------------|------------------------------------------------------------|
| `Answer`          | `string`               | The Extracted or Determined Answer to the question (No Math Allowed)   | "100,000.0 Employees in 2012"            | "NA"                                                       |
| `Needs_Transform` | `bool`                 | If the answer needs to be transformed into the target unit.            | true                                     | false                                                      |
| `Comment`         | `string`               | Any additional comments that may be relevant to the answer.            | "Only Employees in Washington Mentioned" | "Board members voted against pay gap analysis 70% Against" |
| `Sources`         | `array Source Objects` | The Source Objects Which were actually used and relevant to the Answer | [List of Source Objects]                 | [List of Source Objects]                                   |

```json
{
  "Answer": "100,000.0 Employees in 2012",
  "Needs_Transform": true,
  "Comment": "Only Employees in Washington Mentioned",
  "Sources": [
    {
      "Source_Name_Filename": "Apple 2019 Corporate Social Report",
      "Page_Number": 34,
      "LLM_Layout": "### Page 34\n\n#Our Workforce\nSince 2014 we have ..."
    }
  ]
}
```

***

### Resources
* [Output Parsers] https://python.langchain.com/docs/modules/model_io/output_parsers/
* [LangSmith] https://python.langchain.com/docs/langsmith/walkthrough
* 
