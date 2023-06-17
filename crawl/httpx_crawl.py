import httpx

# httpx默认有timeout超时时间5s 超过5s则会报错
# http client 推荐写法, headers赋值也是在这里面
with httpx.Client(http2=True,verify=False,timeout=None) as client:
    resp=client.get("https://spa16.scrape.center/")
    print(resp.text)
    print(resp.status_code)
    print(resp.headers)

# 异步客户端请求使用
# async with httpx.AsyncClient(http2=True,verify=False,timeout=None) as client:
#     resp=await client.get("https://spa16.scrape.center/")
#     print(resp.text)
#     print(resp.status_code)
#     print(resp.headers)

