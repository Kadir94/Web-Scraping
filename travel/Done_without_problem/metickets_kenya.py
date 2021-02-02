from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    dep_times = []
    prices = []
    date = date.strftime('%m/%d/%Y')
    list_dict = []

    await page.goto('https://metickets.krc.co.ke/', timeout=90000)
    await page.waitForXPath('//*[@id="train_type"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=train_type]',{'clickCount': 1})
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    terminal = await page.waitForXPath('//div/select[contains(@class,"form-control terminal_id")]', timeout=50000)
    await terminal.click()
    await terminal.type(origin)

    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="destination_references"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#destination_references")
    await page.type('#destination_references', destination)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="dateInput"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#dateInput")
    await page.type('#dateInput', date)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//div/select[contains(@class,"form-control depature_time")]', timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#depature_time")
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="content"]/div/div/div/div/div/div',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="car-details"]/div/div/div',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="adults"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=adults]',{'clickCount': 1})

    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    times = await page.xpath('//div/small/span[contains(@class,"span")]')
    price = await page.xpath('//span/span/span[contains(@class,"faretotal")]')
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

# asyncio.get_event_loop().run_until_complete(get_info('Mombasa Terminus', 'Voi',datetime.date.today(),logger=None))

