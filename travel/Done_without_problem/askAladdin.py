from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    info = []
    trip1 = None
    trip2 = None
    trip3 = None
    trip4 = None
    list_dict = []
    date = None
    try:
        await page.goto('https://ask-aladdin.com/egypt-transport-system/bus-timetables/', timeout=200000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")] ..."{ENDE}')
    while True:
        try:
            trip1 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+destination}")]',timeout=1000)
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
        if trip1:
            await trip1.click()
            break
        elif trip1 is None:
            try:
                trip2 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{"From"+" "+origin+" "+"to"+" "+destination}")]',timeout=1000)
            except TimeoutError:
                logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
        if trip2:
            await trip2.click()
            break
        elif trip2 is None:
            try:
                trip3 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+"the"+" "+destination}")]',timeout=1000)
            except Exception:
                logger.error('Timeout')
        if trip3:
            await trip3.click()
            break
        elif trip3 is None:
            try:
                trip4 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+"/"+destination}")]',timeout=1000)
            except TimeoutError:
                logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/h4/a[contains(text() ..."{ENDE}')
        if trip4:
            try:
                await trip4.click()
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
            break
    chosen = await page.xpath('//div/div[@aria-expanded="true"]/div/div/div/table/tbody/tr/td')
    for i in chosen:
        name = await page.evaluate('(element) => element.textContent', i)
        info.append(name)
    company = info[3::3]
    dep_time = info[4::3]
    price = info[5::3]

    for (c,d,p) in zip(company,dep_time,price):
        list_dict.append({
            'Date': date,
            'DepartureTime': d,
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
    return total_data


# asyncio.get_event_loop().run_until_complete(get_info('Cairo', 'Alexandria',date=None,logger=None))

