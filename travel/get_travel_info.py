from pyppeteer import launch
import asyncio


async def get_info(orgin_city, dest_city, start_date, end_date):
    browser = await launch(headless=False,autoClose=False)
    page = await browser.newPage()
    await page.goto('https://www.fluege.de/', )
    await page.type('[id=f0-dep-location-]', orgin_city)
    await page.type('[id=f0-arr-location-]', dest_city)
    await page.click('[id=f0Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f0Date]', start_date)
    await page.click('[id=f1Date]', {'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=f1Date]', end_date)
    await page.keyboard.press('Enter')
    await asyncio.wait([page.waitForSelector('div.price js_regularCustomerPrice-active')])

    price = await page.querySelectorAll('div.price js_regularCustomerPrice-active')
    for i in price:
        price_txt = await page.evaluate('(element) => element.textContent', i)
        print(price_txt)

asyncio.get_event_loop().run_until_complete(get_info('Paris CDG','Berlin SXF','20.12.2020','25.12.2020'))
