from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
from pyppeteer import launch
import asyncio


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger)-> Dict:

    departure_time = []
    arrival_time = []
    prices = []
    list_dict = []
    # date_ = datetime.fromisoformat(date)
    # date_ = date_.strftime('%d.%m.%Y')
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    try:
        await page.goto('https://www.pv.lv/en/', timeout=90000)
    except (TimeoutError, PageError):
        print("timeout1")
        # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="from-station"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print("timeout2")
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="from-station"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#from-station")
    await page.type('[id=from-station]', origin)
    try:
        option = await page.waitForXPath(f'//ul/li[contains(text(),"{origin}")]',{'visible': True, 'timeout': 10000})
        await option.click()
    except Exception:
        print('cannot click option')
    try:
        await page.waitForXPath('//*[@id="to-station"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print("timeout3")
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="to-station"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#to-station")
    await page.type('[id=to-station]', destination)
    try:
        option2 = await page.waitForXPath(f'//ul/li[contains(text(),"{destination}")]',{'visible': True, 'timeout': 10000})
        await option2.click()
    except Exception:
        print('cannot click option2')
    try:
        await page.waitForXPath('//*[@id="switch-date-f"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print("timeout4")
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="switch-date-f"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#switch-date-f")
    await page.click('[id=switch-date-f]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#switch-date-f', date)
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div[contains(@class,"row")]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print("timeout5")
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
    dep_time = await page.xpath('//div/div[contains(@class,"col-3 col-time")]')
    arr_time = await page.xpath('//div/div[contains(@class,"col-4 col-time")]')
    price = await page.xpath('//div/div[contains(@class,"col-6 col-ticket-price")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
    del departure_time[0]

    for a in arr_time:
        ar_time_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_time.append(ar_time_txt)
    del arrival_time[0]

    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
        prices = [x.strip('   ') for x in prices]
    del prices[0]
    prices = [x[-6:] for x in prices]
    for d, a, p in zip(departure_time,arrival_time, prices):
        list_dict.append({
            'date': date,
            'departure_time': d,
            'arrival_time': a,
            'price': p
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

# asyncio.get_event_loop().run_until_complete(get_info('Rīga', 'Jelgava',datetime.datetime.today(),logger=None))
asyncio.get_event_loop().run_until_complete(get_info(page=None,country_id=None,origin='Cēsis',origin_id=None, destination='Valmiera',destination_id=None,total_size=None,hash_id=None,order=None,date="16.02.2021",logger=Logger))


