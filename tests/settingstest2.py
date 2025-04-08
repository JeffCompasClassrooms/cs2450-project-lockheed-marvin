from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # good for CI

# Connect to Selenium running in Docker container
driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=chrome_options
)

wait = WebDriverWait(driver, 5)

# 🔁 Update this URL to match the Flask app’s route that serves your HTML
url = "http://localhost:5000/settings"

start_time = time.time()
driver.get(url)
end_time = time.time()

print(f"Page loaded in {end_time - start_time:.2f} seconds")

passed = 0
failed = 0

print(selenium.__version__)
print("--=Beginning Tests - Averie Perriton=--")

try:
    profile_image = driver.find_element(By.XPATH, "//img[contains(@src, 'balanced-global-leader')]")
    assert profile_image.is_displayed()
    print("[PASSED] - Profile image is up")
    passed += 1
except:
    print("[FAILED] - Profile image not found")
    failed += 1

try:
    upload_button = driver.find_element(By.XPATH, "//label[contains(text(), 'Upload new photo')]")
    assert upload_button.is_displayed()
    print("[PASSED] - Upload new photo button is visible")
    passed += 1
except:
    print("[FAILED] - Upload new photo button not working")
    failed += 1

try:
    username_field = driver.find_element(By.XPATH, "//input[@value='civillian123']")
    assert username_field.is_displayed()
    print("[PASSED] - Username input field is visible")
    passed += 1
except:
    print("[FAILED] - Username input field is missing")
    failed += 1

try:
    email_field = driver.find_element(By.XPATH, "//input[@value='jdoe@gmail.com']")
    assert email_field.is_displayed()
    email_warning = driver.find_element(By.XPATH, "//div[contains(text(), 'Your email is not confirmed')]")
    assert email_warning.is_displayed()
    print("[PASSED] - Email field and warning are visible")
    passed += 1
except:
    print("[FAILED] - Email field or warning not found")
    failed += 1

try:
    bio_textarea = driver.find_element(By.XPATH, "//textarea[contains(text(), 'Just your average joe')]")
    assert bio_textarea.is_displayed()
    print("[PASSED] - Bio textBox is visible")
    passed += 1
except:
    print("[FAILED] - Bio textBox is missing")
    failed += 1

try:
    country_dropdown = driver.find_element(By.XPATH, "//select[@class='custom-select']")
    selected_option = country_dropdown.find_element(By.XPATH, ".//option[@selected='']")
    assert selected_option.text.strip() == "Canada"
    print("[PASSED] - Country dropdown is working")
    passed += 1
except:
    print("[FAILED] - Country dropdown issue")
    failed += 1

try:
    password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
    assert len(password_fields) == 3
    print("[PASSED] - 3 password fields found")
    passed += 1
except:
    print("[FAILED] - Password fields not found")
    failed += 1

try:
    save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save changes')]")
    assert save_button.is_displayed()
    print("[PASSED] - Save Changes button is visible")
    passed += 1
except:
    print("[FAILED] - Save Changes button is missing")
    failed += 1

try:
    notification_switches = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    assert len(notification_switches) >= 3
    print("[PASSED] - Notification checkboxes are present")
    passed += 1
except:
    print("[FAILED] - Notification checkboxes not found")
    failed += 1

driver.quit()

print(f"Settings passed {passed}/10 and failed {failed}/10 tests")
