from typing import List

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Filters



def get_match_regex(*strs_to_match):
    s = '|'.join(strs_to_match)
    return Filters.regex(f'^({s})$')


def reply_keyboard(
        buttons: List[List[str]], one_time_keyboard=False
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton(y) for y in x] for x in buttons],
        one_time_keyboard=one_time_keyboard,
    )


def inline_keyboard(
        buttons: List[List[str]], callbacks: List[List[str]]
) -> InlineKeyboardMarkup:
    keyboard = []
    for buttons_row, callbacks_row in zip(buttons, callbacks):
        keyboard.append(
            [
                inline_button(button, callback)
                for button, callback in zip(buttons_row, callbacks_row)
            ]
        )
    return InlineKeyboardMarkup(keyboard)


def inline_button(text: str, callback_data: str) -> InlineKeyboardButton:
    if text.startswith('https://'):
        button = InlineKeyboardButton(text='Читать', url=text, callback_data=callback_data)
    else:
        button = InlineKeyboardButton(text=text, callback_data=callback_data)

    return button
