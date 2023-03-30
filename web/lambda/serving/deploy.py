import boto3

from datetime import datetime

IN_BUCKET_NAME = "trenduk-serving"

if __name__ == "__main__":
    
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=IN_BUCKET_NAME)

    latest_date, latest_file_name = datetime.strptime("2000-01-01", "%Y-%m-%d"), "none.db"
    for data in response['Contents']:
        filename = data['Key']
        date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d")
        
        if date > latest_date:
            latest_date = date
            latest_file_name = filename
    
    file = s3_client.download_file(IN_BUCKET_NAME, latest_file_name, "../api/batch_view.db")
    file = s3_client.download_file(IN_BUCKET_NAME, latest_file_name, "../api/realtime_view.db")