from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    departure_time = []
    prices = []
    list_dict = []
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y.%#m.%#d')
    try:
        await page.goto('https://www.intercity.co.nz/', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_from"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="BookTravelForm_getBookTravelForm_from"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_from")
    await page.type('[id=BookTravelForm_getBookTravelForm_from]', origin)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_to")
    await page.keyboard.press('Backspace')
    await page.type('[id=BookTravelForm_getBookTravelForm_to]', destination)
    await page.keyboard.press('Enter')
    choice = None
    try:
        choice = await page.waitForXPath('//div/ul[@class="autocomplete-list"]', {'visible': True, 'timeout': 7000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not Find {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/ul[@class="autocomplete-list"] ..."{ENDE}')
    if choice:
        first_link_dep = await choice.xpath("//div/ul/li[@class='autocomplete-suggestion']")
        try:
            await first_link_dep[0].click()
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/ul/li[@class="autocomplete-suggestion"] ..."{ENDE}')
    try:
        await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_date"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="BookTravelForm_getBookTravelForm_date"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#BookTravelForm_getBookTravelForm_date")
    try:
        await page.waitForXPath('//div/div[contains(@class,"month-wrapper")]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/div[contains(@class,"month-wrapper")] ..."{ENDE}')
    months = ['month','january','february','march','april','may','june','july','august','september','october','november','december']
    day = date_.split('.')[2]
    month = date_.split('.')[1]
    year = date_.split('.')[0]
    month_wanted = None
    day_wanted = None
    while True:
        try:
            month_wanted = await page.waitForXPath(f'//div/table/thead/tr/th[contains(text(),"{months[int(month)]+" "+year}")]',timeout=1000)
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/table/thead/tr/th[contains(text() ..."{ENDE}')
        if month_wanted:
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except TimeoutError:
                logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//th/span[@class="next"] ..."{ENDE}')
    while True:
        try:
            day_wanted = await page.waitForXPath(f'//table/tbody/tr/td/div[contains(text(),"{day}")]',{'visible': True, 'timeout': 7000})
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//table/tbody/tr/td/div[contains(text() ..."{ENDE}')
        if day_wanted:
            await day_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except TimeoutError:
                logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//th/span[@class="next"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_action_submit")
    try:
        await page.waitForXPath('//ul/li[contains(@class,"fare-item js-fare-item")]',{'visible': True, 'timeout': 90000})
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
    try:
        await page.waitForXPath('//div[contains(@class,"summary-price")]',{'visible': True, 'timeout': 90000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[contains(@class,"summary-price")] ..."{ENDE}')

    dep_time = await page.xpath('//div/div[contains(@class,"fare-time")]')
    price = await page.xpath('//div/div[contains(@class,"price")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
        departure_time = [x.replace('\n', '') for x in departure_time]
        departure_time = [x.strip('                  ') for x in departure_time]
    times = departure_time[1::2]
    arrival_tim = times[1::2]
    departure_tim = times[::2]
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
        prices = [x.replace('From', '') for x in prices]
        prices = [x.replace(' ', '') for x in prices]
        prices = [s.strip() for s in prices]
    prices = prices[::2]
    prices = prices[1::2]
    for d, a, p in zip(departure_tim, arrival_tim, prices):
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



