import boto3
import csv
client=boto3.client('rekognition', aws_access_key_id="",
                    aws_secret_access_key="",
                    region_name='ap-south-1')
def create_collection(collection_id):
    print('Creating collection:'+collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: '+response['CollectionArn'])
    print('Status code : '+str(response['StatusCode']))
    print('Done...')
def main():
    collection_id='students123'
    create_collection(collection_id)
if __name__=="__main__":
    main()