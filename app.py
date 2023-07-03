# 使用系統和 config 檔案的函式庫功能
import os
import configparser
import json

# 使用 Flask 的函式庫功能
from flask import Flask, request, abort

# 使用 LINE Bot SDK 的函式庫功能
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, MessageTemplateAction, TemplateSendMessage, ConfirmTemplate


# 設定讀入 config.ini 檔案
config = configparser.ConfigParser()
config.read('config.ini')


# Flask Web Service 啟用
app = Flask(__name__)

line_bot_api = LineBotApi(config.get('line-bot',
                                     'channel_access_token'))
handler = WebhookHandler(config.get('line-bot',
                                    'channel_secret'))

@app.route('/')
def hello_Flask():

    msg = "Hello, Flask Web Service test 4!"
    
    return msg

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 從 Line 傳入的訊息
    msg = event.message.text
                                               
    # # 回傳相同文字內容
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

#  # 判斷訊息內容
#     if msg == '有話要說':
#         # 在這裡定義你的FlexMessage物件，並將其命名為flex_message
#         FlexMessage = json.load(open('card.json','r',encoding='utf-8'))

#         # 回傳 Flex Message
#         line_bot_api.reply_message(event.reply_token, FlexSendMessage('有話要說',FlexMessage))
#     else:
#         # 回傳相同文字內容
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

 # 判斷訊息內容
    if msg == '確認樣板':
        # # 在這裡定義你的FlexMessage物件，並將其命名為flex_message
        # FlexMessage = json.load(open('card.json','r',encoding='utf-8'))

        # # 回傳 Flex Message
        # line_bot_api.reply_message(event.reply_token, FlexSendMessage('有話要說',FlexMessage))

        ConfirmMessage = TemplateSendMessage(
            alt_text="確認樣板",
            template=ConfirmTemplate(
                text="目前現場看診號為1111號，下一個線上取號為110號，您是否確認取號, 第二次測式",
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label="是",
                        text="是"
                    ),
                    MessageTemplateAction(
                        label="否",
                        text="否"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, ConfirmMessage)
    else:


  
        # 回傳相同文字內容
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

if __name__ == "__main__":
    app.run()
