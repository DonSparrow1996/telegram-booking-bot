import asyncio
import re

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import *
from keyboards import (
    get_main_keyboard,
    get_service_keyboard,
    get_time_keyboard,
    get_cancel_keyboard
)


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Booking(StatesGroup):
    service = State()
    time = State()
    name = State()
    phone = State()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        START_TEXT.format(business=BUSINESS_NAME),
        reply_markup=get_main_keyboard()
    )


@dp.message(lambda message: message.text == BUTTON_BOOK)
async def book_start(message: types.Message, state: FSMContext):
    await message.answer(CHOOSE_SERVICE_TEXT, reply_markup=get_service_keyboard())
    await state.set_state(Booking.service)

@dp.message(lambda message: message.text == BUTTON_CANCEL)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer(CANCEL_TEXT, reply_markup=get_main_keyboard())

@dp.message(Booking.service)
async def choose_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(CHOOSE_TIME_TEXT, reply_markup=get_time_keyboard())
    await state.set_state(Booking.time)


@dp.message(Booking.time)
async def choose_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(
    ENTER_NAME_TEXT,
    reply_markup=get_cancel_keyboard()
)
    await state.set_state(Booking.name)


@dp.message(Booking.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(ENTER_PHONE_TEXT)
    await state.set_state(Booking.phone)


@dp.message(Booking.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text

    if not re.match(r"^\+?\d{10,15}$", phone):
        await message.answer(INVALID_PHONE_TEXT)
        return

    await state.update_data(phone=phone)

    data = await state.get_data()

    await bot.send_message(
        ADMIN_ID,
        f"""🔥 Новий запис!

🛠 Послуга: {data['service']}
🕒 Час: {data['time']}
👤 Ім'я: {data['name']}
📞 Телефон: {data['phone']}
"""
    )

    await message.answer(SUCCESS_TEXT, reply_markup=get_main_keyboard())
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
