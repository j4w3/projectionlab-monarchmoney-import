import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

print("Navigating to the login page...")
driver.get("https://app.projectionlab.com/login")

# Wait and click the "Sign in with Email" button
print("Clicking the 'Sign in with Email' button...")
wait = WebDriverWait(driver, 10)
sign_in_button_xpath = "//button[contains(@class, 'firebaseui-idp-button') and .//span[contains(text(), 'Sign in with Email')]]"
wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()

# Wait for the email text field to be visible and enter the email using XPath
print("Entering email...")
email_input_xpath = "//input[@type='email' and contains(@class, 'firebaseui-id-email')]"
email_input = wait.until(EC.visibility_of_element_located((By.XPATH, email_input_xpath)))
email_input.clear()
email_input.send_keys(os.getenv("PROJECTIONLAB_EMAIL"))
print("Email entered: ", os.getenv("PROJECTIONLAB_EMAIL"))

# Wait and click the "Next" button
print("Clicking 'Next'...")
next_button_xpath = "//button[contains(text(), 'Next')]"
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
next_button.click()

# Print out all of the visible text on the page to verify the actions were completed successfully
page_text = driver.find_element(By.TAG_NAME, "body").text
print("Visible text on the page:", page_text)

# Wait for the password text field to be visible and enter the password using XPath
print("Entering password...")
password_input_xpath = "//input[@type='password' and contains(@class, 'firebaseui-id-password')]"
password_input = wait.until(EC.visibility_of_element_located((By.XPATH, password_input_xpath)))
password_input.clear()
password_input.send_keys(os.getenv("PROJECTIONLAB_PASSWORD"))

# Dismiss the Cookie Consent banner by clicking the "OK" button
print("Clearing banner...")
ok_button_id = "onetrust-accept-btn-handler"
wait.until(EC.element_to_be_clickable((By.ID, ok_button_id))).click()

# Use JavaScript to click the "Sign In" button
print("Signing in...")
sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'firebaseui-id-submit')]")))
driver.execute_script("arguments[0].click();", sign_in_button)

# Wait a couple of seconds for the login process to complete
time.sleep(4)

# Ensure the page has loaded or transitioned before proceeding
wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

# Print out all of the visible text on the page to verify the actions were completed successfully
page_text = driver.find_element(By.TAG_NAME, "body").text
print("Visible text on the page:", page_text)

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

driver.close()
