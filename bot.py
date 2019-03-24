import json
import os
import random

from flask import Flask
from flask import request
from flask import make_response

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("type": "service_account",
                                "project_id": "line-bot-af799",
                                "private_key_id": "37f5bffdaf9b6983304d2ad46318e2671ff1c3f7",
                                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDhv9CP6GBVHuwB\nJB27398E8DhQah5RsXrJHal5o5oOKL/maL5lxVyL/EOxPrDaU3oLzaUp8nXmK/m1\nzFQB1mqvP96dO3IJRpgqhmNq68abWKTq8WXiwmzBxf2FwFV9M/Ed663Ph8bvyFEI\ntFKiQVj9AFMQmyjAjtOnlFrhZz+24DuNZbfMlCirCL6aOYo7Jgv/Tii9n4GUxPVo\n7WDAfC1I4YUfH2qSU5RL/Ch0N1f7VMFG0FNiWzEcf/2RxW8T4T6usakCIGYe/jvX\nsUv65qzArcNyBuPJLGi9Urw0fnWmeHDrf57Wa+VONgBfh9CWi/NDKiK0HbipMwWV\nbsvW6MjhAgMBAAECggEAK1rNeOnBoG9XF1QCktuIhvgEdKsgpgNOB7RW4SnCkyAP\n1LX+hOiNoMPCk1ZtHAzmlkA5DVCHhHwjEZ9LbevqIryDKhKp0K66WAZlrvnXc2un\nhoh0TwOUY/V8fjSlJm20i5DA2Wej1NaVe3S4HvmqV7J5gWmu/qYfb2JePsY3tgzH\nV/9siEAuN1Km7N0VvSqn4w+j1x/ltTzHJ8LcKZAfrU8M2EdrYylktgha2h2CwULH\n8hqWBGDAAGNiyWpK4suq0h7if1WPuI3cjURhbNRtd7dCeUqzcREtF1v6Tk2xWP5Y\nWCoG/+A+7zYVVwJcIEW+LXjVuJpTEHYVD9NHekOlTQKBgQD/ojbLf1f5l76AYJYw\nmF/kUVJojkprZveavM++VWmCGRj1c0Kj/98EAQj1Y/OK1DwExh45KHhKp/jOS241\nu9GbjSrzD85vakBdKMfxjhmK66gL46cn9K1UJ6dbYHwpIAjILiw176mFTDhogBYH\nvIm2qO6spItiHdPSgiKD6Ow5pQKBgQDiEqMEIEUbzGIxa8e8Vs1vfUzFSjOI4bTr\nE/hAcEjDILehYrSYrIufCRLXE/rI3uuuBz86CHIDMoiDazw42VVyFhDTI8J0xNQj\nvnKDzo01b8buAmsWsnXvPDglSH6FMqNQo11nRBpnYbvs9j8KGoYRuNvDpdCNvY1J\n6JU1LkCVjQKBgDKvNPIQI59HKOxHOkAUVh7syMwWOkclOT6i5QW15Z933mz8F2Bw\n4QToN6B/2s/R2LyRk3h9v6v9teUhK47X2G1hBfz/S0zn4i8WYN5R8FqM8tq4nnHb\nn2oqGpKRhMyan2MhVH61MAVP4XdGvhd2mE9xGzF7xm8DvvXj+3fv/LZJAoGBALNO\nrNU88xNVTBx+q/EJt+9Rpm5kp/NNcb1yHVietldtv7fVHgBp+mOtQrAsPKDNjoh9\nXvycbjFzByuVBjLgzhCqx7Vvi3AqHUgsaY95aC6V9WYZrO5XpYqWbMHFefQTcc0n\nhZG+RmLw9ajAtsdAuk2cHVJUVdHWIhYYzx9bDAaRAoGBALpq/spLr8Cjq2ikHW8T\nVme+TauiyZRL/mPcVQRq6VzT5W8XX6oKId36z694rTMgbb/nb3f5PnMI9J5jCvRK\nIAYHsujy9U2MzdVkz7Vk9Q51LVkbyCQdJdhdsc6s1Mo065IeHG/g2/VCozR5um6n\ncl1pEWXUNFBrpZDWeTJtVTAy\n-----END PRIVATE KEY-----\n",
                                "client_email": "firebase-adminsdk-pt28c@line-bot-af799.iam.gserviceaccount.com",
                                "client_id": "116407728427108674646",
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pt28c%40line-bot-af799.iam.gserviceaccount.com")
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

        doc_ref = db.collection(u'movies').document(u'wFcZmjthSbXhyOGOGgJY')
        doc = doc_ref.get().to_dict()
        print(doc)

        movie_name = doc['movie_name']
        rel_date = doc['release_date']
        speech = f'ตอนนี้มีเรื่อง {movie_name} เข้าโรงวันที่ {rel_date}'

    elif intent == 'เพิ่มรายชื่อ':
        speech = f'ชื่อจริง, นามสกุล, อายุ'

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
