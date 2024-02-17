from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton
from utils.db_api.database import DataBase

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import menu


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        chat = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username

    async def text_handler(self, message: Message, state: FSMContext):
        tg_id = message.from_user.id
        m_id = message.message_id
        chat_type = message.chat.type

    def register_handlers(self):
        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
        self.dp.register_message_handler(callback=self.text_handler, state="*", content_types=["text"])

    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)