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


driver = webdriver.Chrome('./drivers/chromedriver')


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

#Ning: the URL will be different in your case
#you need to check and modify
driver.get("http://localhost:8069/web#cids=1&menu_id=644&action=913")
print("Ning: I have invoked My Library app")
time.sleep(3)

create_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/button[3]")
#create_button = driver.find_element(By.CLASS_NAME, "btn btn-primary o_list_button_add") #Ning: somehow did not work
create_button.click()
time.sleep(3)

search_bar = driver.find_element(By.NAME, "name")
search_bar.send_keys("NingBook2")
search_bar = driver.find_element(By.NAME, "short_name")
search_bar.send_keys("Book2")
time.sleep(3)




save_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/button[1]")
#save_button=driver.find_element(By.NAME, "Save record")

#save_button = driver.find_element(by=By.CLASS_NAME, value="/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/button[1]")
save_button.click()



time.sleep(10)

driver.close()
exit(0)

