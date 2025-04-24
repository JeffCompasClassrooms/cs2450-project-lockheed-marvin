from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import time
import os
import json

# 👇 Custom storage class with pretty-printing
class PrettyJSONStorage(JSONStorage):
    def __init__(self, path):
        self._path = path
        super().__init__(path)

    def _read(self):
        print("📖 PrettyJSONStorage is reading from the file.")
        return super()._read()

    def _write(self, data):
        print("💾 PrettyJSONStorage is writing with indentation.")
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

class CustomStorage(CachingMiddleware):
    def __init__(self, path):
        super().__init__(PrettyJSONStorage(path))

def run_tests(driver):
    passed = 0

    driver.get("http://localhost:5000/")
    time.sleep(2)

    print("--= Beginning Tests =--")



    try:
        # Fill in login form
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        test_username = "testuser"
        test_password = "testpassword"

        username_input.send_keys(test_username)
        password_input.send_keys(test_password)

        # Try to login
        login_button = driver.find_element(By.XPATH, "//button[@name='type' and @value='Login']")
        login_button.click()

        time.sleep(2)  # Wait for login attempt to process

        # Check for success
        if "Welcome" in driver.page_source or "Dashboard" in driver.title:
            print("✅ Login Test Passed")
            passed += 1

        else:
            print("⚠️ Login failed, trying to create account...")

            # Go back to login screen (if necessary)
            driver.get("http://localhost:5000/loginscreen")
            time.sleep(2)

            # Refill form
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(test_username)
            password_input.send_keys(test_password)

            # Click the Create Account button
            create_button = driver.find_element(By.XPATH, "//button[@name='type' and @value='Create']")
            create_button.click()

            time.sleep(2)

            if "Welcome" in driver.page_source or "Dashboard" in driver.title:
                print("✅ Account created and login successful")
                passed += 1
            else:
                print("❌ Failed to create account")

    except Exception as e:
        print("Error: ", e)
        print("[FAILED] - Webpage has no subtitle element'")

    try:
        addfriend_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][name='addfriend']")
        print("[PASSED] - addfriend button exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - addfriend button not found.")

    try:
        post_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][name='post-submit']")
        print("[PASSED] - Post button exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Post button not found.")    

    try:
        log_out_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][name='logout']")
        print("[PASSED] - Log Out button exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Log Out button not found.")
        
    try:
        feed_text = driver.find_element(By.CSS_SELECTOR, 'textarea[name="post"][placeholder="What is on your mind?"]')
        print("[PASSED] - User has a textarea.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - User doesn't have a textarea.")
        
    try:
        image_input = driver.find_element(By.CSS_SELECTOR, "input[type='file'][name='picture_url']")
        print("[PASSED] - Image file exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Image file not found.")
        
    try:
        video_input = driver.find_element(By.CSS_SELECTOR, "input[type='file'][name='video_url']")
        print("[PASSED] - Log Out button exists.")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - Log Out button not found.")

    try:
        friend_search = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='username']")
        print("[PASSED] - You are able to look for friends")
        passed+=1
    except Exception as e:
        print("Error:", e)
        print("[FAILED] - You have no way of looking up friends")

    print("--= Starting Logout Test =--")
    try:
        # Wait for the logout element to be clickable/visible
        time.sleep(2)

        # Try to find a logout button (by text or attribute)
        try:
            # Case 1: If it's a button
            logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
            logout_button.click()
        except:
            try:
                # Case 2: If it's a link
                logout_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
                logout_link.click()
            except:
                print("❌ Could not find logout button or link.")
                return

        time.sleep(2)

        # Check if logout was successful (back at login screen or similar)
        if "login" in driver.current_url.lower() or "log in" in driver.page_source.lower():
            passed+=1
            print("✅ Logout Test Passed")
        else:
            print("❌ Logout may have failed. Still logged in or unexpected page.")

    except Exception as e:
        print(f"❌ Exception during logout test: {e}")


    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db.json')
        
        # Load JSON directly
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Search for user by username/password
        users = data.get("users", {})
        to_delete_key = None
        for key, user in users.items():
            if user.get("username") == "testuser" and user.get("password") == "testpassword":
                to_delete_key = key
                break

        if to_delete_key:
            del users[to_delete_key]
            print(f"🗑️ Deleted user {to_delete_key} from users table.")

            # Save changes back with pretty print
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            passed += 1
        else:
            print("⚠️ Test user not found in raw JSON.")

    except Exception as e:
        print(f"❌ Error deleting test user manually: {e}")


    print("--= Ending Tests =--")
    if passed == 10:
        print("ALL TESTS PASSED!")
    else:
        print(str(10-passed) + " TESTS FAILED!")
        print(driver.get_log('browser'))
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
