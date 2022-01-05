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

from mc_chimera.rapper import Rapper

app = FastAPI()
rapper = Rapper()

ACCESS_TOKEN = os.getenv('MC_CHIMERA_LINE_ACCESS_TOKEN')
SECRET = os.getenv('MC_CHIMERA_LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.get('/')
async def root():
    return rapper.verse('test')

@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = (await request.body()).decode('utf-8')
    print('Request body: ' + body)

    try:
      handler.handle(body, signature)
    except InvalidSignatureError:
      raise HTTPException(status_code=400, detail='Invalid signature')

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    res = rapper.verse(event.message.text)
    try:
        result = line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=res))
        print(result)
    except Exception as ex:
        print(ex)

