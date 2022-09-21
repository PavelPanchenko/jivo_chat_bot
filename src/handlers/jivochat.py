import json
import logging

from fastapi import APIRouter
from loader import bot
from src.database.base import update_user_db, UserUpdate, get_user_one_db
from src.handlers.start import start_chat_button, close_chat_button

routers = APIRouter(prefix="/jivo")


@routers.post('/wh')
async def get_message(on_message: dict):
    print('on_message ', on_message)
    try:
        user = await get_user_one_db(on_message['recipient']['id'])

        if user.in_chat:
            if on_message['message']['type'] == 'text':
                await bot.send_message(
                    chat_id=on_message['recipient']['id'],
                    text=on_message['message']['text']
                )

            if on_message['message']['type'] == 'photo':
                await bot.send_photo(
                    chat_id=on_message['recipient']['id'],
                    photo=on_message['message']['file']
                )
        return json.dumps({"result": "ok"})
    except Exception as ex:
        logging.warning({"status": "false", "message": ex})


# https://ad51-165-22-69-40.eu.ngrok.io/jivo/wh
# https://ad51-165-22-69-40.eu.ngrok.io/jivo/wh/event

@routers.post('/wh/event')
async def get_event(event: dict):
    try:
        user = await get_user_one_db(event['visitor']['phone'])

        if user.in_chat:
            if event['event_name'] == 'chat_accepted':
                await bot.send_message(
                    chat_id=event['visitor']['phone'],
                    text=f"Оператор {event['agent']['name']} присоединился к чату",
                    reply_markup=close_chat_button
                )
                await update_user_db(UserUpdate(tg_id=event['visitor']['phone'], in_chat=True))

            if event['event_name'] == 'chat_finished':
                await bot.send_message(
                    chat_id=event['visitor']['phone'],
                    text=f"Оператор закрыл диалог",
                    reply_markup=start_chat_button
                )
                await update_user_db(UserUpdate(tg_id=event['visitor']['phone'], in_chat=False))
        return json.dumps({"result": "ok"})
    except Exception as ex:
        return {"status": "false", "message": ex}
