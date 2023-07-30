from playwright.sync_api import sync_playwright
import time
import requests
from collections.abc import MutableMapping
BASE_URL = 'https://spa2.scrape.center/'
INDEX_URL = BASE_URL + '/api/movie?limit={limit}&offset={offset}&token={token}'
MAX_PAGE = 10
LIMIT = 10
content = sync_playwright().start()
browser = content.chromium.launch()
page = browser.new_page()
# 用于替换浏览器加载的js文件
page.route = {
    '/js/chunk-10192a00.243cb8b7.js',
    lambda route: route.fulfill(path='./chunk.js')
}
page.goto(BASE_URL)
page.wait_for_load_state('networkidle')
def get_token(offset):
    result = page.evaluate('''
        return window.encrypt("%s", "%s")
    ''' % ('/api/movie', offset))
    return result
for i in range(MAX_PAGE):
    offset = LIMIT * i
    token = get_token(offset)
    url = INDEX_URL.format(limit=LIMIT, offset=offset, token=token)
    print(url)
    response = requests.get(url)
    print(response.json())
    time.sleep(1)