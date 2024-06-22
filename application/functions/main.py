# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import db, initialize_app
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate("./secret.json")
# firebase_admin.initialize_app(cred)

initialize_app()
#
#
@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("bussDown")