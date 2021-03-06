import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle
# getting all known data

# with open('cv_images.dat', 'rb') as f:
#     images = pickle.load(f)
with open('classname.dat', 'rb') as f:
    classnames = pickle.load(f)
    


# def findencodings(images):
#     encodelist=[]
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode=face_recognition.face_encodings(img)[0]
#         encodelist.append(encode)
#     with open('dataset_faces.dat', 'wb') as f:
#         pickle.dump(encodelist, f)
#     return encodelist

print("Getting encodings....")
with open('dataset_faces.dat', 'rb') as f:
    encodeknown = pickle.load(f)
# if len(images) != len(encodeknown):
#     print("updating encodings......")
#     encodeknown=findencodings(images)
#     print("encodings update done.....")



#marking
def markings(name):
    with open("found_faces.csv","r+") as f:
        mydatalist=f.readlines()

        per=0
        now = datetime.now()
        timenow = str(now).split()
        date = timenow[0]
        time = timenow[1].split(".")[0]
        for line in mydatalist:
            entry=line.split(",")
            if entry[0]==name and entry[1]==date:
                per+=1
        if per==0:
            mandata=f"\n{name},{date},{time}"
            f.writelines(mandata)
            print("data recorded : ",mandata)
# getting query data

cap=cv2.VideoCapture(0)
while True:
    sucess,img=cap.read()
    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    facescurframe=face_recognition.face_locations(imgs)
    encodescurframe = face_recognition.face_encodings(imgs,facescurframe)
    for encodeface,faceloc in zip(encodescurframe,facescurframe):
        matches=face_recognition.compare_faces(encodeknown,encodeface)
        facedis=face_recognition.face_distance(encodeknown,encodeface)

        matchindex=np.argmin(facedis)

        if facedis[matchindex]>0.7:
            print("no match found")
            continue
        if matches[matchindex]:
            name=classnames[matchindex]
            print(name)
            y1,x2,y2,x1=faceloc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
            markings(name)
    cv2.imshow("face recogniser",img)

    cv2.waitKey(1)