import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://faceattendancesystem-1cf6e-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    "7015" : {
        "name" : "Ashrita Lahon",
        "Roll No" : 220710007015,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    },
    "7011" : {
        "name" : "Anwesha Changkakoty",
        "Roll No" : 220710007011,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    },
    "7051" : {
        "name" : "Sampriti Kalita",
        "Roll No" : 220710007051,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    },
    "7016" : {
        "name" : "Atrayee Phukan",
        "Roll No" : 220710007016,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    },
    "7018" : {
        "name" : "Bhikrant Borah",
        "Roll No" : 220710007018,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    },
    "7038" : {
        "name" : "Nabajyoti Das",
        "Roll No" : 220710007038,
        "total_attendance" : 0,
        "last_attendance_time" : "03-10-2024 00:54:34",
        "Starting year" : "2022"
    }


#    #Store the rest students data in same manner
}
for key,value in data.items():
    ref.child(key).set(value)