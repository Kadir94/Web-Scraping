from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    list_dict = []
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y-%m-%d')
    try:
        await page.goto('https://andestransit.com/', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    alerts = None
    try:
        alerts = await page.waitForXPath('//div/button[contains(text(),"Got it!")]',{'visible': True, 'timeout': 5000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//span[contains(text() ..."{ENDE}')
    if alerts:
        await alerts.click()
    else:
        pass
    try:
        await page.waitForXPath('//*[@id="search-origin-public"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="search-origin-public"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-origin-public")
    await page.type('[id=search-origin-public]', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath(f'//div[contains(text(),"{origin}")]',{'visible': True, 'timeout': 5000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[contains(text() ..."{ENDE}')
    if suggestion_1:
        try:
            await suggestion_1.click()
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[contains(text() ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-destination-public")
    await page.type('[id=search-destination-public]', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath(f'//div[contains(text(),"{destination}")]',{'visible': True, 'timeout': 5000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[contains(text() ..."{ENDE}')
    if suggestion_2:
        try:
            await suggestion_2.click()
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[contains(text() ..."{ENDE}')
    search = None
    try:
        search = await page.waitForXPath('//div/input[@value="Go"]',{'visible':True, 'timeout':50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/input[@value="Go"] ..."{ENDE}')
    if search:
        await search.click()
    try:
        await page.waitForXPath('//section/div[@id="calendar"]',visible=True, timeout=50000)
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//section/div[@id="calendar"] ..."{ENDE}')
    date_wanted = None
    while True:
        try:
            date_wanted = await page.waitForXPath(f'//tr/td[@data-date="{date_}"]',timeout=10000)
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//tr/td[@data-date=..."{ENDE}')
        if date_wanted:
            await date_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div/button[@class="fc-next-button fc-button fc-state-default fc-corner-left fc-corner-right"]')
                await next_button.click()
            except TimeoutError:
                logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/button[@class="fc-next-button fc-button fc-state-default fc-corner-left fc-corner-right"] ..."{ENDE}')
    try:
        await page.waitForXPath('//table[contains(@class,"best-bets")]',{'visible': True, 'timeout': 50000})
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
    dep_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.DepartureTime")]')
    arr_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.ArrivalTime")]')
    price = await page.xpath('//td/a/span[contains(@data-bind,"text : $data.TotalPrevPrice()")]')
    for (d,a,p) in zip(dep_time,arr_time,price):
        dep_time_txt = await page.evaluate('(element) => element.textContent', d)
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        price_txt = await page.evaluate('(element) => element.textContent', p)

        list_dict.append({
            'Date': date,
            'DepartureTime': dep_time_txt,
            'ArrivalTime': arr_time_txt,
            'Price': price_txt.strip()+" USD"
        })
    total_data = {
        'country_id': country_id,
        'origin_id': origin_id,
        'destination_id': destination_id,
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data


# asyncio.get_event_loop().run_until_complete(get_info('Cali (Airport)','BOGOTA (COLOMBIA)',datetime.today(),logger=None))



