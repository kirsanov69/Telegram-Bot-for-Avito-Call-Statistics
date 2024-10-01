import aiohttp
import asyncio
import xlsxwriter
from db import GetDataFromDb



import aiohttp

class AvitoAPI:
    BASE_URL = "https://api.avito.ru/core/v1"

    @staticmethod
    async def get_user_items(user_token):
        url = f"{AvitoAPI.BASE_URL}/items"
        headers = {
            "Authorization": f"Bearer {user_token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("items", [])  # Возвращаем список объявлений
                else:
                    raise Exception(f"Ошибка при получении объявлений: {response.status}")


    @staticmethod
    async def get_call_stats(user_id, item_id, user_token):
        url = f"{AvitoAPI.BASE_URL}/accounts/{user_id}/calls/stats"
        headers = {
            "Authorization": f"Bearer {user_token}"
        }
        params = {
            "item_id": item_id  # ID объявления для которого запрашивается статистика
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Ошибка при получении статистики звонков: {response.status}")
                
async def parse_user_items(user_token):
    # Получаем список объявлений пользователя
    try:
        items = await AvitoAPI.get_user_items(user_token)
        
        if not items:
            return "Объявления не найдены"

        stats = []
        
        # Для каждого объявления получаем статистику звонков
        for item in items:
            item_id = item.get("id")
            user_id = item.get("user_id")
            title = item.get("title")
            
            try:
                call_stats = await AvitoAPI.get_call_stats(user_id, item_id, user_token)
                stats.append({
                    "title": title,
                    "calls": call_stats.get("calls", 0),
                    "answered": call_stats.get("answered", 0),
                    "new": call_stats.get("new", 0),
                    "newAnswered": call_stats.get("newAnswered", 0),
                    "date": call_stats.get("date")
                })
            except Exception as e:
                print(f"Ошибка при получении статистики для объявления {title}: {e}")
    except Exception as e:
        return f"Ошибка при получении объявлений: {e}"
    
    return stats

