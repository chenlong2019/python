from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.add_argument('-headless') # 无头参数
firefox_path = r'C:\Program Files\Mozilla Firefox\geckodriver.exe'
brower = webdriver.Firefox(executable_path=firefox_path,firefox_options=options)
brower.get("http://www.baidu.com")

brower.find_element_by_id('kw').send_keys('selenium')
brower.find_element_by_id('su').click()

time.sleep(3)
print(brower.current_url)
brower.quit()