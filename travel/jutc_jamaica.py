from pyppeteer import launch
import asyncio
import logging



async def get_info(origin, destination):

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
    cols = []
    rows = []
    page = await browser.newPage()
    await page.goto('https://jutc.gov.jm/bus-routes/', timeout=90000)
    await page.waitForXPath('//*[@id="bus-route-filter"]/form/div/div[1]/select',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#bus-route-filter > form > div > div.col-md-3.route-orgin > select")
    await page.type('#bus-route-filter > form > div > div.col-md-3.route-orgin > select', origin)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="bus-route-filter"]/form/div/div[2]/select',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#bus-route-filter > form > div > div.col-md-3.route-destination > select")
    await page.type('#bus-route-filter > form > div > div.col-md-3.route-destination > select', destination)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="bus-route-filter"]/form/div/div[4]/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#bus-route-filter > form > div > div.submit-btn > button")

    await page.waitForXPath('//*[@id="bus-route-tbl"]',{'visible': True, 'timeout': 50000})
    elements = await page.xpath('//*[@id="bus-route-tbl"]/div[1]/div')
    elements1 = await page.xpath('//*[@id="bus-route-tbl"]/div/div')
    for e in elements:
        elements_txt = await page.evaluate('(element) => element.textContent', e)
        cols.append(elements_txt)
    print(cols)
    for e in elements1:
        elements_txt = await page.evaluate('(element) => element.textContent', e)
        rows.append(elements_txt)
    rows = rows[10:]
    rows = [x.replace('\n', '') for x in rows]
    rows = [x.replace('\t', '') for x in rows]
    print(rows)


asyncio.get_event_loop().run_until_complete(get_info('Gordon Town', 'Cross Roads'))

# //div/div/div[contains(@class,"col-md-1")]
