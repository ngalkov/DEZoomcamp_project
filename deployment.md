# Deployment

There are several steps to deploy project:
- local setup
- cloud setup
- pipelines configuration:
    - initial data ingestion
    - monthly data updates
- dashboard setup

These steps are described below.  
All of the following commands must be run from the root of the project unless otherwise specified.

## Local setup
This can be done on your local machine or on the cloud VM.

### Setup Prerequisites
 - Python 3.9 or above
 - Pipenv
 - Terraform
 - Yandex Cloud command-line interface (CLI)

If you do not have any of these, please follow the respective guides:
  - [Python Installation](https://docs.python.org/3/using/index.html)
  - [Popenv Installation](https://github.com/pypa/pipenv#installation)
  - [Terraform Installation](https://developer.hashicorp.com/terraform/downloads)
  - [Yandex Cloud CLI](https://cloud.yandex.com/en/docs/cli/quickstart#install)

To install this project, follow the steps below:
 - Create a new folder and navigate to it.
 - Clone the project repository  
     ```
    git clone https://github.com/ngalkov/DEZoomcamp_project
    ```
 - Create the new virtual environment:  
      ```
    pipenv install
    ```
 - Activate virtual environment
      ```
    pipenv shell
    ```

## Cloud setup
We use [Yandex Cloud](https://cloud.yandex.com) for cloud deployment. 

Before we start, let's configure the Yandex Cloud. Do the following:

- Sign up for Yandex Cloud and create a billing account:
   1. Go to the [management console](https://console.cloud.yandex.com/) and log in to Yandex Cloud or register if you don't have an account yet.
   2. On the [billing page](https://console.cloud.yandex.com/billing), make sure you linked a [billing account](https://cloud.yandex.com/en-ru/docs/billing/concepts/billing-account) and it has the `ACTIVE` or `TRIAL_ACTIVE` status. If you don't have a billing account, [create one](https://cloud.yandex.com/en-ru/docs/billing/quickstart/). You can use the [free trial](https://cloud.yandex.com/en-ru/docs/getting-started/free-trial/concepts/quickstart) if you are new to Yandex Cloud.

- Prepare resources for deployment:
   1. Go to the [cloud page](https://console.cloud.yandex.com/cloud) and create a new cloud (you can use existing one if you like).
   2. Create a [folder](https://cloud.yandex.com/en-ru/docs/resource-manager/operations/folder/create) to run project infrastructure.
   3. Create [service account.](https://cloud.yandex.com/en-ru/docs/iam/operations/sa/create) Assign this account a roles `editor`, `storage.editor`
   4. Get [OAuth token](https://cloud.yandex.com/en-ru/docs/iam/concepts/authorization/oauth-token). This will be used for your authentication.
   5. Create [static access keys.](https://cloud.yandex.com/en-ru/docs/iam/operations/sa/create-access-key) These will be used to manage resources.
   6. Get an [SSL certificate](https://cloud.yandex.com/en-ru/docs/managed-clickhouse/operations/connect#get-ssl-cert).

   > [Learn more about clouds and folders.](https://cloud.yandex.com/en-ru/docs/resource-manager/concepts/resources-hierarchy)

Deploy project infrastructure with [Terraform](https://www.terraform.io/).  
1. Navigate to the `terraform` folder of the project on your local system.
   ```
   cd <path_to_project>/teraform
   ```  
2. Run
   ```
   terraform init
   ```
   This command performs several different initialization steps in order to prepare the current working directory for use with Terraform. 
3. There is `secret.tfvars.example` file in this folder. Rename it to `secret.tfvars`. Fill in all required fields. See previous section on how to obtain these values  
   Fields `db_username` and `db_password` will be used when creating the database so come up with your own username and password.   
4. Run
   ```
   terraform plan -var-file=secret.tfvars
   ```
   This command creates and prints an execution plan, which lets you preview the changes that Terraform plans to make to your infrastructure. It does not yet create anything.  
5. Run
   ```
   terraform apply -var-file=secret.tfvars
   ```
   This will create Yandex Object Storage (it's our Data Lake) and ClickHouse cluster (it's our Data Warehouse). It may take some time (a few minutes).

Configure Clickhouse cluster.  
Open ClickHouse management console and add database `uk_property_dbt`. 
Add your user  permission for this base.
>*I didn't find a way to do it with Terrraform yet.*
 
## Pipelines configuration
**TODO: Describe in more detail.**
### Configure Prefect 
-  Configure credentials:  
   There is `.env.example` file in the project root folder.This file contains the credentials. Rename it to `.env`. Fill in all required fields. Some of the fields are the same as in `./terraform/secret.tfvars`.
- Create Prefect blocks:  
   ```
   ./script/make_yc_blocks.py
   ```


### Iinitial data ingestion
Run
```
./scripts/initial_pipeline
```
This will upload data into Datalake and DWH.

### Monthly data updates
Start Prefect server:
```
prefect server start
```

Schedule monthly update:  
```
prefect deployment build ./scripts/monthly_pipeline.py:run_monthly_update -n "Monthly update"
```
```
prefect deployment apply run_monthly_update-deployment.yaml
```
Configure deployment in Prefect UI. Shedule deployment to run every month.

Start agent
```
prefect agent start --work-queue "default"
```

## DBT
Add the following to `~.dgt/profiles.yml`
```
clickhouse_uk_property:
  target: dev
  outputs:
    dev:
      type: clickhouse
      schema: uk_property_dbt
      host: <your_clickhouse_host>
      port: 8443
      user: <your_clickhouse_user>
      password: <your_clickhouse_password>
      secure: True
```

## Dashboard setup
**TODO: Describe in more detail.**

We use [DataLens](https://datalens.yandex.com/) to visualise our data.

The process is relatively simple and well described in the [documentation](https://cloud.yandex.com/en-ru/docs/datalens/quickstart)
