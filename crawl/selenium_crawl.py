from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
from urllib.parse import urljoin
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s')

INDEX_URL='https://spa2.scrape.center/page/{}'
DETAIL_URL = 'https://spa2.scrape.center'

TIME_OUT=10
TOTAL_PAGE=10

option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)
# 设置浏览器无头模式
# option.add_argument('--headless')

browser = webdriver.Chrome(options=option)
# 设置等待延迟
wait = WebDriverWait(browser, TIME_OUT)

def scrape_page(url,condition,locator):
    logging.info('scraping %s',url)
    try:
        # 加载页面
        browser.get(url)
        # 采用指定条件监听页面
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('loading page %s timeout',url)

def scrape_index(page):
    url = INDEX_URL.format(page)
    logging.info(url)
    scrape_page(url,EC.visibility_of_element_located,(By.CSS_SELECTOR,'#index .item'))

def parse_index():
    elements=browser.find_elements(By.CSS_SELECTOR,'#index .item')
    for item in elements:
        # get_attribute 获取指定属性 如href class
        href=item.find_element(By.TAG_NAME,'a').get_attribute('href')
        # yield返回一个迭代器对象
        yield urljoin(DETAIL_URL,href)

def scrape_detail(url):
    scrape_page(url,condition=EC.visibility_of_element_located,
                locator=(By.TAG_NAME,'h2'))

def parse_detail(url):
    # 如果成功执行scrape_detail 没有抛出异常则证明执行成功
    url=browser.current_url
    name=browser.find_element(By.TAG_NAME,'h2').text
    categories=[element.text for element in browser.find_elements(By.CSS_SELECTOR,'.categories button span')]
    cover=browser.find_element(By.CSS_SELECTOR,'.cover').get_attribute('src')
    score=browser.find_element(By.CSS_SELECTOR,'.score').text
    drama=browser.find_element(By.CSS_SELECTOR,'.drama p').text
    return {
        'name':name,
        'categories':categories,
        'cover':cover,
        'score':score,
        'drama':drama
    }

def main():
    try:
        for page in range(1,TOTAL_PAGE+1):
            scrape_index(page)
            urls=parse_index()
            # logging.info(list(urls))
            for url in list(urls):
                scrape_detail(url)
                result=parse_detail(url)
                logging.info(result)

    except Exception as e:
        logging.error(e)
    finally:
        browser.close()

def test():
    browser = webdriver.Chrome()
    # url='http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    # browser.get(url)
    # browser.switch_to.frame('iframeResult')
    # source = browser.find_element(By.CSS_SELECTOR,'#draggable')
    # target = browser.find_element(By.CSS_SELECTOR,'#droppable')
    # actions = ActionChains(browser)
    # actions.drag_and_drop(source,target)
    # actions.perform()

    browser.get('https://www.zhihu.com/explore')
    print(browser.get_cookies())
    browser.add_cookie({'name':'name','domain':'www.zhihu.com','value':'germey'})
    cookie = browser.get_cookies()
    for c in cookie:
        print(c)
    print(browser.get_cookies())
    browser.delete_all_cookies()
    browser.execute_script('window.open()')
    time.sleep(5)
    print(browser.window_handles)
    print(browser.get_cookies())

if __name__ == '__main__':
    main()