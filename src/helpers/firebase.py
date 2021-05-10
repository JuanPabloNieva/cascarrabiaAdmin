import pyrebase
import os

config = {
    "apiKey": "AIzaSyCKPFF6HfcmmKHeH_KBdTzjKZt67fImjkg",
    "authDomain": "testapi-d2ef9.firebaseapp.com",
    "databaseURL": "https://testapi-d2ef9-default-rtdb.firebaseio.com",
    "projectId": "testapi-d2ef9",
    "storageBucket": "testapi-d2ef9.appspot.com",
    "messagingSenderId": "101372487685",
    "appId": "1:101372487685:web:f62f0a6d1c7b80149c946c",
    "measurementId": "G-XXC67W3F4B"
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
