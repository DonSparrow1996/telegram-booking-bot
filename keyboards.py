from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import (
    BUTTON_BOOK,
    BUTTON_CANCEL,
    SERVICES,
    AVAILABLE_TIMES
)


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_BOOK)]],
        resize_keyboard=True
    )


def get_service_keyboard():
    keyboard = [[KeyboardButton(text=service)] for service in SERVICES]
    keyboard.append([KeyboardButton(text=BUTTON_CANCEL)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def get_time_keyboard():
    keyboard = []

    for i in range(0, len(AVAILABLE_TIMES), 2):
        row = [
            KeyboardButton(text=AVAILABLE_TIMES[i])
        ]

        if i + 1 < len(AVAILABLE_TIMES):
            row.append(KeyboardButton(text=AVAILABLE_TIMES[i + 1]))

        keyboard.append(row)

    keyboard.append([KeyboardButton(text=BUTTON_CANCEL)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_CANCEL)]],
        resize_keyboard=True
    )
