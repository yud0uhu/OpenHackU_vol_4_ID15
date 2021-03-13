from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReplyButton, MessageAction, QuickReply,
    StickerMessage, StickerSendMessage, FollowEvent, ImageMessage, ImageSendMessage
)
import os
import random
import re
import fatWord as fw

app = Flask(__name__)

# 環境変数取得
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
# YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

# 自分のチャネルトークンを書く、Herokuデプロイ時は不要
# 自分のチャネルシークレットを書く、Herokuデプロイ時は不要

line_bot_api = LineBotApi(
    "YOUR_CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("YOUR_CHANNEL_SECRET")


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


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='友達追加ありがとう！\n遊び方ガイドはこちら↓\n '
                             'https://note.com/roast_official/n/ndc7d00f38d44\n「まんざい」と入力してみてね！')
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    language_list = ["やかましいわ！", "知らんがな", "欧米かっ！", "ちょっと何言ってるかわからない",
                     "太るって！", "病院行きな", "食べすぎだよ", "やかましいわ"]
    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}"))
             for language in language_list]

    if event.message.text in language_list:
        sticker_list = [['11537', 52002750], ['11537', 52002751], ['11537', 52002763],
                        ['11538', 51626501], ['11538', 51626506], ['11538', 51626515]]
        r = random.randint(0, 5)

        # スタンプを返す
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=sticker_list[r][0], sticker_id=sticker_list[r][1]))

    # 「漫才」「まんざい」を受け取ったとき
    elif event.message.text == "まんざい" or event.message.text == "漫才":
        messages = TextSendMessage("ぜんざい", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)

    # 「コマンド」を受け取ったとき
    elif event.message.text == "コマンド":
        messages = TextSendMessage("ルマンド", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)

    # 受け取ったメッセージが10字より大きいとき
    elif len(event.message.text) > 10:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("単語が長いよ！" + "\uDBC0\uDC8F"))

    # 3の倍数のときにぼける
    elif event.message.text.isdigit():
        i = int(event.message.text)
        # print(i)
        if i % 3 == 0:
            sticker_list = [['11537', 52002750], ['11537', 52002751], ['11537', 52002763],
                            ['11538', 51626501], ['11538', 51626506], ['11538', 51626515]]
            r = random.randint(0, 5)
            line_bot_api.reply_message(
                event.reply_token,
                StickerSendMessage(package_id=sticker_list[r][0], sticker_id=sticker_list[r][1]))
        elif '3' in str(i):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage("3がついています"))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage("Pardon?" + "\uDBC0\uDC9F"))

    elif re.compile(r'^[a-zA-Z0-9_!"#$%&-+:/\\ \']+$').match(event.message.text) is not None:
        print(type(event.message.text))
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("Pardon?" + "\uDBC0\uDC9F"))
#            event.reply_token, TextSendMessage(type(event.message.text)))

        # elif type(event.message) == 'sticker':
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         StickerSendMessage(package_id=sticker_list[4][0], sticker_id=sticker_list[4][1]))
    else:
        word = event.message.text
        kaiseki_text = fw.message_generate(word)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=kaiseki_text))

    # 数字やローマ字、不可能な変換の時の処理


# スタンプメッセージを受け取ったとき
@ handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
                               StickerSendMessage(package_id=11539, sticker_id=52114129))


# 画像メッセージを受け取ったとき
@ handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
                               StickerSendMessage(package_id=11538, sticker_id=51626506))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
