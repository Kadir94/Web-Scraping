from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page, country_id, origin, origin_id, destination, destination_id, total_size, hash_id, order, date,
                   logger: Logger) -> Dict:
    dep_infos = []
    prices = []
    list_dict = []
    car = "A4 Avant (2008 +)"
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y-%#m-%#d')
    try:
        await page.goto('https://www.directferries.de/', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/section/label', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/label ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_type > label:nth-child(2)")
    try:
        await page.waitForXPath('//*[@id="route_outbound"]', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="route_outbound"] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#route_outbound")
    await page.type('#route_outbound', origin)
    await page.type('#route_outbound', destination)
    try:
        await page.waitForXPath('//*[@id="journey_route_parent"]/div/aside/ul/li', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="journey_route_parent"]/div/aside/ul/li ..."{ENDE}')
    try:
        route = await page.waitForXPath(f'//ul/li[@data-routename="{origin + destination}"]',
                                        {'visible': True, 'timeout': 50000})
        await route.click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//ul/li[@data-routename= ..."{ENDE}')
    try:
        await page.waitForXPath('//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")]',
                                {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")] ..."{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_timing.timing_outbound.hide_until_times")
    date_wanted = None
    while True:
        try:
            date_wanted = await page.waitForXPath(f'//div[@data-full="{date_}"]', timeout=1000)
        except TimeoutError:
            logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@data-full=..."{ENDE}')
        if date_wanted:
            await date_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div[@aria-label="Next Month"]')
                await next_button.click()
            except TimeoutError:
                logger.error(
                    f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@aria-label="Next Month"]..."{ENDE}')
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/section/section/ul/li/a',
                                {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/section/ul/li/a"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_info.hide_until_summary > section.trip_outbound.both_ways > ul:nth-child(4) > li:nth-child(3) > a")
    try:
        await page.waitForXPath('//div[@id="vehicle_base"]', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@id="vehicle_base"]"{ENDE}')
    try:
        await page.waitForXPath('//*[@id="vehicle_base"]/div/label', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="vehicle_base"]/div/label"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#vehicle_base > div.popup_body > label:nth-child(4)")
    try:
        await page.waitForXPath('//div/fieldset[@class="car_make_fields"]', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[@class="car_make_fields"]"{ENDE}')
    try:
        car_choice = await page.waitForXPath('//div/fieldset[@class="car_make_fields"]',
                                             {'visible': True, 'timeout': 50000})
        car_options = await car_choice.xpath('//label/input[@value="32"]')
        await car_options[0].click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[@class="car_make_fields"]"{ENDE}')
    try:
        model_choice = await page.waitForXPath('//div/fieldset[contains(@class,"car_model_fields")]',
                                               {'visible': True, 'timeout': 50000})
        model_options = await model_choice.xpath(f'//label[contains(text(),"{car}")]')
        await model_options[0].click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[contains(@class,"car_model_fields")]"{ENDE}')
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/aside/footer/button', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/aside/footer/button"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > aside > footer > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 50000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//div[@class="ab-2062-flex"]', {'visible': True, 'timeout': 50000})
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
    dep_info = await page.xpath('//div/div[contains(@class,"ab-2062-col-1")]')
    price = await page.xpath('//div/div/b')
    for d in dep_info:
        dep_info_txt = await page.evaluate('(element) => element.textContent', d)
        dep_infos.append(dep_info_txt)
        dep_infos = [x.replace('\n', '') for x in dep_infos]
        dep_infos = [x.strip('                                                                        ') for x in
                     dep_infos]
    del dep_infos[1::3]
    times = [x[75:90] for x in dep_infos]
    dep_time = times[0::2]
    arr_time = times[1::2]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[7::5]
    for d, a, p in zip(dep_time, arr_time, prices):
        list_dict.append({
            'Date': date,
            'DepartureTime': d.strip('       '),
            'ArrivalTime': a.strip('        '),
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



