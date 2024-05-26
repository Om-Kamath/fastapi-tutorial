import firebase_admin
from firebase_admin import credentials, firestore, storage
import names
from functions import delete_persisted_db

cred = credentials.Certificate("app/fastapi-c578e-firebase-adminsdk-dg77k-0454ae4afb.json")
firebase_admin.initialize_app(cred,  {'storageBucket': 'fastapi-c578e.appspot.com'})

bucket = storage.bucket()

# Write code to upload a file to Firebase Storage
def upload_to_firebase(filepath, filename):
    delete_persisted_db()
    user = names.get_first_name()
    blob = bucket.blob(f"{user}/{filename}")
    blob.upload_from_filename(filepath, content_type="application/pdf")
    blob.make_public()
    url = blob.public_url
    print("File uploaded to Firebase Storage",url)
    return url