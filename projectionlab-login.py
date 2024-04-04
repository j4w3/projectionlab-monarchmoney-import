from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Import time module

options = ChromeOptions()
options.binary_location = os.getenv("CHROME_BINARY_PATH")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path=os.getenv("CHROME_DRIVER_PATH"), options=options)

driver.get("https://app.projectionlab.com/login")

# Wait and click the "Sign in with Email" button
wait = WebDriverWait(driver, 10)
sign_in_button_xpath = "//button[contains(@class, 'firebaseui-idp-button') and .//span[contains(text(), 'Sign in with Email')]]"
wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()

# Wait for the email text field to be visible and enter the email using XPath
email_input_xpath = "//input[@type='email' and contains(@class, 'firebaseui-id-email')]"
email_input = wait.until(EC.visibility_of_element_located((By.XPATH, email_input_xpath)))
email_input.clear()
email_input.send_keys("jojomojo@gmail.com")

# Wait and click the "Next" button
next_button_xpath = "//button[contains(text(), 'Next')]"
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
next_button.click()

# Wait for the password text field to be visible and enter the password using XPath
password_input_xpath = "//input[@type='password' and contains(@class, 'firebaseui-id-password')]"
password_input = wait.until(EC.visibility_of_element_located((By.XPATH, password_input_xpath)))
password_input.clear()
password_input.send_keys("Asdf1234!")

# Dismiss the Cookie Consent banner by clicking the "OK" button
ok_button_id = "onetrust-accept-btn-handler"
wait.until(EC.element_to_be_clickable((By.ID, ok_button_id))).click()

# Use JavaScript to click the "Sign In" button
sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'firebaseui-id-submit')]")))
driver.execute_script("arguments[0].click();", sign_in_button)

# Wait a couple of seconds for the login process to complete
time.sleep(4)

# Ensure the page has loaded or transitioned before proceeding
wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

# Print out all of the visible text on the page to verify the actions were completed successfully
page_text = driver.find_element(By.TAG_NAME, "body").text
print("Visible text on the page:", page_text)

driver.close()
