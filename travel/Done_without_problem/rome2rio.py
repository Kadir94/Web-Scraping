import asyncio
# from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from pyppeteer.page import PageError, Page
from pyppeteer.errors import TimeoutError
from logging import Logger
from typing import Dict
from pyppeteer import launch


async def get_info1(
        page: Page,
        country_id: int,
        origin: str,
        origin_id: int,
        destination: str,
        destination_id: int,
        logger: Logger) -> Dict:
    total_prices = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    while True:

        try:
            await page.goto('https://www.rome2rio.com', timeout=50000)
        except (TimeoutError, PageError):
            # logger.error(f'{DARK_PURPLE}Page either crushed or time exceeded{ENDE}')
            print("Page no loaded")
        try:
            cur = await page.waitForXPath('//div/ul/li[@class="navbar__users-settings"]', {'visible': True,'timeout': 5000})
            await cur.click()
        except Exception:
            print('no currency')
        try:
            euro = await page.waitForXPath('//div/ul/li/a[@data-id="EUR"]',{'visible': True, 'timeout': 5000})
            await euro.click()
        except Exception:
            print("no euro")
        try:
            await page.waitForXPath('//div[@class="search"]', {'visible': True, 'timeout': 5000})
            res_1 = True
        except TimeoutError:
            res_1 = False
        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-from")
            await page.type('#search-from', origin)
        except Exception:
            pass

        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search-to")
            await page.type('#search-to', destination)
            await page.keyboard.press('Enter')
        except Exception:
            pass

        try:
            await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#search_hotels:checked")
        except Exception:
            pass
        await page.evaluate('''(selector) => document.querySelector(selector).click()''', "#transport-search")
        results = None
        try:
            results = await page.waitForXPath('//div[@class="routes--mv js-route-list"]',
                                              {'visible': True, 'timeout': 10000})
            res_2 = True
        except TimeoutError:
            res_2 = False

        if res_1 and res_2:
            train_details = await results.xpath(
                '//div[@data-test="route:train"]/p/span[@class="route__price tip-west"]')
            if not train_details:
                train_details = await results.xpath(
                    '//div[@data-test="route:train,train"]/p/span[@class="route__price tip-west"]')

            bus_details = await results.xpath('//div[@data-test="route:bus"]/p/span[@class="route__price tip-west"]')
            night_bus_datails = await results.xpath(
                '//div[@data-test="route:nightbus"]/p/span[@class="route__price tip-west"]')
            rideshare_datails = await results.xpath(
                '//div[@data-test="route:rideshare"]/p/span[@class="route__price tip-west"]')
            car_details = await results.xpath('//div[@data-test="route:car"]/p/span[@class="route__price tip-west"]')
            tram_details = await results.xpath('//div[@data-test="route:tram"]/p/span[@class="route__price tip-west"]')
            ferry_details = await results.xpath(
                '//div[@data-test="route:carferry"]/p/span[@class="route__price tip-west"]')

            train_prices = ['train']
            bus_prices = ['bus']
            night_bus_prices = ['night_bus']
            ride_share_prices = ['ride_share']
            car_prices = ['car']
            tram_prices = ['tram']
            ferry_prices = ['ferry']
            for i in train_details:
                price_txt = await page.evaluate('(element) => element.textContent', i)
                train_prices.append(price_txt)
            for p in bus_details:
                price_txt = await page.evaluate('(element) => element.textContent', p)
                bus_prices.append(price_txt)
            for n in night_bus_datails:
                price_txt = await page.evaluate('(element) => element.textContent', n)
                night_bus_prices.append(price_txt)
            for r in rideshare_datails:
                price_txt = await page.evaluate('(element) => element.textContent', r)
                ride_share_prices.append(price_txt)
            for c in car_details:
                price_txt = await page.evaluate('(element) => element.textContent', c)
                car_prices.append(price_txt)
            for t in tram_details:
                price_txt = await page.evaluate('(element) => element.textContent', t)
                tram_prices.append(price_txt)
            for f in ferry_details:
                price_txt = await page.evaluate('(element) => element.textContent', f)
                ferry_prices.append(price_txt)

            prices_list = [
                tram_prices, bus_prices, night_bus_prices, ride_share_prices, car_prices, train_prices,ferry_prices]
            for prices in prices_list:
                prices = [x.replace('\xa0', '') for x in prices]
                prices = list(filter(None, prices))
                if len(prices) > 1:
                    for i in range(1, len(prices)):
                        new_1 = prices[i].replace('€', '')
                        new = new_1.split('-')
                        if float(new[0]) > float(new[-1]):
                            total_prices.append({'type': f'{prices[0]}', 'max': float(new[0]), 'min': float(new[-1])})
                        else:
                            total_prices.append({'type': f'{prices[0]}', 'max': float(new[-1]), 'min': float(new[0])})
                else:
                    total_prices.append({'type': f'{prices[0]}', 'max': 0, 'min': 0})

            total_data = {
                'country_id': country_id,
                'origin': origin,
                'origin_id': origin_id,
                'destination_id': destination_id,
                'destination': destination,

                'total_prices': total_prices,
                'status': 200  # Success
            }
            print(total_data)
        else:
            client = await page.target.createCDPSession()
            await client.send('Network.clearBrowserCookies')
            await client.send('Network.clearBrowserCache')


asyncio.get_event_loop().run_until_complete(
        get_info1(page=None, country_id=None, origin='Douglas', origin_id=None, destination='Dublin',
                 destination_id=None,
                 logger=Logger))
