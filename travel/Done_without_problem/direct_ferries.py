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
    dep_infos = []
    prices = []
    dct = {'Departure': [], 'Arrival': [], 'Dep_Time': [], 'Arr_Time': [], 'Price': []}
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.directferries.de/', timeout=90000)
    await page.waitForXPath('//*[@id="deal_finder1"]/div[1]/section[1]/label[2]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > section.journey_type > label:nth-child(2)")

    await page.waitForXPath('//*[@id="route_outbound"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#route_outbound")
    await page.type('#route_outbound', origin)
    await page.type('#route_outbound', destination)
    await asyncio.sleep(2)
    await page.waitForXPath('//*[@id="journey_route_parent"]/div[15]/aside/ul/li',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#journey_route_parent > div:nth-child(16) > aside > ul > li:nth-child(1)")

    await page.waitForXPath('//div/section[contains(@class,"journey_timing timing_outbound hide_until_times")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > section.journey_timing.timing_outbound.hide_until_times")
    date_wanted = None
    while True:
        try:
            date_wanted = await page.waitForXPath(f'//div[@data-full="{date}"]',timeout=1000)
        except Exception:
            logger.info('Cannot pick the date')
        if date_wanted:
            await date_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div[@aria-label="Next Month"]')
                await next_button.click()
            except Exception:
                logger.info('Cannot click the next month button')
    await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/section[4]/section[1]/ul[2]/li[3]/a',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > section.journey_info.hide_until_summary > section.trip_outbound.both_ways > ul:nth-child(4) > li:nth-child(3) > a")
    await page.waitForXPath('//div[@id="vehicle_base"]',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="vehicle_base"]/div[2]/label[3]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#vehicle_base > div.popup_body > label:nth-child(4)")
    car_choice = await page.waitForXPath('//div/fieldset/ol[contains(@class,"item_list vehicle_make")]',{'visible': True, 'timeout': 50000})
    car_options = await car_choice.xpath("//*[@id='deal_finder1']/div[2]/aside/div/div[2]/fieldset/ol/li")
    await car_options[5].click()

    model_choice = await page.waitForXPath('//div/fieldset/ol[contains(@class,"item_list vehicle_model")]',{'visible': True, 'timeout': 50000})
    model_options = await model_choice.xpath("//*[@id='deal_finder1']/div[2]/aside/div/div[2]/fieldset[2]/ol/li")
    await model_options[20].click()
    await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/aside/footer/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > aside > footer > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div[2]/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")

    await page.waitForXPath('//*[@id="divQuotesContainer"]/div[3]/div/div[1]/div[1]',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="divQuotesContainer"]/div[3]/div/div[1]/div[1]/div[2]',{'visible': True, 'timeout': 50000})
    dep_info = await page.xpath('//div/div[contains(@class,"ab-2062-col-1")]')
    price = await page.xpath('//div/div/b')
    for d in dep_info:
        dep_info_txt = await page.evaluate('(element) => element.textContent', d)
        dep_infos.append(dep_info_txt)
        dep_infos = [x.replace('\n', '') for x in dep_infos]
        dep_infos = [x.strip('                                                                        ') for x in dep_infos]
    del dep_infos[1::3]
    locations = [x[:10] for x in dep_infos]
    times = [x[75:90] for x in dep_infos]
    depar_loc = locations[0::2]
    arr_loc = locations[1::2]
    dep_time = times[0::2]
    arr_time = times[1::2]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[7::5]
    for d in depar_loc:
        dct['Departure'].append(d)
    for a in arr_loc:
        dct['Arrival'].append(a)
    for t in dep_time:
        dct['Dep_Time'].append(t)
    for r in arr_time:
        dct['Arr_Time'].append(r)
    for p in prices:
        dct['Price'].append(p)
    print(dct)


asyncio.get_event_loop().run_until_complete(get_info('Calais ', '- Dover','2021-2-2'))



