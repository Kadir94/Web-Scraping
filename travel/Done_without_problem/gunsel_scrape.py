from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    dep_times = []
    prices = []
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%d/%m/%Y')
    list_dict = []
    try:
        await page.goto('https://lines.gunsel.ua/en', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="select2-fromStation-container"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="select2-fromStation-container"] ..."{ENDE}')
    await page.click('[id=select2-fromStation-container]',{'clickCount': 1})
    await page.type('[id=inputFromStation]', origin)
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//*[@id="select2-toStation-container"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="select2-toStation-container"] ..."{ENDE}')
    await page.click('[id=select2-toStation-container]',{'clickCount': 1})
    await page.type('[id=toStationParent]', destination)
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//*[@id="travelDate"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="travelDate"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#travelDate")
    await page.click('[id=travelDate]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#travelDate', date_)
    try:
        search_button = await page.waitForXPath('//div/button[@translate="bus_search"]',{'visible': True, 'timeout': 50000})
        await search_button.click()
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/button[@translate="bus_search"] ..."{ENDE}')
    try:
        await page.waitForXPath('//tr/td[contains(@class,"date-time")]',{'visible': True, 'timeout': 90000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE} No {ENDE}{INBOX}{LIGHT_BLUE}"FINAL RESULTS"{ENDE}')
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
    times = await page.xpath('//tr/td[contains(@class,"date-time")]')
    price = await page.xpath('//div[contains(@class,"price-column w-100")]')
    for t in times:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        dep_times.append(time_txt)
    departure_times = dep_times[::2]
    departure_times = [x[0:6] for x in departure_times]
    arrival_times = dep_times[1::2]
    arrival_times = [x[0:6] for x in arrival_times]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    new_prices = [x[0:8] for x in prices]

    for d,a,p in zip(departure_times,arrival_times,new_prices):
        list_dict.append({
            'Date': date,
            'DepartureTime': d.strip(' '),
            'ArrivalTime': a.strip(' '),
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
    return total_data


# asyncio.get_event_loop().run_until_complete(get_info('Odessa', 'Kyiv',datetime.today(),logger=None))

