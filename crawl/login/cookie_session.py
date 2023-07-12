import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BASE_URL='https://login2.scrape.center/'
login_url=urljoin(BASE_URL, '/login')
index_url=urljoin(BASE_URL,'/page/1')

USERNAME='admin'
PASSWORD='admin'

# 使用requests进行请求比较繁琐
# response=requests.post(login_url,data={
#     'username':USERNAME,
#     'password':PASSWORD
# },allow_redirects=False)
#
# cookies=response.cookies
# print(cookies)
#
# response_index=requests.get(index_url,cookies=cookies)
# print(response_index.status_code)
# print(response_index.request.headers)
# print(response_index.url)
# print(response_index.text)

num=0
# 使用session会自动保存每次请求后设置的cookies
# session=requests.Session()
# session.post(login_url,data={
#     'username':USERNAME,
#     'password':PASSWORD
#     })
#
# cookies=session.cookies
# print(cookies)
#
# response=session.get(index_url)
#
# print(response.status_code)
# print(response.text)

# 使用selenium模拟浏览器操作

browser=webdriver.Chrome()
browser.get(BASE_URL)
# css 选择器
browser.find_element(By.CSS_SELECTOR,'input[name="username"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[name="password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
time.sleep(10)

cookies=browser.get_cookies()
print(cookies)

# 将cookie赋值给session
session=requests.Session()
for cookie in cookies:
    print(cookie['name'],cookie['value'])
    session.cookies.set(cookie['name'],cookie['value'])

response=session.get(index_url)
print(response.status_code)
print(response.url)