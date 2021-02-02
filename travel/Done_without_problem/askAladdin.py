from pyppeteer import launch
import asyncio
import logging
import time
import sys


async def get_info(page,country_id,origin,origin_id, destination,destination_id,total_size,hash_id,order,date,logger):

    info = []
    trip1 = None
    trip2 = None
    trip3 = None
    trip4 = None
    list_dict = []
    await page.goto('https://ask-aladdin.com/egypt-transport-system/bus-timetables/', timeout=200000)
    await page.waitForXPath('//div/div/div/h4/a[contains(@class,"accordion-toggle collapsed")]',{'visible': True, 'timeout': 50000})
    while True:
        try:
            trip1 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+destination}")]',timeout=1000)
        except Exception:
            logger.info('trip1 can not found')
        if trip1:
            await trip1.click()
            break
        elif trip1 is None:
            try:
                trip2 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{"From"+" "+origin+" "+"to"+" "+destination}")]',timeout=1000)
            except Exception:
                logger.info('trip2 can not found')
        if trip2:
            await trip2.click()
            break
        elif trip2 is None:
            try:
                trip3 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+" "+"to"+" "+"the"+" "+destination}")]',timeout=1000)
            except Exception:
                logger.info('trip3 can not found')
        if trip3:
            await trip3.click()
            break
        elif trip3 is None:
            try:
                trip4 = await page.waitForXPath(f'//div/h4/a[contains(text(),"{origin+"/"+destination}")]',timeout=1000)
            except Exception:
                logger.info('trip3 can not found')
        if trip4:
            await trip4.click()
            break
        else:
            logger.info('No trip in Given Locations')
            break
    chosen = await page.xpath('//div/div[@aria-expanded="true"]/div/div/div/table/tbody/tr/td')
    for i in chosen:
        name = await page.evaluate('(element) => element.textContent', i)
        info.append(name)
    company = info[3::3]
    dep_time = info[4::3]
    price = info[5::3]

    for (c,d,p) in zip(company,dep_time,price):
        list_dict.append({
            'country_id': country_id,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'Date': date,
            'DepartureTime': d,
            'ArrivalTime': None,
            'Price': p
        })
    total_data = {
        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
    }
    return total_data


# asyncio.get_event_loop().run_until_complete(get_info('Cairo', 'Alexandria',date=None,logger=None))

