import requests
import re

# requests请求保存其他文件 使用resp.content
# resp=requests.get("https://ssr1.scrape.center/page/1",verify=False)
# with open("a.html","wb") as f:
#     f.write(resp.content)

# requests文件上传
# files={"file":open("a.html","rb")}
# resp=requests.post("https://ssr1.scrape.center/",files=files,verify=False)
# print(resp.text)

# 获取cookie
# resp=requests.get("https://ssr1.scrape.center/",verify=False)
# cookies=resp.cookies
# for key,value in cookies.items():
#     print(key+"="+value)

resp=requests.get("https://ssr1.scrape.center/",verify=False)
pattern=re.compile('<h2.*?>(.*?)</h2>',re.S)
result=re.findall(pattern,resp.text)
print(result)