from lxml.html import HtmlElement,fromstring

html=open('detail.html','r',encoding='utf-8').read()
element=fromstring(html)

# 标题提取
METAS=[
    '//meta[starts-with(@property,"og:title")]/@content',
    '//meta[starts-with(@name,"og:title")]/@content',
    '//meta[starts-with(@name,"title")]/@content',
    '//meta[starts-with(@property,"title")]/@content',
    '//meta[starts-with(@property,"page:image")]/@content',
]

def extract_by_meta(element:HtmlElement):
    for meta in METAS:
        title=element.xpath(meta)
        if title:
            return ''.join(title)
        
def extract_by_title(element:HtmlElement):
    return ''.join(element.xpath('//title/text()')).strip()

def extract_by_h(element:HtmlElement):
    hs=''.join(element.xpath('//h1/text()|//h2/text()|//h3/text()|//h4/text()')).strip()
    return hs or []

def similarity(s1,s2):
    if not s1 or not s2:
        return 0
    s1_set=set(list(s1))
    s2_set=set(list(s2))
    intersection=s1_set.intersection(s2_set)
    union=s1_set.union(s2_set)
    return len(intersection)/len(union)

# 取出标题
def extract_title(element:HtmlElement):
    title_extract_by_meta=extract_by_meta(element)
    title_extract_by_title=extract_by_title(element)
    title_extract_by_h=extract_by_h(element)

    if title_extract_by_meta:
        return title_extract_by_meta

    title_extract_by_h=sorted(title_extract_by_h,key=lambda x:similarity(x,title_extract_by_title),reverse=True)
    if title_extract_by_h:
        return title_extract_by_h[0]

    return title_extract_by_title