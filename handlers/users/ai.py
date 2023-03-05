from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp
from states.talk_state import AI
import openai


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

    history = 'Это ИИ создан для помощи людям. Он должен давать точный ответ на любой вопрос и поддерживать разговор.\n'
    if len(data) > 1:
        for index in range(0, len(data)):
            print(index)
            print(data[index])
            if data[index].get('question') is None:
                print(123213123)
                data[index]['question'] = message.text
                history += f"Вопрос: {data[index]['question']}\nОтвет:"
            else:
                history += f"Вопрос: {data[index].get('question')}\nОтвет: {data[index].get('answer')}\n"
    else:
        data[0]['question'] = message.text
        history += f"Вопрос: {data[0].get('question')}\nОтвет:"
    request = openai.Completion.create(
        engine="text-davinci-003",
        prompt='"""\n{}\n"""'.format(history),
        temperature=0.5,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0)
    resp_ai = request["choices"][0]["text"]
    data[-1]['answer'] = resp_ai.replace('\n', '')
    data.append({"question": None, "answer": None})
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



