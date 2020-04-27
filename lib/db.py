import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore
import os
import os 

# Need to download this from firebase console ... 
cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'firebase_creds.json'))
firebase_admin.initialize_app(cred)

db = firestore.client()

prof = db.collection(u'ratemyprofressors')
courses = db.collection('courses')

'''
Example of writing data
prof.document('12324').set({
    u'first': u'Vinicius',
    u'last': u'Petrucci',
    u'rating': 4.8
})

'''

