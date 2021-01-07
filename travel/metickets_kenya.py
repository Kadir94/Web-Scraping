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
    info = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://metickets.krc.co.ke/', timeout=90000)
    await page.waitForXPath('//*[@id="train_type"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=train_type]',{'clickCount': 1})
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    await page.waitForXPath('//div/select[contains(@class,"form-control terminal_id")]', timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#content > div > div > div > form > div > div:nth-child(3) > div > div > select")
    await page.type('#content > div > div > div > form > div > div:nth-child(3) > div > div > select', origin)
    await asyncio.sleep(2)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="destination_references"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#destination_references")
    await page.type('#destination_references', destination)
    await asyncio.sleep(2)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="dateInput"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#dateInput")
    await page.type('#dateInput', date)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//div/select[contains(@class,"form-control depature_time")]', timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#depature_time")
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="content"]/div/div/div/div[1]/div/div',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="car-details"]/div/div[1]/div[2]',{'visible': True, 'timeout': 50000})
    times = await page.xpath('//div/small/span[contains(@class,"span")]')
    locs = await page.xpath('//ul/li/a[contains(@href,"#")]')
    for i in times:
        time_txt = await page.evaluate('(element) => element.textContent', i)
        dep_times.append(time_txt)
    departure_times = dep_times[::2]
    arrival_times = dep_times[1::1]
    print(departure_times)
    print(arrival_times)
    for l in locs:
        locs_txt = await page.evaluate('(element) => element.textContent', l)
        info.append(locs_txt)
    print(info)

asyncio.get_event_loop().run_until_complete(get_info('Mombasa Terminus', 'Voi','01/08/2021'))
