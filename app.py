# 使用系統和 config 檔案的函式庫功能
import os
import configparser
import openai
import tiktoken

# 使用 Flask 的函式庫功能
from flask import Flask, request, abort

# 使用 LINE Bot SDK 的函式庫功能
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage


# 設定讀入 config.ini 檔案
config = configparser.ConfigParser()
config.read('config.ini')


# Flask Web Service 啟用
app = Flask(__name__)

line_bot_api = LineBotApi(config.get('line-bot',
                                     'channel_access_token'))
handler = WebhookHandler(config.get('line-bot',
                                    'channel_secret'))


# openai setting
os.environ["OPENAI_API_KEY"] = config.get('line-bot',
                                          'openai_api_key')
@app.route('/')
def hello_Flask():

    msg = "這是第二次測式"
    
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


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":
      num_tokens = 0
      for message in messages:
          num_tokens += 4
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":
                  num_tokens += -1
      num_tokens += 3  
      return num_tokens

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 從 Line 傳入的訊息
    msg = event.message.text

    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [{"role": "user", "content": msg}]

    # 自製的 tokens 計算，用來預先處理 prompt
    count = num_tokens_from_messages(messages)
    print(f"{count} prompt tokens counted by num_tokens_from_messages().")

    if count <= 160:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=messages,
                                                temperature=0,
                                                max_tokens=256)

        reply_msg = response.choices[0].message["content"]

        # counting tokens
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokes = response["usage"]["completion_tokens"]
        total_tokens = response["usage"]["total_tokens"]
        
    else:
        reply_msg = "很抱歉，您輸入的提示語句過長，請調整長度"

    # 回傳相同文字內容
    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_msg))


if __name__ == "__main__":
    app.run()
