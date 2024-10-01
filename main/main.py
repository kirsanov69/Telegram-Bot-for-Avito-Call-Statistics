from aiogram import Bot, Dispatcher, Router
from config import load_config
from aiogram.types import PreCheckoutQuery

config = load_config('config')

# # Создание бота и диспетчера
TOKEN = config.tg_bot.token           # Сохраняем токен в переменную bot_token
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Определение обработчика pre_checkout_query
@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
