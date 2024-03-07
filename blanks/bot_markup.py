from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from blanks.bot_dicts import towns_dicts

menu = ReplyKeyboardMarkup(resize_keyboard=True).add("Создать заказ").add("Стать водителем")

towns_markup = InlineKeyboardMarkup()
for number, town in towns_dicts.items():
    towns_markup.add(
        InlineKeyboardButton(
            text=town,
            callback_data=f"town_{number}"
        )
    )

addition_markup = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Детское кресло",
        callback_data="addition_1"
    )
).add(
    InlineKeyboardButton(
        text="Животные",
        callback_data="addition_2"
    )
).add(
    InlineKeyboardButton(
        text="Багаж",
        callback_data="addition_3"
    )
).add(
    InlineKeyboardButton(
        text="Доставка (по предоплате)",
        callback_data="addition_4"
    )
).add(
    InlineKeyboardButton(
        text="Оформить заказ",
        callback_data="complete_order"
    )
)


refusal_reasons = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Уехал с другими",
        callback_data="reason_1"
    )
).add(
    InlineKeyboardButton(
        text="Долгое время ожидания",
        callback_data="reason_2"
    )
).add(
    InlineKeyboardButton(
        text="Не устраивает цена",
        callback_data="reason_3"
    )
).add(
    InlineKeyboardButton(
        text="Передумал ехать",
        callback_data="reason_4"
    )
)