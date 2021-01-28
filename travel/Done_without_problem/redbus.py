from pyppeteer import launch
import asyncio
import logging
import datetime


async def get_info(origin, destination,date,logger):

    departure_time = []
    arrival_time = []
    prices = []
    dict = []
    date = date.strftime('%Y.%#m.%d')
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.redbus.pe/en/', timeout=90000)
    await page.waitForXPath('//*[@id="src"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=src]',{'clickCount': 1})
    await page.type('[id=src]', origin)
    suggestion_1 = None
    try: 
        suggestion_1 = await page.waitForXPath('//div/ul[contains(@class,"autoFill")]',{'visible': True, 'timeout': 50000})
    except Exception:
        # logger.info('No suggestions1')
        print('No suggestions1')
    if suggestion_1:
        try:
            choose = await suggestion_1.xpath('//*[@id="search"]/div/div[1]/div/ul/li')
            await choose[0].click()
        except Exception:
            # logger.error('can not click the suggestion1')
            print('can not click the suggestion1')
    await page.waitForXPath('//*[@id="dest"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=dest]',{'clickCount': 1})
    await page.type('[id=dest]', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//div/ul[contains(@class,"autoFill")]',{'visible': True, 'timeout': 50000})
    except Exception:
        # logger.info('No suggestions2')
        print('No suggestions2')
    if suggestion_2:
        try:
            choose2 = await suggestion_2.xpath('//*[@id="search"]/div/div[2]/div/ul/li')
            await choose2[0].click()
        except Exception:
            # logger.error('can not click the suggestion2')
            print('can not click the suggestion2')
    await page.waitForXPath('//*[@id="onward_cal"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#onward_cal")
    await page.waitForXPath('//*[@id="rb-calendar_onward_cal"]',{'visible': True, 'timeout': 50000})
    months = ['month','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    day = date.split('.')[2]
    month = date.split('.')[1]
    year = date.split('.')[0]
    print(month)
    print(year)
    print(day)
    month_wanted = None
    day_wanted = None
    print(months[int(month)]+year)
    while True:
        try:
            month_wanted = await page.waitForXPath(f'//div/table/tbody/tr/td[contains(text(),"{months[int(month)]+" "+year}")]',timeout=1000)
        except Exception:
            print("lol1")
            # logger.info('Cannot pick the month')
        if month_wanted:
            print("month found")
            break
        else:
            try:
                next_button = await page.waitForXPath('//*[@id="rb-calendar_onward_cal"]/table/tbody/tr[1]/td[3]/button',{'visible': True, 'timeout': 10000})
                await next_button.click()
            except Exception:
                print("lol3")
                # logger.info('Cannot click the next month button')
    while True:
        try:
            day_wanted = await page.waitForXPath(f'//div/table/tbody/tr/td[@class="wd day" and contains(text(),"{day}")]',{'visible': True, 'timeout': 10000})
        except Exception:
            print("lol")
        if day_wanted:
            print('dayFound')
            await day_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//tr/td[@class="next"]')
                await next_button.click()
            except Exception:
                print("lol3")
                # logger.info('Cannot click the next month button')

    await page.click('[id=search_btn]',{'clickCount': 1})

    await asyncio.wait([page.waitForXPath('//div[contains(@class,"clearfix bus-item")]',{'visible': True, 'timeout': 50000})])
    dp_time = await page.xpath('//div[contains(@class,"dp-time")]')
    arr_time = await page.xpath('//div[contains(@class,"bp-time")]')
    price = await page.xpath('//div/div/span[contains(@class,"f-19 f-bold")]')
    for t in dp_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', t)
        departure_time.append(dp_time_txt)
    print(departure_time)
    for a in arr_time:
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_time.append(arr_time_txt)
    print(arrival_time)
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    print(prices)
    for d, a, p in zip(departure_time,arrival_time, prices):
         dict.append({
            'Origin': origin,
            'Destanation': destination,
            'Date': date,
            'DepartureTime': d,
            'ArrivalTime': a,
            'Price': p
         })
    print(dict)
asyncio.get_event_loop().run_until_complete(get_info('Trujillo (All Locations)', 'Lima (Todos)',datetime.datetime.today(),logger=None))


