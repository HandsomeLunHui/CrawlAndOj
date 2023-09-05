from concurrent.futures import ThreadPoolExecutor,as_completed
import logging
import os
import requests
import math

import sys

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# search url
# https://www.ximalaya.com/revision/search/main
# core: all
# kw: 盗墓笔记
# spellchecker: true
# device: iPhone
# live: true


# 参数为id 与 一共有多少条声音
# https://www.ximalaya.com/revision/play/v1/show?id=69424894&num=1&sort=0&size=30&ptype=0
# id: 69424894
# num: 1
# sort: 0
# size: 30
# ptype: 0

# 下载的url id 为 trackId
# https://www.ximalaya.com/revision/play/v1/audio?id=550969109&ptype=1
# id: 550969109
# ptype: 1

CONCURRENCY=5   # 最大并发量

def crawlJson(url,param):

    cookies = {
        'HMACCOUNT_BFESS': '03F529B1B5FEA2AD',
        'BDUSS_BFESS': 'XlLV2I4bE1EZHU2dGpySTBkZEtPeE1YY1hqRGlxeVhSbjg0NDMwanF6a0pkVDlrSVFBQUFBJCQAAAAAAAAAAAEAAAC7SBCMw9e~qsDKu~nC1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnoF2QJ6Bdkd',
        'HMTK': '1',
        'BAIDUID_BFESS': '8068B676A72F4952A6A4A7CD0F63D258:FG=1',
        'ZFY': 'lrObr34idldGhwxURNpGu8A:A9Qi6lIWlZlkxkRVGqVo:C',
        'ab_sr': '1.0.1_ZjRmZDRiMDVkM2UwY2U5ZGUwNWE3YzNmYWI2NWQxYTE3NWVlNmIxM2I5NzllYmRmZTA2NDMwNDFlYzJiNmIyODYyMTJhOWEzMjFmZmZhOTEzYWU1OWZjMDRkYTJmMjJjZDgzMGVjN2Q2ODBjNTI1MjBlMzc2ZjY4MmFhMGIzZTNkYTc0NTZhMDEyYzFkNTY3M2Q5MmZiMmZkZTIxOGE2OGUwMDI4YTJkMGRiMDkxNTMyYjQ4YTZiZTJkNzU1NTRi',
    }

    headers = {
        'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        # 'Cookie': 'HMACCOUNT_BFESS=03F529B1B5FEA2AD; BDUSS_BFESS=XlLV2I4bE1EZHU2dGpySTBkZEtPeE1YY1hqRGlxeVhSbjg0NDMwanF6a0pkVDlrSVFBQUFBJCQAAAAAAAAAAAEAAAC7SBCMw9e~qsDKu~nC1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnoF2QJ6Bdkd; HMTK=1; BAIDUID_BFESS=8068B676A72F4952A6A4A7CD0F63D258:FG=1; ZFY=lrObr34idldGhwxURNpGu8A:A9Qi6lIWlZlkxkRVGqVo:C; ab_sr=1.0.1_ZjRmZDRiMDVkM2UwY2U5ZGUwNWE3YzNmYWI2NWQxYTE3NWVlNmIxM2I5NzllYmRmZTA2NDMwNDFlYzJiNmIyODYyMTJhOWEzMjFmZmZhOTEzYWU1OWZjMDRkYTJmMjJjZDgzMGVjN2Q2ODBjNTI1MjBlMzc2ZjY4MmFhMGIzZTNkYTc0NTZhMDEyYzFkNTY3M2Q5MmZiMmZkZTIxOGE2OGUwMDI4YTJkMGRiMDkxNTMyYjQ4YTZiZTJkNzU1NTRi',
        'Referer': 'https://www.ximalaya.com/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        logging.info('scraping %s',url)
        response=requests.get(url,params=param,headers=headers,cookies=cookies)
        if response.status_code==200:
            return response.json()
    except Exception as e:
        logging.error('error occurred while scraping %s :%s',url,e)

def getSongId(response):
    if response:
        arry=[]
        for item in response['data']['album']['docs']:
            if item['vipType']==0 and item['vipFreeType']==0:
                arry.append([item['title'],item['playCount'],item['albumId'],item['tracksCount']])
        return arry

def crawlSoundId(albumId,number):
    soundUrl='https://www.ximalaya.com/revision/play/v1/show'
    for num in range(math.ceil(number/30)):
        param={
            'id': albumId,
            'num': num+1,
            'sort': 0,
            'size': 30,
            'ptype': 0,
        }
        respnse=crawlJson(soundUrl,param)
        yield respnse['data']['tracksAudioPlay']

def crawlDownloadUrl(soundId,name):
    url='https://www.ximalaya.com/revision/play/v1/audio'
    param={
        'id': soundId,
        'ptype': 1,
    }
    respnse=crawlJson(url,param)
    return name,respnse['data']['src']

def getContent(url):
    response=requests.get(url)
    if response.status_code==200:
        return response.content

def writeToFile(name,content):
    logging.info(f'Start writing content for {name}')
    if not os.path.exists(f'../crawlXimaLaya/{songName}/{name}.mp3'):
        with open(f'../crawlXimaLaya/{songName}/{name}.mp3', 'wb') as f:
            f.write(content)
        logging.info(f'Successfully wrote content for {name}')
    else:
        logging.info(f'File exists for {name}')

def main(kw):
    searchUrl='https://www.ximalaya.com/revision/search/main'
    param = {
        'core': 'all',
        'kw': kw,
        'spellchecker': 'true',
        'device': 'iPhone',
        'live': 'true'
    }
    ret=crawlJson(searchUrl,param)
    songList=getSongId(ret)
    for index,item in enumerate(songList):
        print(index,item)

    while True:
        num = input('请选择下载的序号：')
        if num == 'n':
            logging.info('exit')
            sys.exit(0)
        else:
            try:
                num = int(num)
                break
            except:
                print('请输入合法选项!')
    os.path.exists(f'../crawlXimaLaya/{kw}') or os.mkdir(f'../crawlXimaLaya/{kw}')

    albumId=songList[num][2]
    number=songList[num][3]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures=[executor.submit(crawlDownloadUrl,id['trackId'],id['trackName']) for soundId in crawlSoundId(albumId,number) for id in soundId]
        for future in as_completed(futures):
            name,content=future.result()
            writeToFile(name,getContent(content))

if __name__ == '__main__':
    songName = input('请输入搜索的有声书名：')
    main(songName)
