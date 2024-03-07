from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates
from config import admin_id


async def automobile_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    photo = message.photo[-1].file_id

    async with state.proxy() as data:
        fio = data["fio"]
        dli = data["dli"]
        arc = data["arc"]
        brand = data["car_brand"]
        auto = photo

        username, fullname = db.get_user(tg_id=tg_id)

        db.add_driver(
            tg_id=tg_id,
            fio=fio,
            dli=dli,
            arc=arc,
            auto=auto,
            brand=brand,
            status="waiting"
        )

        media = MediaGroup()
        media.attach_photo(photo=dli, caption="dli")
        media.attach_photo(photo=arc, caption="arc")
        media.attach_photo(photo=auto, caption="auto")

        await bot.send_media_group(
            chat_id=admin_id,
            media=media
        )

        await bot.send_message(
            chat_id=admin_id,
            text=f"Fullname: {fullname}\n"
                 f"Username: @{username}\n"
                 f"ФИО: {fio}\n"
                 f"Марка и номер машины: {brand}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Одобрить ✅",
                    callback_data=f"approve_driver_{tg_id}"
                )
            ).add(
                InlineKeyboardButton(
                    text="Отклонить ❌",
                    callback_data=f"decline_driver_{tg_id}"
                )
            )
        )

        await bot.send_message(
            chat_id=tg_id,
            text="Ожидайте. Вам придёт сообщение по вашей заявке"
        )