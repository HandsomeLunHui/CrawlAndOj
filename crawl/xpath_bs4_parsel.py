from lxml import etree
from bs4 import BeautifulSoup
import json
import csv


# 读取xml文件
# html=etree.parse('./test.html',etree.HTMLParser())
# result=etree.tostring(html)
# print(result.decode('utf-8'))

# 使用xpath获取节点值或属性
# html=etree.parse('./test.html',etree.HTMLParser())
# result=html.xpath('//li/a[@class="entry-title"]//text()')
# print(result)

with open('./test.html',"r",encoding="utf-8") as f:
    html=f.read()
    soup=BeautifulSoup(html,'lxml')
    # print(soup.prettify())
    # print(soup.find_all(name="li"))
    for li in soup.select("a"):
        print(li.get_text())


    for li in soup.find_all(name="li"):
        print(type(li))
        print(li.get_text())
        print(li.attrs)


    # result=soup.select('li.entry-title a')[0].get_text()
    # print(result)

    # result=soup.select('li.entry-title a')[0].attrs['href']
    # print(result)

    # result=soup.select('li.entry-title a')[0].parent.parent.get_text()
    # print(result)

    # result=soup.select('li.entry-title a')[0].parent.parent.attrs['class']
    # print(result)

    # result=soup.select('li.entry-title a')[0].parent.parent.parent.get_text()
    # print(result)

    # result=soup.select('li.entry-title a')[0].parent.parent.parent.attrs['class']
    # print(result)

# json.dumps()
# json.loads()
# json之间的数据转换
