import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path = r"C:\Users\avepe\OneDrive\Documents\chromedriver-win32\chromedriver-win32\chromedriver.exe"

service = Service(executable_path = driver_path)

driver = webdriver.Chrome(service = service)



wait = WebDriverWait(driver, 3)


start_time = time.time()
driver.get(r'file:\\C:\Users\avepe\OneDrive\Documents\cs2450\MyState\settings.htm')
end_time = time.time()

loaded = print(f"Page loaded in {end_time - start_time:.2f} seconds")

passed = 0
failed = 0



settings_file_path = r'file:///C:/Users/avepe/OneDrive/Documents/cs2450/MyState/settings.htm'

driver.get(settings_file_path)

print(selenium.__version__)

print("--=Beginning Tests - Averie Perriton=--")

WebDriverWait(driver, 5)

if not loaded: ##bool of a print statement is None and therefore False!!!
    print("[PASSED] - Settings Page Loaded")
    passed += 1 
else:
    print("[FAILED] - Settings Page failed to load")
    failed += 1
    loaded != False
try:
    profile_image = driver.find_element(By.XPATH, "//img[contains(@src, 'balanced-global-leader')]")
    assert profile_image.is_displayed()
    print("[PASSED] - Profile image is up")
    passed+=1 

except:
    print("[FAILED] - Profile image not found")
    failed+=1

try:
    upload_button = driver.find_element(By.XPATH, "//label[contains(text(), 'Upload new photo')]")
    assert upload_button.is_displayed()
    print("[PASSED] - Upload new photo button is visible")
    passed+=1 

except:
    print("[FAILED] - Upload new photo button not working")
    failed+=1
    
try:
    username_field = driver.find_element(By.XPATH, "//input[@value='civillian123']")
    assert username_field.is_displayed()
    print("[PASSED] - Username input field is visible")
    passed+=1
except:
    print("[FAILED] - Username input field is missing")
    failed+=1
    
    
try:
    email_field = driver.find_element(By.XPATH, "//input[@value='jdoe@gmail.com']")
    assert email_field.is_displayed()
    email_warning = driver.find_element(By.XPATH, "//div[contains(text(), 'Your email is not confirmed')]")
    assert email_warning.is_displayed()
    print("[PASSED] - Email field and warning are visible")
    passed+=1
except:
    print("[FAILED] - Email field or warning not found")
    failed+=1

try:
    bio_textarea = driver.find_element(By.XPATH, "//textarea[contains(text(), 'Just your average joe')]")
    assert bio_textarea.is_displayed()
    print("[PASSED] - Bio textBox is visible")
    passed+=1
except:
    print("[FAILED] - Bio textBox is missing")
    failed+=1

try:
    country_dropdown = driver.find_element(By.XPATH, "//select[@class='custom-select']")
    selected_option = country_dropdown.find_element(By.XPATH, "//option[@selected='']")
    assert selected_option.text == "Canada"
    print("[PASSED] - Country dropdown is working")
    passed+=1
except:
    print("[FAILED] - Country dropdown issue")
    failed+=1

try:
    password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
    assert len(password_fields) == 3
    print("[PASSED] - 3 password fields found")
    passed+=1
except:
    print("[FAILED] - Password fields not found")
    failed+=1

try:
    save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save changes')]")
    assert save_button.is_displayed()
    print("[PASSED] - Save Changes button is visible")
    passed+=1
except:
    print("[FAILED] - Save Changes button is missing")
    failed+=1


try:
    notification_switch = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    assert len(notification_switch) >= 3
    print("[PASSED] - Notification checkboxes are present")
    passed+=1
except:
    print("[FAILED] - Notification checkboxes not found")
    failed+=1

driver.quit()

print(rf'Settings passed {passed}/10 and failed {failed}/10 tests')



    

    







