from playwright.sync_api import sync_playwright
import requests
import os
import logging

# https://music.163.com/#/search/m/?id=1406025645&s={}&type=1

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

os.path.exists('music') or os.mkdir('music')

class CrawlWangyiyun:
    def __init__(self):
        self.name=input('请输入搜索的音乐信息：')
        self.json=None
        self.downloadNumber=0
        self.musicInfo=[]
        self.downloadInfo={}

    # 拦截请求
    def on_response(self,response):
        if 'weapi/cloudsearch/get/' in response.url and response.status == 200:
            self.json=response.json()

    def _crawlSearchHtml(self):
        with sync_playwright()  as p:
            logging.info('start crawl music info')
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"})
            page.on('response',self.on_response)
            page.goto(f"https://music.163.com/#/search/m/?id=1406025645&s={self.name}&type=1")
            page.wait_for_load_state('load')
            browser.close()
            logging.info('crawl music info success')

    def _getMusicId(self):
        if self.json:
            for key,item in enumerate(self.json['result']['songs']):
                self.musicInfo.append({
                        'key':key,
                        'id':item['id'],
                        'name':item['name'],
                        'album':item['al']['name'],
                        'singer':item['ar'][0]['name'],})

    def _choiceMusic(self):
        for item in self.musicInfo:
            print(f'{item["key"]}、{item["name"]}--{item["singer"]}--{item["album"]}')
        while True:
            choice=int(input('请输入下载歌曲的序号<int>：'))
            if isinstance(choice,int):
                self.downloadNumber=choice
                break
            else:
                print('这不是合法的选项')
        self.downloadInfo=self.musicInfo[self.downloadNumber]

    def _downloadMusic(self):
        logging.info('start download music')
        musicId=self.downloadInfo['id']
        name=self.downloadInfo['name']
        downloadUrl=f'http://music.163.com/song/media/outer/url?id={musicId}'
        resp=requests.get(downloadUrl)
        if resp.status_code==200:
            with open('music/'+name+'.mp3','wb') as f:
                f.write(resp.content)
                logging.info('download music success')
        else:
            logging.info('download music fail')

    def main(self):
        self._crawlSearchHtml()
        self._getMusicId()
        self._choiceMusic()
        self._downloadMusic()

if __name__ == '__main__':
    wangyiyun=CrawlWangyiyun()
    wangyiyun.main()

