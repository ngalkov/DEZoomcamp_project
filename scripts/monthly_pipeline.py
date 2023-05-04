import subprocess
import os
from pathlib import Path
from datetime import datetime

from prefect import flow, task
from prefect_aws.s3 import S3Bucket 

from config import DATA_DIR, UPDATE_FILE_URL, S3_ENDPOINT_URL, S3_BUCKET_NAME
from cloud_utils import download_file, upload_to_s3, get_clickhouse_client
from queries import create_table_query, ingest_data_query


@task()
def update_datalake() -> None:
    current_month = datetime.now().month
    month_file_name = f'{current_month:02}.csv'
    local_path = Path(DATA_DIR,'price', 'update',  month_file_name)
    s3_object_name = f'price/update/{month_file_name}'
    
    print(f"Downloading file {UPDATE_FILE_URL}")
    download_file(UPDATE_FILE_URL, local_path)
    
    print(f"Uploading file {month_file_name} to s3")
    upload_to_s3(local_path, s3_object_name) 


@task()
def update_warehouse():
    client = get_clickhouse_client()
    table_params = { 
        'name':'update',
        's3_url': f'{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/price/update/*.csv'
    }
    
    print(f'Creating table {table_params["name"]}')
    client.command('DROP TABLE IF EXISTS {name};'.format(**table_params))
    client.command(create_table_query.format(**table_params))
    
    print(f'Ingesting data from {table_params["s3_url"]}')
    client.command(ingest_data_query.format(**table_params))


@task()
def execute_dbt():
    os.chdir('dbt/uk_property/')
    subprocess.run(['sh', '-c', 'dbt run'], check=True)
    os.chdir('../../')


@flow(log_prints=True)
def run_monthly_update():
    update_datalake()
    update_warehouse()
    execute_dbt()


if __name__  == '__main__':
    run_monthly_update()
