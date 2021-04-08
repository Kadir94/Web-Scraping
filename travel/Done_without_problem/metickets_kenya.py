from datetime import datetime
import asyncio
from pyppeteer import launch
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
# from serializers.serializer import Response, ResponseItem
from currency_converter import CurrencyConverter


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger:Logger) -> Dict:

    dep_times = []
    prices = []
    # date_ = datetime.fromisoformat(date)
    # date_ = date_.strftime('%m/%d/%Y')
    list_dict = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    try:
        await page.goto('https://metickets.krc.co.ke/', timeout=90000)
    except (TimeoutError, PageError):
        # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
        print("111111")
    try:
        await page.waitForXPath('//*[@id="train_type"]', {'visible': True, 'timeout': 1000})
        await page.click('#train_type')
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="train_type"] ..."{ENDE}')
        print('train type')
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

    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    try:
        terminal = await page.waitForXPath('//div/select[@name="terminal_id"]', timeout=1000)
        await terminal.click()
        await terminal.type(origin)
        await page.keyboard.press('Enter')
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/select[@name="terminal_id"] ..."{ENDE}')
        print("22222")
    try:
        dest = await page.waitForXPath('//div/select[@name="destination_id"]',timeout=1000)
        await dest.click()
        await dest.type(destination)
        await page.keyboard.press('Enter')
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="destination_references"] ..."{ENDE}')
        print("22222")
    try:
        await page.waitForXPath('//*[@id="dateInput"]',{'visible': True, 'timeout': 1000})
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="dateInput"] ..."{ENDE}')
        print("22222")
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#dateInput")
    await page.type('#dateInput', date)
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div/select[contains(@class,"form-control depature_time")]', timeout=1000)
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/select[contains(@class,"form-control depature_time")] ..."{ENDE}')
        print("22222")
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#depature_time")
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div[@class="tab-content"]',{'visible': True, 'timeout': 5000})
    except TimeoutError:
        # logger.error(f'{DARK_PURPLE} No {ENDE}{INBOX}{LIGHT_BLUE}"FINAL RESULTS"{ENDE}')
        print('no response')
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
    converter = CurrencyConverter()
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        price_txt = float(price_txt.strip().replace('KSH', ' '))
        price_txt = round(converter.convert(price_txt, 'JPY', 'EUR'), 2)
        prices.append(price_txt)
    for departure, arrival, prce in zip(departure_times,arrival_times, prices):
        list_dict.append({
            'Date': date,
            'DepartureTime': departure,
            'ArrivalTime': arrival,
            'Price': prce
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


asyncio.get_event_loop().run_until_complete(get_info(page=None,country_id=None,origin='Nairobi',origin_id=None, destination='Mombasa',
                                                     destination_id=None,total_size=None,hash_id=None,order=None,date='03/23/2021',logger=Logger))