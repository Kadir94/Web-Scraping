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
    time = []
    dep_loc = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.rail.co.il/en', timeout=90000)
    cookies=None
    while True:
        try:
            cookies = await page.waitForXPath('//*[@id="ZA_CAMP_DIV_1"]',{'visible': True, 'timeout': 10000})
        except Exception:
            print("No Cookie")
        if cookies:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#ZA_CANVAS_763351_CLOSE_X2_13_IMG")
            break
        else:
            pass
            break

    await page.waitForXPath('//*[@id="trainSearchMain"]/div/div/div/div/div/input[@aria-label="Select a departure station"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#trainSearchMain > div > div > div > div.col-md-2.col-sm-5.col-xs-10.fromBox > div.typeahead.ng-isolate-scope > input")
    await page.type('#trainSearchMain > div > div > div > div.col-md-2.col-sm-5.col-xs-10.fromBox > div.typeahead.ng-isolate-scope > input', origin)
    suggestion_1 = None
    try:
       suggestion_1 = await page.waitForXPath('//*[@id="ul-solbox-autocomplete-1"]', {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible Questions')
    if suggestion_1:
        first_link_dep = await suggestion_1.xpath('.//*[@class="results ng-scope"]')
        try:
            await first_link_dep[0].click()
        except Exception:
            logger.error('Did not work -> Arrival question')
    await page.waitForXPath('//*[@id="trainSearchMain"]/div/div/div/div/div/input',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#trainSearchMain > div > div > div > div.col-md-2.col-sm-5.col-xs-10.toBox > div.typeahead.ng-isolate-scope > input")
    await page.type('#trainSearchMain > div > div > div > div.col-md-2.col-sm-5.col-xs-10.toBox > div.typeahead.ng-isolate-scope > input', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//*[@id="ul-solbox-autocomplete-2"]', {'visible': True, 'timeout': 7000})
    except Exception:
        logger.info('No Possible Questions')
    if suggestion_2:
        first_link_arr = await suggestion_2.xpath('.//*[@class="results ng-scope"]')
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> Date')
    await page.waitForXPath('//*[@id="trainSearchMain"]/div/div/div/div/fieldset/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#trainSearchMain > div > div > div > div.col-md-2.col-sm-11.col-xs-10.dateTimeBox > fieldset > button")
    await page.waitForXPath('//*[@id="elemId_15"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#elemId_15")
    await page.type('#elemId_15', date)

    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#trainSearchMain > div > div > div > div.col-md-2.col-sm-11.col-xs-10.dateTimeBox > fieldset > div > div.SboxTimePicker.col-md-6.col-sm-6.col-xs-12 > div.displayAndProceed > a")
    await page.waitForXPath('//*[@id="trainSearchMain"]/div/div/div/div/button[@class="ng-binding"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#trainSearchMain > div > div > div > div.col-md-2.col-sm-11.col-xs-10.searchBtnBox > button")
    await asyncio.wait([page.waitForXPath('//div[contains(@class,"hours ng-binding")]', timeout=90000)])
    await asyncio.wait([page.waitForXPath('//li[contains(@class,"platform ng-binding")]', timeout=90000)])
    times = await page.xpath('//div[contains(@class,"hours ng-binding")]')
    dep_locs = await page.xpath('//li[contains(@class,"platform ng-binding")]')
    for t in times:
        times_txt = await page.evaluate('(element) => element.textContent', t)
        time.append(times_txt)
    departure_times = time[::2]
    arrival_times = time[1::2]
    departure_times = [x[14:] for x in departure_times]
    arrival_times = [x[12:] for x in arrival_times]
    print(departure_times)
    print(arrival_times)
    for l in dep_locs:
        dep_loc_txt = await page.evaluate('(element) => element.textContent', l)
        dep_loc.append(dep_loc_txt)
    dep_loc = [x[23:] for x in dep_loc]
    print(dep_loc)

asyncio.get_event_loop().run_until_complete(get_info('Tel Aviv-University', 'Tel Aviv-Savidor Center','23/01/2021'))


