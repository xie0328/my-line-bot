from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('NB2Mry0UxiEFbcv05lm5XxsoU5Z3yGWRTXwFQ0oGUl+DKDXiO9cRO29cqm8CcEACVDdUcsETRqQkF4DmHpeH+2vzlx2jkhnxxwFskxVZROyLGY4DSDqIQHySFHMYnH5ifI2u94SNTk1lcQfBcVlvjAdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('422e7743babe8225e9601a0e7b4a8c7f')

@app.route("/")
def home():
    return "LINE BOT API Server is running"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()