import pathlib
import os
import sys
import boto3

CURRENT_DIR = pathlib.Path(__file__).resolve().parent.parent

# Adicione o diretório ao sys.path
sys.path.append(str(CURRENT_DIR))

from config import config

s3 = boto3.resource('s3')

try:
    print('Bucket name:', config.BUCKET_NAME)
    s3.create_bucket(Bucket=config.BUCKET_NAME)
    print('S3 bucket has been created successfully')
except Exception as e:
    print('S3 error:', e)
