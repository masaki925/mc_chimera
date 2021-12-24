import os
from fastapi import FastAPI, request, abort

from linebot import (
  LineBotApi, WebhookHandler
)
from linebot.exceptions import (
  InvalidSignatureError
)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage
)


app = FastAPI()

ACCESS_TOKEN = os.getenv('MC_CHIMERA_LINE_ACCESS_TOKEN')
SECRET = os.getenv('MC_CHIMERA_LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route(“/callback”, methods=[‘POST’])
def callback():
  signature = request.headers[‘X-Line-Signature’]
  body = request.get_data(as_text=True)
  app.logger.info(“Request body: ” + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)

  return ‘OK’

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))

