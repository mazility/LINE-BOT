from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('SY3Zi2N44O/ebyElL/L1a3/j6h425Q0ta/a1oFItkpCBQ3oadw0IAp41DLuOE+i90lX0g3oq0ys+l2L4HDneosZJ7Ua5g4BIG/mJd/U9+pgmoM4wsItTMfb5aqYDGeQWZItkiuOCJeM7vDolhq4FIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a3bc2b99d25742a9810396205c3ba4c6')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
