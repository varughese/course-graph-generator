import firebase_admin
from firebase_admin import credentials, db

# Need to download this from firebase console ... 
cred = credentials.Certificate('./rmp_scraper/secretkey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pitt-course-scheduler412.firebaseio.com/'
})


profs_ref = db.reference('prof')