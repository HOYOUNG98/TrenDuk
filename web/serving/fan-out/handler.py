from io import BytesIO
import boto3
import zipfile

# S3
BUCKET_NAME = "trenduk-batch"
FILE_NAME = "initiate.zip"

def fan_out(event, _):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=BUCKET_NAME)

    for data in response['Contents']:
        file = s3_client.get_object(Bucket=BUCKET_NAME, Key=data['Key'])

        buffer = BytesIO(file['Body'].read())

        zipped = zipfile.ZipFile(buffer)
        print(len(zipped.namelist()))

    return "Hello World"

if __name__ == "__main__":
    fan_out(None,None)