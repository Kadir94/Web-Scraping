from datetime import datetime

import asyncio
from pyppeteer import launch
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict


async def get_info(page, country_id, origin, origin_id, destination, destination_id, total_size, hash_id, order, date,
                   logger: Logger) -> Dict:
    """
    The Scraper which built on Pyppeteer. Finds info considering the given params.
    :param page: Page object used to navigate in Tab of Browser.
    :param origin: Starting point for scraping.
    :param destination: Endpoint for scraping.
    :param date: The date to scrape the info for.
    :param logger: Page level logger.
    :param country_id: ID of country being scraped. (Will be used to fetch the country form DB).
    :param origin_id: ID of origin city. Will be used to fetch the city object.
    :param destination_id: ID of destination city.
    :param order: Order of the split (partial) data. (Used in ordering the total data before producing).
    :param hash_id: Hash ID to determine to which data (the original whole data) this split belongs to.
    :param total_size: How many splits we need to collect before being sure that whole data is actually processed.
    :return: Dict
    """
    dep_infos = []
    prices = []
    list_dict = []
    car = "A4 Avant (2008 +)"
    # date_ = datetime.fromisoformat(date)
    # date_ = date_.strftime('%Y-%-m-%-d')
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    try:
        await page.goto('https://www.directferries.co.uk/', timeout=90000)
    except (TimeoutError, PageError):
        # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
        print("22222")

    try:
        await page.waitForXPath('//*[@id="deal_finder1"]', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="dealP"]"{ENDE}')
        print("22222")

    try:
        one_way = await page.waitForXPath('//div/section/label[@for="journey_oneway"]',{'visible': True, 'timeout':10000})
        await one_way.click()
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=[@class="radio-inline oneway"] ..."{ENDE}')
        print("cant click oneway")

    try:
        await page.waitForXPath('//*[@id="route_outbound"]', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="route_outbound"] ..."{ENDE}')
        print("111")

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#route_outbound")
    await page.type('#route_outbound', origin + ' - ' + destination)
    await page.keyboard.press('ArrowUp')
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")]',
                                {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")] ..."{ENDE}')
        print('1414')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_timing.timing_outbound.hide_until_times")
    date_wanted = None
    max_ = 0
    while True:
        if max_ <= 12:
            try:
                date_wanted = await page.waitForXPath(f'//div[@data-full="{date}"]', {'visible': True, 'timeout': 500})
            except TimeoutError:
                # logger.error(
                #     f'{DARK_PURPLE} {date_} Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@data-full=..."{ENDE}')
                print('1313')
            if date_wanted:
                await date_wanted.click()
                break
            else:
                try:
                    next_button = await page.waitForXPath('//div[@aria-label="Next Month"]',
                                                          {'visible': True, 'timeout': 500})
                    await next_button.click()
                    max_ += 1
                except TimeoutError:
                    # logger.error(
                    #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@aria-label="Next Month"]..."{ENDE}')
                    print('1212')
        else:
            print("haha")
            break
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
        print("1221")

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
        print("1717")

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/section/section/ul/li/a',
                                {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/section/ul/li/a"{ENDE}')
        print("111")

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_info.hide_until_summary > section.trip_outbound.both_ways > ul:nth-child(4) > li:nth-child(3) > a")

    try:
        no_vehicle = await page.waitForXPath('//div/label[@for="vehicle_type_0"]', {'visible': True, 'timeout': 10000})
        await no_vehicle.click()
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"//div/label[contains(text(),"Auto")]"{ENDE}')
        print("no vehicle")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/a',
                                {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/section/ul/li/a"{ENDE}')
        print("111")
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > a")
    try:
        currency = await page.waitForXPath('//*[@id="currency_popup"]/div[2]/section/ol/li[2]',
                                {'visible': True, 'timeout': 10000})
        await currency.click()
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/section/ul/li/a"{ENDE}')
        print("111")
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#currency_popup > footer > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        # logger.error(
        #     f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')
        print('no search')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")

    try:
        await page.waitForXPath('//div[@class="ab-2062-flex"]', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        print("22222")
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
    dep_info = await page.xpath('//div/div[contains(@class,"ab-2062-col-1")]')
    price = await page.xpath('//div/div/b')
    for d in dep_info:
        dep_info_txt = await page.evaluate('(element) => element.textContent', d)
        dep_infos.append(dep_info_txt)
        dep_infos = [x.replace('\n', '') for x in dep_infos]
        dep_infos = [x.strip(' ') for x in
                     dep_infos]
    del dep_infos[1::3]
    times = [x[75:90] for x in dep_infos]
    dep_time = times[0::2]
    arr_time = times[1::2]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[7::4]
    for d, a, p in zip(dep_time, arr_time, prices):
        list_dict.append({
            'date': date,
            'departure_time': d.strip('       '),
            'arrival_time': a.strip('        '),
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


asyncio.get_event_loop().run_until_complete(get_info(page=None,country_id=None,origin='Douglas',origin_id=None, destination='Dublin',destination_id=None,total_size=None,hash_id=None,order=None,date='2021-8-15',logger=Logger))