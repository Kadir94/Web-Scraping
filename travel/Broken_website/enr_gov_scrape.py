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
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://enr.gov.eg/ticketing/public/smartSearch.jsf', timeout=200000)
    await page.waitForXPath('//*[@id="smartSearch"]/div[2]',{'visible': True, 'timeout': 50000})
    # await page.waitForXPath('//td/select[contains(@class,"validate[required]")]',{'visible': True, 'timeout': 50000})
    # await page.click('[class=validate[required]]',{'clickCount': 1})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#smartSearch:startStationInput")
    await page.type('#smartSearch:startStationInput', origin)
    # await page.type('[class=validate[required]]', origin)
    await page.keyboard.press('Enter')
#     await page.click('[id=smartSearch]',{'clickCount': 1})
#     # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#smartSearch\3a endStationInput")
#     # await page.type('#smartSearch\:endStationInput', destination)
#     await page.type('[id=smartSearch]', destination)
#     await page.keyboard.press('Enter')
#     await page.waitForXPath('//*[@id="smartSearch"]',{'visible': True, 'timeout': 50000})
#     # await page.waitForXPath('//*[@id="smartSearch:departureDateInput"]',{'visible': True, 'timeout': 50000})
#     await page.click('[id=smartSearch]', {'clickCount': 1})
#     # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#smartSearch\3a departureDateInput")
#     # await page.type('#smartSearch\3a departureDateInput', date)
#     await page.type('[id=smartSearch]', date)
#     # await page.click('[id=switch-date-f]',{'clickCount': 1})
#  # await page.click('[id=select2-input_origen-container]',{'clickCount': 1})
# #smartSearch\3a departureDateInput

asyncio.get_event_loop().run_until_complete(get_info('Cairo', 'Alexandria','07/01/2021'))

# //*[@id="smartSearch:departureDateInput"]
