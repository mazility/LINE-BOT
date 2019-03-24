import json
import os

from flask import Flask
from flask import request
from flask import make_response

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
    "type": os.environ.get('FIREBASE_TYPE'),
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace("\\n","\n"),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
    "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
})
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello~</h1>'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)

    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]

    if intent == 'ถามหนังน่าดู':

        doc_ref = db.collection(u'movies').get()
        #document(u'wFcZmjthSbXhyOGOGgJY')
        #doc = doc_ref.get().to_dict()
        #print(doc)
        for doc in doc_ref:
            speech = f'(u'{} => {}'.format(doc.id, doc.to_dict()))'
        #movie_name = doc['movie_name']
        #rel_date = doc['release_date']
        #speech = f'ตอนนี้มีเรื่อง {movie_name} เข้าโรงวันที่ {rel_date}'

    elif intent == 'เพิ่มรายชื่อ':
        speech = f'กรุณาพิม: (ชื่อจริง, นามสกุล, อายุ)'

    else:

        speech = "ผมไม่เข้าใจ คุณต้องการอะไร"

    res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):
    return {
        "fulfillmentText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
