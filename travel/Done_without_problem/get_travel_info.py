from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):
    prices = []
    dep_info = []
    arr_times = []
    list_dict = []
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%d.%m.%Y')
    try:
        await page.goto('https://www.fluege.de/', timeout=50000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#flightForm > div.flight-type-wrapper > div.js_flight-type.flight-type.oneway > label")
    await page.type('[id=f0-dep-location-]', origin)
    await page.type('[id=f0-arr-location-]', destination)
    await page.click('[id=f0Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f0Date]', date_)
    await page.keyboard.press('Enter')
    question_1 = None
    try:
        question_1 = await page.waitForXPath("//*[@id='f0DepSection']", {'visible': True, 'timeout': 7000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="f0DepSection"] ..."{ENDE}')
    if question_1:
        first_link_dep = await question_1.xpath(".//*[@class='js_select-airport']")
        try:
            await first_link_dep[0].click()
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=.//*[@class="js_select-airport"] ..."{ENDE}')
    question_2 = None
    try:
        question_2 = await page.waitForXPath('//*[@id="f0ArrSection"]', {'visible': True, 'timeout': 7000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="f0ArrSection"] ..."{ENDE}')

    if question_2:
        first_link_arr = await question_2.xpath('.//*[@class="js_select-airport"]')
        try:
            await first_link_arr[0].click()
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=.//*[@class="js_select-airport"] ..."{ENDE}')
    try:
        await page.waitForXPath('//div[contains(@class,"column-price-flag")]', timeout=90000)
        await page.waitForXPath('//div/span[contains(@class,"city highlight")]', timeout=90000)
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
    price = await page.xpath('//div[contains(@class,"column-price-flag")]')
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
    departure = await page.xpath('//div[contains(@class,"location-departure")]')
    arrival = await page.xpath('//div[contains(@class,"location-arrival")]')
    for d in departure:
        departure_txt = await page.evaluate('(element) => element.textContent', d)
        dep_info.append(departure_txt)
        dep_info = [x.replace('\n', '') for x in dep_info]
    new_dep_tim = [x[0:5] for x in dep_info]
    for a in arrival:
        arrival_txt = await page.evaluate('(element) => element.textContent', a)
        arr_times.append(arrival_txt)
        arr_times = [x.replace('\n', '') for x in arr_times]

    new_arr_tim = [x[0:5] for x in arr_times]
    for d,a,p in zip(new_dep_tim,new_arr_tim,prices):
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


# asyncio.get_event_loop().run_until_complete(get_info('Berlin', 'Paris', datetime.datetime.today(),logger=None))
