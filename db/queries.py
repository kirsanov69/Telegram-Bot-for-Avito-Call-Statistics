from .models import Users
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from utils import parse_user_items
import os

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class AddDataToDb():
    @staticmethod

    async def add_user_to_db(session, telegram_id, username, tokens):
        user = Users(telegram_id=telegram_id, username=username, tokens=tokens)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user     


    async def add_tokens_to_user(session, user_id, tokens):
        user = session.query(Users).filter(Users.id == user_id).first()
        user.tokens = tokens
        await session.commit()
        await session.refresh(user)
        return user

class GetDataFromDb():

    async def get_user_by_telegram_id(session, telegram_id):
        
        user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        return user

    async def get_tokens_by_user_id(session, user_id):
        user = session.query(Users).filter(Users.id == user_id).first()
        return user.tokens             

TEST_MODE = os.getenv("TEST_MODE", "False") == "True"

class AvitoAPI:
    @staticmethod
    async def get_ads(user_id):
        if TEST_MODE:
            return [
                {"title": "Тестовое объявление 1", "calls": 10, "answered": 5},
                {"title": "Тестовое объявление 2", "calls": 15, "answered": 7},
            ]
        else:
            # Реальный запрос к API Avito
            response = await parse_user_items(user_id)
            return response

