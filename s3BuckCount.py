import boto3
import csv
import os

def lambda_handler(event, context):
    # TODO implement
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    
    fileName = "/tmp/s3_bucket_details.csv"
    
    with open(fileName, mode='w', newline='') as csv_file:
        fieldnames = ['Bucket Name', 'Creation Date', 'Last Modified', 'Objects Count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
    
    
        # Bucket Name, Creation Date, Modified Date, Number of Objects
        for bucket in response['Buckets']:
            
            #1
            bucket_name = bucket['Name']
            #print(bucket_name)
            #2
            creation_date = bucket['CreationDate']
            #print(creation_date)
            if 'Contents' in s3_client.list_objects_v2(Bucket=bucket_name):
                objects = s3_client.list_objects_v2(Bucket=bucket_name)['Contents']  
            else:
                objects = []
            #print(objects)
            if objects:
                for i in objects:
                    modified_date = i['LastModified']
            else:
                modified_date = "No Objects"
            #3
            #print(modified_date)
            #4
            objects_count = len(objects)
            #print(objects_count)
            print("Bucket Details: ", bucket_name, creation_date, modified_date, objects_count)
            
            writer.writerow({'Bucket Name': bucket_name, 'Creation Date': str(creation_date), 
            'Last Modified': str(modified_date), 'Objects Count': objects_count})
        
        
    s3_client.upload_file(fileName, 'csvbucket0101', 's3_bucket_details.csv')
        
    #os.remove(csvPath)

        
    """
    for name in response['Owner']:
        #owner_name = name['DisplayName']
        owner_id = name['ID']
        print("Owner Details: ", owner_id)
    """
        
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }

