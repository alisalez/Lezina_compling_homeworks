# -*- coding: utf-8 -*-
"""bot

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NXdEni6H1FvmU-6E01bP02EO3Ti1KAJL
"""

!pip install aiogram -q

import json
import logging
from aiogram import Bot, Dispatcher, types  # Основные классы для работы с ботом
import asyncio  # Модуль для работы с асинхронным кодом
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiofiles

# Токен API бота
API_TOKEN = ""

# Настраиваем логирование, чтобы видеть информацию о работе бота в консоли
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

!wget -O faq.json https://raw.githubusercontent.com/vifirsanova/compling/refs/heads/main/tasks/task3/faq.json

# Загружаем данные из faq.json
with open('faq.json', encoding='utf-8') as f:
    data = json.load(f)

data

# Ключевые слова и категории
faq_keywords = {
    "цены": "цены, стоимость, заказ, оплата",
    "часы работы": "часы работы, время работы, доступность",
    "доставка": "доставка, сроки доставки, стоимость доставки, отслеживание",
    "возврат": "возврат, обмен, возврат товара, гарантия",
    "контакты": "связаться, телефон, email, адрес"
}

# Создаём клавиатуру с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О компании"), KeyboardButton(text="Связаться с оператором")]
    ],
    resize_keyboard=True
)

# Обрабатываем команды "/start" и "/help"
@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот, который может отвечать на частые вопросы.", reply_markup=keyboard)

# Обрабатываем текстовые сообщения (FAQ)
@dp.message()
async def answer_faq(message: types.Message):
    text = message.text.lower()

    # Проверяем кнопки
    if text == "о компании":
        await message.answer("Наша компания занимается доставкой товаров по всей стране.")
        return
    elif text == "связаться с оператором":
        await message.answer("Перевожу на оператора...")
        return

    # Поиск ответа по ключевым словам
    response = "Я не знаю ответа на этот вопрос."
    for category, keywords in faq_keywords.items():
        if any(keyword in text for keyword in keywords.split(", ")):
            for item in data["faq"]:
                if category in item["question"].lower():
                    response = item["answer"]
                    break
            break

    await message.answer(response)

# Запуск бота
async def main():
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    await main()