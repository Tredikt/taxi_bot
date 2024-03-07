from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates
from config import admin_id


async def car_brand_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    text = message.text

    async with state.proxy() as data:
        data["car_brand"] = text

    await bot.send_message(
        chat_id=tg_id,
        text="Отправьте фото автомобиля, чтобы вас приняли как водителя, нужно, что фото было чётким"
    )

    await BotStates.automobile.set()