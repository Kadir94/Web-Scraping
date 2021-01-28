from pyppeteer import launch
import asyncio
import logging
import datetime


async def get_info(orgin_city, dest_city, start_date,logger):
    prices = []
    dep_info = []
    arr_times = []
    dict = []
    start_date = start_date.strftime('%d.%m.%Y')
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.fluege.de/', timeout=50000)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#flightForm > div.flight-type-wrapper > div.js_flight-type.flight-type.oneway > label")
    await page.type('[id=f0-dep-location-]', orgin_city)
    await page.type('[id=f0-arr-location-]', dest_city)
    await page.click('[id=f0Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f0Date]', start_date)
    await page.keyboard.press('Enter')
    question_1 = None
    try:
        question_1 = await page.waitForXPath("//*[@id='f0DepSection']", {'visible': True, 'timeout': 7000})
    except Exception:
        # logger.info('No Possible questions')
        print('No Possible questions')
    if question_1:
        first_link_dep = await question_1.xpath(".//*[@class='js_select-airport']")
        try:
            await first_link_dep[0].click()
        except Exception:
            # logger.error('Did not work -> Departure question')
            print('Did not work -> Departure question')
    question_2 = None
    try:
        question_2 = await page.waitForXPath('//*[@id="f0ArrSection"]', {'visible': True, 'timeout': 7000})
    except Exception:
        # logger.info('No Possible Questions')
        print('No Possible Questions')
    if question_2:
        first_link_arr = await question_2.xpath('.//*[@class="js_select-airport"]')
        try:
            await first_link_arr[0].click()
        except Exception:
            # logger.error('Did not work -> Arrival question')
            print('Did not work -> Arrival question')

    await asyncio.wait([page.waitForXPath('//div[contains(@class,"column-price-flag")]', timeout=90000)])
    await asyncio.wait([page.waitForXPath('//div/span[contains(@class,"city highlight")]', timeout=90000)])

    price = await page.xpath('//div[contains(@class,"column-price-flag")]')
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
    departure = await page.xpath('//div[contains(@class,"location-departure")]')
    arrival = await page.xpath('//div[contains(@class,"location-arrival")]')
    for d in departure:
        departure_txt = await page.evaluate('(element) => element.textContent', d)
        dep_info.append(departure_txt)
        dep_info = [x.replace('\n', '') for x in dep_info]
    new_dep_tim = [x[0:5] for x in dep_info]
    for a in arrival:
        arrival_txt = await page.evaluate('(element) => element.textContent', a)
        arr_times.append(arrival_txt)
        arr_times = [x.replace('\n', '') for x in arr_times]

    new_arr_tim = [x[0:5] for x in arr_times]
    for d,a,p in zip(new_dep_tim,new_arr_tim,prices):
        dict.append({
            'Origin': orgin_city,
            'Destination': dest_city,
            'Date': start_date,
            'DepartureTime': d,
            'ArrivalTime': a,
            'Price': p
        })
    print(dict)

asyncio.get_event_loop().run_until_complete(get_info('Berlin', 'Paris', datetime.datetime.today(),logger=None))
