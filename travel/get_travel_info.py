from pyppeteer import launch
import asyncio
import logging


async def get_info(orgin_city, dest_city, start_date, end_date):
    prices = []
    dep_info = []
    arr_times = []
    date_info = []

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

    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.fluege.de/', timeout=50000)
    await page.type('[id=f0-dep-location-]', orgin_city)
    await page.type('[id=f0-arr-location-]', dest_city)
    await page.click('[id=f0Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f0Date]', start_date)
    await page.click('[id=f1Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f1Date]', end_date)
    await page.keyboard.press('Enter')
    question_1 = None
    try:
        question_1 = await page.waitForXPath("//*[@id='f0DepSection']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible questions')
    if question_1:
        first_link_dep = await question_1.xpath(".//*[@class='js_select-airport']")
        try:
            await first_link_dep[0].click()
        except Exception:
            logger.error('Did not work -> Departure question')
    question_2 = None
    try:
        question_2 = await page.waitForXPath('//*[@id="f0ArrSection"]', {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible Questions')
    if question_2:
        first_link_arr = await question_2.xpath('.//*[@class="js_select-airport"]')
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> Arrival question')

    await asyncio.wait([page.waitForXPath('//div[contains(@class,"column-price-flag")]', timeout=90000)])
    await asyncio.wait([page.waitForXPath('//div/span[contains(@class,"city highlight")]', timeout=90000)])

    price = await page.xpath('//div[contains(@class,"column-price-flag")]')
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]


    departure = await page.xpath('//div[contains(@class,"location-departure")]')
    arrival = await page.xpath('//div[contains(@class,"location-arrival")]')
    date = await page.xpath('//*[contains(@class,"prominent-date")]')

    dct = {'DepartureLoc': [], 'DepartureTime': [], 'ArrivalTime': [], 'ArrivalLoc': [], 'Date': []}
    for d in departure:
        departure_txt = await page.evaluate('(element) => element.textContent', d)
        dep_info.append(departure_txt)
        dep_info = [x.replace('\n', '') for x in dep_info]

    new_dep_tim = [x[0:5] for x in dep_info]
    new_dep_loc = [x[8:] for x in dep_info]

    for v in new_dep_tim:
        dct['DepartureTime'].append(v)
    for l in new_dep_loc:
        dct['DepartureLoc'].append(l)

    for a in arrival:
        arrival_txt = await page.evaluate('(element) => element.textContent', a)
        arr_times.append(arrival_txt)
        arr_times = [x.replace('\n', '') for x in arr_times]

    new_arr_tim = [x[0:5] for x in arr_times]
    new_arr_loc = [x[8:] for x in arr_times]

    for a in new_arr_tim:
        dct['ArrivalTime'].append(a)
    for m in new_arr_loc:
        dct['ArrivalLoc'].append(m)

    for e in date:
        date_txt = await page.evaluate('(element) => element.textContent', e)
        date_info.append(date_txt)
        date_info = [x.replace('\n', '') for x in date_info]
    for d in date_info:
        dct['Date'].append(d)

    print(prices)
    print(dct)


asyncio.get_event_loop().run_until_complete(get_info('Germany', 'Paris', '25.12.2020', '28.12.2020'))
