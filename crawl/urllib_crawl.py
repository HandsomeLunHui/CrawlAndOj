import urllib.request
import urllib.parse

url="https://www.httpbin.org/post"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "host":"www.httpbin.org",
         }
dict={
    "name":"Germey"
}

data=bytes(urllib.parse.urlencode(dict),encoding="utf8")
req=urllib.request.Request(url=url,data=data,headers=headers,method="POST")
response=urllib.request.urlopen(req)
print(response.read().decode("utf8"))
