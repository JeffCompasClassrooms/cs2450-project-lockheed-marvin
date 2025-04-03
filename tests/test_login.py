from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def run_tests(driver):
    passed = 0

    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests =--")

    try:
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='Login']")
        print("[PASSED] - Login button exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Login button not found.")

    try:
        delete_button = driver.find_element(By.CSS_SELECTOR, "button[type ='submit'][value='Delete']")
        print("[FAILED] - Delete button has not been removed.")
    except Exception as e:
        print("Error: ", e.msg)
        print("[PASSED] - Delete button not found.")
        passed+=1

    try:
        create_button = driver.find_element(By.CSS_SELECTOR, "button[type ='submit'][value='Create']")
        print("[PASSED] - Create button exists")
        passed += 1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Create button does not exist")


    try:
        username_form = driver.find_element(By.CSS_SELECTOR, "input[type ='text'][name='username']")
        print("[PASSED] - User can enter username")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - User cannot enter username")


    try:
        password_form = driver.find_element(By.CSS_SELECTOR, "input[type ='password'][name='password']")
        print("[PASSED] - User can enter password")
        passed += 1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - User cannot enter password")

    try:
        username_required = driver.find_element(By.CSS_SELECTOR, "input[type = 'text'][name='username']").get_attribute("required")
        print("[PASSED] - The user must enter a username")
        passed += 1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - User doesn't have to enter a username")


    try:
        utah_tech_link = driver.find_element(By.LINK_TEXT, "https://utahtech.edu")
        print("[FAILED] - Link to Utah Tech still exists")

    except Exception as e:
        print("Error: ", e.msg)
        print("[PASSED] - Link to UtahTech does not exist")
        passed += 1

    try:
        password_required = driver.find_element(By.CSS_SELECTOR, "input[type = 'password'][name='password']").get_attribute("required")
        print("[PASSED] - User must enter a password")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - User doesn't have to enter a password")

    try:
        subtitle_text = driver.find_element(By.CSS_SELECTOR, "p.lead")
        if subtitle_text.text != "A billion dollars and it's yours!":
            print("[PASSED] - Webpage no-longer says 'A billion dollars and it's yours!'")
            passed += 1
        else:
            print("[FAILED] - Webpage still says 'A billion dollars and it's yours!'")
    except Exception as e:
        print("Error: ", e)
        print("[FAILED] - Webpage has no subtitle element'")

    try:
        title_text = driver.find_element(By.CSS_SELECTOR, "a.navbar-brand")
        if title_text.text != "YouFace 2.0":
            print("[PASSED] - Title no-longer says YouFace 2.0")
            passed += 1
        else:
            print("[FAILED] - Title still says YouFace 2.0")
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Webpage has no title element.")


    print("--= Ending Tests =--")
    if passed == 10:
        print("ALL TESTS PASSED!")
    else:
        print(str(10-passed) + " TESTS FAILED!")
    driver.quit()

#See if we're running locally or remotely.
try:
    # Specify the path to ChromeDriver
    chrome_driver_path = "/usr/local/bin/chromedriver" #you'll need to put the path to YOUR chromedriver here
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    run_tests(driver)

except:
    print("Invalid path! This script is running on GitHub.")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Don't specify chromedriver path!
    driver = webdriver.Chrome(options=options)
    run_tests(driver)
