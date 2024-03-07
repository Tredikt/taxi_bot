from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates


async def auto_registration_certificate_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    photo = message.photo[-1].file_id

    async with state.proxy() as data:
        data["arc"] = photo

    await bot.send_message(
        chat_id=tg_id,
        text="Отправьте номер и марку автомобиля.\n"
             "Пример: Лада Гранта А732НГ"
    )

    await BotStates.car_brand.set()