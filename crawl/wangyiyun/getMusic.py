import base64
import codecs
import math
import random
import requests
from Crypto.Cipher import AES
import logging

# 流程：根据输入关键字(可输入作者 区分要下载的歌曲)获取search列表
# 从search列表中获取id进行解密
# 完成下载

# 初始化loggin配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# search msg
# d='{"s":"黑铁的鱼影","limit":"8","csrf_token":""}'
# geturl msg
# d = '{"ids":"[2063718207]","level":"standard","encodeType":"aac","csrf_token":""}'


class CloudMusic:
    def __init__(self):
        self.musicHeaders = {
    'authority': 'music.163.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ntes_nnid=17866be70af721f36b19e492a321d2e3,1678173549905; _ntes_nuid=17866be70af721f36b19e492a321d2e3; NMTID=00OG2HNWpJL86Zs8kRetYkU3pKd-WUAAAGGuvA7dw; WM_TID=n0GBYSMt0%2BxFRBQEUROUPd%2BM7kQP8lh7; WEVNSM=1.0.0; WNMCID=sivnzh.1678173550624.01.0; __bid_n=187610fb2f9610537c4207; FPTOKEN=v3VlxJJCca5HZi/WPnjxtVnFlstJBJGYz/wj9Tm/TMsXdRQNZHIbjF+YhpWlBDrTuy4LbmsIPe4QQGQOs8PVLykf1E2H+KB4m5YlTSWwhLmJXFZ42aOls8y0zM+I6cjPoz4hHPGXutpI89S+hjWXxqygFuy13M3vRcF/jAUzf0zIN4my6/Cu+WkuXI2uOr6wciqpB/KdDQSW/hcl7VLtkY8/TPj7wzz4C6tK7adr2Qrv8NCMcOEzlcc3kpUv19YFlNOHuBNb3gdf+hZ2N2TpdWWnw+rvAk55eICKL4C90pSOJKlyhakzT++hUrcUW33C5VvvtjbpLRCuLoiMsWMRwU0RfnhaA7vsw1zaaCzwybsYIT0N6Q2yGYIn+e61tjhFSsD1Tw2lemnnlZZu54r07w==|7j6v1D5dWpdEbpy+Rzn9fErYga8UQ0qRu4TdMO0VmDA=|10|5fb92cbfed1ed845245ec70977944db6; Hm_lvt_f8682ef0d24236cab0e9148c7b64de8a=1689927544; vinfo_n_f_l_n3=bbe4f85b1b5795d8.1.0.1689927529736.0.1689928076247; JSESSIONID-WYYY=0UXIn0muuwykQh2D%2BbOxbJHbg5w978KVg%5CzhYhgSYTVm0hyDShQoHVGbdo5sams4I6YHtJqcbMNMC1KajNUn%2B0gv720RPmPH5ngN7D0E2Cv9w95xlIeWfeGetmoHlRmyqirVahy16cNunGey8%2F6uq025ojq%2FUYRmgiJz5MMBshUC9HPZ%3A1690687397532; _iuqxldmzr_=32; sDeviceId=YD-ofADAUUPT25EBlFUFQeRk9gki2zoqN5T; WM_NI=j5gUxxaqklPkr12Q7TpMbcO6FJ3Ly%2Bxmr8ewnZdLqVudQ3qr4QdAMUvcODCxdZO16NT%2BydhZ7GB6dTkxfENI37VeBmQislygb4dVEuvTr34JYNlIQ%2FsBdennTVajbH1RMzY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebbd85fbcab9cadb73b918a8ba2c15f869f9fb1d574fbefb98ab267f59a8983cb2af0fea7c3b92aaaeba9b6fb74a3afa58dd361b2effeb2b660b493ae84ce3e8696fdadfc21bcb3bed9e87dae86acadf45eb7bc9fd4f47af88faca2d05fb6bd81a5c274a88681d2b54698f5b785eb52f5998ed7e760a9a8aaa6cd43f1e99a86c16793b7bd8dfc6da2ecacb7c87fb68cbed4b7429b92a4aad425b19eac86ed66988aaf8be144f38e839bdc37e2a3; ntes_utid=tid._.Yejsr2HaKchEBxBVEFPRgpx0in39rJyv._.0; playerid=75198147',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
}
        self.searchHeaders={
    'authority': 'music.163.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ntes_nnid=17866be70af721f36b19e492a321d2e3,1678173549905; _ntes_nuid=17866be70af721f36b19e492a321d2e3; NMTID=00OG2HNWpJL86Zs8kRetYkU3pKd-WUAAAGGuvA7dw; WM_TID=n0GBYSMt0%2BxFRBQEUROUPd%2BM7kQP8lh7; WEVNSM=1.0.0; WNMCID=sivnzh.1678173550624.01.0; __bid_n=187610fb2f9610537c4207; FPTOKEN=v3VlxJJCca5HZi/WPnjxtVnFlstJBJGYz/wj9Tm/TMsXdRQNZHIbjF+YhpWlBDrTuy4LbmsIPe4QQGQOs8PVLykf1E2H+KB4m5YlTSWwhLmJXFZ42aOls8y0zM+I6cjPoz4hHPGXutpI89S+hjWXxqygFuy13M3vRcF/jAUzf0zIN4my6/Cu+WkuXI2uOr6wciqpB/KdDQSW/hcl7VLtkY8/TPj7wzz4C6tK7adr2Qrv8NCMcOEzlcc3kpUv19YFlNOHuBNb3gdf+hZ2N2TpdWWnw+rvAk55eICKL4C90pSOJKlyhakzT++hUrcUW33C5VvvtjbpLRCuLoiMsWMRwU0RfnhaA7vsw1zaaCzwybsYIT0N6Q2yGYIn+e61tjhFSsD1Tw2lemnnlZZu54r07w==|7j6v1D5dWpdEbpy+Rzn9fErYga8UQ0qRu4TdMO0VmDA=|10|5fb92cbfed1ed845245ec70977944db6; Hm_lvt_f8682ef0d24236cab0e9148c7b64de8a=1689927544; vinfo_n_f_l_n3=bbe4f85b1b5795d8.1.0.1689927529736.0.1689928076247; _iuqxldmzr_=32; sDeviceId=YD-ofADAUUPT25EBlFUFQeRk9gki2zoqN5T; WM_NI=j5gUxxaqklPkr12Q7TpMbcO6FJ3Ly%2Bxmr8ewnZdLqVudQ3qr4QdAMUvcODCxdZO16NT%2BydhZ7GB6dTkxfENI37VeBmQislygb4dVEuvTr34JYNlIQ%2FsBdennTVajbH1RMzY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebbd85fbcab9cadb73b918a8ba2c15f869f9fb1d574fbefb98ab267f59a8983cb2af0fea7c3b92aaaeba9b6fb74a3afa58dd361b2effeb2b660b493ae84ce3e8696fdadfc21bcb3bed9e87dae86acadf45eb7bc9fd4f47af88faca2d05fb6bd81a5c274a88681d2b54698f5b785eb52f5998ed7e760a9a8aaa6cd43f1e99a86c16793b7bd8dfc6da2ecacb7c87fb68cbed4b7429b92a4aad425b19eac86ed66988aaf8be144f38e839bdc37e2a3; ntes_utid=tid._.Yejsr2HaKchEBxBVEFPRgpx0in39rJyv._.0; JSESSIONID-WYYY=1Ia8Est1De6wEGlpKtRnJreMrVOz6l3KBcbnc1NlZPsyquPW9v7EQSqFlKAem5%5CqN%2BmBdJhiGP3iMC%2BnHgbtv%2BV%2FqtYGVsdeEE7pZssFpGdSv5X9rA1mu%2FNvZXmGQAgkh%2BDOE2%2BfCw4KVx8BTV4vAj3HB1H0q1Wv5g%5CFad4%2FckxBFbAl%3A1690694673176; playerid=22570659',
    'nm-gcore-status': '1',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com/search/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
}

        self.cookies = {
    '_ntes_nnid': '17866be70af721f36b19e492a321d2e3,1678173549905',
    '_ntes_nuid': '17866be70af721f36b19e492a321d2e3',
    'NMTID': '00OG2HNWpJL86Zs8kRetYkU3pKd-WUAAAGGuvA7dw',
    'WM_TID': 'n0GBYSMt0%2BxFRBQEUROUPd%2BM7kQP8lh7',
    'WEVNSM': '1.0.0',
    'WNMCID': 'sivnzh.1678173550624.01.0',
    '__bid_n': '187610fb2f9610537c4207',
    'FPTOKEN': 'v3VlxJJCca5HZi/WPnjxtVnFlstJBJGYz/wj9Tm/TMsXdRQNZHIbjF+YhpWlBDrTuy4LbmsIPe4QQGQOs8PVLykf1E2H+KB4m5YlTSWwhLmJXFZ42aOls8y0zM+I6cjPoz4hHPGXutpI89S+hjWXxqygFuy13M3vRcF/jAUzf0zIN4my6/Cu+WkuXI2uOr6wciqpB/KdDQSW/hcl7VLtkY8/TPj7wzz4C6tK7adr2Qrv8NCMcOEzlcc3kpUv19YFlNOHuBNb3gdf+hZ2N2TpdWWnw+rvAk55eICKL4C90pSOJKlyhakzT++hUrcUW33C5VvvtjbpLRCuLoiMsWMRwU0RfnhaA7vsw1zaaCzwybsYIT0N6Q2yGYIn+e61tjhFSsD1Tw2lemnnlZZu54r07w==|7j6v1D5dWpdEbpy+Rzn9fErYga8UQ0qRu4TdMO0VmDA=|10|5fb92cbfed1ed845245ec70977944db6',
    'Hm_lvt_f8682ef0d24236cab0e9148c7b64de8a': '1689927544',
    'vinfo_n_f_l_n3': 'bbe4f85b1b5795d8.1.0.1689927529736.0.1689928076247',
    'JSESSIONID-WYYY': '0UXIn0muuwykQh2D%2BbOxbJHbg5w978KVg%5CzhYhgSYTVm0hyDShQoHVGbdo5sams4I6YHtJqcbMNMC1KajNUn%2B0gv720RPmPH5ngN7D0E2Cv9w95xlIeWfeGetmoHlRmyqirVahy16cNunGey8%2F6uq025ojq%2FUYRmgiJz5MMBshUC9HPZ%3A1690687397532',
    '_iuqxldmzr_': '32',
    'sDeviceId': 'YD-ofADAUUPT25EBlFUFQeRk9gki2zoqN5T',
    'WM_NI': 'j5gUxxaqklPkr12Q7TpMbcO6FJ3Ly%2Bxmr8ewnZdLqVudQ3qr4QdAMUvcODCxdZO16NT%2BydhZ7GB6dTkxfENI37VeBmQislygb4dVEuvTr34JYNlIQ%2FsBdennTVajbH1RMzY%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6eebbd85fbcab9cadb73b918a8ba2c15f869f9fb1d574fbefb98ab267f59a8983cb2af0fea7c3b92aaaeba9b6fb74a3afa58dd361b2effeb2b660b493ae84ce3e8696fdadfc21bcb3bed9e87dae86acadf45eb7bc9fd4f47af88faca2d05fb6bd81a5c274a88681d2b54698f5b785eb52f5998ed7e760a9a8aaa6cd43f1e99a86c16793b7bd8dfc6da2ecacb7c87fb68cbed4b7429b92a4aad425b19eac86ed66988aaf8be144f38e839bdc37e2a3',
    'ntes_utid': 'tid._.Yejsr2HaKchEBxBVEFPRgpx0in39rJyv._.0',
    'playerid': '75198147',
}


        self.searchUrl='https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        self.MusicUrl="https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="

        self.e = '010001'
        self.f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g = '0CoJUm6Qyw8W8jud'



    def setGetMusicMsg(self,id):
        msg='{"ids":"['+str(id)+']","level":"standard","encodeType":"aac","csrf_token":""}'
        return msg

    def setGetSearchMsg(self,searchStr):
        msg='{"s":"'+searchStr+'","limit":"8","csrf_token":""}'
        return msg

    # wangyiyun音乐使用的同一加密流程
    def generate_str(self,length):
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for i in range(length):
            index = random.random() * len(str)
            index = math.floor(index)
            res = res + str[index]
        return res

    def AES_encrypt(self,text, key):
        iv = '0102030405060708'.encode('utf-8')
        text = text.encode('utf-8')
        pad = 16 - len(text) % 16
        text = text + (pad * chr(pad)).encode('utf-8')
        key = key.encode('utf-8')
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text.decode('utf-8')

    def RSA_encrypt(self,str, key, f):
        str = str[::-1]
        str = bytes(str, 'utf-8')
        sec_key = int(codecs.encode(str, encoding='hex'), 16) ** int(key, 16) % int(f, 16)
        return format(sec_key, 'x').zfill(256)

    def get_param(self,d, e, f, g):
        i = self.generate_str(16)
        encText = self.AES_encrypt(d, g)
        params = self.AES_encrypt(encText, i)
        encSecKey = self.RSA_encrypt(i, e, f)
        return params, encSecKey

    def getUrlJson(self,msg,url):
        encText, encSecKey = self.get_param(msg, self.e, self.f, self.g)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        res = requests.post(url, headers=self.searchHeaders, data=data, verify=False)
        if res.status_code == 200:
            return res.json()
        return {}

