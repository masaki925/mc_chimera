import os
from fastapi import FastAPI, Request, HTTPException

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


@app.route('/callback', methods=['POST'])
async def callback(request: Request):
  signature = request.headers.get("X-Line-Signature", "")
  body = (await request.body()).decode('utf-8')
  app.logger.info('Request body: ' + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    raise HTTPException(status_code=400, detail='Invalid signature')

  return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))

