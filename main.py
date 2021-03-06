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

line_bot_api = LineBotApi(
    '0F0ruLLyrRShKHfjJgSxMyW0A+ZWGdpYewXwweClo5QMGK4ML9DbucKPd8UfXK7B/b39il/kPp5GQq7jvImnzdBEQc6gMukxEJSOAv5n+8UzdsUMPmcfTMTbh22oBR2CSHGDHD5x+lS7LYcZkYXDVQdB04t89/1O/w1cDnyilFU=" --app food-conversion-bot-niku')
handler = WebhookHandler(
    '2f785eda6e1e891ed9cf1c58592717b5')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
