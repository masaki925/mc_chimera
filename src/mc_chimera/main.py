import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks

from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

from mc_chimera.rapper import Rapper


# APIクライアントとパーサーをインスタンス化
ACCESS_TOKEN = os.getenv('MC_CHIMERA_LINE_ACCESS_TOKEN')
SECRET = os.getenv('MC_CHIMERA_LINE_CHANNEL_SECRET')

line_api = AioLineBotApi(channel_access_token=ACCESS_TOKEN)
parser = WebhookParser(channel_secret=SECRET)

app = FastAPI()
rapper = Rapper()

async def handle_events(events):
    for ev in events:
        try:
            await line_api.reply_message_async(
                    ev.reply_token,
                    TextMessage(text=rapper.verse(ev.message.text)))
        except Exception as ex:
            print(ex)

@app.get('/')
async def root():
    return rapper.verse('test')

@app.post('/callback')
async def callback(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse(
        (await request.body()).decode('utf-8'),
        request.headers.get('X-Line-Signature', ''))

    background_tasks.add_task(handle_events, events=events)

    return 'OK'

