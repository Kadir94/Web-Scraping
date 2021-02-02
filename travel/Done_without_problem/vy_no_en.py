from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys

async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    times = []
    prices = []
    list_dict = []
    dates = date.strftime('%Y.%#m.%#d')
    time = date.strftime('%H:%M')
    await page.goto('https://www.vy.no/en/', timeout=50000)

    await page.type('[id=departure-place-input]', origin)
    await page.waitForXPath('//*[@id="departure-place-inputAutocompleteList"]/li/button',{'visible': True, 'timeout': 50000})
    try:
        await page.click('[id=departure-place-inputAutocompleteList]', {'clickCount': 1})
    except Exception:
        logger.error('Invalid Origin Name')

    await page.type('[id=arrival-place-input]', destination)
    await page.waitForXPath('//*[@id="arrival-place-inputAutocompleteList"]/li/button',{'visible': True, 'timeout': 50000})
    try:
        await page.click('[id=arrival-place-inputAutocompleteList]', {'clickCount': 1})
    except Exception:
        logger.error('Invalid Destination Name')

    required_date = await page.waitForXPath('//*[@id="datepicker--from"]',{'visible': True, 'timeout': 50000})
    await required_date.click()
    months = ['month','January','February','March','April','May','June','July','August','September','October','November','December']
    day = dates.split('.')[2]
    month = dates.split('.')[1]
    month_wanted = None
    day_wanted = None
    while True:
        try:
            month_wanted = await page.waitForXPath(f'//div/div/span[contains(text(),"{months[int(month)]}")]',timeout=1000)
        except Exception:
            logger.info('Cannot pick the month')
        if month_wanted:
            break
        else:
            try:
                next_button = await page.waitForXPath('//div/button[@class="_abec2f5c"]')
                await next_button.click()
            except Exception:
                print("lol3")
                logger.info('Cannot click the next month button')
    table = await page.waitForXPath('//div/table[@class="_4dd5d956"]',{'visible': True, 'timeout': 70000})
    while True:
        try:
            day_wanted = await table.xpath(f'//td/button[contains(text(),"{day}")]')
        except Exception:
            print("lol")
        if day_wanted:
            await day_wanted[0].click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div/button[@class="_abec2f5c"]')
                await next_button.click()
            except Exception:
                logger.info('Cannot click the next month button')

    await page.waitForXPath('//*[@id="timepicker--departure"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=timepicker--departure]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=timepicker--departure]', time)
    await page.keyboard.press('Enter')

    await page.waitForXPath('//*[@id="new-travel-planner"]',{'visible': True, 'timeout': 50000})
    await page.xpath('//div[@id="new-travel-planner"]')
    try:
        await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#new-travel-planner > div._f2938568 > span._6cc748f6 > button")
    except Exception:
        logger.error('Can not find the Search Button')

    try:
        await page.waitForXPath('//li/div[@class="_3c22a6bd"]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Can not find the Travel Info')

    time_info = await page.xpath('//div/span[contains(@class ,"_6a6a0e2b")]')
    for t in time_info:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        times.append(time_txt)
    dep_times = [x[0:6] for x in times]
    arr_times = [x[8:13] for x in times]
    price = await page.xpath('//div/button/span[contains(@class ,"_8c3d6635")]')
    for j in price:
        price_txt = await page.evaluate('(element) => element.textContent', j)
        prices.append(price_txt)
    for d, a, p in zip(dep_times, arr_times, prices):
        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': dates,
            'DepartureTime': d,
            'ArrivalTime': a,
            'Price': p.strip('Buy from')
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data

# asyncio.get_event_loop().run_until_complete(get_info('Allkopi Parkveien', 'Fridtjof Nansens vei',datetime.datetime.today(),logger=None))

