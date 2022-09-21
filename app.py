from aiogram import Dispatcher, Bot
from aiogram.types import Update

from src.database.base import database
from src.handlers.jivochat import routers
from src.settings.config import BOT_TOKEN, HOST, PORT
import uvicorn as uvicorn
from fastapi import FastAPI
import logging


from loader import dp, bot
import src.middlewares
import src.handlers

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
logging.basicConfig(format=_log_format, filename='logs.log', level=30)


app = FastAPI()
app.include_router(routers)


WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
WEBHOOK_URL = HOST + WEBHOOK_PATH


@app.post('/bot/{BOT_TOKEN}')
async def bot_webhook(update: dict):
    try:
        telegram_update = Update(**update)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(telegram_update)
    except Exception as ex:
        logging.warning(ex)


@app.on_event('startup')
async def on_startup():
    await database.connect()
    await bot.delete_webhook()
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    print(f'APP started on port {PORT}')


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level=30)

