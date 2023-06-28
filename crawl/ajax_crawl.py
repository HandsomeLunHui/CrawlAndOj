import pymysql
import requests
import json
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

INDEX_URL='https://spa1.scrape.center/api/movie/'
DETAIL_URL='https://spa1.scrape.center/api/movie/{}/'
Total_page=10

data={
    'limit': 10,
    'offset': 10
}

def scrape_api(url,data):
    logging.info('scraping %s',url)
    try:
        response = requests.get(url,params=data)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error("error %s",e)
        return None

def scrape_index(page):
    data['offset'] = data['limit'] * (page - 1)
    return scrape_api(INDEX_URL,data)

def scrape_detail(id):
    url=DETAIL_URL.format(id)
    logging.info('scraping %s', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error("error %s", e)
        return None

def main():
    for page in range(1,Total_page+1):
        index_data=scrape_index(page)
        for item in index_data.get('results'):
            detail_data=scrape_detail(item.get('id'))
            name=item.get('name')
            publish=item.get('published_at')
            regions=item.get('regions')
            score=item.get('score')
            category=item.get('categories')
            drama=detail_data.get('drama')
            if detail_data:
                logging.info('detail data %s %s %s %s %s %s',name,publish,regions,score,category,drama)

if __name__ == '__main__':
    main()