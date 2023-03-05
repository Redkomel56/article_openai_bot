from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1,inline_keyboard=[[InlineKeyboardButton(text="Начать чат с ИИ", callback_data="start")]])
    await message.answer(f"Привет, {message.from_user.full_name}! Этот бот написан для статьи. Он предоставит доступ к ChatGPT.", reply_markup=kb)
