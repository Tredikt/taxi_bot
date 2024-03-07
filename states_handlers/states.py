from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    FIO = State()
    driver_license = State()
    auto_registration_certificate = State()
    car_brand = State()
    automobile = State()

    order = State()
    landing_point = State()
    end_point = State()
    variable_point = State()