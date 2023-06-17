import requests
import logging
import re
from urllib.parse import urljoin
import os
import json
import multiprocessing


logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
TOTAL_PAGE=10
RESULTS_DIR = "results"
# 判断文件夹是否存在 不存在则创建
os.path.exists(RESULTS_DIR) or os.mkdir(RESULTS_DIR)

class Scrape():
    def __init__(self):
        self.BASE_URL="https://ssr1.scrape.center/"


    # 获取每页的信息
    def scrape_page(self,url):
         logging.info(f"scraping page {url}")
         try:
             response=requests.get(url,verify=False)
             if response.status_code==200:
                 return response.text
             logging.error(f"error scraping page {url}")
             return None
         except Exception as e:
             # 将logging.error里面的exc_info参数设置为True即可打印堆栈信息
             # logging.error(f"error scraping page {url}",exc_info=True)
             logging.error(f"error scraping page {url}")

             return None

    # 获取列表页
    def scrape_index(self,page):
        # 设置每个列表页的url
        index_url=urljoin(self.BASE_URL,f"page/{page}")
        return self.scrape_page(index_url)

    # 获取每个详情页的url
    def scrape_url(self,html):
        pattern=re.compile('<a.*?href="(.*?)".*?class="name"',re.S)
        detail_urls=re.findall(pattern,html)

        if not detail_urls:
            return []
        for detail_url in detail_urls:
            detail_url=urljoin(self.BASE_URL,detail_url)
            yield detail_url

    # 获取详情页
    def scrape_detail(self,url):
        return self.scrape_page(url)

    # 解析详情页
    def parse_detail(self,html):
        cover_pattern=re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover"',re.S)
        name_pattern=re.compile('<h2.*?>(.*?)</h2></a>',re.S)
        category_pattern=re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>',re.S)
        publish_pattern=re.compile('(\d{4}-\d{2}-\d{2})\s?上映',re.S)
        drama_pattern=re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>',re.S)
        score_pattern=re.compile('<p.*?score.*?>(.*?)</p>',re.S)

        cover=re.search(cover_pattern,html).group(1).strip() if re.search(cover_pattern,html) else None
        name=re.search(name_pattern,html).group(1).strip() if re.search(name_pattern,html) else None
        category=re.findall(category_pattern,html) if re.findall(category_pattern,html) else []
        publish=re.search(publish_pattern,html).group(1) if re.search(publish_pattern,html) else None
        drama=re.search(drama_pattern,html).group(1).strip() if re.search(drama_pattern,html) else None
        score=re.search(score_pattern,html).group(1).strip() if re.search(score_pattern,html) else None

        return {
            "cover":cover,
            "name":name,
            "category":category,
            "publish":publish,
            "drama":drama,
            "score":score
        }

    # 将数据保存为json文件 json.dump()
    def save_data(self,data):
        name=data.get("name")
        data_path=os.path.join(RESULTS_DIR,f"{name}.json")
        json.dump(data,open(data_path,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

def main(page):
    scrape=Scrape()
    # 获取每个index页面的html
    html=scrape.scrape_index(page)
    # 获取每个index页面中每个电影详情页的url列表
    detail_urls=scrape.scrape_url(html)
    for detail_url in detail_urls:
        # 获取每个详情页的html
        detail_html=scrape.scrape_detail(detail_url)
        # 解析数据
        result=scrape.parse_detail(detail_html)
        logging.info("get detail data %s",result)
        logging.info("save data to json file")
        scrape.save_data(result)
        logging.info("save data successfully")

if __name__ == '__main__':
    # 创建进程池
    pool=multiprocessing.Pool()
    pages=range(1,TOTAL_PAGE+1)
    pool.map(main,pages)
    pool.close()
    pool.join()

