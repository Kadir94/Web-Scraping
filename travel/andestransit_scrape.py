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
    arrival_time = []
    prices = []
    location = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://andestransit.com/', timeout=90000)
    await page.waitForXPath('//*[@id="search-origin-public"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-origin-public")
    await page.type('[id=search-origin-public]', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath('//html/body/div[4]/div[1][contains(@class,"autocomplete-suggestion")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "body > div:nth-child(14) > div:nth-child(1)")
        except Exception:
             logger.info('Couldn not find Suggestion')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-destination-public")
    await page.type('[id=search-destination-public]', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//html/body/div[7]/div[1][contains(@class,"autocomplete-suggestion")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "body > div:nth-child(17) > div:nth-child(1)")
        except Exception:
             logger.info('Couldn not find Suggestion')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #searchForm-public > div:nth-child(3) > input")

    # await page.waitForXPath('//div/div[contains(@class,"fc-bg")]',{'visible': True, 'timeout': 50000})
    # await asyncio.sleep(5)
    # await page.waitForXPath('//tr/td[contains(@class,"fc-event-container")]',{'visible': True, 'timeout': 50000})
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#calendar > div.fc-view-container > div > table > tbody > tr > td > div > div > div:nth-child(5) > div.fc-bg > table > tbody > tr > td.fc-day.fc-widget-content.fc-sat.fc-other-month.fc-future.whitebg.has-ticket.green")
    await asyncio.wait([page.waitForXPath('//table[contains(@class,"best-bets")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.DepartureTime")]')
    arr_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.ArrivalTime")]')
    price = await page.xpath('//td/a/span[contains(@data-bind,"text : $data.TotalPrevPrice()")]')

    for t in dep_time:
        dep_time_txt = await page.evaluate('(element) => element.textContent', t)
        departure_time.append(dep_time_txt)
    print(departure_time)
    for t in arr_time:
        arr_time_txt = await page.evaluate('(element) => element.textContent', t)
        arrival_time.append(arr_time_txt)
    print(arrival_time)
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    print(prices)
    await page.xpath('//td/span[contains(@class,"details")]')
    await page.click('[class=details]',{'clickCount': 1})
    locs = await page.xpath('//tr/td[contains(@data-bind,"text: $data.ServiceName")]')
    for l in locs:
        locs_txt = await page.evaluate('(element) => element.textContent', l)
        location.append(locs_txt)
    print(location)
asyncio.get_event_loop().run_until_complete(get_info('BOGOTA', 'Cali (Airport)','25'))

