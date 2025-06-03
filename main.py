import cv2
import pickle
import os
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
from prettytable import PrettyTable

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
   'databaseURL': "https://faceattendancesystem-1cf6e-default-rtdb.firebaseio.com/",
   'storageBucket': "faceattendancesystem-1cf6e.appspot.com"
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread('Resources/background.png')#background

folderModePath = 'Resources/Modes'
modepathList = os.listdir(folderModePath)
imgModeList = []
for path in modepathList:
   imgModeList.append(cv2.imread(os.path.join(folderModePath,path))) 

#print(len(imgModeList))
print("Loading Encoded file ....")  #loading encoding file
file = open('EncodedFile.p' , 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, StudentIds = encodeListKnownWithIds
#print(StudentIds)
print("Encoded File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []
seen=set()
printed_students=set()

table = PrettyTable()
table.field_names = ["Roll No", "Name", "Total Attendance", "Starting Year"]

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        facedis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(facedis)

        if matches[matchIndex]:
            id = StudentIds[matchIndex]
            if id not in seen:
                print("Known face detected")
            

            # Once a match is found, retrieve the student info from the database
            studentInfo = db.reference(f'Students/{id}').get()
            seen.add(id)
            

            # Add student info to the table
            table.add_row([studentInfo['Roll No'], studentInfo['name'], studentInfo['total_attendance'], studentInfo['Starting year']])

            # Print the updated table after every match
            if id not in printed_students:
                print(table)
                printed_students.add(id)

            # Get the Image from the storage
            blob = bucket.get_blob(f'Images/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            # Update the rest of the data as before
            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%d-%m-%Y %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

            if secondsElapsed > 30:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance']) 
                ref.child('last_attendance_time').set(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
