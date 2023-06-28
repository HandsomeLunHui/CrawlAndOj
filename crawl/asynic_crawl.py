import asyncio
import time
import aiohttp
import requests


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

start=time.time()

async def get(url):
    # 创建一个session对象
    session = aiohttp.ClientSession()
    response = await session.get(url)
    # await 关键字将耗时等待的操作挂起 让出控制权
    await response.text()
    await session.close()
    return response

async def request():
    url="https://www.httpbin.org/delay/5"
    print('waiting for:',url)
    r = await get(url)
    print('get response from:',url,r)

tasks=[asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))



end=time.time()
print('cost time:',end-start)
