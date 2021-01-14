from pyppeteer import launch
import asyncio
import logging


async def get_info(origin, destination,date):

    logger = logging.getLogger('Scrape App')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('../scrape.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s,%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    departure_time = []
    arrival_time = []
    prices = []
    dep_loc = []
    arr_loc = []

    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.pv.lv/en/', timeout=90000)
    await page.waitForXPath('//*[@id="from-station"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#from-station")
    await page.type('[id=from-station]', origin)
    await page.waitForXPath('//*[@id="to-station"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#to-station")
    await page.type('[id=to-station]', destination)
    await page.waitForXPath('//*[@id="switch-date-f"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#switch-date-f")
    await page.click('[id=switch-date-f]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#switch-date-f', date)
    await page.keyboard.press('Enter')
    # await page.click('[id=switch-date-f]',{'clickCount': 1})
    await asyncio.wait([page.waitForXPath('//div[contains(@class,"row")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//div/div[contains(@class,"col-3 col-time")]')
    arr_time = await page.xpath('//div/div[contains(@class,"col-4 col-time")]')
    price = await page.xpath('//div/div[contains(@class,"col-6 col-ticket-price")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
    dep_loc.append(departure_time[0])
    del departure_time[0]
    print(dep_loc)
    print(departure_time)

    for a in arr_time:
        ar_time_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_time.append(ar_time_txt)
    arr_loc.append(arrival_time[0])
    del arrival_time[0]
    print(arr_loc)
    print(arrival_time)

    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
        prices = [x.strip('   ') for x in prices]
    del prices[0]
    print(prices)

asyncio.get_event_loop().run_until_complete(get_info('Rīga', 'Jelgava','16.01.2021'))

