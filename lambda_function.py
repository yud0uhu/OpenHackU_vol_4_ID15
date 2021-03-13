# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage,
#     QuickReplyButton, MessageAction, QuickReply,
#     StickerMessage, StickerSendMessage, FollowEvent, ImageMessage, ImageSendMessage
# )
# from linebot.exceptions import (
#     LineBotApiError, InvalidSignatureError
# )
# import json
# import urllib.request
# import random
# import re
# import fatWord as fw
# import os
# import sys
# import logging

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
# if channel_secret is None:
#     logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
#     sys.exit(1)
# if channel_access_token is None:
#     logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#     sys.exit(1)

# line_bot_api = LineBotApi(channel_access_token)
# handler = WebhookHandler(channel_secret)


# def lambda_handler(event, context):
#     if "x-line-signature" in event["headers"]:
#         signature = event["headers"]["x-line-signature"]
#     elif "X-Line-Signature" in event["headers"]:
#         signature = event["headers"]["X-Line-Signature"]
#     body = event["body"]
#     ok_json = {"isBase64Encoded": False,
#                "statusCode": 200,
#                "headers": {},
#                "body": ""}
#     error_json = {"isBase64Encoded": False,
#                   "statusCode": 500,
#                   "headers": {},
#                   "body": "Error"}

#     # @handler.add(FollowEvent)
#     # def handle_follow(event):
#     #     line_bot_api.reply_message(
#     #         event.reply_token,
#     #         TextSendMessage(text='友達追加ありがとう！\n遊び方ガイドはこちら↓\n '
#     #                         'https://note.com/roast_official/n/ndc7d00f38d44\n「まんざい」と入力してみてね！')
#     #     )

#     @handler.add(MessageEvent, message=TextMessage)
#     def handle_message(event):
#         language_list = ["やかましいわ！", "知らんがな", "欧米かっ！", "ちょっと何言ってるかわからない",
#                          "太るって！", "病院行きな", "食べすぎだよ", "やかましいわ"]
#         items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}"))
#                  for language in language_list]

#         if event.message.text in language_list:
#             sticker_list = [['11537', 52002750], ['11537', 52002751], ['11537', 52002763],
#                             ['11538', 51626501], ['11538', 51626506], ['11538', 51626515]]
#             r = random.randint(0, 5)

#             # スタンプを返す
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 StickerSendMessage(package_id=sticker_list[r][0], sticker_id=sticker_list[r][1]))

#         # # 「漫才」「まんざい」を受け取ったとき
#         # elif event.message.text == "まんざい" or event.message.text == "漫才":
#         #     messages = TextSendMessage(
#         #         "ぜんざい", quick_reply=QuickReply(items=items))
#         #     line_bot_api.reply_message(event.reply_token, messages=messages)

#         # # 「コマンド」を受け取ったとき
#         # elif event.message.text == "コマンド":
#         #     messages = TextSendMessage(
#         #         "ルマンド", quick_reply=QuickReply(items=items))
#         #     line_bot_api.reply_message(event.reply_token, messages=messages)

#         # # 受け取ったメッセージが10字より大きいとき
#         # elif len(event.message.text) > 10:
#         #     line_bot_api.reply_message(
#         #         event.reply_token, TextSendMessage("単語が長いよ！" + "\uDBC0\uDC8F"))

#         # # 3の倍数のときにぼける
#         # elif event.message.text.isdigit():
#         #     i = int(event.message.text)
#         #     # print(i)
#         #     if i % 3 == 0:
#         #         sticker_list = [['11537', 52002750], ['11537', 52002751], ['11537', 52002763],
#         #                         ['11538', 51626501], ['11538', 51626506], ['11538', 51626515]]
#         #         r = random.randint(0, 5)
#         #         line_bot_api.reply_message(
#         #             event.reply_token,
#         #             StickerSendMessage(package_id=sticker_list[r][0], sticker_id=sticker_list[r][1]))
#         #     elif '3' in str(i):
#         #         line_bot_api.reply_message(
#         #             event.reply_token, TextSendMessage("3がついています"))
#         #     else:
#         #         line_bot_api.reply_message(
#         #             event.reply_token, TextSendMessage("Pardon?" + "\uDBC0\uDC9F"))

#         # elif re.compile(r'^[a-zA-Z0-9_!"#$%&-+:/\\ \']+$').match(event.message.text) is not None:
#         #     print(type(event.message.text))
#         #     line_bot_api.reply_message(
#         #         event.reply_token, TextSendMessage("Pardon?" + "\uDBC0\uDC9F"))

#         else:
#             word = event.message.text
#             kaiseki_text = fw.message_generate(word)
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=kaiseki_text))

#         # 数字やローマ字、不可能な変換の時の処理

#     try:
#         handler.handle(body, signature)
#     except LineBotApiError as e:
#         logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
#         for m in e.error.details:
#             logger.error("  %s: %s" % (m.property, m.message))
#         return error_json
#     except InvalidSignatureError:
#         return error_json

#     return ok_json


# # スタンプメッセージを受け取ったとき
# '''
# @ LINE_HANDLER.add(MessageEvent, message=StickerMessage)
# def handle_message(event):
#     LINE_BOT_API.reply_message(event.reply_token,
#                                 StickerSendMessage(package_id=11539, sticker_id=52114129))

# # 画像メッセージを受け取ったとき

# @ LINE_HANDLER.add(MessageEvent, message=ImageMessage)
# def handle_message(event):
#     LINE_BOT_API.reply_message(event.reply_token,
#                                 StickerSendMessage(package_id=11538, sticker_id=51626506))
# '''
