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
    dep_times = []
    arr_times = []
    locs = []
    prices = []
    months = ['month','Januar','Februar','März','April','Mai','Juni','juli','August','September','Oktober','November','Dezember']
    day = date.split('.')[2]
    month = date.split('.')[1]
    year = date.split('.')[0]
    print(month)
    print(year)
    print(day)
    print(months[int(month)]+year)
    browser = await launch({
                            'args': [
                            '--window-size=1280,1080',
                                ]
                            }, headless=False, autoClose=False, defaultViewport=None, width=1000, height=1200)
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 1600})
    await page.goto('https://12go.asia/de', timeout=90000)
    search_block = await page.waitForXPath('//div[@class="vue-search-form-trips container vue-search-form-component"]',{'visible': True, 'timeout': 50000})
    origin_input = await search_block.xpath('//div[@class="form-control prefield"]')
    await origin_input[0].click()
    write_origin = await page.waitForXPath('//div[@class="vue-typeahead-form-group form-element"]',{'visible': True, 'timeout': 50000})
    write = await write_origin.xpath('//input[@class="form-control"]')
    await write[0].type(origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.xpath('//div[contains(@class,"vue-typeahead-suggestions popup")]')
    except Exception:
        print("no suggestion1")
    if suggestion_1:
        try:
            await suggestion_1[0].click()
        except Exception:
            print("no click")
    else:
        print('click nope')
    # await write[1].type(destination)
    # await page.waitForXPath('//div[')
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div")
    #
    # # await page.click('[class=form-control prefield]', {'clickCount': 1})
    # await page.waitForXPath('//div/div/input[@class="form-control"]',{'visible': True, 'timeout': 50000})
    # await page.evaluate('''(selector) => document.querySelector(selector).click({'clickCount': 3})''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input")
    # await page.keyboard.press('Backspace')
    # await page.type('#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input', origin)
    # # await page.keyboard.press('Enter')
    # # await page.waitForXPath('//div/div/input[@class="form-control"]',{'visible': True, 'timeout': 50000})
    # # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input")
    # # await page.type('#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(1) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input', origin)
    # # await asyncio.sleep(1)
    # suggestion_1 = None
    # try:
    #     suggestion_1 = await page.waitForXPath('//div/div/div[contains(@class,"vue-typeahead-suggestions popup")]',{'visible': True, 'timeout': 50000})
    # except Exception:
    #     logger.info('No Possible suggestion')
    # if suggestion_1:
    #     await asyncio.sleep(1)
    #     first_link_dep = await suggestion_1.xpath('//div/div/div[contains(@class,"vue-typeahead-suggestions-item")]')
    #     try:
    #         await first_link_dep[0].click()
    #     except Exception:
    #             logger.error('Did not work -> please write arrival')
    # await page.type('#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(2) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input', destination)
    # # await page.waitForXPath('//div/div[@class="form-control prefield"]',{'visible': True, 'timeout': 50000})
    # # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(2) > div > div > div > div > div > div")
    # # await page.type('#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.places > div:nth-child(2) > div > div > div > div > div > div.vue-modal-wrapper.full-height > div > div > div.vue-modal-header > div > input', destination)
    # suggestion_2 = None
    # try:
    #     suggestion_2 = await page.waitForXPath('//div[contains(@class,"vue-typeahead-suggestions popup")]',{'visible': True, 'timeout': 50000})
    # except Exception:
    #     logger.info('No Possible suggestion')
    # if suggestion_2:
    #     await asyncio.sleep(1)
    #     first_link_arr = await suggestion_2.xpath(".//*[@class='vue-typeahead-suggestions-item']")
    #     try:
    #         await first_link_arr[0].click()
    #     except Exception:
    #         logger.error('Did not work -> please write date')
    # # # date_input = await page.waitForXPath('//*[@id="form-datepicker"]/div[@class="vue-search-form-group-field"]',{'visible': True, 'timeout': 50000})
    # # # await date_input.click()
    # month_wanted = None
    # day_wanted = None
    # await asyncio.sleep(2)
    # # next_button = await page.waitForXPath('//div/button[@class="calendar-arrow-incr"]',timeout=50000)
    # # await next_button.click()
    # # wrapper = await page.waitForXPath('//div/div[@class="calendar-wrapper"]',timeout=50000)
    # calendar = await page.waitForXPath('//div/div[@class="calendar-wrapper"]',{'visible': True, 'timeout': 50000})
    # day_desired = await page.waitForXPath('')
    # while True:
    #     try:
    #         month_wanted = await calendar.xpath(f'//span[contains(text(),"{months[int(month)]+" "+year}")]')
    #     except Exception:
    #         print('lol')
    #         # logger.info('Cannot pick the month')
    #     if month_wanted:
    #         print("month found")
    #         break
    #     else:
    #         try:
    #             next_button = await page.waitForXPath('//div/div/button[@class="calendar-arrow-incr"]',{'visible': True, 'timeout': 50000})
    #             await next_button.click()
    #         except Exception:
    #             print("lol3")
    # while True:
    #     try:
    #         day_wanted = await calendar.xpath(f'//div[contains(text(),"{day}")]')
    #     except Exception:
    #         print("lol4")
    #     if day_wanted:
    #         print("day found")
    #         await asyncio.sleep(2)
    #         await day_wanted[0].click()
    #         break
    #     else:
    #         try:
    #             next_button = await page.waitForXPath('//div/button[@class="calendar-arrow-incr"]',timeout=5000)
    #             await next_button.click()
    #         except Exception:
    #             print("lol5")
                # logger.info('Cannot click the next month button')
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-footer > div > div.vue-field-datepicker-buttons > button.btn.btn-primary.btn-lg")
    # await page.waitForXPath('//div/div/div[contains(@class,"vue-modal-footer")]',{'visible': True, 'timeout': 50000})
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.vue-portal-target > div > div.vue-modal > div > div.vue-modal-footer > button")
    # await page.waitForXPath('//div/div[contains(@class,"vue-search-form-group action")]',{'visible': True, 'timeout': 50000})
    # await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#app > div.wrapper > header > div:nth-child(4) > div > div.vue-search-form-content > div > div.vue-search-form-group.action > button")
    #
    # await page.waitForXPath('//div[contains(@class,"trip-card clickable")]',{'visible': True, 'timeout': 50000})
    # departure_time = await page.xpath('//div/div[contains(@class,"trip-points-line-left bold")]')
    # arrival_time = await page.xpath('//div/div[contains(@class,"trip-points-line-left")]')
    # locations = await page.xpath('//div/div[contains(@class,"trip-points-line-desc one-line")]')
    # price = await page.xpath('//div/div[contains(@class,"price")]')
    # for d in departure_time:
    #     dep_time_txt = await page.evaluate('(element) => element.textContent', d)
    #     dep_times.append(dep_time_txt)
    # print(dep_times)
    # for a in arrival_time:
    #     arr_time_txt = await page.evaluate('(element) => element.textContent', a)
    #     arr_times.append(arr_time_txt)
    # arr_times = arr_times[2::3]
    # print(arr_times)
    # for l in locations:
    #     locs_txt = await page.evaluate('(element) => element.textContent', l)
    #     locs.append(locs_txt)
    # dep_loc = locs[0::2]
    # arr_loc = locs[1::2]
    # print(dep_loc)
    # print(arr_loc)
    # for p in price:
    #     price_txt = await page.evaluate('(element) => element.textContent', p)
    #     prices.append(price_txt)
    #     prices = [x.strip('   ') for x in prices]
    # new_price = [x[:8] for x in prices]
    # new_price = [x.strip(' ') for x in new_price]
    # print(new_price)

asyncio.get_event_loop().run_until_complete(get_info('Chiang mai', 'Pattaya','2021.3.25'))


