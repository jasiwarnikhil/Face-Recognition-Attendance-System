import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("FireFlyID.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/Students"
})
#https://facerecognitionsystem-4dcd3-default-rtdb.firebaseio.com/
ref = db.reference('Students')

data = {
    "211": {
      "last_attendance_time": "2022-12-11 00:54:34",
      "major": "CSE AIML",
      "name": "Harsh K",
      "standing": "O",
      "starting_year": 2022,
      "total_attendance": 1,
      "year": 2
    },
    "215": {
      "last_attendance_time": "2022-12-11 00:54:34",
      "major": "CSE AIML",
      "name": "Aadi K",
      "standing": "O",
      "starting_year": 2022,
      "total_attendance": 1,
      "year": 2
    },
    "209": {
      "last_attendance_time": "2022-12-11 00:54:34",
      "major": "CSE AIML",
      "name": "Nikhil J",
      "standing": "O",
      "starting_year": 2022,
      "total_attendance": 1,
      "year": 2
    },
    "216": {
      "last_attendance_time": "2022-12-11 00:54:34",
      "major": "CSE AIML",
      "name": "Roshan K",
      "standing": "O",
      "starting_year": 2022,
      "total_attendance": 1,
      "year": 2
    },
    # "256": {
    #   "last_attendance_time": "2022-12-11 00:54:34",
    #   "major": "CE",
    #   "name": "Shivam D",
    #   "standing": "O",
    #   "starting_year": 2021,
    #   "total_attendance": 1,
    #   "year": 3
    # },
    "800": {
      "last_attendance_time": "2022-12-11 00:54:34",
      "major": "Teacher",
      "name": "IP D",
      "standing": "O",
      "starting_year": 2021,
      "total_attendance": 1,
      "year": 3
    }
}

for key, value in data.items():
    ref.child(key).set(value)