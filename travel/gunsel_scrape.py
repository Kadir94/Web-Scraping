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

    dep_times = []
    prices = []
    locs = []
    dct = {'DepartureLoc': [], 'ArrivalLoc': [],'DepartureTime': [], 'ArrivalTime': [],  'price': []}
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://lines.gunsel.ua/en', timeout=90000)
    await page.waitForXPath('//*[@id="select2-fromStation-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-fromStation-container]',{'clickCount': 1})
    await page.type('[id=inputFromStation]', origin)
    try:
        await page.keyboard.press('Enter')
    except Exception:
        logger.error('Invalid Origin City Name')
    await page.waitForXPath(' //*[@id="select2-toStation-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-toStation-container]',{'clickCount': 1})
    await page.type('[id=toStationParent]', destination)
    try:
        await page.keyboard.press('Enter')
    except Exception:
        logger.error('Invalid Destination City Name')

    await page.click('[id=travelDate]', {'clickCount': 1})
    await page.waitForXPath('//*[@class="calendar-table"]',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//tr/td[contains(@class,"available")]',{'visible': True, 'timeout': 50000})
    # chosen_date = await page.xpath('//tr/td[contains(@class,"available")]'
    # chosen_date = await page.evaluate('(td class="available" data-title="r3c4">25</td) => element.textContent',date)
    # await page.click(chosen_date[0], {'clickCount': 1})
    # await chosen_date[0].click()  <td class="available" data-title="r3c4">25</td>
    await asyncio.wait([page.waitForXPath('//tr/td[contains(@class,"date-time")]',{'visible': True, 'timeout': 90000})])

    time = await page.xpath('//tr/td[contains(@class,"date-time")]')
    price = await page.xpath('//div[contains(@class,"price-column w-100")]')
    locations = await page.xpath('//td/small[contains(@class, "station-address")]')

    for t in time:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        dep_times.append(time_txt)
    departure_times = dep_times[::2]
    arrival_times = dep_times[1::2]

    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    new_prices = [x[0:8] for x in prices]

    for l in locations:
        loc_txt = await page.evaluate('(element) => element.textContent', l)
        locs.append(loc_txt)
        locs[:] = [i for i in locs if i != '  ']
    locs = locs[12:]
    departure_locs = locs[::2]
    arrival_locs = locs[1::2]

    for n in departure_locs:
       dct['DepartureLoc'].append(n)
    for k in arrival_locs:
       dct['ArrivalLoc'].append(k)
    for v in departure_times:
       dct['DepartureTime'].append(v)
    for m in arrival_times:
       dct['ArrivalTime'].append(m)
    for p in new_prices:
       dct['price'].append(p)

    print(dct)

asyncio.get_event_loop().run_until_complete(get_info('Odessa', 'Kyiv','25'))
