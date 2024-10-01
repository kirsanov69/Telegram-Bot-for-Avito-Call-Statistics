from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from db import GetDataFromDb, AddDataToDb, async_session
from main import bot
from utils import parse_user_items
from tg_message_data import Message
import os
TEST_MODE = os.getenv("TEST_MODE", "False") == "True"


# Клавиатура с кнопкой "Показать статистику"
def get_stat_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    stat_button =InlineKeyboardButton(text="📊 Показать статистику", callback_data='stat')
    markup.add(stat_button)
    return markup

# Хендлер для команды отправки токена
async def handle_send_token(message: Message):
    token = message.text.split()[1:]
    user_id = message.from_user.id

    async with async_session() as session:
        # Проверка режима работы
        if TEST_MODE:
            # Использование тестовых данных
            await message.answer("Вы в тестовом режиме. Токен сохранен (фиктивно)!")
        else:
            # Реальная работа с базой данных и сохранение токенов
            user_tokens = await GetDataFromDb.get_tokens_by_user_id(session, user_id)
            if not user_tokens:
                await AddDataToDb.add_user_to_db(session, telegram_id=user_id, username=message.from_user.username, tokens=token)
            else:
                user_tokens.append(token)
                await AddDataToDb.update_user_tokens(session, user_id, user_tokens)
            await message.answer(f"Токен сохранен: {token}!", reply_markup=get_stat_keyboard())

# Хендлер для парсинга и генерации XLSX
async def handle_show_stats(callback_query: CallbackQuery):
    user_token = await GetDataFromDb.get_user_token(callback_query.from_user.id)  # Предполагается, что у вас уже есть токен в базе
    
    if not user_token:
        await bot.answer("Токен не найден. Сначала отправьте токен!")
        return
    
    # Парсим объявления и собираем статистику
    stats = await parse_user_items(user_token)
    
    # Отправляем пользователю результаты
    if isinstance(stats, str):
        await bot.answer(stats)
    else:
        response_message = "Статистика звонков по вашим объявлениям:\n"
        for stat in stats:
            response_message += (
                f"Объявление: {stat['title']}\n"
                f"Всего звонков: {stat['calls']}\n"
                f"Отвеченные звонки: {stat['answered']}\n"
                f"Новые звонки: {stat['new']}\n"
                f"Новые и отвеченные звонки: {stat['newAnswered']}\n"
                f"Дата: {stat['date']}\n\n"
            )
        await bot.answer(response_message)
