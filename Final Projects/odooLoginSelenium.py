from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
#You may want to study the following:
#https://selenium-python.readthedocs.io/locating-elements.html
#showing differnt ways of find_element(By. ...

#https://chromedriver.chromium.org/downloads
#Check this to make sure your Chrome and selenium driver versions match to each other (or, you may have weird problems)


driver = webdriver.Chrome('./venv/bin/chromedriver')


def update_form_field(driver, field_name, field_value):
	search_bar = driver.find_element(By.NAME, field_name)
	search_bar.clear()
	time.sleep(1)
	search_bar.send_keys(field_value)


driver.get("http://localhost:8069/web/login")
print("Ning: Step1 passed")

update_form_field(driver, "login", "your-email@example.com")
update_form_field(driver, "password", "your-password")
driver.find_element(By.NAME, "login").send_keys(Keys.RETURN)
print("Ning: I have Logged in!")
time.sleep(3)

 
time.sleep(10)

driver.close()
exit(0)

