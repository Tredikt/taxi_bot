from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates
from config import admin_id


async def end_point_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    text = message.text

    async with state.proxy() as data:
        data["end_point"] = text

    await bot.send_message(
        chat_id=tg_id,
        text="Добавить промежуточный адрес?",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Да",
                callback_data="add_variable_point"
            ),
            InlineKeyboardButton(
                text="Нет",
                callback_data="cancel_variable_point"
            )
        )
    )