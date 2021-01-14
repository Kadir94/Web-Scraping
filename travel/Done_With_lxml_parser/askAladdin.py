from pyppeteer import launch
import asyncio
import logging
import requests
import lxml.html as lh
import pandas as pd


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
    await page.goto('https://ask-aladdin.com/egypt-transport-system/bus-timetables/', timeout=200000)
    await page.waitForXPath('//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "body > section.inrpgwrapper.dtlpgwrapper > div > div > div.left.col-lg-10.col-md-10.col-sm-10.col-xs-12 > div > div.abutpgwrapper_col2_intro_row4 > section > div:nth-child(6) > div:nth-child(3) > div > div.panel-heading > h4 > a")
    await page.waitForXPath('//*[@id="collapse1"]',{'visible': True, 'timeout': 50000})
    page1 = requests.get('https://ask-aladdin.com/egypt-transport-system/bus-timetables/')
    doc = lh.fromstring(page1.content)
    tr_elements = doc.xpath('//table/tbody/tr')
    col = []
    i = 0
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))
    for j in range(1, len(tr_elements)):
        table = tr_elements[j]
        if len(table) != 3:
            break
        i = 0
        for t in table.iterchildren():
            data = t.text_content()
            if i > 0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i += 1
    dicts = {title:column for (title,column) in col}
    df = pd.DataFrame(dicts)
    print(df.head())

asyncio.get_event_loop().run_until_complete(get_info('Cairo', 'Alexandria','07/01/2021'))
