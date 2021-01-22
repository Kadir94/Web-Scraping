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
    prices = []
    browser = await launch(headless=False, autoClose=False, width=2400, height=2400)
    page = await browser.newPage()
    await page.goto('https://www.intercity.co.nz/', timeout=90000)
    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_from"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_from")

    await page.type('[id=BookTravelForm_getBookTravelForm_from]', origin)
    await page.keyboard.press('Enter')
    await asyncio.sleep(1)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #BookTravelForm_getBookTravelForm_to")
    await page.keyboard.press('Backspace')
    await page.type('[id=BookTravelForm_getBookTravelForm_to]', destination)
    choice = None
    try:
        choice = await page.waitForXPath('//div/ul[@class="autocomplete-list"]', {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible questions')
    if choice:
        first_link_dep = await choice.xpath("//div/ul/li[@class='autocomplete-suggestion']")
        try:
            await first_link_dep[0].click()
        except Exception:
            logger.error('Did not work -> Date')
    await page.waitForXPath('//*[@id="BookTravelForm_getBookTravelForm_date"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#BookTravelForm_getBookTravelForm_date")
    await page.waitForXPath('//div/div[contains(@class,"month-wrapper")]',{'visible': True, 'timeout': 50000})
    months = ['month','january','february','march','april','may','june','july','august','september','october','november','december']
    day = date.split('.')[2]
    month = date.split('.')[1]
    year = date.split('.')[0]
    print(month)
    print(year)
    print(day)
    month_wanted = None
    day_wanted = None
    print(months[int(month)]+year)
    next_button = await page.waitForXPath('//th/span[@class="next"]')
    await next_button.click()
    while True:
        try:
            month_wanted = await page.waitForXPath(f'//div/table/thead/tr/th[contains(text(),"{months[int(month)]+" "+year}")]',timeout=1000)
        except Exception:
            print("lol1")
            # logger.info('Cannot pick the month')
        if month_wanted:
            print("month found")
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except Exception:
                print("lol3")
                # logger.info('Cannot click the next month button')
    while True:
        try:
            day_wanted = await page.waitForXPath(f'//table/tbody/tr/td/div[contains(text(),"{day}")]',timeout=1000)
        except Exception:
            print("lol")
        if day_wanted:
            await day_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//th/span[@class="next"]')
                await next_button.click()
            except Exception:
                print("lol3")
                logger.info('Cannot click the next month button')
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
        prices = [x.replace('From', '') for x in prices]
        prices = [x.replace('                                                                            ', '') for x in prices]
        prices = [s.strip() for s in prices]
    prices = prices[::2]
    prices = prices[1::2]
    print(prices)

asyncio.get_event_loop().run_until_complete(get_info('Auckland - Central', 'Hamilton - Central','2021.4.22'))
