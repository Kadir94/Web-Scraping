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
    arr_times = []
    locs = []
    prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://12go.asia/de', timeout=90000)
    await page.waitForXPath('//*[@id="app"]/div[1]/header/div[4]/div/div[1]/div/div[1]/div[1]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div")
    await page.waitForXPath('//*[@id="app"]/div[2]/div/div[2]/div/div[1]/div/input',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-header > div > input")
    await page.type('#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-header > div > input', origin)
    await asyncio.sleep(3)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath('//div[contains(@class,"vue-modal-body js-modal-window-body")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_1:
        first_link_dep = await suggestion_1.xpath(".//*[@class='vue-typeahead-suggestions popup']")
        try:
            await first_link_dep[0].click()
        except Exception:
                logger.error('Did not work -> please write arrival')
    await page.type('#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-header > div > input', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//div[contains(@class,"vue-modal-body js-modal-window-body")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_2:
        first_link_arr = await suggestion_2.xpath(".//*[@class='vue-typeahead-suggestions popup']")
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> please write date')

    await page.waitForXPath('//div/div[contains(@class,"vue-modal-box")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-footer > div > div.vue-field-datepicker-buttons > button.btn.btn-primary.btn-lg")
    await page.waitForXPath('//div/div/div[contains(@class,"vue-modal-footer")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-footer > button")
    await page.waitForXPath('//div/div[contains(@class,"vue-search-form-group action")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.action > button")

    await page.waitForXPath('//div[contains(@class,"trip-card clickable")]',{'visible': True, 'timeout': 50000})
    departure_time = await page.xpath('//div/div[contains(@class,"trip-points-line-left bold")]')
    arrival_time = await page.xpath('//div/div[contains(@class,"trip-points-line-left")]')
    locations = await page.xpath('//div/div[contains(@class,"trip-points-line-desc one-line")]')
    price = await page.xpath('//div/div[contains(@class,"price")]')
    for d in departure_time:
        dep_time_txt = await page.evaluate('(element) => element.textContent', d)
        dep_times.append(dep_time_txt)
    print(dep_times)
    for a in arrival_time:
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        arr_times.append(arr_time_txt)
    arr_times = arr_times[2::3]
    print(arr_times)
    for l in locations:
        locs_txt = await page.evaluate('(element) => element.textContent', l)
        locs.append(locs_txt)
    dep_loc = locs[0::2]
    arr_loc = locs[1::2]
    print(dep_loc)
    print(arr_loc)
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
        prices = [x.strip('   ') for x in prices]
    new_price = [x[:8] for x in prices]
    new_price = [x.strip(' ') for x in new_price]
    print(new_price)

asyncio.get_event_loop().run_until_complete(get_info('Chiang Mai', 'Pattaya','11/1/2021'))

