import os
import json
import boto3
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']
    
    # Set the destination bucket and key (where cleaned files will be stored)
    dest_bucket = 'your-destination-bucket'
    dest_key = src_key.replace('.zip', '-cleaned.csv')  # Assuming the output is CSV
    
    try:
        # Read the zipped file from S3
        s3_response = s3.get_object(Bucket=src_bucket, Key=src_key)
        zipped_data = s3_response['Body'].read()
        
        # Unzip the file
        with ZipFile(BytesIO(zipped_data)) as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as unzipped_file:
                # Read CSV data into a pandas DataFrame
                df = pd.read_csv(unzipped_file)
                
                # Drop rows with null values
                df_cleaned = df.dropna()
                
                # Convert cleaned DataFrame back to CSV
                cleaned_csv = df_cleaned.to_csv(index=False)
                
                # Upload the cleaned CSV to the destination bucket
                s3.put_object(Bucket=dest_bucket, Key=dest_key, Body=cleaned_csv)
                
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed and cleaned file: {src_key}')
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
