from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

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
