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
    infos = []
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.tracopacr.com/Rutas_Horarios', timeout=90000)
    await page.waitForXPath('//*[@id="select2-input_origen-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-input_origen-container]',{'clickCount': 1})
    await page.waitForXPath('//span/input[contains(@class,"select2-search__field")]',{'visible': True, 'timeout': 50000})
    await page.type('body > span > span > span.select2-search.select2-search--dropdown > input', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath('//span/span[contains(@class,"select2-results")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_1:
        first_link_dep = await suggestion_1.xpath(".//*[@class='select2-results__options']")
        try:
            await first_link_dep[0].click()
        except Exception:
                logger.error('Did not work -> please write arrival')
    await asyncio.sleep(2)
    await page.waitForXPath('//*[@id="select2-input_destino-container"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=select2-input_destino-container]',{'clickCount': 1})
    await page.waitForXPath('//span/input[contains(@class,"select2-search__field")]',{'visible': True, 'timeout': 50000})
    await page.type('body > span > span > span.select2-search.select2-search--dropdown > input', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//span/span[contains(@class,"select2-results")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_2:
        first_link_arr = await suggestion_2.xpath(".//*[@class='select2-results__options']")
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> please write date')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#input_fecha")
    await page.type('#input_fecha', date)
    await asyncio.sleep(3)
    await page.waitForXPath('//table[contains(@class,"datatable_horarios table table-striped table-bordered dataTable no-footer")]',{'visible': True, 'timeout': 50000})
    info = await page.xpath('//table/tbody/tr[contains(@role,"row")]')
    for i in info:
        info_txt = await page.evaluate('(element) => element.textContent', i)
        infos.append(info_txt)
        infos = [x.replace('\n', '') for x in infos]
        infos = [x.strip('           ') for x in infos]
    departure = [x[48:53] for x in infos]
    dep_loc = [x[65:85] for x in infos]
    arr_loc = [x[87:107] for x in infos]
    print(departure)
    print(dep_loc)
    print(arr_loc)

asyncio.get_event_loop().run_until_complete(get_info('SAN MATEO OROTINA', 'SELECCIONE UN LUGAR','18012021'))

