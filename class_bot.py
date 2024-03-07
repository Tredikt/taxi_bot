from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from utils.db_api.database import DataBase

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import BotStates

from blanks.bot_markup import menu, towns_markup, refusal_reasons
from blanks.bot_texts import rules_text

from handlers.callback_handler import callback_handler
from states_handlers.fio_handler import fio_handler
from states_handlers.driver_license_handler import driver_license_handler
from states_handlers.auto_registration_certificate_handler import auto_registration_certificate_handler
from states_handlers.car_brand_handler import car_brand_handler
from states_handlers.automobile_handler import automobile_handler

from states_handlers.landing_point_handler import landing_point_handler
from states_handlers.end_point_handler import end_point_handler
from states_handlers.variable_point_handler import variable_point_handler


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        await state.finish()
        chat = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username
        fullname = message.from_user.full_name

        users = self.db.get_users()
        if tg_id not in users:
            self.db.add_user(
                tg_id=tg_id,
                username=username,
                fullname=fullname
            )

            await self.bot.send_message(
                chat_id=tg_id,
                text=rules_text
            )

        await self.bot.send_message(
            chat_id=tg_id,
            text="Приветствую тебя в нашем боте!",
            reply_markup=menu
        )

    async def text_handler(self, message: Message, state: FSMContext):
        # print(message)
        tg_id = message.from_user.id
        m_id = message.message_id
        chat_type = message.chat.type
        text = message.text

        drivers_ids = self.db.get_approved_drivers()
        driver_id = self.db.get_driver_bunch(customer_id=tg_id)
        customer_id = self.db.get_customer_bunch(driver_id=tg_id)

        if text.lower() == "создать заказ":
            remove_message = await self.bot.send_message(
                chat_id=tg_id,
                text=".",
                reply_markup=ReplyKeyboardRemove()
            )

            await self.bot.delete_message(
                chat_id=tg_id,
                message_id=remove_message.message_id
            )

            await self.bot.send_message(
                chat_id=tg_id,
                text="Выберите город",
                reply_markup=towns_markup
            )
            await BotStates.order.set()

        elif text.lower() == "стать водителем":
            await self.bot.send_message(
                chat_id=tg_id,
                text="Введите своё ФИО\n\n"
                     "ОБЯЗАТЕЛЬНО: русскими буквами с пробелами\n"
                     "Пример - Руденко Александр Сергеевич"
            )
            await BotStates.FIO.set()

        elif text.lower() == "завершить заказ":
            customer_id = self.db.get_customer_bunch(driver_id=tg_id)
            await self.bot.send_message(
                chat_id=customer_id,
                text="Заказ завершён",
                reply_markup=menu
            )

            await self.bot.send_message(
                chat_id=tg_id,
                text="Заказ завершён",
                reply_markup=menu
            )

            self.db.delete_bunch(driver_id=tg_id)
            self.db.delete_order_text(customer_id=customer_id)
            self.db.delete_order_message(customer_id=customer_id)

        elif text.lower() == "отказаться от заказа":
            await self.bot.send_message(
                chat_id=tg_id,
                text="Укажите причину отказа",
                reply_markup=refusal_reasons
            )

        elif tg_id in drivers_ids and customer_id:
            customer_id = self.db.get_customer_bunch(driver_id=tg_id)

            await self.bot.copy_message(
                chat_id=customer_id,
                from_chat_id=tg_id,
                message_id=m_id
            )

        elif driver_id:
            await self.bot.copy_message(
                chat_id=driver_id,
                from_chat_id=tg_id,
                message_id=m_id
            )

    def register_handlers(self):
        self.dp.register_callback_query_handler(callback=callback_handler, state="*")

        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")

        self.dp.register_message_handler(callback=landing_point_handler, content_types=["text"], state=BotStates.landing_point)
        self.dp.register_message_handler(callback=end_point_handler, content_types=["text"], state=BotStates.end_point)
        self.dp.register_message_handler(callback=variable_point_handler, content_types=["text"], state=BotStates.variable_point)

        self.dp.register_message_handler(callback=fio_handler, content_types=["text"], state=BotStates.FIO)
        self.dp.register_message_handler(callback=driver_license_handler, content_types=["photo"], state=BotStates.driver_license)
        self.dp.register_message_handler(callback=auto_registration_certificate_handler, content_types=["photo"], state=BotStates.auto_registration_certificate)
        self.dp.register_message_handler(callback=car_brand_handler, content_types=["text"], state=BotStates.car_brand)
        self.dp.register_message_handler(callback=automobile_handler, content_types=["photo"], state=BotStates.automobile)

        self.dp.register_message_handler(callback=self.text_handler, state="*", content_types=["text"])

    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)