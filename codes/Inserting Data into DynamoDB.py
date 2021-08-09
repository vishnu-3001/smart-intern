import cv2
import boto3
import csv
import datetime as dt
import time
import requests
vedio_capture = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

client = boto3.client('rekognition', aws_access_key_id="",
                    aws_secret_access_key="",
                    region_name='ap-south-1')

s3client = boto3.client('s3', aws_access_key_id="",
                    aws_secret_access_key="",
                    region_name='ap-south-1')

def uploadimage():
    bucket ='students-vit'
    filename = 'test.jpg'
    relative_filename = 'test.jpg'
    
    s3client.upload_file(filename,bucket,relative_filename)
    print("file Uploaded")
    
    
def photo():
    bucket = 'students-vit'
    collection_id = 'students123'
    fileNames = ['test.jpg']
    threshold = 70
    maxFaces = 2
    
    for fileName in fileNames:
        response = client.search_faces_by_image(CollectionId = collection_id,Image={'S3Object': {'Bucket':bucket,'Name':fileName }},
                                               FaceMatchThreshold=threshold,MaxFaces = maxFaces
                                               
                                               
                                               )
        faceMatches = response['FaceMatches']
        print('Matching faces')
        
        for match in faceMatches:
            print('FaceId:'+match['Face']['FaceId'])
            print('External Id:' + match['Face']["ExternalImageId"])
            name1=match['Face']["ExternalImageId"]
            name=name1.split(".")
            name=name[0]
            date=str(dt.datetime.now())[0:11]
            time=dt.datetime.now().strftime('%H')
            period=""
            if(time=='9'):
                period="period1"
            elif(time=='10'):
                period="period2"
            else:
                period="period3"
            url="https://dfm1pj7315.execute-api.ap-south-1.amazonaws.com/attendance_input?name="+name+"&period="+period
            status=requests.request("GET",url)
            print(status.json())
            print("uploaded to DB")
            print("student detected :"+name)
            print('Similarity:' + "{:.2f}".format(match['Similarity'])+"%")
            
def main():       
    while True:
        current_time=dt.datetime.now().strftime("%d-%m-%y %H-%M-%S ")
        time_1=dt.datetime.now()
        print("present time: ",time_1)
        hr=time_1.strftime('%H')
        sd=time_1.minute
        ret,frame = vedio_capture.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor =1.2,minNeighbors=5)
        
        
        for(x,y,w,h) in faces:
            print(faces.shape)
            cv2.putText(frame,"faces detected: " + str(faces.shape[0]),(50,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,225),2)
            cv2.rectangle(frame,(x,y),(x+w+30, y+h+30),(0,255,0),1)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h+30,x:x+w+30]
            imgname = "test.jpg"
            cv2.imwrite(imgname,roi_color)
            uploadimage()
            a = photo()
            print(a)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imshow('Video',frame)
        
    vedio_capture.release()
    cv2.destroyAllWindows()
if __name__=="__main__":
    main()
            
        