# headers = {
#     'authority': 'music.163.com',
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'content-type': 'application/x-www-form-urlencoded',
#     # 'cookie': '_ntes_nnid=17866be70af721f36b19e492a321d2e3,1678173549905; _ntes_nuid=17866be70af721f36b19e492a321d2e3; NMTID=00OG2HNWpJL86Zs8kRetYkU3pKd-WUAAAGGuvA7dw; WM_TID=n0GBYSMt0%2BxFRBQEUROUPd%2BM7kQP8lh7; WEVNSM=1.0.0; WNMCID=sivnzh.1678173550624.01.0; __bid_n=187610fb2f9610537c4207; FPTOKEN=v3VlxJJCca5HZi/WPnjxtVnFlstJBJGYz/wj9Tm/TMsXdRQNZHIbjF+YhpWlBDrTuy4LbmsIPe4QQGQOs8PVLykf1E2H+KB4m5YlTSWwhLmJXFZ42aOls8y0zM+I6cjPoz4hHPGXutpI89S+hjWXxqygFuy13M3vRcF/jAUzf0zIN4my6/Cu+WkuXI2uOr6wciqpB/KdDQSW/hcl7VLtkY8/TPj7wzz4C6tK7adr2Qrv8NCMcOEzlcc3kpUv19YFlNOHuBNb3gdf+hZ2N2TpdWWnw+rvAk55eICKL4C90pSOJKlyhakzT++hUrcUW33C5VvvtjbpLRCuLoiMsWMRwU0RfnhaA7vsw1zaaCzwybsYIT0N6Q2yGYIn+e61tjhFSsD1Tw2lemnnlZZu54r07w==|7j6v1D5dWpdEbpy+Rzn9fErYga8UQ0qRu4TdMO0VmDA=|10|5fb92cbfed1ed845245ec70977944db6; Hm_lvt_f8682ef0d24236cab0e9148c7b64de8a=1689927544; vinfo_n_f_l_n3=bbe4f85b1b5795d8.1.0.1689927529736.0.1689928076247; JSESSIONID-WYYY=0UXIn0muuwykQh2D%2BbOxbJHbg5w978KVg%5CzhYhgSYTVm0hyDShQoHVGbdo5sams4I6YHtJqcbMNMC1KajNUn%2B0gv720RPmPH5ngN7D0E2Cv9w95xlIeWfeGetmoHlRmyqirVahy16cNunGey8%2F6uq025ojq%2FUYRmgiJz5MMBshUC9HPZ%3A1690687397532; _iuqxldmzr_=32; sDeviceId=YD-ofADAUUPT25EBlFUFQeRk9gki2zoqN5T; WM_NI=j5gUxxaqklPkr12Q7TpMbcO6FJ3Ly%2Bxmr8ewnZdLqVudQ3qr4QdAMUvcODCxdZO16NT%2BydhZ7GB6dTkxfENI37VeBmQislygb4dVEuvTr34JYNlIQ%2FsBdennTVajbH1RMzY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebbd85fbcab9cadb73b918a8ba2c15f869f9fb1d574fbefb98ab267f59a8983cb2af0fea7c3b92aaaeba9b6fb74a3afa58dd361b2effeb2b660b493ae84ce3e8696fdadfc21bcb3bed9e87dae86acadf45eb7bc9fd4f47af88faca2d05fb6bd81a5c274a88681d2b54698f5b785eb52f5998ed7e760a9a8aaa6cd43f1e99a86c16793b7bd8dfc6da2ecacb7c87fb68cbed4b7429b92a4aad425b19eac86ed66988aaf8be144f38e839bdc37e2a3; ntes_utid=tid._.Yejsr2HaKchEBxBVEFPRgpx0in39rJyv._.0; playerid=75198147',
#     'origin': 'https://music.163.com',
#     'referer': 'https://music.163.com/',
#     'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
# }
#
# def get_song():
#     url="https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
#     e = '010001'
#     f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
#     g = '0CoJUm6Qyw8W8jud'
#     msg='{"ids":"[2063718207]","level":"standard","encodeType":"aac","csrf_token":""}'
#     encText,encSecKey=get_param(msg,e,f,g)
#     data={
#         'params':encText,
#         'encSecKey':encSecKey
#     }
#     res=requests.post(url,headers=headers,data=data,verify=False)
#     if res.status_code==200:
#         try:
#             return res.json()
#         except Exception as e:
#             print(e)
#             return {}
#     return {}
#
# def generate_str(length):
#     str='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#     res=''
#     for i in range(length):
#         index=random.random()*len(str)
#         index=math.floor(index)
#         res=res+str[index]
#     return res
#
# def AES_encrypt(text,key):
#     iv='0102030405060708'.encode('utf-8')
#     text=text.encode('utf-8')
#     pad=16-len(text)%16
#     text=text+(pad*chr(pad)).encode('utf-8')
#     key=key.encode('utf-8')
#     encryptor=AES.new(key,AES.MODE_CBC,iv)
#     encrypt_text=encryptor.encrypt(text)
#     encrypt_text=base64.b64encode(encrypt_text)
#     return encrypt_text.decode('utf-8')
#
# def RSA_encrypt(str,key,f):
#     str=str[::-1]
#     str=bytes(str,'utf-8')
#     sec_key=int(codecs.encode(str,encoding='hex'),16)**int(key,16) % int(f,16)
#     return format(sec_key, 'x').zfill(256)
#
# def get_param(d,e,f,g):
#     i=generate_str(16)
#     encText=AES_encrypt(d,g)
#     params=AES_encrypt(encText,i)
#     encSecKey=RSA_encrypt(i,e,f)
#     return params,encSecKey

if __name__ == '__main__':
    wy=CloudMusic()
    msg=wy.setGetSearchMsg('美丽的鳍')
    print(msg)
    print(wy.getUrlJson(msg,wy.searchUrl))