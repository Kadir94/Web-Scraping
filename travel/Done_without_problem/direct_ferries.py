from pyppeteer import launch
import asyncio
import logging
import datetime
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    dep_infos = []
    prices = []
    list_dict = []
    car = "A4 Avant (2008 +)"
    date = date.strftime('%Y-%#m-%#d')
    await page.goto('https://www.directferries.de/', timeout=90000)
    await page.waitForXPath('//*[@id="deal_finder1"]/div/section/label',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > section.journey_type > label:nth-child(2)")

    await page.waitForXPath('//*[@id="route_outbound"]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#route_outbound")
    await page.type('#route_outbound', origin)
    await page.type('#route_outbound', destination)
    await asyncio.sleep(2)
    await page.waitForXPath('//*[@id="journey_route_parent"]/div/aside/ul/li',{'visible': True, 'timeout': 50000})
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
    await page.waitForXPath('//*[@id="deal_finder1"]/div/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div/section/section/ul/li/a',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > section.journey_info.hide_until_summary > section.trip_outbound.both_ways > ul:nth-child(4) > li:nth-child(3) > a")
    await page.waitForXPath('//div[@id="vehicle_base"]',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="vehicle_base"]/div/label',{'visible': True, 'timeout': 50000})

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#vehicle_base > div.popup_body > label:nth-child(4)")
    await page.waitForXPath('//div/fieldset[@class="car_make_fields"]',{'visible': True, 'timeout': 50000})
    car_list = await page.waitForXPath('//fieldset/ol[@class="item_list vehicle_make"]',{'visible': True, 'timeout': 50000})
    car_choice = await car_list.xpath('//li/label/input[@id="vehicle_make_outbound_32"]')
    await car_choice[0].click()

    model_choice = await page.waitForXPath('//div/fieldset/ol[contains(@class,"item_list vehicle_model")]',{'visible': True, 'timeout': 50000})
    model_options = await model_choice.xpath(f"//*[@id='deal_finder1']/div/aside/div/div/fieldset/ol/li/label[contains(text(),'{car}')]")
    await model_options[0].click()
    await page.waitForXPath('//*[@id="deal_finder1"]/div/aside/footer/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > aside > footer > button")
    await page.waitForXPath('//*[@id="deal_finder1"]/div/button',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#deal_finder1 > div.deal_finder_wrap > button")

    await page.waitForXPath('//*[@id="divQuotesContainer"]/div/div/div/div',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="divQuotesContainer"]/div/div/div/div/div',{'visible': True, 'timeout': 50000})
    dep_info = await page.xpath('//div/div[contains(@class,"ab-2062-col-1")]')
    price = await page.xpath('//div/div/b')
    for d in dep_info:
        dep_info_txt = await page.evaluate('(element) => element.textContent', d)
        dep_infos.append(dep_info_txt)
        dep_infos = [x.replace('\n', '') for x in dep_infos]
        dep_infos = [x.strip('                                                                        ') for x in dep_infos]
    del dep_infos[1::3]
    times = [x[75:90] for x in dep_infos]
    dep_time = times[0::2]
    arr_time = times[1::2]
    for p in price:
        price_txt = await page.evaluate('(element) => element.textContent', p)
        prices.append(price_txt)
    prices = prices[7::5]
    for d, a, p in zip(dep_time, arr_time, prices):
        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': date,
            'DepartureTime': d.strip('       '),
            'ArrivalTime': a.strip('        '),
            'Price': p
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data



asyncio.get_event_loop().run_until_complete(get_info('Calais ', '- Dover',datetime.datetime.today(),logger=None))




