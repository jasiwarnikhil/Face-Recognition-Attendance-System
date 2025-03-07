import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("FireflyID.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/Students",
    'storageBucket': "facerecognitionsystem-4dcd3.appspot.com"
})
#https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/
#facerecognitionsystem-4dcd3.appspot.com
# importing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

print("Encoding Started ...")
encodeListknown = findEncodings(imgList)
encodeListknownWithIds = [encodeListknown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListknownWithIds, file)
file.close()
print("File Saved")