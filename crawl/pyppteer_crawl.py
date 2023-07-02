import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq



async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://spa2.scrape.center/')
    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names=[item.text() for item in doc('.item .name').items()]
    print('Names:',names)
    await browser.close()

# asyncio.get_event_loop().run_until_complete(main())

async def main2():
    width,height=1366,768
    browser=await launch()
    # 创建一个新窗口
    page=await browser.newPage()
    await page.setViewport({'width':width,'height':height})
    await page.goto('https://spa2.scrape.center/')
    await page.waitForSelector('.item .name')
    await page.screenshot({'path':'example.png'})
    dimensions=await page.evaluate('''()=>({
        return {
            width:document.documentElement.clientWidth,
            height:document.documentElement.clientHeight,
            deviceScaleFactor:window.devicePixelRatio,}
        })''')
    print(dimensions)
    await browser.close()


async def main3():
    width,height=1920,1080
    # window-size={},{} 设置窗口大小
    browser=await launch(headless=False,devtools=True,args=['--disable-infobars',f'--window-size={width},{height}'])
    # context=await browser.createIncognitoBrowserContext()  开启无痕模式
    page=await browser.newPage()
    await page.setViewport({'width':1920,'height':1080})
    await page.evaluateOnNewDocument('Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')
    await page.goto('https://spa2.scrape.center/')
    await asyncio.sleep(10)
    await browser.close()

async def main4():
    browser=await launch(headless=False)
    page=await browser.newPage()
    await page.goto('https://spa2.scrape.center/')
    page=await browser.newPage()
    await page.goto('https://www.baidu.com')
    pages=await browser.pages()
    print(pages)
    page1=pages[1]
    await page1.bringToFront()
    await asyncio.sleep(10)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main4())