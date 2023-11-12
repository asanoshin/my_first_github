# # 使用系統和 config 檔案的函式庫功能
# import os
# import configparser
# import json

# # 使用 Flask 的函式庫功能
# from flask import Flask, request, abort

# # 使用 LINE Bot SDK 的函式庫功能
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, MessageTemplateAction, TemplateSendMessage, ConfirmTemplate, CarouselTemplate,  CarouselColumn


# # 設定讀入 config.ini 檔案
# config = configparser.ConfigParser()
# config.read('config.ini')


# # Flask Web Service 啟用
# app = Flask(__name__)

# line_bot_api = LineBotApi(config.get('line-bot',
#                                      'channel_access_token'))
# handler = WebhookHandler(config.get('line-bot',
#                                     'channel_secret'))

# @app.route('/')
# def hello_Flask():

#     msg = "Hello, Flask Web Service test 4!"
    
#     return msg

# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         print(body, signature)
#         handler.handle(body, signature)
        
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):

#     # 從 Line 傳入的訊息
#     msg = event.message.text
                                               
#     # 回傳相同文字內容
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))



# if __name__ == "__main__":
#     app.run()
# ----------------------------


import os
import pandas as pd
from flask import Flask, request, render_template
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

# 設定 LINE Messaging API 資訊
# 替換以下行的 YOUR_CHANNEL_ACCESS_TOKEN 和 YOUR_CHANNEL_SECRET
line_bot_api = LineBotApi('CFpKo+Ei6jeRbHhKFB6H70Fs806m2HIyydxv0GmqKR5d1kgNtBaf6Dq1vPnIVv10RwrrfNPDMLULyAltA6v0ANkq2a3eFnVHChajvOoJfv1YvGpHqTftBXPjl/PwQYzeRbA/yGxFhrcxNZAlPP07LgdB04t89/1O/w1cDnyilFU=')
YOUR_CHANNEL_SECRET = '495877a8a3b6ced6a694c97e969bd231'
# U879e3796fbb1185b9654c34152d07ed9


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            line_id = row[0]
            message = row[1]
            line_bot_api.push_message(line_id, TextSendMessage(text=message))
        
        # 在這裡刪除文件
        os.remove(file.filename)

        return 'Messages sent'

    return 'Upload error'

if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run()




# ----------------------
# from flask import Flask, request
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

# app = Flask(__name__)

# line_bot_api = LineBotApi('CFpKo+Ei6jeRbHhKFB6H70Fs806m2HIyydxv0GmqKR5d1kgNtBaf6Dq1vPnIVv10RwrrfNPDMLULyAltA6v0ANkq2a3eFnVHChajvOoJfv1YvGpHqTftBXPjl/PwQYzeRbA/yGxFhrcxNZAlPP07LgdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('495877a8a3b6ced6a694c97e969bd231')

# @app.route("/callback", methods=['POST'])
# def callback():
#     # 從請求中獲取 X-Line-Signature 標頭和請求主體
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)

#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_id = event.source.user_id  # 獲取用戶 ID
#     print("User ID:", user_id)  # 在伺服器上記錄用戶 ID

#     # 回應用戶
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=f"您的用戶 ID 是: {user_id}")
#     )

# if __name__ == "__main__":
#     app.run()
