import aiohttp
import asyncio
from datetime import datetime


async def get_info(code,origin,destination,date):
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y-%m-%d')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'core_url{code}/{"eur"}/{"en-US"}/{origin}/{destination}/anytime/{date_}?apikey=apikey') as response:
            print(await response.text())
            print(response.status)


asyncio.get_event_loop().run_until_complete(get_info('FR','us','de',str(datetime.today())))


