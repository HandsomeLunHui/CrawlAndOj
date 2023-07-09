import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
from pyppeteer.errors import TimeoutError
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

INDEX_URL='https://spa2.scrape.center/page/{page}'
DETAIL_URL = 'https://spa2.scrape.center'

TIME_OUT=10
TOTAL_PAGE=10

HEADLESS=False
WIDTH,HEIGHT=1366,764

browser,tab=None,None

async def init():
    # 使用全局变量方便其他函数调用
    global browser,tab
    # pyppeteer 使用的是launch创建一个browser对象
    browser=await launch(headless=HEADLESS,args=['--disable-infobars',f'--window-size={WIDTH},{HEIGHT}'])
    # 创建一个新页面
    tab=await browser.newPage()
    await tab.setViewport({'width':WIDTH,'height':HEIGHT})

# 定义一个通用的爬取函数
async def scrape_page(url,selector):
    logging.info('scraping %s',url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector,options={
            'timeout':TIME_OUT*100})
    except TimeoutError:
        logging.error('request %s timeout',url,exc_info=True)

# 爬取列表页
async def scrape_index(page):
    url=INDEX_URL.format(page=page)
    await scrape_page(url,'.item .name')

# 解析列表页url
async def parse_index():
    return await tab.querySelectorAllEval('.item .name','nodes=>nodes.map(node=>node.href)')

# 爬取详情页
async def scrape_detail(url):
    # 等待h2节点加载出来
    await scrape_page(url,'h2')

# 解析详情页
async def parse_detail():
    url=tab.url
    try:
        name=await tab.querySelectorEval('h2','node=>node.innerText')
        categories=await tab.querySelectorAllEval('.categories button span','nodes=>nodes.map(node=>node.innerText)')
        cover=await tab.querySelectorEval('.cover','node=>node.src')
        score=await tab.querySelectorEval('.score','node=>node.innerText')
        drama=await tab.querySelectorEval('.drama p','node=>node.innerText')

        return {
            'name':name,
            'categories':categories,
            'cover':cover,
            'score':score,
            'drama':drama,
        }

    except Exception  as e:
        logging.error(e)
async def main5():
    await init()
    try:
        for page in range(1,TOTAL_PAGE+1):
            await scrape_index(page)
            urls=await parse_index()
            for url in urls:
                await scrape_detail(url)
                detail=await parse_detail()
                logging.info('get detail:%s',detail)
    except Exception as e:
        logging.error(e)
    finally:
        await browser.close()

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

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main5())