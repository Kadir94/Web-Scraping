from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    departure_time = []
    price = []
    date = date.strftime('%d/%m/%Y')
    list_dict = []
    await page.goto('https://www.irishrail.ie/', timeout=90000)
    await page.waitForXPath('//*[@id="CybotCookiebotDialogBody"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#CybotCookiebotDialogBodyButtonAccept")

    await page.waitForXPath('//*[@id="HFS_from"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_from")
    await page.type('[id=HFS_from]', origin)
    suggestion_1 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No suggestions1')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except Exception:
            logger.error('can not click the suggestion1')
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_to")
    await page.type('[id=HFS_to]', destination)
    suggestion_2 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No suggestions2')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except Exception:
            logger.error('can not click the suggestion2')
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#HFS_date_REQ0")
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("aria-haspopup")''', "#HFS_date_REQ0")
    await page.click('[id=HFS_date_REQ0]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#HFS_date_REQ0', date)

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HafasQueryForm > div.f02__cta > button")
    await asyncio.wait([page.waitForXPath('//div[contains(@class,"lyr_itemResults")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//div/div[contains(@class,"lyr_timeRow lyr_plantime")]')
    prices = await page.xpath('//div/div/span[contains(@class,"lyr_bigValue")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
    arrival_time = departure_time[1::2]
    departure_time = departure_time[::2]
    for p in prices:
        prices_txt = await page.evaluate('(element) => element.textContent', p)
        price.append(prices_txt)
    for d, a, p in zip(departure_time,arrival_time, price):
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

# asyncio.get_event_loop().run_until_complete(get_info('Dublin Connolly', 'Limerick (Colbert)',datetime.datetime.today(),logger=None))
