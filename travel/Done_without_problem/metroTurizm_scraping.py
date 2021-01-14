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
    departure_locs = []
    arrival_locs = []
    times = []
    prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.metroturizm.com.tr/en/', timeout=90000)

    await page.waitForXPath('//*[@id="Metro"]/div[1]/div[2]/div/div',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#Metro > div.row > div:nth-child(2) > div > div > button")
    await page.waitForXPath('//*[@id="Metro"]/div[1]/div[2]/div/div/div',{'visible': True, 'timeout': 50000})
    await page.type('[id=Metro]', origin)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', " #Metro > div.row > div:nth-child(4) > div > div > button")
    await page.type('[id=Metro]', destination)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="inpSearchJourneyBusBoardingDate"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).removeAttribute("readonly")''', "#inpSearchJourneyBusBoardingDate")
    await page.click('[id=inpSearchJourneyBusBoardingDate]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('#inpSearchJourneyBusBoardingDate', date)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#btnIndexSearchJourneys")
    await page.waitForXPath('//div[contains(@class,"journey-item")]',{'visible': True, 'timeout': 90000})
    departure = await page.xpath('//div/span[contains(@class,"start ng-binding")]')
    arrival = await page.xpath('//div/span[contains(@class,"end ng-binding")]')
    time = await page.xpath('//div/span[contains(@class,"journey-item-hour ng-binding")]')
    price = await page.xpath('//div/span[contains(@class,"price ng-binding")]')
    for i in departure:
        departure_txt = await page.evaluate('(element) => element.textContent', i)
        departure_locs.append(departure_txt)
        departure_locs = [x.replace('\n', '') for x in departure_locs]
        departure_locs = [x.strip('                  ') for x in departure_locs]
    print(departure_locs)
    for a in arrival:
        arrival_txt = await page.evaluate('(element) => element.textContent', a)
        arrival_locs.append(arrival_txt)
        arrival_locs = [x.replace('\n', '') for x in arrival_locs]
        arrival_locs= [x.strip('                  ') for x in arrival_locs]
    print(arrival_locs)
    for t in time:
        time_txt = await page.evaluate('(element) => element.textContent', t)
        times.append(time_txt)
        times = [x.replace('\n', '') for x in times]
        times = [x.strip('                  ') for x in times]
    departure_times = times[::2]
    arrival_times = times[1::2]
    print(departure_times)
    print(arrival_times)
    string = "TL"
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = ["{}{}".format(i,string) for i in prices]
    print(prices)


asyncio.get_event_loop().run_until_complete(get_info('SAMSUN', 'ANKARA','25.01.2021'))


