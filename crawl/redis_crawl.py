from redis import StrictRedis,ConnectionPool

# 通过url构造
# url='redis://:217217@localhost:6379/0'
# pool=ConnectionPool.from_url(url)


#redis默认没有密码 所以构造的时候不用传入
redis=StrictRedis(host='localhost',port=6379,db=0)
# redis=StrictRedis(connection_pool=pool)
redis.set('jack','nihao')
print(redis.get('name'))
print(type(redis.get('name')))
print(redis.dbsize())

mail='''
626957925 <626957925@qq.com>; 1335435558 <1335435558@qq.com>; 1617984042 <1617984042@qq.com>; charmber <charmber@qq.com>; 530925206 <530925206@qq.com>; 415225449 <415225449@qq.com>; blogchen <blogchen@qq.com>; jlwen <jlwen@hnu.edu.cn>; 2015363056 <2015363056@mail.wtu.edu.cn>; 794861654 <794861654@qq.com>; 1054880760 <1054880760@qq.com>; 1252261273 <1252261273@qq.com>; jonas4wzw <jonas4wzw@stu.xju.edu.cn>; yangsl9822 <yangsl9822@163.com>; s200131043 <s200131043@stu.cqupt.edu.cn>; sxs17300289459 <sxs17300289459@163.com>; aliye511 <aliye511@sina.com>; 2568418021 <2568418021@qq.com>; 2033445094 <2033445094@QQ.com>; xichen0721 <xichen0721@163.com>; 2251220539 <2251220539@qq.com>; 423713382 <423713382@qq.com>; 1216881140 <1216881140@qq.com>; duanyujia000304 <duanyujia000304@qq.com>; 1115243090 <1115243090@qq.com>; qswxhn.ljy <qswxhn.ljy@qq.com>; zhangfengzhou_748 <zhangfengzhou_748@163.com>; xyzhangzhuoer <xyzhangzhuoer@163.com>; 414815934 <414815934@qq.com>; fahaxiki_jiahe <fahaxiki_jiahe@163.com>; 1183305910 <1183305910@qq.com>; leewooong <leewooong@outlook.com>; 893917377 <893917377@qq.com>; lunhui <2815807479@qq.com>; wenchen_1009 <wenchen_1009@163.com>; shiqi <shiqi@chd.edu.cn>; 2607509835 <2607509835@qq.com>; 835097324 <835097324@qq.com>; 893126465 <893126465@qq.com>; yangyssaltedfish <yangyssaltedfish@163.com>; yangyao228 <yangyao228@foxmail.com>; 762597665 <762597665@qq.com>; 17695619597 <17695619597@163.com>; 2020262492 <2020262492@mail.nwpu.edu.cn>; uestcsewz <uestcsewz@163.com>; 1015263901 <1015263901@qq.com>; 1440221774 <1440221774@qq.com>; 852356187 <852356187@qq.com>; junpengt <junpengt@163.com>; 1355868097 <1355868097@qq.com>; wetwer <wetwer@qq.com>; 403969930 <403969930@qq.com>; 2609571688 <2609571688@qq.com>; elssm0302 <elssm0302@gmail.com>; 1143774827 <1143774827@qq.com>; 849358823 <849358823@qq.com>; zhengzhang097 <zhengzhang097@gmail.com>; 893170152 <893170152@qq.com>; chengyu_gan <chengyu_gan@163.com>; 18811640851 <18811640851@163.com>; slaystart <slaystart@gmail.com>; yurui66666 <yurui66666@sina.com>; liuvickyhq <liuvickyhq@163.com>; zengyue97 <zengyue97@gmail.com>; jamieliang <jamieliang@foxmail.com>; 1357075020 <1357075020@qq.com>; 3219679788 <3219679788@qq.com>; 13920138984 <13920138984@139.com>; 1252436059 <1252436059@qq.com>
'''

mail_list=mail.split(';')
print(len(mail_list))
for it in mail_list:
    it=it.strip()
    if it:
        print(it)

# import requests
# import os
# from lxml import etree
# from bs4 import BeautifulSoup
#
#
# total=67
# index_url='https://www.xbookcn.net/book/abin/{page}.htm'
#
# cookies = {
#     '_gid': 'GA1.2.854632690.1688821839',
#     'cf_chl_2': '21139fa6526bbc9',
#     'cf_clearance': 'mGMaPc5b8kO.Tn_GkKQAltIYR3bR593Fkw2vsYuLxKo-1688821934-0-250',
#     '_ga': 'GA1.1.1173449167.1688821839',
#     '_ga_JKNXPWV2R8': 'GS1.1.1688821838.1.1.1688822018.0.0.0',
# }
#
# headers = {
#     'authority': 'www.xbookcn.net',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'cache-control': 'max-age=0',
#     # 'cookie': '_gid=GA1.2.854632690.1688821839; cf_chl_2=21139fa6526bbc9; cf_clearance=mGMaPc5b8kO.Tn_GkKQAltIYR3bR593Fkw2vsYuLxKo-1688821934-0-250; _ga=GA1.1.1173449167.1688821839; _ga_JKNXPWV2R8=GS1.1.1688821838.1.1.1688822018.0.0.0',
#     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
# }
#
# response = requests.post('https://www.xbookcn.net/book/abin/2.htm', cookies=cookies, headers=headers)
# response.encoding='gb2312'
# text=response.text
# print(text)
# soup=BeautifulSoup(text,'lxml')
# print(soup.title.string)


# print(response.text)