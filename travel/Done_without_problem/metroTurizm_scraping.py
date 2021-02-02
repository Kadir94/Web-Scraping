from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    times = []
    prices = []
    date = date.strftime('%d.%m.%Y')
    list_dict = []
    await page.goto('https://www.metroturizm.com.tr/en/', timeout=90000)
    await page.waitForXPath('//*[@id="Metro"]/div/div/div/div',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#Metro > div.row > div:nth-child(2) > div > div > button")
    await page.waitForXPath('//*[@id="Metro"]/div/div/div/div/div',{'visible': True, 'timeout': 50000})
    await page.type('[id=Metro]', origin)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #Metro > div.row > div:nth-child(4) > div > div > button")
    await page.type('[id=Metro]', destination)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="inpSearchJourneyBusBoardingDate"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#inpSearchJourneyBusBoardingDate")
    await page.click('[id=inpSearchJourneyBusBoardingDate]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#inpSearchJourneyBusBoardingDate', date)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#btnIndexSearchJourneys")
    await page.waitForXPath('//div[contains(@class,"journey-item")]',{'visible': True, 'timeout': 90000})
    time_info = await page.xpath('//div/span[contains(@class,"journey-item-hour ng-binding")]')
    price = await page.xpath('//div/span[contains(@class,"price ng-binding")]')
    for t in time_info:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        times.append(time_txt)
        times = [x.replace('\n', '') for x in times]
        times = [x.strip('                  ') for x in times]
    departure_times = times[::2]
    arrival_times = times[1::2]
    string = "TL"
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = ["{}{}".format(i,string) for i in prices]
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

# asyncio.get_event_loop().run_until_complete(get_info('SAMSUN', 'ANKARA',datetime.datetime.today(),logger=None))



