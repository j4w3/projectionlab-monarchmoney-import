import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
chrome_options = ChromeOptions()
chrome_options.binary_location = os.getenv("CHROME_BINARY_PATH")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Updated instantiation for Selenium 4.x
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
actions = ActionChains(driver)

print("Navigating to the login page...")
driver.get("https://app.projectionlab.com/login")



# Wait and click the "Sign in with Email" button
print("Clicking the 'Sign in with Email' button...")
wait = WebDriverWait(driver, 10)
sign_in_button = driver.find_element(By.XPATH, '//*[@id="auth-container"]/button[2]')
driver.execute_script("arguments[0].click();", sign_in_button)

# Wait for the email text field to be visible and enter the email using XPath
print("Entering email...")
email_input = driver.find_element(By.XPATH, '//*[@id="input-7"]')
email_input.clear()
email_input.send_keys(os.getenv("PROJECTIONLAB_EMAIL"))
print("Email entered")

# Wait for the password text field to be visible and enter the password using XPath
print("Entering password...")
password_input = driver.find_element(By.XPATH, '//*[@id="input-9"]')
password_input.clear()
password_input.send_keys(os.getenv("PROJECTIONLAB_PASSWORD"))
print("Password entered")

# Use JavaScript to click the "Sign In" button
print("Signing in...")
sign_in_button = driver.find_element(By.XPATH, '//*[@id="auth-container"]/form/button')
driver.execute_script("arguments[0].click();", sign_in_button)

# Wait a couple of seconds for the login process to complete
time.sleep(2)

# Ensure the page has loaded or transitioned before proceeding
wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

# Wait a couple of seconds for the login process to complete
time.sleep(2)

# Inject output script
file_path = 'commands.txt'  # Adjust this path if the file is stored elsewhere

try:
    with open('commands.txt', 'r') as file:
        commands = file.read().strip().split('\n')
        print(commands)
    for command in commands:
        print(command)
        driver.execute_script(command)
    print("Commands executed successfully.")
except Exception as e:
    print(f"Failed to execute commands: {str(e)}")

# Wait a couple of seconds
time.sleep(30)

# Wait and click the "Menu Tab" button
print("Opening menu tab...")
menu_button_xpath = "//button[contains(@class,'v-app-bar__nav-icon') and contains(@class,'v-btn--icon')]"
menu_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, menu_button_xpath)))
menu_button.click()

# Open the "Current Finances" tab
print("Opening Current Finances...")
finances_menu_xpath = "//a[contains(@class, 'v-list-item') and .//span[contains(text(), 'Current Finances')]]"
finances_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, finances_menu_xpath)))
finances_menu.click()

# Wait and click on a current finance field to update Progress for the day
print("Clicking on the decimal input text box...")
input_xpath = "//input[@type='text' and @inputmode='decimal']"
decimal_input_box = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
decimal_input_box.click()

# Deselect the finance field by moving to coordinates and clicking (e.g., x=100, y=200)
print("Deselecting to save...")
actions.move_by_offset(400, 50).click().perform()

# Wait a couple of seconds before closing
time.sleep(30)
driver.close()
