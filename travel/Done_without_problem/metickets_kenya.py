from pyppeteer import launch
import asyncio
import logging
import datetime


async def get_info(origin, destination,date,logger):

    dep_times = []
    info = []
    prices = []
    date = date.strftime('%m/%d/%Y')
    dict = []

    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://metickets.krc.co.ke/', timeout=90000)
    await page.waitForXPath('//*[@id="train_type"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=train_type]',{'clickCount': 1})
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    await page.waitForXPath('//div/select[contains(@class,"form-control terminal_id")]', timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#content > div > div > div > form > div > div:nth-child(3) > div > div > select")
    await page.type('#content > div > div > div > form > div > div:nth-child(3) > div > div > select', origin)

    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="destination_references"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#destination_references")
    await page.type('#destination_references', destination)
    await asyncio.sleep(2)
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
         dict.append({
            'Origin': origin,
            'Destanation': destination,
            'Date': date,
            'DepartureTime': d,
            'ArrivalTime': a,
            'Price': p
         })
    print(dict)
asyncio.get_event_loop().run_until_complete(get_info('Mombasa Terminus', 'Voi',datetime.date.today(),logger=None))

