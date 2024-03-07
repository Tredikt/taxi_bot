from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates


async def fio_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    text = message.text
    examination_symbols = "абвгдеёжзийклмнопрстуфхчцшщъыьэюя "

    for symbol in text:
        if symbol.lower() not in examination_symbols:
            await bot.send_message(
                chat_id=tg_id,
                text="Неверно указаны ФИО, попробуйте снова"
            )
    else:
        async with state.proxy() as data:
            data["fio"] = text

        await bot.send_message(
            chat_id=tg_id,
            text="Отправьте фото прав, чтобы вас приняли как водителя, нужно, что фото было чётким"
        )

        await BotStates.driver_license.set()