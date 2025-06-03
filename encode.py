import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase
#try:
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancesystem-1cf6e-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancesystem-1cf6e.appspot.com"
})
#    print("Firebase initialized successfully")
#except Exception as e:
#    print(f"Error initializing Firebase: {e}")
#
## Load images from folder
folderPath = 'Images'
pathList = os.listdir(folderPath)
#print("Found images:", pathList)
#
imgList = []
StudentIds = []
#
## Read images and prepare Student IDs
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
#    if img is None:
#        print(f"Failed to load image: {path}")
#        continue  # Skip if the image couldn't be read
#    imgList.append(img)
    StudentIds.append(os.path.splitext(path)[0])
#
#    # Upload image to Firebase Storage
    fileName = f'{folderPath}/{path}'
#    try:
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
#        print(f"Uploaded {fileName} to Firebase Storage")
#    except Exception as e:
#        print(f"Error uploading {fileName} to Firebase Storage: {e}")
#
#print("Student IDs:", StudentIds)
#
## Function to find face encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
#        if len(encodings) > 0:
        encodeList.append(encode)
#        else:
#            print("No face found in image, skipping.")
    return encodeList
#
## Start face encoding
print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
#
#if encodeListKnown:
encodeListKnownWithIds = [encodeListKnown, StudentIds]
print("Encoding Complete")
#
#    # Save encodings to a file
file = open("EncodedFile.p", 'wb') 
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("Encoded file saved")
#else:
#    print("No encodings found to save.")
