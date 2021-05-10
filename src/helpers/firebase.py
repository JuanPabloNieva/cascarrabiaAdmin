import pyrebase
import os

from config import *

config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,
    "databaseURL": DATABASE_URL,
    "projectId": PROJECT_ID,
    "storageBucket": STORAGE_BUCKET,
    "messagingSenderId": MESSAGING_SENDER_ID,
    "appId": APP_ID,
    "measurementId": MEASUREMENT_ID
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
auth = firebase.auth()


def generate_url_image(imagen):
    ubicacionImgFirebase = 'imagenes/{0}'.format(imagen.filename)

    if os.path.isdir(os.path.join('uploads')):
        pass
    else:
        os.mkdir(os.path.join('uploads'))
    imagen.save(os.path.join('uploads', imagen.filename))
    path_img = os.path.join('uploads', imagen.filename)

    storage.child(ubicacionImgFirebase).put(str(path_img))

    url_img = storage.child(ubicacionImgFirebase).get_url(1)

    return url_img
