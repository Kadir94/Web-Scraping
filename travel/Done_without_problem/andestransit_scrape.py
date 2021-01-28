from pyppeteer import launch
import asyncio
import logging
import datetime


async def get_info(origin, destination,date,logger):

    dict = []
    date = date.strftime('%Y-%m-%d')
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://andestransit.com/', timeout=90000)
    await page.waitForXPath('//*[@id="search-origin-public"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-origin-public")
    await page.type('[id=search-origin-public]', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath('//html/body/div/div[contains(@class,"autocomplete-suggestion")]',{'visible': True, 'timeout': 3000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_1:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "body > div:nth-child(14) > div:nth-child(1)")
        except Exception:
             logger.info('Couldn not find Suggestion')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-destination-public")
    await page.type('[id=search-destination-public]', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//html/body/div/div[contains(@class,"autocomplete-suggestion")]',{'visible': True, 'timeout': 3000})
    except Exception:
        logger.info('No Sugessions')
    if suggestion_2:
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "body > div:nth-child(17) > div:nth-child(1)")
        except Exception:
            logger.info('Couldn not find Suggestion')

    await page.waitForXPath('//div/input[@name="submitBtn"]',visible=True, timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#searchForm-public > div:nth-child(3) > input")
    await page.waitForXPath('//section/div[@id="calendar"]',visible=True, timeout=50000)
    date_wanted = None
    while True:
        try:
            date_wanted = await page.waitForXPath(f'//tr/td[@data-date="{date}"]',timeout=10000)
        except Exception:
            print('lol1')
            # logger.info('Cannot pick the date')
        if date_wanted:
            await date_wanted.click()
            break
        else:
            try:
                next_button = await page.waitForXPath('//div/button[@class="fc-next-button fc-button fc-state-default fc-corner-left fc-corner-right"]')
                await next_button.click()
            except Exception:
                print('lol2')
                # logger.info('Cannot click the next month button')
    await asyncio.wait([page.waitForXPath('//table[contains(@class,"best-bets")]',{'visible': True, 'timeout': 50000})])
    dep_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.DepartureTime")]')
    arr_time = await page.xpath('//tr/td/span[contains(@data-bind,"text: $data.ArrivalTime")]')
    price = await page.xpath('//td/a/span[contains(@data-bind,"text : $data.TotalPrevPrice()")]')
    for (d,a,p) in zip(dep_time,arr_time,price):
        dep_time_txt = await page.evaluate('(element) => element.textContent', d)
        arr_time_txt = await page.evaluate('(element) => element.textContent', a)
        price_txt = await page.evaluate('(element) => element.textContent', p)
        dict.append({
            'Origin': origin,
            'Destanation': destination,
            'Date': date,
            'DepartureTime': dep_time_txt,
            'ArrivalTime': arr_time_txt,
            'Price': price_txt.strip()+" USD"
        })

    return dict

asyncio.get_event_loop().run_until_complete(get_info('BOGOTA', 'Cali (Airport)',datetime.datetime.today(),logger=None))



