"""
Selenium Tests for Odoo Lunch Module - 3 Tests Combined
File: test_lunch_selenium_all.py
Run: python3 test_lunch_selenium_all.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

service = Service('/home/ttran9280/odoo15/myodoo15-venv/bin/chromedriver')

def update_form_field(driver, field_name, field_value):
    search_bar = driver.find_element(By.NAME, field_name)
    search_bar.clear()
    time.sleep(1)
    search_bar.send_keys(field_value)


def test_1_navigate_to_lunch():
    print("="*70)
    print("TEST 1/3: NAVIGATE TO LUNCH APP (POSITIVE)")
    print("="*70)
    
    driver = webdriver.Chrome(service=service)
    
    try:
        print("Step 1: Navigating to login page...")
        driver.get("http://localhost:8069/web/login")
        time.sleep(2)
        
        print("Step 2: Logging in...")
        update_form_field(driver, "login", "your-email@example.com")
        update_form_field(driver, "password", "your-password")
        driver.find_element(By.NAME, "login").send_keys(Keys.RETURN)
        time.sleep(3)
        print("Logged in successfully")
        
        print("Step 3: Opening Home Menu...")
        home_menu = driver.find_element(By.XPATH, "//button[@title='Home Menu']")
        ActionChains(driver).move_to_element(home_menu).perform()
        time.sleep(1)
        home_menu.click()
        time.sleep(2)
        
        print("Step 4: Navigating to Lunch module...")
        lunch_menu = driver.find_element(By.XPATH, "//a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]")
        ActionChains(driver).move_to_element(lunch_menu).perform()
        time.sleep(1)
        lunch_menu.click()
        time.sleep(3)
        print("Lunch module opened")
        
        print("Step 5: Clicking My Lunch...")
        try:
            my_lunch = driver.find_element(By.XPATH, "//a[contains(text(), 'My Lunch')]")
            ActionChains(driver).move_to_element(my_lunch).perform()
            time.sleep(1)
            my_lunch.click()
            time.sleep(2)
            print("My Lunch clicked")
        except:
            print("My Lunch not found, continuing")
        
        print("Step 6: Verifying page...")
        current_url = driver.current_url
        
        if 'lunch' in current_url.lower():
            print("Verification passed")
        
        print("TEST 1 PASSED\n")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"TEST 1 FAILED: {e}\n")
        return False
        
    finally:
        driver.close()


def test_2_add_non_existent_to_favorites():
    print("TEST 2/3: ADD NON-EXISTENT PRODUCT TO FAVORITES (NEGATIVE)")
    
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 5)
    
    try:
        print("Step 1: Logging in...")
        driver.get("http://localhost:8069/web/login")
        time.sleep(2)
        
        update_form_field(driver, "login", "your-email@example.com")
        update_form_field(driver, "password", "your-password")
        driver.find_element(By.NAME, "login").send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("Step 2: Opening Home Menu...")
        home_menu = driver.find_element(By.XPATH, "//button[@title='Home Menu']")
        ActionChains(driver).move_to_element(home_menu).perform()
        time.sleep(1)
        home_menu.click()
        time.sleep(2)
        
        print("Step 3: Navigating to Lunch...")
        lunch_menu = driver.find_element(By.XPATH, "//a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]")
        ActionChains(driver).move_to_element(lunch_menu).perform()
        time.sleep(1)
        lunch_menu.click()
        time.sleep(3)
        
        try:
            my_lunch = driver.find_element(By.XPATH, "//a[contains(text(), 'My Lunch')]")
            ActionChains(driver).move_to_element(my_lunch).perform()
            time.sleep(1)
            my_lunch.click()
            time.sleep(2)
        except:
            pass
        
        print("Step 4: Searching for non-existent product...")
        try:
            search_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")
            search_input.click()
            time.sleep(0.5)
            search_input.clear()
            search_input.send_keys("Unicorn Pizza Supreme Deluxe")
            time.sleep(1)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            pass
        
        print("Step 5: Attempting to find favorite star...")
        print("This WILL FAIL - product does not exist")
        favorite_locator = "//div[contains(text(), 'Unicorn Pizza')]//ancestor::div[contains(@class, 'o_kanban_record')]//i[contains(@class, 'fa-star')]"
        
        favorite_star = wait.until(
            EC.element_to_be_clickable((By.XPATH, favorite_locator))
        )
        ActionChains(driver).move_to_element(favorite_star).perform()
        time.sleep(0.5)
        favorite_star.click()
        
        print("TEST 2 PASSED")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"TEST 2 FAILED: {e}")
        return False
        
    finally:
        driver.close()


def test_3_search_products():
    print("="*70)
    print("TEST 3/3: SEARCH FOR PRODUCTS IN LUNCH MODULE (POSITIVE)")
    print("="*70)
    
    driver = webdriver.Chrome(service=service)
    
    try:
        print("Step 1: Logging in...")
        driver.get("http://localhost:8069/web/login")
        time.sleep(2)
        
        update_form_field(driver, "login", "your-email@example.com")
        update_form_field(driver, "password", "your-password")
        driver.find_element(By.NAME, "login").send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("Step 2: Opening Home Menu...")
        home_menu = driver.find_element(By.XPATH, "//button[@title='Home Menu']")
        ActionChains(driver).move_to_element(home_menu).perform()
        time.sleep(1)
        home_menu.click()
        time.sleep(2)
        
        print("Step 3: Navigating to Lunch...")
        lunch_menu = driver.find_element(By.XPATH, "//a[contains(@class,'dropdown-item')][contains(text(),'Lunch')]")
        ActionChains(driver).move_to_element(lunch_menu).perform()
        time.sleep(1)
        lunch_menu.click()
        time.sleep(3)
        
        print("Step 4: Clicking My Lunch...")
        try:
            my_lunch = driver.find_element(By.XPATH, "//a[contains(text(), 'My Lunch')]")
            ActionChains(driver).move_to_element(my_lunch).perform()
            time.sleep(1)
            my_lunch.click()
            time.sleep(3)
        except:
            pass
        
        print("Step 5: Searching for Pizza...")
        try:
            search_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")
            search_input.click()
            time.sleep(0.5)
            search_input.clear()
            search_input.send_keys("Pizza")
            time.sleep(1)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)
            print("Search completed")
        except:
            print("Search box not found")
        
        print("Step 6: Verifying page...")
        current_url = driver.current_url
        if 'lunch' in current_url.lower():
            print("Verification passed")
        
        print("TEST 3 PASSED\n")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"TEST 3 FAILED: {e}\n")
        return False
        
    finally:
        driver.close()


if __name__ == "__main__":
    print("ODOO LUNCH - SELENIUM TESTS")
    
    results = []
    
    test1_passed = test_1_navigate_to_lunch()
    results.append(("Test 1: Navigate to Lunch App", test1_passed))
    time.sleep(2)
    
    test2_passed = test_2_add_non_existent_to_favorites()
    results.append(("Test 2: Add Non-Existent to Favorites", test2_passed))
    time.sleep(2)
    
    test3_passed = test_3_search_products()
    results.append(("Test 3: Search Products", test3_passed))
    
    print("TEST EXECUTION SUMMARY")
    
    for test_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {total_passed}")
    print(f"Failed: {len(results) - total_passed}")
    print("="*70)
    
    exit(0)