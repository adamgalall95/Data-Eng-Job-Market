# Job-Market-Insights

## Objectives
In today's rapidly changing economic landscape, understanding market demand for job employment is crucial for both job seekers and employers. As industries evolve and new technologies emerge, so do the skills.
This project is dedicated to develping a ELT solution which utilises Azure data stack to deliver insights into Data Engineering job market in Australia. The goal of this solution is provide job hunters with insights for better adaptability to changing market demands, and to broaden their applicantion pool.


## Consumers of your data

- Data engineering job hunters


# Solution architecture

![azure-databricks-modern-analytics-architecture](https://github.com/adamgalall95/Data-Eng-Job-Market/assets/145528713/4dfa2d49-26af-4f02-9921-3e3aeb92acf0)



## Breakdown of workflow:

- Azure Functions: built using python and schedualed to extract new data engineering job posts daily using third-party APIs.
- Azure Data Factory: triggers transformation pipeline and manages data movement between bronze, silver, and gold layers.
- Azure Databricks: transformation script is developed using Pysaprk and the key feature of the transfomration stage is text analysis of job description.
- Azure Synapse: serverless SQL pool is used to reads data from gold layer in azure data lake and perform ad hoc analysis.
- PowerBI: PowerBI report is connected to Synapse to import data from gold layer and is updated monthly.


## Power Bi report:

https://app.powerbi.com/view?r=eyJrIjoiZjU1YzkyMGQtM2UzZC00ZmJhLTlkNGUtNGRiYTBlNjc0MGRjIiwidCI6ImFlYTFmYzBhLTgzYjMtNGY1MC04NjUwLWE5OTk1NzgzODcyYSJ9
