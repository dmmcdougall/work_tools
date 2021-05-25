from selenium import webdriver
import time

my_path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(my_path)

# driver.get("https://artsvision.net/epcor.asp")
# print(driver.title)
# driver.quit()

driver.get("https://techwithtim.net")
print(driver.title)


time.sleep(5)
driver.quit()