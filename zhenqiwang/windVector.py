from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()
# prefs = {'profile.default_content_settings.popups': 0,"download.default_directory": pachongshuju}
# chromeOptions.add_experimental_option("prefs", prefs)
#chromeOptions.add_argument("headless")
driver=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chromeOptions)
driver.get("https://map.zq12369.com/data/gzip/20190920/0.25/201909200700-wind-surface-level-gfs-0.25.json")
print(driver.page_source)