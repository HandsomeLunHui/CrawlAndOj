import hashlib
import time
import requests
import json
import logging


class CoolMusic:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.headers={
        "cookie": "",  # 这里加上自己的cookie，有会员就可以下载付费音乐，自己充还是白嫖别人的就看各位了
        "authority": "complexsearch.kugou.com",
        "referer": "https://www.kugou.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        self.name=input('请输入音乐名称:')

    def getMd5(self):
        text = [
            "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
            "appid=1014",
            "bitrate=0",
            "callback=callback123",
            "clienttime={}".format(int(time.time() * 1000)),
            "clientver=1000",
            "dfid=4XSnWz14ZQos2PYFIl2MiDLH",
            "filter=10",
            "inputtype=0",
            "iscorrection=1",
            "isfuzzy=0",
            "keyword={}".format(self.name),
            "mid=8a6709b0f4f0674f12dabeb3a710313a",
            "page=1",
            "pagesize=30",
            "platform=WebFilter",
            "privilege_filter=0",
            "srcappid=2919",
            "token=",
            "userid=0",
            "uuid=8a6709b0f4f0674f12dabeb3a710313a",
            "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
        ]
        data = "".join(text)  # 变成字符串
        md5 = hashlib.md5(data.encode(encoding='utf-8')).hexdigest()  # md5加密
        return md5

    def searchMusic(self):
        url = "https://complexsearch.kugou.com/v2/search/song"
        params = {
            "callback": "callback123",
            "srcappid": "2919",
            "clientver": "1000",
            "clienttime": int(time.time() * 1000),
            "mid": "8a6709b0f4f0674f12dabeb3a710313a",
            "uuid": "8a6709b0f4f0674f12dabeb3a710313a",
            "dfid": "4XSnWz14ZQos2PYFIl2MiDLH",
            "keyword": f"{self.name}",
            "page": "1",
            "pagesize": "30",
            "bitrate": "0",
            "isfuzzy": "0",
            "inputtype": "0",
            "platform": "WebFilter",
            "userid": "0",
            "iscorrection": "1",
            "privilege_filter": "0",
            "filter": "10",
            "token": "",
            "appid": "1014",
            "signature": self.getMd5()
        }
        response=requests.get(url=url, headers=self.headers, params=params).text[12:-2]
        searchList = json.loads(response)
        musicList = searchList['data']['lists']
        for s, li in enumerate(musicList):
            ids = li['EMixSongID']
            AlbumName = li['SongName']
            singername = li['SingerName']
            print(s + 1, AlbumName, singername)
        return searchList

    def downloadContent(self):
        musicList=self.searchMusic()
        num=input("请输入下载的音乐序号:")
        ID = musicList['data']['lists'][int(num) - 1]['EMixSongID']
        self.name = musicList['data']['lists'][int(num) - 1]['SongName']
        urls = 'https://wwwapi.kugou.com/yy/index.php'
        params = {
            "r": "play/getdata",
            "callback": "jQuery19101351666471912658_1674051302167",
            "dfid": "4XSnWz14ZQos2PYFIl2MiDLH",
            "appid": "1014",
            "mid": "8a6709b0f4f0674f12dabeb3a710313a",
            "platid": "4",
            "encode_album_audio_id": f"{ID}",
            "_": "1674051302168"
        }
        response = json.loads(requests.get(url=urls, headers=self.headers, params=params).text[41:-2])
        last = response['data']['play_url']
        content = requests.get(url=last, headers=self.headers).content
        return content

    def writeMusic(self):
        content=self.downloadContent()
        with open('coolMusic/' + f'{self.name}.mp3', 'wb') as sp:
            sp.write(content)
            logging.info(f'{self.name}音乐下载成功')

    def main(self):
        self.writeMusic()


# name = input('请输入音乐名称:')
# text = [
#     "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
#     "appid=1014",
#     "bitrate=0",
#     "callback=callback123",
#     "clienttime={}".format(int(time.time() * 1000)),
#     "clientver=1000",
#     "dfid=4XSnWz14ZQos2PYFIl2MiDLH",
#     "filter=10",
#     "inputtype=0",
#     "iscorrection=1",
#     "isfuzzy=0",
#     "keyword={}".format(name),
#     "mid=8a6709b0f4f0674f12dabeb3a710313a",
#     "page=1",
#     "pagesize=30",
#     "platform=WebFilter",
#     "privilege_filter=0",
#     "srcappid=2919",
#     "token=",
#     "userid=0",
#     "uuid=8a6709b0f4f0674f12dabeb3a710313a",
#     "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
# ]
# data = "".join(text)  # 变成字符串
# md5 = hashlib.md5(data.encode(encoding='utf-8')).hexdigest()  # md5加密
#
# url = "https://complexsearch.kugou.com/v2/search/song"
# headers = {
#     "cookie": "",  # 这里加上自己的cookie，有会员就可以下载付费音乐，自己充还是白嫖别人的就看各位了
#     "authority": "complexsearch.kugou.com",
#     "referer": "https://www.kugou.com/",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
# }
# params = {
#     "callback": "callback123",
#     "srcappid": "2919",
#     "clientver": "1000",
#     "clienttime": int(time.time() * 1000),
#     "mid": "8a6709b0f4f0674f12dabeb3a710313a",
#     "uuid": "8a6709b0f4f0674f12dabeb3a710313a",
#     "dfid": "4XSnWz14ZQos2PYFIl2MiDLH",
#     "keyword": f"{name}",
#     "page": "1",
#     "pagesize": "30",
#     "bitrate": "0",
#     "isfuzzy": "0",
#     "inputtype": "0",
#     "platform": "WebFilter",
#     "userid": "0",
#     "iscorrection": "1",
#     "privilege_filter": "0",
#     "filter": "10",
#     "token": "",
#     "appid": "1014",
#     "signature": md5
# }
# lll = json.loads(requests.get(url=url, headers=headers, params=params).text[12:-2])
# kkk = lll['data']['lists']
# for s, li in enumerate(kkk):
#     ids = li['EMixSongID']
#     AlbumName = li['SongName']
#     singername = li['SingerName']
#     print(s + 1, AlbumName, singername)
#
#
# num = input('下载哪一个:')
# ID = lll['data']['lists'][int(num) - 1]['EMixSongID']
# name = lll['data']['lists'][int(num) - 1]['SongName']
# urls = 'https://wwwapi.kugou.com/yy/index.php'
# params = {
#     "r": "play/getdata",
#     "callback": "jQuery19101351666471912658_1674051302167",
#     "dfid": "4XSnWz14ZQos2PYFIl2MiDLH",
#     "appid": "1014",
#     "mid": "8a6709b0f4f0674f12dabeb3a710313a",
#     "platid": "4",
#     "encode_album_audio_id": f"{ID}",
#     "_": "1674051302168"
# }
# respons = json.loads(requests.get(url=urls, headers=headers, params=params).text[41:-2])
# last = respons['data']['play_url']
# downlode = requests.get(url=last, headers=headers).content
# with open('coolMusic/' + f'{name}.mp3', 'wb') as sp:
#     sp.write(downlode)
#     print(last)
#     print(f'{name}下载完成')

if __name__ == '__main__':
    music=CoolMusic()
    music.writeMusic()
