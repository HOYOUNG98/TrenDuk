from io import BytesIO
import boto3
import zipfile
import os
import shutil

from tqdm import tqdm

# S3
BATCH_BUCKET_NAME = "trenduk-batch"

def fan_out():

    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=BATCH_BUCKET_NAME)

    # Iterate through objects in Batch Layer Bucket and distinguish them by years
    # Skip duplicate files by using visited set
    visited = set()
    os.mkdir("tmp/zip_shards")
    for data in response['Contents']:
        
        os.mkdir("tmp/extracted")
        file = s3_client.get_object(Bucket=BATCH_BUCKET_NAME, Key=data['Key'])
        buffer = BytesIO(file['Body'].read())
        zipped = zipfile.ZipFile(buffer)
        zipped.extractall("tmp/extracted")

        for file in tqdm(os.listdir("tmp/extracted")):
            if file in visited:
                continue
            year = file[8:12]

            with zipfile.ZipFile(f'tmp/zip_shards/{year}.zip', 'a') as yearly_zip:
                yearly_zip.write("tmp/extracted/" + file, file)
                visited.add(file)
        
        shutil.rmtree("tmp/extracted")

    return 

if __name__ == "__main__":
    fan_out()