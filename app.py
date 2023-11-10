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


from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 使用您提供的Channel Access Token
CHANNEL_ACCESS_TOKEN = 'CFpKo+Ei6jeRbHhKFB6H70Fs806m2HIyydxv0GmqKR5d1kgNtBaf6Dq1vPnIVv10RwrrfNPDMLULyAltA6v0ANkq2a3eFnVHChajvOoJfv1YvGpHqTftBXPjl/PwQYzeRbA/yGxFhrcxNZAlPP07LgdB04t89/1O/w1cDnyilFU='

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    user_id = request.form['line_id']
    message = request.form['message']
    if send_to_line(user_id, message):
        return '訊息已發送'
    else:
        return '發送失敗'

def send_to_line(user_id, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
    return response.status_code == 200

if __name__ == '__main__':
    app.run(debug=True)
