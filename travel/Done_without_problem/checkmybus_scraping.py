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
    arr_times = []
    dep_times = []
    locs = []
    prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.checkmybus.de/', timeout=90000)
    cookies_frame = page.frames[0]
    await cookies_frame.waitForSelector('#gdpr-c-acpt', {'visible': True})
    await cookies_frame.evaluate('''(selector) => document.querySelector(selector).click()''', "#gdpr-c-acpt")

    await page.waitForXPath('//*[@id="origincityname"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=origincityname]',{'clickCount': 1})
    await page.type('[id=origincityname]', origin)
    departure_choice = await page.waitForXPath('//*[@id="searchform"]/fieldset/div[1]/div/div[3]',{'visible': True, 'timeout': 50000})
    try:
        await departure_choice.click()
    except Exception:
        logger.info('Departure City Is Not Valid')

    await page.click('[id=destinationcityname]',{'clickCount': 1})
    await page.type('[id=destinationcityname]', destination)
    arrival_choice = await page.waitForXPath('//*[@id="searchform"]/fieldset/div[2]/div/div[2]',{'visible': True, 'timeout': 50000})
    try:
        await arrival_choice.click()
    except Exception:
        logger.info('Arrival City Is Not Valid')
    await page.waitForXPath('//*[@id="Date"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#Date")
    await page.click('[id=Date]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#Date', date)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#passengersfield")
    await page.waitForXPath('//*[@id="execSearch"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#execSearch")
    await page.waitForXPath('//*[@id="searchResults"]/div[1]/div/div/div',{'visible': True, 'timeout': 50000})
    await asyncio.wait([page.waitForXPath('//div/div/span[1][contains(@class,"pricePrefix")]',{'visible': True, 'timeout': 50000})])
    time_departure = await page.xpath('//div[contains(@class,"time departure")]')
    time_arrival = await page.xpath('//div[contains(@class,"time arrival")]')
    locations = await page.xpath('//div/span[contains(@class,"station-name")]')
    price = await page.xpath('//div/span[2]')
    for i in time_departure:
        dep_time_txt = await page.evaluate('(element) => element.textContent', i)
        dep_times.append(dep_time_txt)
    print(dep_times)
    for i in time_arrival:
        arr_time_txt = await page.evaluate('(element) => element.textContent', i)
        arr_times.append(arr_time_txt)
    print(arr_times)
    for i in locations:
        loc_txt = await page.evaluate('(element) => element.textContent', i)
        locs.append(loc_txt)
    arr_loc = locs[::2]
    dep_loc = locs[1::2]
    print(arr_loc)
    print(dep_loc)
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[26::3]
    prices = [x.strip('\xa0') for x in prices]
    print(prices)


asyncio.get_event_loop().run_until_complete(get_info('Andorra la Vella, Andorra', 'Barcelona, Spain','17.01.2021'))


