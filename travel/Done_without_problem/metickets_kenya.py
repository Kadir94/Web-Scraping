from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
import asyncio
from pyppeteer import launch


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    dep_times = []
    prices = []
    # date_ = datetime.fromisoformat(date)
    # date_ = date.strftime('%m/%d/%Y')
    list_dict = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    try:
        await page.goto('https://metickets.krc.co.ke/', timeout=90000)
    except (TimeoutError, PageError):
        print('Timeout')
        # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="train_type"]',{'visible': True, 'timeout': 50000})
        await page.click('[id=train_type]',{'clickCount': 1})
    except TimeoutError:
        print('Timeout')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="train_type"] ..."{ENDE}')
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    try:
        terminal = await page.waitForXPath('//div/select[@name="terminal_id"]', timeout=50000)
        await terminal.click()
        await terminal.type(origin)
        await page.keyboard.press('Enter')
    except TimeoutError:
        print('Timeout')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/select[@name="terminal_id"] ..."{ENDE}')
    try:
        dest = await page.waitForXPath('//div/select[@name="destination_id"]',timeout=50000)
        await dest.click()
        await dest.type(destination)
        await page.keyboard.press('Enter')
    except TimeoutError:
        print('Timeout1')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="destination_references"] ..."{ENDE}')
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#destination_references")
    # await page.type('#destination_references', destination)
    # await asyncio.sleep(1)
    # await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//*[@id="dateInput"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print('Timeout2')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="dateInput"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#dateInput")
    await page.type('#dateInput', date)
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div/select[contains(@class,"form-control depature_time")]', timeout=50000)
    except TimeoutError:
        print('Timeout3')
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/select[contains(@class,"form-control depature_time")] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#depature_time")
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div[@class="tab-content"]',{'visible': True, 'timeout': 50000})
    except TimeoutError:
        print('Timeout4')
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
    times = await page.xpath('//div/small/span[contains(@class,"span")]')
    price = await page.xpath('//div[2]/div[1]/dl/dd[contains(text(),"KSH")]')
    for i in times:
        time_txt = await page.evaluate('(element) => element.textContent', i)
        dep_times.append(time_txt)
    departure_times = dep_times[::2]
    arrival_times = dep_times[1::1]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    for d, a, p in zip(departure_times,arrival_times, prices):
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
    print(total_data)

asyncio.get_event_loop().run_until_complete(get_info(page=None,country_id=None,origin='Nairobi Terminus',origin_id=None, destination='Mombasa Terminus',destination_id=None,total_size=None,hash_id=None,order=None,date='02/15/2021',logger=Logger))

