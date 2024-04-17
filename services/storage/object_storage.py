import boto3
from botocore.exceptions import (
    ClientError,
    ParamValidationError,
    EndpointConnectionError,
)

from config.settings import S3


s3 = boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        region_name="ru-central1",
        aws_access_key_id=S3.get("KEY_ID"),
        aws_secret_access_key=S3.get("SECRET_KEY"),
)

def upload_bytes(name, body):
    try:
        data = s3.put_object(Bucket=S3.get('BUCKET_NAME'), Key=name, Body=body)
        if data["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return f'https://storage.yandexcloud.net/{S3.get('BUCKET_NAME')}/{name}'
        else:
            return False
    except ClientError:
        return False

    except (ParamValidationError, EndpointConnectionError):
        return False

def upload_file(name, file):
    data = s3.upload_fileobj(Fileobj=file, Bucket=S3.get('BUCKET_NAME'), Key=name)

    return f'https://storage.yandexcloud.net/{S3.get('BUCKET_NAME')}/{name}'
