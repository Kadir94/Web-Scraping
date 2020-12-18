from pyppeteer import launch
import asyncio
import time


async def get_info(orgin_city, dest_city, start_date, end_date):
    prices = []
    cities = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.fluege.de/', timeout=50000)
    await page.type('[id=f0-dep-location-]', orgin_city)
    await page.type('[id=f0-arr-location-]', dest_city)
    await page.click('[id=f0Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f0Date]', start_date)
    await page.click('[id=f1Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f1Date]', end_date)
    await page.keyboard.press('Enter')
    # await asyncio.wait([page.waitForXPath('//div/a[contains(@class, "js_select-airport")]',timeout=50000)])
    if await page.waitForXPath('//div/a[contains(@class, "js_select-airport")]',timeout=50000):
        await asyncio.wait(page.click('[class=main-airport]'))
    else:
        pass
    time.sleep(5)
    if await page.waitForXPath('//div/a[contains(@class, "parent-airport")]',Visible=True, timeout=50000):
        # clk = '[class=parent-airport]'
        await page.click('[class=main-airport]',visible=True)
    else:
        pass

    await asyncio.wait([page.waitForXPath('//div[contains(@class,"column-price-flag")]', timeout=90000)])
    await asyncio.wait([page.waitForXPath('//div/span[contains(@class,"city highlight")]', timeout=90000)])

    price = await page.xpath('//div[contains(@class,"column-price-flag")]')
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        prices.append(price_txt)
        prices = [x.replace('\n', '') for x in prices]
    print(prices)

    # city = await page.xpath('//div/span[contains(@class,"city highlight")]')
    # for c in city:
    #     city_txt = await page.evaluate('(element) => element.textContent', c)
    #     cities.append(city_txt)
    #     cities = [x.replace('\n', '') for x in cities]
    # print(cities)
    # print(dict(zip(prices,cities)))
asyncio.get_event_loop().run_until_complete(get_info('Germany','France','25.12.2020','28.12.2020'))
