import cv2
import os
import pickle
import EncodeGenerator
import face_recognition
import numpy as np
from datetime import datetime
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("FireflyID.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/Students",
        'storageBucket': "facerecognitionsystem-4dcd3.appspot.com"
    })
#https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/
#facerecognitionsystem-4dcd3.appspot.com
bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # Change to 0 if you have only one camera
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources\\background.png")

#importing mode images into a list
folderModePath = 'Resources\Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
#print(modePathList)
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#print(len(imgModeList))
    
# Load the encoding file
print("Loading Encode File")
with open('EncodeFile.p', 'rb') as file:  # Open the file in binary mode for reading
    encodeListknownWithIds = pickle.load(file)
encodeListknown, studentIds = encodeListknownWithIds
file.close()
print("Encode File Loaded")
#print(studentIds)

modeType = 0
counter = 0
id = -1
imgStudent = []

# Check if image is loaded
if imgBackground is None:
    print("Failed to load background image")
else:
    while True:
        success, img = cap.read()
        if success:  # Check if image is loaded

            imgS =cv2.resize(img, (0,0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurrentFrame = face_recognition.face_locations(imgS)
            encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

            imgBackground[162:162+480,55:55+640] = img
            imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

            if faceCurrentFrame:
                for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
                    matches = face_recognition.compare_faces(encodeListknown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
                    #print("matches", matches)
                    #print("faceDis", faceDis)

                    matchIndex = np.argmin(faceDis)
                    #print("Match Index", matchIndex)

                    if matches[matchIndex]:
                        #print("Known Face Detected")
                        #print(studentIds[matchIndex])
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        bbox = 55+x1, 162+y1, x2 - x1, y2 - y1
                        imgBackground = cvzone. cornerRect(imgBackground, bbox, rt = 0)
                        id = studentIds[matchIndex]

                        if counter == 0:
                            cvzone.putTextRect(imgBackground,"Loading", (275, 400))
                            cv2.imshow("Face Attendence", imgBackground)
                            cv2.waitKey(1)
                            counter = 1
                            modeType = 1

                if counter!=0:
                    if counter == 1:
                        #Get the Data
                        studentInfo = db.reference(f'Students/{id}').get()
                        print(studentInfo)
                        #Get the image from the storage
                        blob = bucket.get_blob(f'Images/{id}.png')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                        #Update data of attendence

                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                        "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                        print(secondsElapsed)
                        if secondsElapsed > 30: #57600 
                            ref = db.reference(f'Students/{id}')
                            studentInfo['total_attendance'] +=1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]


                    if modeType != 3:

                        if 10 < counter < 20:
                            modeType = 2

                        imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                        
                        if counter <= 10:
                            cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                            cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                            cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)



                            (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w)//2
                            cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                            imgBackground[175:175+216, 909: 909+216] = imgStudent


                        counter+=1

                        if counter >= 20:
                            counter = 0
                            modeType = 0
                            studentInfo = []
                            imgStudent = []
                            imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

            else:
                modeType = 0
                counter = 0

            #cv2.imshow("Webcam", img)
            cv2.imshow("Face Attendence", imgBackground)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Failed to load webcam image")
            break

cap.release()
cv2.destroyAllWindows()