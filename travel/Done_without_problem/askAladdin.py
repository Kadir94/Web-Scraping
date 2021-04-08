from datetime import datetime

from currency_converter import CurrencyConverter
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
from pyppeteer import launch
import asyncio


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    info = []
    prices = []
    trip1 = None
    trip2 = None
    trip3 = None
    list_dict = []
    date = None
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    try:
        await page.goto('https://ask-aladdin.com/egypt-transport-system/bus-timetables/', timeout=9000)
    except (TimeoutError, PageError):
        # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
        print('Timeout')
    try:
        await page.waitForXPath('//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")]',{'visible': True, 'timeout': 5000})
    except TimeoutError:
        print('Timeout1')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")] ..."{ENDE}')
    while True:
        try:
            trip1 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+destination}")]',timeout=1000)
        except TimeoutError:
            print('Timeout2')
            # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
        if trip1:
            await trip1.click()
            break
        elif trip1 is None:
            try:
                trip2 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{"From"+" "+origin+" "+"to"+" "+destination}")]',timeout=1000)
            except TimeoutError:
                print('Timeout3')
                # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
        if trip2:
            await trip2.click()
            break
        elif trip2 is None:
            try:
                trip3 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+"the"+" "+destination}")]',timeout=1000)
            except TimeoutError:
                print('Timeout4')
                # logger.error('Timeout')
        if trip3:
            await trip3.click()
            break
        elif trip3 is None:
            try:
                trip4 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+"/"+destination}")]',timeout=1000)
                await trip4.click()
            except TimeoutError:
                # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
                print('Timeout6')
                # logger.error(f'{DARK_PURPLE} No {ENDE}{INBOX}{LIGHT_BLUE}"FINAL RESULTS"{ENDE}')
                return {
                    'country_id': country_id,
                    'origin_id': origin_id,
                    'destination_id': destination_id,

                    'data': [],
                    'total_size': total_size,
                    'order': order,
                    'hash_id': hash_id,
                    'status': 400  # No data found
                }
    chosen = await page.xpath('//div/div[@aria-expanded="true"]/div/div/div/table/tbody/tr/td')
    for i in chosen:
        name = await page.evaluate('(element) => element.textContent', i)
        info.append(name)
    dep_time = info[4::3]
    price = info[5::3]
    converter = CurrencyConverter()
    for p in price:
        price = float(p.replace('\xa0', ' ').replace('EGP', '').replace('LE', ' '))
        price = round(converter.convert(price, 'ZAR', 'EUR'),2)
        prices.append(price)
    for (d,p) in zip(dep_time, prices):
        list_dict.append({
            'Date': date,
            'DepartureTime': d.replace('\xa0', ''),
            'ArrivalTime': None,
            'Price': p
        })
    total_data = {
        'country_id': country_id,
        'origin_id': origin_id,
        'destination_id': destination_id,
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
        'status': 200  # Success
    }
    print(total_data)


asyncio.get_event_loop().run_until_complete(get_info(page=None,country_id=None,origin='Sharm',origin_id=None, destination='Cairo',destination_id=None,total_size=None,hash_id=None,order=None,date=None,logger=Logger))

# async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger)
