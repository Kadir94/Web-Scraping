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
    locations = []
    dep_loc = []
    arr_loc = []
    times = []
    times2 = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://thebusschedule.com/EN/sv/index.php', timeout=90000)
    await page.waitForXPath('//*[@id="inputString"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=inputString]',{'clickCount': 1})
    await page.type('[id=inputString]', origin)
    await asyncio.sleep(2)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath("//*[@id='suggestions']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible questions')
    if suggestion_1:
        first_link_dep = await suggestion_1.xpath(".//*[@id='autoSuggestionsList']")
        try:
            await first_link_dep[1].click()
        except Exception:
            logger.error('Did not work -> Arrival')
    await asyncio.sleep(2)

    await page.waitForXPath('//*[@id="inputString2"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=inputString2]',{'clickCount': 1})
    await page.type('[id=inputString2]', destination)
    await asyncio.sleep(2)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath("//*[@id='suggestions2']", {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible questions')
    if suggestion_2:
        first_link_arr = await suggestion_2.xpath(".//*[@id='autoSuggestionsList2']")
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> Date')

    await page.waitForXPath('//*[@id="jDate"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=jDate]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=jDate]', date)
    await page.waitForXPath('//*[@id="page-wrapper"]/div/div/div/div[2]/div/div/div/form/div/div[1]/div[6]/div/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"    #page-wrapper > div > div > div > div:nth-child(5) > div > div > div > form > div > div.col-md-7 > div.col-lg-5.pull-right > div > button")
    await page.waitForXPath('//*[@id="page-wrapper"]/div/div[1]/div/div[2]/div/div[6]/div/table',{'visible': True, 'timeout': 50000})
    locs = await page.xpath('//div/span/b')
    time = await page.xpath('//*[@id="page-wrapper"]/div/div[1]/div/div[2]/div/div[6]/div/table/tbody/tr[1]/td[6]')
    time2 = await page.xpath('//*[@id="page-wrapper"]/div/div[1]/div/div[2]/div/div[6]/div/table/tbody/tr[3]/td[6]')

    for l in locs:
        locs_txt = await page.evaluate('(element) => element.textContent', l)
        locations.append(locs_txt)
    dep_loc.append(locations[0])
    arr_loc.append(locations[1])
    print(dep_loc)
    print(arr_loc)
    for t in time:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        times.append(time_txt)
    dep_times = [x[0:5] for x in times]
    arr_times = [x[5:10] for x in times]
    for t in time2:
        time2_txt = await page.evaluate('(element) => element.textContent', t)
        times2.append(time2_txt)
    dep_times2 = [x[0:5] for x in times2]
    arr_times2 = [x[5:10] for x in times2]
    departure_times = dep_times+dep_times2
    print(departure_times)
    arrival_times = arr_times+arr_times2
    print(arrival_times)
asyncio.get_event_loop().run_until_complete(get_info('San Salvador', 'Santa Ana','01/15/2021'))

