from pyppeteer import launch
import asyncio
import logging


async def get_info(origin,destination):

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
    info = []
    trip1 = None
    trip2 = None
    trip3 = None
    trip4 = None
    dct = {'Company': [], 'Time Of Departure': [], 'Price': []}
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://ask-aladdin.com/egypt-transport-system/bus-timetables/', timeout=200000)
    await page.waitForXPath('//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")]',{'visible': True, 'timeout': 50000})
    while True:
        try:
            trip1 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+destination}")]',timeout=1000)
        except Exception:
            print('trip1 can not found')
        if trip1:
            await trip1.click()
            break
        elif trip1 is None:
            try:
                trip2 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{"From"+" "+origin+" "+"to"+" "+destination}")]',timeout=1000)
            except Exception:
                print('trip2 can not found')
        if trip2:
            await trip2.click()
            break
        elif trip2 is None:
            try:
                trip3 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+"the"+" "+destination}")]',timeout=1000)
            except Exception:
                print('trip3 can not found')
        if trip3:
            await trip3.click()
            break
        elif trip3 is None:
            try:
                trip4 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+"/"+destination}")]',timeout=1000)
            except Exception:
                print('trip3 can not found')
        if trip4:
            await trip4.click()
            break
        else:
            print('No trip in Given Locations')
            break
    chosen = await page.xpath('//div/div[@aria-expanded="true"]/div/div/div/table/tbody/tr/td')
    for i in chosen:
        name = await page.evaluate('(element) => element.textContent', i)
        info.append(name)
    company = info[3::3]
    dep_time = info[4::3]
    price = info[5::3]
    for c in company:
        dct['Company'].append(c)
    for d in dep_time:
        dct['Time Of Departure'].append(d)
    for p in price:
        dct['Price'].append(p)
    print(dct)


asyncio.get_event_loop().run_until_complete(get_info('Cairo', 'Alexandria'))

