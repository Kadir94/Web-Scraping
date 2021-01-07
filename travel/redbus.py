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
    departure_locs = []
    arrival_time = []
    arrival_loc = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.redbus.pe/', timeout=90000)
    await page.waitForXPath('//*[@id="src"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=src]',{'clickCount': 1})
    await page.type('[id=src]', origin)
    suggestion_1 = None
    try:
        await page.waitForXPath('//*[@id="search"]/div/div[1]/div/ul',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No suggestions1')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #search > div > div.fl.search-box.clearfix > div > ul > li.selected")
        except Exception:
            logger.error('can not click the suggestion1')
    await page.waitForXPath('//*[@id="dest"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=dest',{'clickCount': 1})
    await page.type('[id=dest]', destination)
    suggestion_2 = None
    try:
        await page.waitForXPath('//*[@id="search"]/div/div[2]/div/ul',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No suggestions2')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #search > div > div:nth-child(3) > div > ul > li.selected")
        except Exception:
            logger.error('can not click the suggestion2')
    await page.click('[id=onward_cal]',{'clickCount': 1})
    await page.click('[id=search_btn]',{'clickCount': 1})

    await asyncio.wait([page.waitForXPath('//div[contains(@class,"clearfix bus-item")]',{'visible': True, 'timeout': 50000})])
    dp_time = await page.xpath('//div[contains(@class,"dp-time")]')
    dp_loc = await page.xpath('//div[contains(@class,"dp-loc")]')
    arr_time = await page.xpath('//div[contains(@class,"bp-time")]')
    arr_loc = await page.xpath('//div[contains(@class,"bp-loc")]')
    for t in dp_time:
        dp_time_txt = await page.evaluate('(element) => element.textContent', t)
        departure_time.append(dp_time_txt)
    print(departure_time)
    for l in dp_loc:
        dp_locs_txt = await page.evaluate('(element) => element.textContent', l)
        departure_locs.append(dp_locs_txt)
    print(departure_locs)
    for a in arr_time:
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_time.append(arr_time_txt)
    print(arrival_time)
    for a in arr_loc:
        arr_loc_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_loc.append(arr_loc_txt)
    print(arrival_loc)

asyncio.get_event_loop().run_until_complete(get_info('Terminal Bagua, Bagua', 'Lima (Todos)','25'))
