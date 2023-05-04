# The UK property prices
## Overview
> Note:The documentation is incomplete and needs to be elaborated.  
However, the code should work.

This project is a part of the [Data Engineering Zoomcamp course](https://github.com/DataTalksClub/data-engineering-zoomcamp) held by [DataTalks.Club](https://datatalks.club/).

This project covers some areas of Data Engineering and Business Intelligence Tools.  
The project includes the following:
- building the cloud infrastructure,
- creation of a pipeline for transfer data,
- uploading data into the database,
- setting up a monthly update,
- transformftion of the data to prepare it for the BI dashboard
- creation of a BI dashboard.  

## Problem description

In this project we will be looking at data on property sales.

Property sales data is useful for understanding the real estate market. It provides insights into property values, market trends, neighborhood analysis, and investment opportunities. 

By analyzing the prices of recently sold properties, we can get an idea of how much homes are worth in that area. We can also get a sense of whether the market is trending up or down by analyzing the number of homes sold, the average sale price, and the time it takes for properties to sell. 

Additionally, we can identify neighborhoods that are experiencing growth and are likely to see an increase in property values in the future. 

Overall, this information can be useful for buyers, sellers, and investors.

## Dataset

The data for this project is from [the HM Land Registry](https://www.gov.uk/government/organisations/land-registry/about).
> Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

The UK property dataset contains data about prices paid for real-estate property in England and Wales. The data is available since 1995, and the size of the dataset in uncompressed form is about 4 GiB.  
- Source: [https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)
 - Description of the fields: [https://www.gov.uk/guidance/about-the-price-paid-data](https://www.gov.uk/guidance/about-the-price-paid-data)

There are 3 option to download the data.
- single file: contains all the up to date data from 1995 to the current date
- yearly file: contains annual files of up to date data, ranging from 1995 to the current date.
- monthly file: contains a single monthly file of the transactions received in the period from the first to the last day of the corresponding month

The average size of single file (first option) is ~4 GB. So to limit the size of our project we will not use this option. Instead we will use yearly files and limit ourselves to using data from the previous 5 years only (since 2018).

In addition, we will use monthly files. This data is updated on the 20th working day of each month. We will set up an automatic update that will update the data in our project on the 28th of each month 

## Project architecture.
![Workflow diagram](/images/workflow.png)

## Technologies
Following technologies were used in this project
- Terraform: an Infrastructure as code (IaC) tool to define and deploy cloud infrastructure
- Prefect: a workflow management system to define, schedule, and execute data pipelines
- DBT: a data transformation tool to transform raw data into structured, analytics-ready datasets
- Yandex Cloud:  
   - Yandex Object Storage: S3-compatible bucket to use as a Data lake
   - Managed Service for ClickHouse: OLAP DBMS to use as a Data Warehouse.
   - DataLens: a data visualization tool to create dachboard.

## Workflow
We  use Prefect for workflow orchestration.  
There are two pipelines:

- ### Initial data ingestion.
   This pipelene loads historical data: yearly files up to the current year. It reads raw files from WEB, stores them in the Datalake and ingest data from Datalake into DWH. This pipeline only runs once - immediately after deployment.
- ### Monthly update.
   This pipeline loads data for current month, stores it in Datalake and ingest data from Datalake into DWH. Then it starts DBT to do some data transformation described below. This pipeline runs every month on the 28th.

## Data transformation
**TODO: Describe in more detail.**

We use DBT do transform data.  
The problem with the data is this: the monthly files contain not only new data, but also changes or deletions to previously downloaded data (yearly files).

![DBT diagram](/images/dbt_graph.png)
 
## BI Dashboard
Link to the dashboard:  
[https://datalens.yandex/o4iddxuubt30e](ttps://datalens.yandex/o4iddxuubt30e)

![Dashboard](/images/dashboard.png)

This dashboard contains two charts:

- a chart that shows the change in price over time.
- a chart that shows the distribution of the number of sales depending on the type of property.

The dashboard also contains a selector that allows you to choose a time range.

## Deployment
The deployment process is described in a separate [document](deployment.md).
