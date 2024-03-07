from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import addition_markup
from states_handlers.states import BotStates
from config import admin_id


async def variable_point_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    text = message.text

    async with state.proxy() as data:
        data["variable_point"] = text

    await bot.send_message(
        chat_id=tg_id,
        text="Выберите из списка особенности поездки, либо оформите заказ",
        reply_markup=addition_markup
    )

