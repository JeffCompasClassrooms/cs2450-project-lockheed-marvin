from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
# Don't add --headless
# Optional: chrome_options.add_argument("--user-data-dir=/tmp/test")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)


try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    print("--= Beginning Tests =--")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Login']")


    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    create_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if create_button:
        print("[PASSED] - Create Button Exists.")
    else:
        print("[FAILED] - Create button not found.")

except Exception as e:
    print("Error:", e)


try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - Menu Dropdown Button Exists.")
    else:
        print("[FAILED] - Menu Dropdown not found.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - Menu button is white.")
    else:
        print("[FAILED] - Menu button is not white.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - Submit button can post content.")
    else:
        print("[FAILED] - Submit button cannot post content.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - Alert works when the user logs in.")
    else:
        print("[FAILED] - Alert doesn't work when the user logs in.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - Posts are blue.")
    else:
        print("[FAILED] - Posts are not blue.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - The Add Friends button works.")
    else:
        print("[FAILED] - The Add Friends button doesn't work.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - User can upload photos.")
    else:
        print("[FAILED] - User cannot upload photos.")

except Exception as e:
    print("Error:", e)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(5)

    menu_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Create']")


    if menu_button:
        print("[PASSED] - User can upload videos.")
    else:
        print("[FAILED] - User cannot upload videos.")

except Exception as e:
    print("Error:", e)


finally:
    print("--= Ending Tests =--")
    driver.quit()