from asyncore import write
from collections import defaultdict
from io import BytesIO
import boto3
import zipfile
import os
import shutil

# S3
BATCH_BUCKET_NAME = "trenduk-batch"
SERVING_BUCKET_NAME = "trenduk-serving-yearly"
FILE_NAME = "initiate.zip"

def fan_out(event, _):

    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=BATCH_BUCKET_NAME)

    # Iterate through objects in Batch Layer Bucket and distinguish them by years
    # Skip duplicate files by using visited set
    visited = set()
    os.mkdir("final")
    for data in response['Contents']:
        
        os.mkdir("tmp")
        file = s3_client.get_object(Bucket=BATCH_BUCKET_NAME, Key=data['Key'])
        buffer = BytesIO(file['Body'].read())
        zipped = zipfile.ZipFile(buffer)
        zipped.extractall("tmp")

        for file in os.listdir("tmp"):
            if file in visited:
                continue
            year = file[8:12]
            with zipfile.ZipFile(f'final/{year}.zip', 'a') as yearly_zip:
                yearly_zip.write("tmp/" + file)
                visited.add(file)
        
        shutil.rmtree("tmp")

    # Write to our Serving Layer Bucket
    if SERVING_BUCKET_NAME not in s3_client.list_buckets():
        s3_client.create_bucket(Bucket=SERVING_BUCKET_NAME)
        for file in os.listdir("final"):
            s3_client.upload_file("final/"+file, SERVING_BUCKET_NAME, file)
        
    shutil.rmtree("final")

    return "Hello World"

if __name__ == "__main__":
    fan_out(None,None)