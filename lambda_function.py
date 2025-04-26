import requests
import csv
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'output-bucket1551' 
    
    url = "https://cvscarlos.github.io/b3-api-dados-historicos/api/v1/tickers-ETF.json"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        nested_data = data.get('data', {})
        csv_file_path = '/tmp/output.csv'
        csv_key = 'output.csv'
        
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['ticker', 'codNeg', 'nome', 'dataMax', 'dataMin'])
            
            for key, value in nested_data.items():
                writer.writerow([key, value.get('codNeg'), value.get('nome'), value.get('dataMax'), value.get('dataMin')])  
        
        s3.put_object(
            Bucket=bucket_name,
            Key=csv_key,
            Body=open(csv_file_path, 'rb')
        )
        
        return {
            'statusCode': 200,
            'body': f"CSV file '{csv_file_path}' created successfully."
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': f'Error: {response.status_code}'
        }