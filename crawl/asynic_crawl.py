import asyncio
import logging
import time
import aiohttp
import json
import os

# def test():
#     # 函数加上 async 关键字之后调用不会执行 而是返回一个协程对象
#     async def excute(x):
#         print(f"number: {x}")
#         return x
#
#     async def request():
#         print("start")
#         r = requests.get("https://www.baidu.com")
#         return r.status_code
#
#
#     tasks=[asyncio.ensure_future(request()) for _ in range(5)]
#
#     print("Tasks:",tasks)
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait(tasks))
#
#     for task in tasks:
#         print(task.result())
#
#     print("end")

# def study():
#     start=time.time()
#
#     async def get(url):
#         # 创建一个session对象
#         session = aiohttp.ClientSession()
#         response = await session.get(url)
#         # await 关键字将耗时等待的操作挂起 让出控制权
#         await response.text()
#         await session.close()
#         return response
#
#     async def request():
#         url="https://www.httpbin.org/delay/5"
#         print('waiting for:',url)
#         r = await get(url)
#         print('get response from:',url,r)
#
#     tasks=[asyncio.ensure_future(request()) for _ in range(5)]
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait(tasks))
#
#     end=time.time()
#     print('cost time:',end-start)
#
# def test_aio():
#     async def fetch(session,url):
#         async with session.get(url) as response:
#             return await response.text()
#     async def main():
#         async with aiohttp.ClientSession() as session:
#             html=await fetch(session,'http://www.baidu.com')
#             print(html)
#     loop=asyncio.get_event_loop()
#     loop.run_until_complete(main())
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://www.baidu.com') as response:
#             # 因为response.text 是协程对象
#             print(await response.text())
#
# asyncio.get_event_loop().run_until_complete(main())

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# data={
#     'limit':18,
#     'offset':0
# }

INDEX_URL='https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL='https://spa5.scrape.center/api/book/{id}'

PAGE_SIZE=18
PAGE_NUMBER=100
CONCURRENCY=5   # 最大并发量

semaphore=asyncio.Semaphore(CONCURRENCY)
session=None

async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s',url)
            async with session.get(url) as response:
                return await response.json()
        except Exception as e:
            logging.error('error occurred while scraping %s :%s',url,e)

async def scrape_index(page):
    offset=PAGE_SIZE*(page-1)
    url=INDEX_URL.format(offset=offset)
    return await scrape_api(url)

async def save_data(data):
    filename=os.path.join('aioBook',f'{data.get("name")}.json')
    logging.info('saving %s',filename)
    json.dump(data,open(filename,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

async def scrape_detail(id):
    url=DETAIL_URL.format(id=id)
    data=await scrape_api(url)
    await save_data(data)

async def main():
    global session
    session=aiohttp.ClientSession()
    scrape_index_tasks=[asyncio.ensure_future(scrape_index(page)) for page in range(1,PAGE_NUMBER+1)]
    results=await asyncio.gather(*scrape_index_tasks)
    ids=[]
    for result in results:
        if not result:continue
        for item in result.get('results'):
            ids.append(item.get('id'))
    logging.info('results %s',json.dumps(results,ensure_ascii=False,indent=2))
    scrape_detail_tasks=[asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    await session.close()

    # scrape_detail_tasks=[asyncio.ensure_future(scrape_detail(id)) for id in ids]
    # results=await asyncio.gather(*scrape_detail_tasks)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())