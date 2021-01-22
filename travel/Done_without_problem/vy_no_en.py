from pyppeteer import launch
import asyncio
import logging


async def get_info(origin, destination,time):

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
    times = []
    locs = []
    prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.vy.no/en/', timeout=50000)

    await page.type('[id=departure-place-input]', origin)
    await page.waitForXPath('//*[@id="departure-place-inputAutocompleteList"]/li/button',{'visible': True, 'timeout': 50000})
    try:
        await page.click('[id=departure-place-inputAutocompleteList]', {'clickCount': 1})
    except Exception:
        logger.error('Invalid Origin Name')
    await page.type('[id=arrival-place-input]', destination)
    await page.waitForXPath('//*[@id="arrival-place-inputAutocompleteList"]/li/button',{'visible': True, 'timeout': 50000})
    try:
        await page.click('[id=arrival-place-inputAutocompleteList]', {'clickCount': 1})
    except Exception:
        logger.error('Invalid Destination Name')
    await page.waitForXPath('//*[@id="timepicker--departure"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=timepicker--departure]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=timepicker--departure]', time)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="new-travel-planner"]',{'visible': True, 'timeout': 50000})
    await page.xpath('//div[@id="new-travel-planner"]')
    try:
        await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#new-travel-planner > div._f2938568 > span._6cc748f6 > button")
    except Exception:
        logger.error('Can not find the Search Button')
    try:
        await page.waitForXPath('//li/div[@class="_3c22a6bd"]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.error('Can not find the Travel Info')

    i = 1
    suggestions = None
    while i <= 5:
        try:
            suggestions = await page.waitForXPath(f'//ol/li/ol/li["{i}"]',{'visible': True, 'timeout': 50000})
        except Exception:
            print('lol')
        if suggestions:
                choose = await suggestions.xpath('//div/div/button[@aria-label="Show more travel details for the travel suggestion"]')
                await choose[1].click()
                gather_time = await page.waitForXPath('//div/ol[@class="_742cac35"]',{'visible': True, 'timeout': 50000})
                time = await gather_time.xpath('//li/div/div[@class="_c08706a8"]')
                dep_loc = await gather_time.xpath('//div/span/p[@class="_5003f5bc"]')
                arr_loc = await gather_time.xpath('//div/p[@class="_f4d37877"]')
                for t in time:
                    time_txt = await page.evaluate('(element) => element.textContent', t)
                    times.append(time_txt)
                for d in dep_loc:
                    dep_loc_txt = await page.evaluate('(element) => element.textContent', d)
                    locs.append(dep_loc_txt)
                for a in arr_loc:
                    arr_loc_txt = await page.evaluate('(element) => element.textContent', a)
                    locs.append(arr_loc_txt)
                i += 1
        else:
            break
    price = await page.xpath('//div/button/span[contains(@class ,"_8c3d6635")]')
    for j in price:
        price_txt = await page.evaluate('(element) => element.textContent', j)
        prices.append(price_txt)
    prices = prices[:len(prices)-5]
    new_times_dep = [x[0:5] for x in times]
    new_times_arr =[x[5:10] for x in times]
    print(new_times_dep)
    print(new_times_arr)
    new_dep_loc = locs[1::3]
    new_arr_loc = locs[2::3]
    print(new_dep_loc)
    print(new_arr_loc)
    print(prices)



asyncio.get_event_loop().run_until_complete(get_info('Allkopi Parkveien', 'Fridtjof Nansens vei','19:45'))

