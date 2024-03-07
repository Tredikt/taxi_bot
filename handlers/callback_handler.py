import aiogram
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext

from utils.functions.get_bot_and_db import get_bot_and_db

from states_handlers.states import BotStates

from blanks.bot_dicts import towns_dicts, addition_dict, reasons_dict
from blanks.bot_markup import addition_markup, menu


async def callback_handler(call: CallbackQuery, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = call["from"]["id"]
    callback = call.data
    m_id = call.message.message_id

    if callback.startswith("approve_driver_"):
        await call.answer(text="Водитель одобрен", show_alert=True)
        await bot.edit_message_reply_markup(
            chat_id=tg_id,
            message_id=m_id,
            reply_markup=InlineKeyboardMarkup()
        )

        driver_id = int(callback.split("_")[2])
        db.approve_driver(tg_id=driver_id)

        await bot.send_message(
            chat_id=driver_id,
            text="Вы были приняты в качестве водителя, теперь вам будут приходить заказы от пользователей"
        )

    elif callback.startswith("decline_driver_"):
        await call.answer(text="Водитель отклонён", show_alert=True)
        await bot.edit_message_reply_markup(
            chat_id=tg_id,
            message_id=m_id,
            reply_markup=InlineKeyboardMarkup()
        )

        driver_id = int(callback.split("_")[2])
        db.approve_driver(tg_id=driver_id)

        await bot.send_message(
            chat_id=driver_id,
            text="Вы были отклонены в качестве водителя, для подробностей свяжитесь с @Taxifishka"
        )

    elif callback.startswith("town"):
        town_number = callback.split("_")[1]
        await bot.edit_message_text(
            chat_id=tg_id,
            message_id=m_id,
            text=f"💬: <i>{towns_dicts[town_number]}</i>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup()
        )

        async with state.proxy() as data:
            data["town"] = towns_dicts[town_number]

        await bot.send_message(
            chat_id=tg_id,
            text="Введите адрес, откуда вас забирать"
        )

        await BotStates.landing_point.set()

    elif callback.startswith("add_variable_point"):
        await bot.edit_message_text(
            chat_id=tg_id,
            text=f"💬: <i>Добавить дополнительную точку</i>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(),
            message_id=m_id
        )

        await bot.send_message(
            chat_id=tg_id,
            text="Введите адрес переменной точки",
        )

        await BotStates.variable_point.set()

    elif callback.startswith("cancel_variable_point"):
        await bot.edit_message_text(
            chat_id=tg_id,
            text=f"💬: <i>Не добавлять дополнительную точку</i>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(),
            message_id=m_id
        )

        await bot.send_message(
            chat_id=tg_id,
            text="Выберите из списка особенности поездки, либо завершите заказ",
            reply_markup=addition_markup
        )

    elif callback.startswith("addition"):
        addition_number = callback.split("_")[1]
        l_text = list()
        l_data = list()
        cd = call.message.reply_markup.inline_keyboard

        async with state.proxy() as data:
            for l_el in cd:
                for el in l_el:
                    text = el["text"]
                    callback_data = el["callback_data"]
                    # print(data, "DATA")
                    print(callback_data, callback)

                    if callback == callback_data and text[0] != "✅":
                        text = "✅ " + text
                        data[f"addition_{addition_number}"] = str(addition_number)
                    elif callback_data == callback and text[0] == '✅':
                        text = text[2:]
                        del data[f"addition_{addition_number}"]

                    l_data.append(callback_data)
                    l_text.append(text)

        i_mp = InlineKeyboardMarkup()
        count = 0
        for text, ca in zip(l_text, l_data):
            i_mp.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=ca
                )
            )

            count += 1

        await bot.edit_message_reply_markup(
            chat_id=tg_id,
            message_id=m_id,
            reply_markup=i_mp
        )

    elif callback == "complete_order":
        try:
            await bot.edit_message_reply_markup(
                chat_id=tg_id,
                message_id=m_id,
                reply_markup=InlineKeyboardMarkup()
            )
        except Exception as e:
            print(e)

        drivers_ids = db.get_approved_drivers()
        text = "Новый заказ!"
        async with state.proxy() as data:
            landing_point = data["landing_point"]
            end_point = data["end_point"]
            variable_point = data.get("variable_point")

            text += f"\nОткуда забирать: <i>{landing_point}</i>"
            if variable_point:
                text += f"\nПромежуточный адрес: <i>{variable_point}</i>"
            text += f"\nКонечная точка: <i>{end_point}</i>\n\n"

            for num in range(1, 5):
                addition_number = data.get(f"addition_{num}")
                if addition_number:
                    text += f"{addition_dict[addition_number]}: ✅\n"

        await bot.send_message(
            chat_id=tg_id,
            text="Ожидайте, с Вами свяжется водитель",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("Отказаться от заказа")
        )

        db.add_order(customer_id=tg_id, order_text=text)

        for driver_id in drivers_ids:
            order_message = await bot.send_message(
                chat_id=driver_id,
                text=text,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Принять заказ",
                        callback_data=f"accept_order_{tg_id}"
                    )
                )
            )

            db.add_order_message(
                customer_id=tg_id,
                driver_id=driver_id,
                m_id=order_message.message_id
            )

        await state.finish()

    elif callback.startswith("accept_order"):
        customer_id = int(callback.split("_")[2])

        await bot.send_message(
            chat_id=customer_id,
            text="Ваш заказ принят. Все следующие сообщения кроме команд будут отправлены водителю.\n"
                 f"Подъедет машина: <b>{db.get_car_brand(driver_id=tg_id)}</b>",
            parse_mode="html"
        )

        db.add_bunch(
            driver_id=tg_id,
            customer_id=customer_id
        )

        order_text = db.get_order_text(customer_id=customer_id)
        drivers_ids = db.get_approved_drivers()
        for driver_id in drivers_ids:
            try:
                await bot.edit_message_text(
                    chat_id=driver_id,
                    message_id=db.get_order_message(
                        driver_id=driver_id,
                        customer_id=customer_id
                    ),
                    text=order_text + f"\n\n<i>Заказ принят</i>",
                    parse_mode="html",
                    reply_markup=InlineKeyboardMarkup()
                )
            except Exception as e:
                print(e)

        await bot.send_message(
            chat_id=tg_id,
            text="Теперь сообщения, которые вы пишите в чат, будут приходить пассажиру",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("Завершить заказ")
        )

    elif callback.startswith("reason"):
        number = callback.split("_")[1]

        driver_id = db.get_driver_bunch(customer_id=tg_id)

        await bot.send_message(
            chat_id=tg_id,
            text="Вы отказались от заказа",
            reply_markup=menu
        )

        await bot.send_message(
            chat_id=driver_id,
            text=f"Пассажир отказался от заказа по причине:\n"
                 f"<b>{reasons_dict[number]}</b>",
            parse_mode="html",
            reply_markup=menu
        )

        db.delete_bunch(driver_id=driver_id)
        db.delete_order_text(customer_id=tg_id)
        db.delete_order_message(customer_id=tg_id)

