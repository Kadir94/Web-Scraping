from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    departure_time = []
    prices = []
    list_dict = []

    date = date.strftime('%Y.%#m.%#d')
    await page.goto('https://www.intercity.co.nz/', timeout=90000)
    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_from"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_from")

    await page.type('[id=BookTravelForm_getBookTravelForm_from]', origin)
    await page.keyboard.press('Enter')
    await asyncio.sleep(1)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_to")
    await page.keyboard.press('Backspace')
    await page.type('[id=BookTravelForm_getBookTravelForm_to]', destination)
    await page.keyboard.press('Enter')
    choice = None
    try:
        choice = await page.waitForXPath('//div/ul[@class="autocomplete-list"]', {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible questions')
    if choice:
        first_link_dep = await choice.xpath("//div/ul/li[@class='autocomplete-suggestion']")
        try:
            await first_link_dep[0].click()
        except Exception:
            logger.error('Did not work -> Date')

    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_date"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#BookTravelForm_getBookTravelForm_date")
    await page.waitForXPath('//div/div[contains(@class,"month-wrapper")]',{'visible': True, 'timeout': 50000})
    months = ['month','january','february','march','april','may','june','july','august','september','october','november','december']
    day = date.split('.')[2]
    month = date.split('.')[1]
    year = date.split('.')[0]
    month_wanted = None
    day_wanted = None

    while True:
        try:
            month_wanted = await page.waitForXPath(f'//div/table/thead/tr/th[contains(text(),"{months[int(month)]+" "+year}")]',timeout=1000)
        except Exception:
            logger.info('Cannot pick the month')
        if month_wanted:
            print("month found")
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except Exception:
                logger.info('Cannot click the next month button')
    while True:
        try:
            day_wanted = await page.waitForXPath(f'//table/tbody/tr/td/div[contains(text(),"{day}")]',{'visible': True, 'timeout': 7000})
        except Exception:
            logger.info('Cannot find the day')
        if day_wanted:
            await day_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except Exception:
                logger.info('Cannot click the next month button')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_action_submit")
    await asyncio.wait([page.waitForXPath('//ul/li[contains(@class,"fare-item js-fare-item")]',{'visible': True, 'timeout': 90000})])
    await asyncio.wait([page.waitForXPath('//div[contains(@class,"summary-price")]',{'visible': True, 'timeout': 90000})])
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
        prices = [x.replace('                                                                            ', '') for x in prices]
        prices = [s.strip() for s in prices]
    prices = prices[::2]
    prices = prices[1::2]
    for d, a, p in zip(departure_tim, arrival_tim, prices):
        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': date,
            'DepartureTime': d,
            'ArrivalTime': a,
            'Price': p
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data



