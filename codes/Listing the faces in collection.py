import boto3
client=boto3.client('rekognition', aws_access_key_id="",
                    aws_secret_access_key="",
                    region_name='ap-south-1')
def list_faces_in_collection(collection_id):
    maxResults=2
    faces_count=0
    tokens=True
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)
    print('Faces in collection : '+collection_id)
    while tokens:
        faces=response['Faces']
        for face in faces:
            print("Face Id :"+face["FaceId"])
            print("External Id: "+face["ExternalImageId"])
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count
def main():
    bucket="students-vit"
    collection_id="students"
    faces_count=list_faces_in_collection(collection_id)
    print("faces count: "+str(faces_count))
if __name__ =="__main__":
    main()
