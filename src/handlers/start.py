import logging

from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from src.database.base import add_user_db, UserIn, update_user_db, get_user_one_db, UserUpdate
from src.utils.messages import start_message, status_chat_200_message
from src.utils.request_to_jivo import send_to_jivo_chat_message, is_online

start_chat_button = ReplyKeyboardMarkup(resize_keyboard=True)
start_chat_button.add(KeyboardButton(text='Начать диалог'))

cancel_chat_button = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_chat_button.add(KeyboardButton(text='Отмена'))


close_chat_button = ReplyKeyboardMarkup(resize_keyboard=True)
close_chat_button.add(KeyboardButton(text='Завершить чат'))


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message):
    tg_id = message.chat.id
    is_user = await get_user_one_db(tg_id)
    if not is_user:
        await add_user_db(UserIn(full_name=message.chat.full_name, tg_id=tg_id, in_chat=False))
    await message.answer(start_message.format(message.chat.first_name), reply_markup=start_chat_button)

items_button = ['Завершить чат', 'Отмена']


@dp.message_handler(lambda msg: msg.text in items_button, state='*')
async def chat_active(message: Message):
    await update_user_db(UserUpdate(tg_id=message.chat.id, in_chat=False))
    await send_to_jivo_chat_message(message, "Пользователь завершил диалог")
    await message.answer("Вы завершили диалог с оператором", reply_markup=start_chat_button)


@dp.message_handler(text='Начать диалог')
async def chat_connect(message: Message):
    try:
        status = is_online()
        if status:
            await message.answer(status_chat_200_message, reply_markup=cancel_chat_button)
            await send_to_jivo_chat_message(message, "Новый диалог")
            await update_user_db(UserUpdate(tg_id=message.chat.id, in_chat=True))

        if not status:
            await message.answer(f'На данный момент операторы не доступны', reply_markup=start_chat_button)
    except Exception as ex:
        logging.warning(ex)


@dp.message_handler()
async def chat_active(message: Message):
    try:
        user = await get_user_one_db(message.chat.id)
        if user.in_chat:
            await send_to_jivo_chat_message(message, message.text)
        else:
            await message.reply(text="Сообщение не доставлено")
    except Exception as ex:
        logging.warning(ex)




