from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument('disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x3000')
chrome_options.add_argument('disable-gpu')
chrome_options.add_argument('hide-scrollbars')
chrome_options.add_argument('headless')
driver = webdriver.Chrome( options=chrome_options)
driver.get('http://www.baidu.com')
print(driver.page_source)
