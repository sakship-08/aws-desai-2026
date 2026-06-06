import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        # Resize to 128x128
        image.thumbnail((128, 128))
        image.save(resized_path)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        # Get the file key and decode it (to handle spaces in filenames)
        key = unquote_plus(record['s3']['object']['key'])
       
        # Security: Only process files in 'uploads/' folder
        if not key.startswith('uploads/'):
            return

        # Define download and upload paths
        # /tmp/ is the only writable directory in Lambda
        download_path = f'/tmp/{uuid.uuid4()}{os.path.basename(key)}'
        upload_path = f'/tmp/resized-{os.path.basename(key)}'
       
        # 1. Download image from S3
        s3_client.download_file(bucket, key, download_path)
       
        # 2. Resize the image
        resize_image(download_path, upload_path)
       
        # 3. Upload to the thumbnails/ folder
        new_key = key.replace('uploads/', 'thumbnails/')
        s3_client.upload_file(upload_path, bucket, new_key)
       
        print(f"Success! Resized {key} and saved to {new_key}")
