from pyppeteer import launch
import asyncio
# import logging


async def get_info(origin, destination,time):

    # logger = logging.getLogger('Scrape App')
    # logger.setLevel(logging.DEBUG)
    # fh = logging.FileHandler('./scrape.log')
    # fh.setLevel(logging.DEBUG)
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s,%(message)s')
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.addHandler(ch)

    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.vy.no/en/', timeout=50000)

    await page.type('[id=departure-place-input]', origin)
    await page.waitForXPath('//*[@id="departure-place-inputAutocompleteList"]/li/button',{'visible': True, 'timeout': 50000})
    await page.click('[id=departure-place-inputAutocompleteList]', {'clickCount': 1})
    await page.type('[id=arrival-place-input]', destination)
    await page.waitForXPath('//*[@id="arrival-place-inputAutocompleteList"]/li[2]/button',{'visible': True, 'timeout': 50000})
    await page.click('[id=arrival-place-inputAutocompleteList]', {'clickCount': 1})
    await page.waitForXPath('//*[@id="timepicker--departure"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=timepicker--departure]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=timepicker--departure]', time)
    await page.waitForXPath('//*[@id="new-travel-planner"]',{'visible': True, 'timeout': 50000})
    #below the click fuction does not click //*[@id="new-travel-planner"]/div[2]/span[2]/button
    # btn = await page.waitForSelector('//button[contains(text(), "Find journey")]')
    # await page.click(btn,{'clickCount': 1})
    await page.keyboard.press('Enter')
    await asyncio.wait([page.waitForXPath('//div/span[contains(@class,"_6a6a0e2b")]',{'visible': True, 'timeout': 90000})])
    # await asyncio.wait([page.waitForXPath('//div[contains(@class,"_c11ce670")]',{'visible': True, 'timeout': 90000})])
    # await page.waitForXPath("//*[@id='buy-button-mobile-9e7156bc-f9a6-4196-aa1c-d7fc6b8c093c']", {'visible': True, 'timeout': 90000})

    trip_tim = await page.xpath('//div/span[contains(@class,"_6a6a0e2b")]')
    price = await page.xpath('//div/button/span[contains(@class ,"_8c3d6635")]')
    trips = []
    arrival_time = []
    departure_time = []
    prices = []

    for j in price:
        price_txt = await page.evaluate('(element) => element.textContent', j)
        prices.append(price_txt)

    prices = prices[::2]
    print(prices)

    for i in trip_tim:
        trip_tim_txt = await page.evaluate('(element) => element.textContent', i)
        trips.append(trip_tim_txt)
        trips = [x.replace('\n', '') for x in trips]
        trips = list(dict.fromkeys(trips))

    new_dep_tim = [x[0:5] for x in trips]
    new_arr_tim = [x[8:] for x in trips]
    for a in new_arr_tim:
        arrival_time.append(a)
    for d in new_dep_tim:
        departure_time.append(d)
    print(departure_time)
    print(arrival_time)


asyncio.get_event_loop().run_until_complete(get_info('Allkopi Parkveien', 'Fridtjof Nansens vei','19:00'))

