import re
from datetime import datetime
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
from serializers.serializer import Response, ResponseItem


async def get_info(page, origin, origin_id, destination, destination_id, total_size, hash_id, order, date,
                   logger: Logger) -> Dict:
    """
    The Scraper which built on Pyppeteer. Finds info considering the given params.
    :param page: Page object used to navigate in Tab of Browser.
    :param origin: Starting point for scraping.
    :param destination: Endpoint for scraping.
    :param date: The date to scrape the info for.
    :param logger: Page level logger.
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
    date_ = datetime.fromisoformat(date)
    date_ = date_.strftime('%Y-%-m-%-d')
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/88.0.4324.182 Safari/537.36')
    try:
        await page.goto('https://www.directferries.de/', timeout=90000)
    except (TimeoutError, PageError):
        logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')

    try:
        cookie = await page.waitForXPath('//*[@id="Home"]/div[6]/div/a', {'visible': True, 'timeout': 10000})
        await cookie.click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/label ..."{ENDE}')

    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/section/label', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/label ..."{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_type > label:nth-child(2)")
    try:
        await page.waitForXPath('//*[@id="route_outbound"]', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="route_outbound"] ..."{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#route_outbound")
    await page.type('#route_outbound', origin + ' - ' + destination)
    await page.keyboard.press('ArrowUp')
    await page.keyboard.press('Enter')
    try:
        await page.waitForXPath('//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")]',
                                {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")] ..."{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_timing.timing_outbound.hide_until_times")
    date_wanted = None
    max_ = 0
    while True:
        if max_ != 12:
            try:
                date_wanted = await page.waitForXPath(f'//div[@data-full="{date_}"]', {'visible': True, 'timeout': 500})
            except TimeoutError:
                logger.error(
                    f'{DARK_PURPLE} {date_} Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@data-full=..."{ENDE}')
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
                    logger.error(
                        f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div[@aria-label="Next Month"]..."{ENDE}')
        else:
            return Response(
                origin_id=origin_id,
                destination_id=destination_id,
                data=list_dict,
                total_size=total_size,
                date=date,
                order=order,
                hash_id=hash_id,
                status=400  # Not found
            )
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/section/section/ul/li/a',
                                {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/section/section/ul/li/a"{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > section.journey_info.hide_until_summary > section.trip_outbound.both_ways > ul:nth-child(4) > li:nth-child(3) > a")
    try:
        auto = await page.waitForXPath('//div/label[contains(text(),"Auto")]', {'visible': True, 'timeout': 10000})
        await auto.click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"//div/label[contains(text(),"Auto")]"{ENDE}')

    try:
        await page.waitForXPath('//div/fieldset[@class="car_make_fields"]', {'visible': True, 'timeout': 20000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[@class="car_make_fields"]"{ENDE}')

    try:
        car_choice = await page.waitForXPath('//div/fieldset[@class="car_make_fields"]',
                                             {'visible': True, 'timeout': 10000})
        car_options = await car_choice.xpath('//label/input[@value="32"]')
        await car_options[0].click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[@class="car_make_fields"]"{ENDE}')

    try:
        model_choice = await page.waitForXPath('//div/fieldset[contains(@class,"car_model_fields")]',
                                               {'visible': True, 'timeout': 10000})
        model_options = await model_choice.xpath(f'//label[contains(text(),"{car}")]')
        await model_options[0].click()
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//div/fieldset[contains(@class,"car_model_fields")]"{ENDE}')

    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/aside/footer/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/aside/footer/button"{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > aside > footer > button")
    try:
        await page.waitForXPath('//*[@id="deal_finder1"]/div/button', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(
            f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"XPATH=//*[@id="deal_finder1"]/div/button"{ENDE}')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',
                        "#deal_finder1 > div.deal_finder_wrap > button")
    try:
        await page.waitForXPath('//div[@class="ab-2062-flex"]', {'visible': True, 'timeout': 10000})
    except TimeoutError:
        logger.error(f'{DARK_PURPLE} No {ENDE}{INBOX}{LIGHT_BLUE}"FINAL RESULTS"{ENDE}')
        return Response(
            origin_id=origin_id,
            destination_id=destination_id,
            data=list_dict,
            total_size=total_size,
            date=date,
            order=order,
            hash_id=hash_id,
            status=400  # Not found
        )
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
    prices1 = prices[7::5]
    prices2 = prices[7::4]
    letter = None
    for i in prices1:
        letter = re.search('[a-zA-Z]', i)
    if letter:
        for departure, arrival, price_ in zip(dep_time, arr_time, prices2):
            list_dict.append(ResponseItem(
                date=date,
                departure_time=departure.strip('       '),
                arrival_time=arrival.strip('        '),
                price=price_.replace('€', ' ').replace(',', '.'),
            ))
    else:
        for departure, arrival, price_ in zip(dep_time, arr_time, prices1):
            list_dict.append(ResponseItem(
                date=date,
                departure_time=departure.strip('       '),
                arrival_time=arrival.strip('        '),
                price=price_.replace('€', ' ').replace(',', '.'),
            ))
    return Response(
        origin_id=origin_id,
        destination_id=destination_id,
        data=list_dict,
        total_size=total_size,
        date=date,
        order=order,
        hash_id=hash_id,
        status=200  # Success
    )
