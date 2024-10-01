from sqlalchemy import  Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import logging
from config import load_config

# Загрузка конфигурации
config = load_config('config')

# Получение данных для подключения к базе данных
user = config.db.user
password = config.db.password
host = config.db.host
port = config.db.port
database = config.db.database





logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log_message(message):
    logger.info(f" {message}")



# Создание базового класса для объявления моделей
Base = declarative_base()

# Определение модели данных пользователя
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(50), default=None)
    tokens = Column(String(500), default=None)
    