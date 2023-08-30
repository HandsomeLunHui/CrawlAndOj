import os
import logging
import concurrent.futures
import requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

cookies = {
    'Hm_lvt_cec763d47d2d30d431932e526b7f1218': '1693381660',
    'Hm_lvt_a71b1bc761fe3f26085e79b5fd6a7f71': '1693381660',
    'cf_chl_2': 'dbf4aed0ada8f2c',
    'cf_clearance': '5P.bwSA4cN1LT4Eyu8CaofLjrlO3QZ4bp2eCrZcloO0-1693381680-0-1-7bdd61a2.23add0ae.ff578781-160.0.0',
    'jieqiVisitTime': 'jieqiArticlesearchTime%3D1693381685',
    'Hm_lpvt_cec763d47d2d30d431932e526b7f1218': '1693381686',
    'Hm_lpvt_a71b1bc761fe3f26085e79b5fd6a7f71': '1693381686',
    'jieqiVisitId': 'article_articleviews%3D80518',
    '__gads': 'ID=c759a4be0541cc95-221e930f56e30027:T=1693381687:RT=1693381687:S=ALNI_MabE3g2opPLggUYF5xXeHa5U6CSwg',
    '__gpi': 'UID=00000c36b5bb6394:T=1693381687:RT=1693381687:S=ALNI_MYnSiwlocIptW7LJyLAyVf4dz7tPg',
}

headers = {
    'authority': 'www.52bqg.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'Hm_lvt_cec763d47d2d30d431932e526b7f1218=1693381660; Hm_lvt_a71b1bc761fe3f26085e79b5fd6a7f71=1693381660; cf_chl_2=dbf4aed0ada8f2c; cf_clearance=5P.bwSA4cN1LT4Eyu8CaofLjrlO3QZ4bp2eCrZcloO0-1693381680-0-1-7bdd61a2.23add0ae.ff578781-160.0.0; jieqiVisitTime=jieqiArticlesearchTime%3D1693381685; Hm_lpvt_cec763d47d2d30d431932e526b7f1218=1693381686; Hm_lpvt_a71b1bc761fe3f26085e79b5fd6a7f71=1693381686; jieqiVisitId=article_articleviews%3D80518; __gads=ID=c759a4be0541cc95-221e930f56e30027:T=1693381687:RT=1693381687:S=ALNI_MabE3g2opPLggUYF5xXeHa5U6CSwg; __gpi=UID=00000c36b5bb6394:T=1693381687:RT=1693381687:S=ALNI_MYnSiwlocIptW7LJyLAyVf4dz7tPg',
    'referer': 'https://www.52bqg.org/modules/article/search.php?searchkey=%B5%C0%B9%EE%D2%EC%CF%C9&__cf_chl_tk=rrMdsFqmgFMKgFFQG4hWR21eRMY7wURGkeE24qTUmOM-1693381680-0-gaNycGzNCvs',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
}

# os.path.exists(f'../crawlNovel/{novelName}') or os.mkdir(f'../crawlNovel/{novelName}')
#
#
# # 获取章节目录
# def getDir():
#     logging.info('start get dir')
#     response = requests.get('https://www.52bqg.org/book_80518/', cookies=cookies, headers=headers)
#     doc = pq(response.text)
#     # global novelName
#     # novelName=doc('.box_con #maininfo #info h1').text()
#     dir=doc('dd:gt(11) a')
#     for item in dir.items():
#         name=item.text()
#         url=urljoin('https://www.52bqg.org/book_80518/',item.attr('href'))
#         yield name,url
#
# # 获取具体内容
# def getContents(name,url):
#     logging.info(f'start get content{name}')
#     response = requests.get(url, cookies=cookies, headers=headers)
#     doc = pq(response.text)
#     contents=doc('div#content')
#     content=''
#     for item in contents.items():
#         content+=item.text()
#     logging.info(f'start success content{name}')
#     return name,content
#
# # 写入文件
# def writeNovel(name,content):
#     logging.info(f'start write content{name}')
#     if os.path.exists(f'../crawlNovel/{novelName}/{name}.txt'):
#         logging.info(f'file exists{name}')
#         return
#
#     with open('../crawlNovel/'+novelName+'/'+name+'.txt','w',encoding='utf-8') as f:
#         f.write(content)
#     logging.info(f'start success content{name}')
#
#
# def main():
#     with ThreadPoolExecutor(max_workers=50) as executor:
#         futures = [executor.submit(getContents,name,url) for name,url in getDir()]
#         for future in as_completed(futures):
#             writeNovel(future.result()[0],future.result()[1])
#
#
# if __name__ == '__main__':
#     # url=urljoin('https://www.52bqg.org/book_80518/','54504305.html')
#     # content=getContents('hello',url)
#     main()


# 共享的 Session 对象，用于管理 cookies 和 headers
session = requests.Session()
# 小说的主页
indexUrl='https://www.52bqg.org/book_80518/'

def get_novel_dir(url):
    logging.info('Start getting directory')
    # url = 'https://www.52bqg.org/book_80518/'
    response = session.get(indexUrl,headers=headers,cookies=cookies)
    doc = pq(response.text)
    dir_links = doc('dd:gt(11) a')
    for link in dir_links.items():
        name = link.text()
        url = urljoin(indexUrl, link.attr('href'))
        yield name, url

def get_chapter_content(name, url):
    logging.info(f'Start getting content for {name}')
    response = session.get(url)
    doc = pq(response.text)
    content = doc('div#content').text()
    return name, content

def write_novel(name, content):
    logging.info(f'Start writing content for {name}')
    if not os.path.exists(f'../crawlNovel/{novelName}/{name}.txt'):
        with open(f'../crawlNovel/{novelName}/{name}.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f'Successfully wrote content for {name}')

def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(get_chapter_content, name, url) for name, url in get_novel_dir(indexUrl)]
        for future in as_completed(futures):
            name, content = future.result()
            write_novel(name, content)

if __name__ == '__main__':
    # novelName=input('请输入小说名：')
    novelName='道诡异仙'
    logging.info(f'Start crawling novel{novelName}')
    os.path.exists(f'../crawlNovel/{novelName}') or os.mkdir(f'../crawlNovel/{novelName}')
    main()
