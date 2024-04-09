import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_webdriver():
    chrome_options = ChromeOptions()
    chrome_options.binary_location = os.getenv("CHROME_BINARY_PATH")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=os.getenv("CHROME_DRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    actions = ActionChains(driver)
    return driver, actions

def login(driver, email, password):
    logging.info("Navigating to the login page...")
    driver.get("https://app.projectionlab.com/login")
    
    # Login sequence
    logging.info("Logging in...")
    perform_login(driver, email, password)
    dismiss_cookie_consent(driver)

def perform_login(driver, email, password):
    sign_in_with_email(driver)
    enter_email(driver, email)
    click_next(driver)
    enter_password(driver, password)
    sign_in(driver)

def sign_in_with_email(driver):
    logging.info("Clicking the 'Sign in with Email' button...")
    sign_in_button_xpath = "//button[contains(@class, 'firebaseui-idp-button') and .//span[contains(text(), 'Sign in with Email')]]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()

def enter_email(driver, email):
    logging.info("Entering email...")
    email_input_xpath = "//input[@type='email' and contains(@class, 'firebaseui-id-email')]"
    email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, email_input_xpath)))
    email_input.clear()
    email_input.send_keys(email)

def click_next(driver):
    logging.info("Clicking 'Next'...")
    next_button_xpath = "//button[contains(text(), 'Next')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath))).click()

def enter_password(driver, password):
    logging.info("Entering password...")
    password_input_xpath = "//input[@type='password' and contains(@class, 'firebaseui-id-password')]"
    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, password_input_xpath)))
    password_input.clear()
    password_input.send_keys(password)

def sign_in(driver):
    logging.info("Signing in...")
    sign_in_button_xpath = "//button[contains(@class, 'firebaseui-id-submit')]"
    sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sign_in_button_xpath)))
    driver.execute_script("arguments[0].click();", sign_in_button)

def dismiss_cookie_consent(driver):
    logging.info("Clearing banner...")
    ok_button_id = "onetrust-accept-btn-handler"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ok_button_id))).click()

def navigate_finances(driver, actions):
    logging.info("Opening menu tab...")
    menu_button_xpath = "//button[contains(@class,'v-app-bar__nav-icon') and contains(@class,'v-btn--icon')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, menu_button_xpath))).click()

    logging.info("Opening Current Finances...")
    finances_menu_xpath = "//a[contains(@class, 'v-list-item') and .//span[contains(text(), 'Current Finances')]]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, finances_menu_xpath))).click()

    logging.info("Clicking on input field...")
    input_xpath = "//input[@type='text' and @inputmode='decimal']"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, finances_menu_xpath))).click()
    
    logging.info("Deselecting input field...")
    actions.move_by_offset(400, 50).click().perform()

    time.sleep(30)

def execute_commands_from_file(driver, file_path):
    logging.info(f"Executing commands from file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            commands = file.read().strip().split('\n')
            for command in commands:
                driver.execute_script(command)
                logging.info(f"Executed command: {command}")
        logging.info("All commands executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute commands: {str(e)}")

    time.sleep(30)

def main():
    driver, actions = create_webdriver()
    try:
        login(driver, os.getenv("PROJECTIONLAB_EMAIL"), os.getenv("PROJECTIONLAB_PASSWORD"))
        execute_commands_from_file(driver, 'commands.txt')
        navigate_finances(driver, actions)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
