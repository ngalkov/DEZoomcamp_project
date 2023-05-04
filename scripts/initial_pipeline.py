from pathlib import Path
from datetime import datetime

from prefect import flow, task

from config import BASE_URL, DATA_DIR, S3_ENDPOINT_URL, S3_BUCKET_NAME
from .cloud_utils import download_file, upload_to_s3, get_clickhouse_client
from .queries import create_table_query, ingest_data_query

@task()
def web_to_datalake(start_year: int) -> None:
    current_year = datetime.now().year
    for year in range(start_year, current_year):
        year_file_name = f'pp-{year:04}.csv'
        year_file_url = f'{BASE_URL}{year_file_name}'
        s3_object_name = f'price/{year_file_name}'
        local_path = Path(DATA_DIR,'price', year_file_name)

        print(f"Downloading file {year_file_url}")
        download_file(year_file_url, local_path)

        print(f"Uploading file {year_file_name} to s3")
        upload_to_s3(local_path, s3_object_name) 


@task()
def datalake_to_data_warehouse():
    client = get_clickhouse_client()
    table_params = { 
        'name':'historical_prices',
        's3_url': f'{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/price/pp-*.csv'
    }
    
    print(f'Creating table {table_params["name"]}')
    client.command('DROP TABLE IF EXISTS {name};'.format(**table_params))
    client.command(create_table_query.format(**table_params))
    
    print(f'Ingesting data from {table_params["s3_url"]}')
    client.command(ingest_data_query.format(**table_params))


@flow(log_prints=True)
def ingest_historical_data(start_year: int):
    web_to_datalake(start_year)
    datalake_to_data_warehouse()
    

if __name__  == '__main__':
    ingest_historical_data(2018)


