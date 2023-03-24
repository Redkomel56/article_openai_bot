from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp
from states.talk_state import AI
import openai
from loader import bot


@dp.callback_query_handler(text='start')
async def chat_start(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1,inline_keyboard=[[InlineKeyboardButton(text="Закончить чат", callback_data="start"), InlineKeyboardButton(text="Стереть память", callback_data="start")]])

    await call.message.answer("Отправть сообщение, чтобы начать переписку", reply_markup=kb)
    await AI.talk.set()
    await state.update_data(history=[{"question": None, "answer": None}])


@dp.message_handler(state=AI.talk)
async def chat_talk(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data = data.get('history')
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text="Закончить чат", callback_data="back"),
         InlineKeyboardButton(text="Стереть память", callback_data="clear")]])
    await message.answer("ИИ думает...", reply_markup=kb)

    history = []
    if len(data) > 1:
        for index in range(0, len(data)):
            if data[index].get('question') is None:
                data[index]['question'] = message.text
                d = {"role": "user", "content": data[index]['question']}
                history.append(d)
            else:
                d = [{"role": "user", "content": data[index]['question']}, {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = message.text
        d = {"role": "user", "content": data[0].get('question')}
        history.append(d)
    print(history)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=500,
        temperature=1,
    )
    resp_ai = request['choices'][0]['message']['content']
    data[-1]['answer'] = resp_ai.replace('\n', '')
    text = f"{message.from_user.username}\nQ:{data[-1]['question']}\nA:{data[-1]['answer']}"
    data.append({"question": None, "answer": None})
    if len(data) > 10:
        await state.update_data(history=[{"question": None, "answer": None}])
    await state.update_data(history=data)
    await message.answer(resp_ai)


@dp.callback_query_handler(text='back', state='*')
async def back(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1,inline_keyboard=[[InlineKeyboardButton(text="Начать чат с ИИ", callback_data="start")]])
    await call.message.answer(f"Привет, {call.from_user.full_name}! Этот бот написан для статьи. Он предоставит доступ к ChatGPT.", reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(text='clear', state='*')
async def clear(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Память ИИ стерта')
    await state.update_data(history=[{"question": None, "answer": None}])



