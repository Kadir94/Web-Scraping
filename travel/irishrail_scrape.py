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
    locs = []
    price = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.irishrail.ie/', timeout=90000)
    await page.waitForXPath('//*[@id="HFS_from"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_from")
    await page.type('[id=HFS_from]', origin)
    suggestion_1 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No suggestions1')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except Exception:
            print("lol")
            logger.error('can not click the suggestion1')

    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HFS_to")
    await page.type('[id=HFS_to]', destination)
    suggestion_2 = None
    try:
        await page.waitForXPath("//*[@id='suggestion']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No suggestions2')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#\30 ")
        except Exception:
            print("lol")
            logger.error('can not click the suggestion2')
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#HafasQueryForm > div.f02__cta > button")
    await asyncio.wait([page.waitForXPath('//div[contains(@class,"lyr_itemResults")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//div/div[contains(@class,"lyr_timeRow lyr_plantime")]')
    locations = await page.xpath('//div/div[contains(@class,"lyr_stationRow")]')
    prices = await page.xpath('//div/div/span[contains(@class,"lyr_bigValue")]')
    for i in dep_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', i)
        departure_time.append(dp_time_txt)
    arrival_time = departure_time[1::2]
    departure_time = departure_time[::2]
    print(departure_time)
    print(arrival_time)
    for l in locations:
        locs_txt = await page.evaluate('(element) => element.textContent', l)
        locs.append(locs_txt)
    arrival_loc = locs[1::2]
    departure_loc = locs[::2]
    print(arrival_loc)
    print(departure_loc)
    for p in prices:
        prices_txt = await page.evaluate('(element) => element.textContent', p)
        price.append(prices_txt)
    del price[-1]
    print(price)
asyncio.get_event_loop().run_until_complete(get_info('Dublin Connolly', 'Limerick (Colbert)','25'))