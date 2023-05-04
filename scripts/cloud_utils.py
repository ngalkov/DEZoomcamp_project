from typing import Optional
from pathlib import Path
from datetime import timedelta

import requests
from prefect import task
from prefect.tasks import task_input_hash
from prefect_aws.s3 import S3Bucket 
from prefect.blocks.system import Secret
import clickhouse_connect


# @task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def download_file(url: str, local_path: Path) -> None:
    """Download file from web to local path"""
    with open(local_path, "wb") as out_file:
        response = requests.get(url)
        out_file.write(response.content)

# @task()
def upload_to_s3(local_path: Path, s3_object_name: Optional[str] = None) -> None:
    """Upload local file to YandexCloud S3"""
    if s3_object_name is None:
        s3_object_name = local_path.name
    yc_s3_block = S3Bucket.load("yc-s3-dezoom")
    yc_s3_block.upload_from_path(from_path=local_path, to_path=s3_object_name)
    return

def get_clickhouse_client():
    client = clickhouse_connect.get_client(
        host=Secret.load("clickhouse-host").get(), 
        port=8443, 
        user=Secret.load("clickhouse-user").get(), 
        password=Secret.load("clickhouse-password").get(),
        secure=True,
        verify=True,
        # ca_cert='CA.pem',
        database='uk_property'
    )
    return client
