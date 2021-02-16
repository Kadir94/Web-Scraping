import aiohttp
import asyncio
from datetime import datetime


async def get_info(code,origin,destination,date):
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y-%m-%d')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{code}/eur/en-US/{origin}/{destination}/anytime/{date_}?apikey=prtl6749387986743898559646983194') as response:
            print(await response.text())
            print(response.status)


asyncio.get_event_loop().run_until_complete(get_info('DE','US','DE',str(datetime.today())))
