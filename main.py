from flask import Flask, request, abort
import os

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

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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

# 特定のキーワードに対して返信する、それ以外はオウム返しをする仕様
# オウム返しで渡しているevent.message.textの文字列に母音の類語を渡したい


@handler.add(MessageEvent, message=TextMessage)
　　　　def handle_text_message(event):
　　　　　　　　　　　　text = event.message.text
　　　　　　　　　　　　if text in ['やかましいわ', '知らんがな', 'ザイフ']:
　　　　　　　　　　　　　　　　　　　　line_bot_api.reply_message(
    event.reply_token,
    sticker_message=StickerSendMessage(
        package_id='1',
        sticker_id='1'
    ))
　　　　　　　　　　　　else:
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
