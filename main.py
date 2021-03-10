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
import os
import dajaregen as dj
import kaiseki as kk

app = Flask(__name__)

# 環境変数取得
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
# YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

# 自分のチャネルトークンを書く、Herokuデプロイ時は不要
line_bot_api = LineBotApi(
    '/DiRhoeKEIwKHh6HFr+5cD1Je/5stHPbqXpC0QtT9kdDHdiOvfWIdbMx49c/F40G/b39il/kPp5GQq7jvImnzdBEQc6gMukxEJSOAv5n+8X0gBzc1AE4x1IKybZrH04Hie5nAG8y4eIyJkQJZgDMsgdB04t89/1O/w1cDnyilFU=')
# 自分のチャネルシークレットを書く、Herokuデプロイ時は不要
handler = WebhookHandler('168c266a7d5b15a5730f456703c7160b')

# line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word = event.message.text
#    dajare_text = dj.dajare_search(word)
    kaiseki_text = kk.word_kaiseki(word)
    line_bot_api.reply_message(
        event.reply_token,
        #        TextSendMessage(text=dajare_text))
        TextSendMessage(text=kaiseki_text))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
