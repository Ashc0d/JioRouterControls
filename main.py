from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os

load_dotenv()
ROUTER_URL = os.getenv("ROUTER_URL", "http://192.168.29.1")
USERNAME   = os.getenv("USERNAME")
PASSWORD   = os.getenv("PASSWORD")

def create_webdriver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def login_and_get_html(driver):
    driver.get(ROUTER_URL)

    #credentials filler
    driver.find_element(By.NAME, "users.username").send_keys(USERNAME)
    driver.find_element(By.NAME, "users.password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.loginBtn").click()

    try:
        # wait for 10 seconds to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tf1_network_lanIPv4Config"))
        )
        login_status = "Login successful!"
    except Exception:
        login_status = "Login failed!"

    #return page source
    return login_status, driver.page_source

if __name__ == "__main__":
    drv = create_webdriver()
    try:
        status, html = login_and_get_html(drv)
        print(status)
        print("="*40)
        print(html[:])
    finally:
        drv.quit()
