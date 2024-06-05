# Job-Market-Insights

## Objectives
In today's rapidly changing economic landscape, understanding market demand for job employment is crucial for both job seekers and employers. As industries evolve and new technologies emerge, so do the skills and roles in demand.
This project is dedicated to develping a ELT solution which utilises Azure data stack. The goal of this solution is provide Data Engineering job hunters in Australia with job market insights for better adaptability to changing market demands, and to broaden their applicantion pool.


## Consumers of your data

- Data engineering job hunters


## Solution architecture

![azure-databricks-modern-analytics-architecture](https://github.com/adamgalall95/Data-Eng-Job-Market/assets/145528713/2c282106-a858-4a82-8189-029a231b67e8)


## Breakdown of steps:

1- Azure Functions: built using python and schedualed to extract new data engineering job posts daily using third-party APIs.
2- Azure Data Factory: triggers transformation pipeline and manages data movement between bronze, silver, and gold layers.
3- Azure Databricks: transformation script is developed using Pysaprk and the key feature of the transfomration stage is text analysis of job description.
4- Azure Synapse: serverless SQL pool is used to reads data from gold layer in azure data lake and perform ad hoc analysis.
5- PowerBI: PowerBI report is connected to Synapse to import data from gold layer and is monthly.
