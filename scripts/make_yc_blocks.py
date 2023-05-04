import os 
from pathlib import Path

from dotenv import load_dotenv
from prefect_aws import AwsCredentials, AwsClientParameters
from prefect_aws.s3 import S3Bucket 
from prefect.blocks.system import Secret

from config import S3_ENDPOINT_URL, S3_BUCKET_NAME

dotenv_file = Path('.env')
if dotenv_file.is_file():
    load_dotenv(dotenv_file)

# S3_ENDPOINT_URL =  os.environ.get('S3_ENDPOINT_URL')
# REGION_NAME = os.environ.get('REGION_NAME')
# S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =  os.environ.get('AWS_SECRET_ACCESS_KEY')
CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST')
CLICKHOUSE_USER = os.environ.get('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD')

yc_creds_block_dezoom = AwsCredentials(
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    aws_client_parameters=AwsClientParameters(endpoint_url=S3_ENDPOINT_URL)
    )
yc_creds_block_dezoom.save("yc-creds-dezoom", overwrite=True)

yc_s3_block_dezoom = S3Bucket(
    bucket_name=S3_BUCKET_NAME,
    credentials=yc_creds_block_dezoom,
)
yc_s3_block_dezoom.save("yc-s3-dezoom", overwrite=True)


Secret(value=CLICKHOUSE_HOST).save(name="clickhouse-host", overwrite=True)
Secret(value=CLICKHOUSE_USER).save(name="clickhouse-user", overwrite=True)
Secret(value=CLICKHOUSE_PASSWORD).save(name="clickhouse-password", overwrite=True)
