from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    arr_times = []
    dep_times = []
    locs = []
    prices = []

    await page.goto('https://www.checkmybus.de/', timeout=90000)
    cookies_frame = page.frames[0]
    await cookies_frame.waitForSelector('#gdpr-c-acpt', {'visible': True})
    await cookies_frame.evaluate('''(selector) => document.querySelector(selector).click()''', "#gdpr-c-acpt")
    try:
        await page.waitForXPath('//*[@id="origincityname"]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    await page.click('[id=origincityname]',{'clickCount': 1})
    await page.type('[id=origincityname]', origin)
    departure_choice = None
    try:
        departure_choice = await page.waitForXPath(f'//div[contains(text(),"{origin}")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    if departure_choice:
        await departure_choice.click()
    else:
        logger.error('Can not find Departure')

    await page.click('[id=destinationcityname]',{'clickCount': 1})
    await page.type('[id=destinationcityname]', destination)
    arrival_choice = None
    try:
        arrival_choice = await page.waitForXPath(f'//div[contains(text(),"{destination}")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    if arrival_choice:
        await arrival_choice.click()
    else:
        logger.info('Arrival City Is Not Valid')
    try:
        await page.waitForXPath('//*[@id="Date"]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#Date")
    await page.click('[id=Date]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#Date', date)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#passengersfield")
    try:
        await page.waitForXPath('//*[@id="execSearch"]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#execSearch")
    try:
        await page.waitForXPath('//*[@id="searchResults"]/div/div/div/div',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Timeout')
    try:
        await asyncio.wait([page.waitForXPath('//div/div/span[contains(@class,"pricePrefix")]',{'visible': True, 'timeout': 50000})])
    except Exception:
        logger.error('Timeout')
    time_departure = await page.xpath('//div[contains(@class,"time departure")]')
    time_arrival = await page.xpath('//div[contains(@class,"time arrival")]')
    locations = await page.xpath('//div/span[contains(@class,"station-name")]')
    price = await page.xpath(f'//div/span[contains(text(),"€")]')
    for i in time_departure:
        dep_time_txt = await page.evaluate('(element) => element.textContent', i)
        dep_times.append(dep_time_txt)
    print(dep_times)
    for i in time_arrival:
        arr_time_txt = await page.evaluate('(element) => element.textContent', i)
        arr_times.append(arr_time_txt)
    print(arr_times)
    for i in locations:
        loc_txt = await page.evaluate('(element) => element.textContent', i)
        locs.append(loc_txt)
    arr_loc = locs[::2]
    dep_loc = locs[1::2]
    print(arr_loc)
    print(dep_loc)
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[3:]
    prices = [x.strip('\xa0') for x in prices]
    print(prices)


asyncio.get_event_loop().run_until_complete(get_info('Andorra la Vella, Andorra', 'Barcelona, Spain','17.02.2021'))



