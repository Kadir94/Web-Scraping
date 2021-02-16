from pyppeteer import launch
import asyncio
import pprint
import json

total_data = []


async def get_info():
    browser = await launch(headless=False, autoClose=True)
    page = await browser.newPage()
    await page.goto('https://www.backpackertrail.de/alle', timeout=90000)
    await page.setViewport({'width': 1200, 'height': 1000})
    countries = await page.xpath('//a[@class="tcb-button-link tcb-plain-text"]')
    country_names = []
    country_links = [await page.evaluate('(element) => element.getAttribute("href")', country) for country in countries]
    for country in country_links:
        con = country.split('/')
        con = list(filter(None, con))
        country_names.append(con[-1])
    i = 0
    for country, country_link in zip(country_names, country_links):
        await page.goto(country_link, timeout=90000)
        cities_list = await page.waitForSelector('ul.tve_clearfix', {'visible': True, 'timeout': 2000})
        cities_names = await cities_list.querySelectorAll('li span')
        cities = [await page.evaluate('(element) => element.textContent', city) for city in cities_names]
        descriptions_list = await page.waitForSelector('.tve_scT.tve_red', {'visible': True, 'timeout': 2000})
        cities_descriptions = await descriptions_list.querySelectorAll('.tcb-col.tve_empty_dropzone')
        descriptions = [await page.evaluate('(element) => element.textContent', description)
                        for description in cities_descriptions]
        list_dict = []

        for city, description in zip(cities, descriptions):
            list_dict.append({
                f'{city}': description
            })
        total_data.append({
            f'{country}': list_dict
        })
        with open(f'descriptions/{country.lower().replace("-", "_")}.json', "w") as write_file:
            json.dump(total_data, write_file)

asyncio.get_event_loop().run_until_complete(
    get_info())

