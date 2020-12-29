from pyppeteer import launch
import asyncio
import logging


async def get_info(origin, destination,date):

    logger = logging.getLogger('Scrape App')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./scrape.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s,%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    departure_time = []
    prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.intercity.co.nz/', timeout=90000)
    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_from"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_from")
    await page.type('[id=BookTravelForm_getBookTravelForm_from]', origin)

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_to")
    await page.keyboard.press('Backspace')
    await page.type('[id=BookTravelForm_getBookTravelForm_to]', destination)
    # await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm"]/div/div[2]/div[1]/div[2]/div/ul',{'visible': True, 'timeout': 50000})
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''', "  #BookTravelForm_getBookTravelForm > div > div.booking-search-fields > div.row.location-picker.js-location-picker > div:nth-child(2) > div > ul > li")
    await page.keyboard.press('Enter')

    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_date"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "  #BookTravelForm_getBookTravelForm_date")
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
    time = departure_time[1::2]
    arrival_tim = time[1::2]
    departure_tim = time[::2]
    print(departure_tim)
    print(arrival_tim)
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
        prices = [s.strip() for s in prices]
    prices = prices[::2]
    prices = prices[1::2]
    print(prices)

asyncio.get_event_loop().run_until_complete(get_info('Auckland - Central', 'Hamilton - Central','25'))
