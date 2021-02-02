from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    dep_times = []
    prices = []
    date = date.strftime('%d/%m/%Y')
    list_dict = []
    await page.goto('https://lines.gunsel.ua/en', timeout=90000)
    await page.waitForXPath('//*[@id="select2-fromStation-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-fromStation-container]',{'clickCount': 1})
    await page.type('[id=inputFromStation]', origin)
    try:
        await page.keyboard.press('Enter')
    except Exception:
        logger.error('Invalid Origin City Name')
    await page.waitForXPath(' //*[@id="select2-toStation-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-toStation-container]',{'clickCount': 1})
    await page.type('[id=toStationParent]', destination)
    try:
        await page.keyboard.press('Enter')
    except Exception:
        logger.error('Invalid Destination City Name')
    await page.waitForXPath('//*[@id="travelDate"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#travelDate")
    await page.click('[id=travelDate]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#travelDate', date)
    search_button = await page.waitForXPath('//div/button[@translate="bus_search"]',{'visible': True, 'timeout': 50000})
    await search_button.click()
    await asyncio.wait([page.waitForXPath('//tr/td[contains(@class,"date-time")]',{'visible': True, 'timeout': 90000})])

    times = await page.xpath('//tr/td[contains(@class,"date-time")]')
    price = await page.xpath('//div[contains(@class,"price-column w-100")]')
    for t in times:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        dep_times.append(time_txt)
    departure_times = dep_times[::2]
    departure_times = [x[0:6] for x in departure_times]
    arrival_times = dep_times[1::2]
    arrival_times = [x[0:6] for x in arrival_times]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    new_prices = [x[0:8] for x in prices]

    for d,a,p in zip(departure_times,arrival_times,new_prices):
        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': date,
            'DepartureTime': d.strip(' '),
            'ArrivalTime': a.strip(' '),
            'Price': p
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data


asyncio.get_event_loop().run_until_complete(get_info('Odessa', 'Kyiv',datetime.datetime.today(),logger=None))

