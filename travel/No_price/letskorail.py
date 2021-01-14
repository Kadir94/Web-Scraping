from pyppeteer import launch
import asyncio
import logging


async def get_info(origin, destination,month,day,time):

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
    await page.goto('http://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1', timeout=90000)
    await page.waitForXPath('//*[@id="resrv_info"]/table',{'visible': True, 'timeout': 50000})
    await page.waitForXPath('//*[@id="slt_m01"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=slt_m01]',{'clickCount': 1})
    await page.type('[id=slt_m01]', month)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="slt_d01"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=slt_d01]',{'clickCount': 1})
    await page.type('[id=slt_d01]', day)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="slt_h01"]',{'visible': True, 'timeout': 50000})
    await page.click('[id=slt_h01]',{'clickCount': 1})
    await page.type('[id=slt_h01]', time)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="resrv_info"]/table/tbody/tr[4]/td/div[1]/input[1]',{'visible': True, 'timeout': 50000})
    await page.click('[id=resrv_info]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=resrv_info]', origin)
    await page.keyboard.press('Enter')
    await page.waitForXPath('//*[@id="resrv_info"]/table/tbody/tr[4]/td/div[2]/input[1]',{'visible': True, 'timeout': 50000})
    await page.click('[id=resrv_info]',{'clickCount': 3})
    await page.keyboard.press('Backspace')
    await page.type('[id=resrv_info]', destination)
    await page.keyboard.press('Enter')
    await page.evaluate('''(selector) => document.querySelector(selector).click()''',"#resrv_info > ul > li > a > img")
    await page.waitForXPath('//*[@id="contents"]/form[1]/div[2]/table',{'visible': True, 'timeout': 50000})
    elements = await page.xpath('//table/tbody/tr/td')
    elem = []
    dct = {'TYPE OFTRAVEL': [], 'TRAIN NO': [], 'TRAIN TYPE': [], 'FROM': [], 'TO': [], 'DEP.TIME': [], 'ARR.TIME': []}
    for e in elements:
        elements_txt = await page.evaluate('(element) => element.textContent', e)
        elem.append(elements_txt)
    new_elem = elem[7:]
    new_elem = [x.replace('\n', '') for x in new_elem]
    new_elem = [x.strip('                                                                                                                                                ') for x in new_elem]
    new_elem = [x for x in new_elem if x != '']
    new_elem = [x for x in new_elem if x != '-']
    print(new_elem)
    traveltype = new_elem[::7]
    trainNo = new_elem[1::7]
    trainType = new_elem[2::7]
    departure = new_elem[3::7]
    arrival = new_elem[4::7]
    dep_time = new_elem[5::7]
    arr_time = new_elem[6::7]
    for t in traveltype:
        dct['TYPE OFTRAVEL'].append(t)
    for n in trainNo:
        dct['TRAIN NO'].append(n)
    for r in trainType:
        dct['TRAIN TYPE'].append(r)
    for d in departure:
        dct['FROM'].append(d)
    for a in arrival:
        dct['TO'].append(a)
    for h in dep_time:
        dct['DEP.TIME'].append(h)
    for m in arr_time:
        dct['ARR.TIME'].append(m)

    print(dct)
asyncio.get_event_loop().run_until_complete(get_info('Seoul', 'Busan','2','6','9'))

