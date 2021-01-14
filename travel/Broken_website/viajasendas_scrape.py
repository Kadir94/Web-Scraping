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
    browser = await launch(headless=False, autoClose=False, width=1200, height=1200)
    page = await browser.newPage()
    await page.goto('https://www.viajesendas.com.ar/', timeout=90000)
    await page.waitForXPath('//div[contains(@class,"form-group")]',{'visible': True, 'timeout': 50000})
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div:nth-child(1) > input.origen-p10.form-control.ui-autocomplete-input")
    await page.type('#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div:nth-child(1) > input.origen-p10.form-control.ui-autocomplete-input', origin)
    suggestion_1 = None
    try:
        suggestion_1 = await page.waitForXPath('//html/body/div[contains(@class,"autocomplete-suggestions ")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_1:
        first_link_dep = await suggestion_1.xpath(".//*[@class='autocomplete-suggestion']")
        try:
            await first_link_dep[0].click()
        except Exception:
            logger.error('Did not work -> please write arrival')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div:nth-child(2) > input.destino-p10.form-control.ui-autocomplete-input")
    await page.type('#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div:nth-child(2) > input.destino-p10.form-control.ui-autocomplete-input', destination)
    suggestion_2 = None
    try:
        suggestion_2 = await page.waitForXPath('//html/body/div[8][contains(@class,"autocomplete-suggestions ")]',{'visible': True, 'timeout': 50000})
    except Exception:
        logger.info('No Possible suggestion')
    if suggestion_2:
        first_link_arr = await suggestion_2.xpath(".//*[@class='autocomplete-suggestion']")
        try:
            await first_link_arr[0].click()
        except Exception:
            logger.error('Did not work -> please write date')

    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div.contenedor-partida-regreso > div:nth-child(1) > input")
    await page.type('#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div.contenedor-partida-regreso > div:nth-child(1) > input', date)
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#mk-page-id-18 > div.theme-content.no-padding > div.wpb_row.vc_row.vc_row-fluid.mk-fullwidth-true.attched-false.vc_custom_1547652333664.js-master-row.mk-full-content-true > div > div > div > div > div > div > div > div > div > div > form > div > div > div.contenedor-inputs > div.contenedor-input.contenedor-boton > div > button")

asyncio.get_event_loop().run_until_complete(get_info('Buenos Aires', 'Santiago','11/1/2021'))

