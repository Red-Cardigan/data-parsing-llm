# esg-llm


## ESG LLM Data Entry Analyst

### Goals
A module that uses an LLM to fill out forms from unstructured text data for ESG reporting.
As well as providing contextualized comments where necessary on additional information that may be relevant.

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
