from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    departure_time = []
    price = []
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%d/%m/%Y')
    list_dict = []
    try:
        await page.goto('https://www.irishrail.ie/', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="CybotCookiebotDialogBody"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="CybotCookiebotDialogBody"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#CybotCookiebotDialogBodyButtonAccept")
    try:
        await page.waitForXPath('//*[@id="HFS_from"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="CybotCookiebotDialogBody"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_from")
    await page.type('[id=HFS_from]', origin)
    suggestion_1 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="suggestion"] ..."{ENDE}')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not click {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="suggestion"] ..."{ENDE}')
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_to")
    await page.type('[id=HFS_to]', destination)
    suggestion_2 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate (2) {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="suggestion"] ..."{ENDE}')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not click (2) {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="suggestion"] ..."{ENDE}')
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#HFS_date_REQ0")
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("aria-haspopup")''', "#HFS_date_REQ0")
    await page.click('[id=HFS_date_REQ0]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#HFS_date_REQ0', date_)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HafasQueryForm > div.f02__cta > button")
    try:
        await page.waitForXPath('//div[contains(@class,"lyr_itemResults")]',{'visible': True, 'timeout': 50000})
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
    dep_time = await page.xpath('//div/div[contains(@class,"lyr_timeRow lyr_plantime")]')
    prices = await page.xpath('//div/div/span[contains(@class,"lyr_bigValue")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
    arrival_time = departure_time[1::2]
    departure_time = departure_time[::2]
    for p in prices:
        prices_txt = await page.evaluate('(element) => element.textContent', p)
        price.append(prices_txt)
    for d, a, p in zip(departure_time,arrival_time, price):
        list_dict.append({
            'Date': date,
            'DepartureTime': d,
            'ArrivalTime': a,
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

# asyncio.get_event_loop().run_until_complete(get_info('Dublin Connolly', 'Limerick (Colbert)',datetime.datetime.today(),logger=None))
