from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    list_dict = []
    date = date.strftime('%Y-%m-%d')
    await page.goto('https://andestransit.com/', timeout=90000)
    alerts = None
    try:
        alerts = await page.waitForXPath('//div/button[contains(text(),"Got it!")]',{'visible': True, 'timeout': 5000})
    except Exception:
       logger.info('No Alerts')
    if alerts:
        await alerts.click()
    else:
        pass
    await page.waitForXPath('//*[@id="search-origin-public"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-origin-public")
    await page.type('[id=search-origin-public]', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath(f'//div[contains(text(),"{origin}")]',{'visible': True, 'timeout': 5000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_1:
        try:
            await suggestion_1.click()
        except Exception:
            logger.info('Couldn not find Suggestion')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-destination-public")
    await page.type('[id=search-destination-public]', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath(f'//div[contains(text(),"{destination}")]',{'visible': True, 'timeout': 5000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_2:
        try:
            await suggestion_2.click()
        except Exception:
            logger.info('Couldn not find Suggestion')
    search = await page.waitForXPath('//div/input[@value="Go"]',{'visible':True, 'timeout':50000})
    await search.click()
    await page.waitForXPath('//section/div[@id="calendar"]',visible=True, timeout=50000)
    date_wanted = None
    while True:
        try:
            date_wanted = await page.waitForXPath(f'//tr/td[@data-date="{date}"]',timeout=10000)
        except Exception:
            logger.info('Cannot pick the date')
        if date_wanted:
            await date_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div/button[@class="fc-next-button fc-button fc-state-default fc-corner-left fc-corner-right"]')
                await next_button.click()
            except Exception:
                logger.info('Cannot click the next month button')
    await asyncio.wait([page.waitForXPath('//table[contains(@class,"best-bets")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.DepartureTime")]')
    arr_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.ArrivalTime")]')
    price = await page.xpath('//td/a/span[contains(@data-bind,"text : $data.TotalPrevPrice()")]')
    for (d,a,p) in zip(dep_time,arr_time,price):
        dep_time_txt = await page.evaluate('(element) => element.textContent', d)
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        price_txt = await page.evaluate('(element) => element.textContent', p)

        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': date,
            'DepartureTime': dep_time_txt,
            'ArrivalTime': arr_time_txt,
            'Price': price_txt.strip()+" USD"
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data


asyncio.get_event_loop().run_until_complete(get_info('Cali (Airport)','BOGOTA (COLOMBIA)',datetime.datetime.today(),logger=None))



