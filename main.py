import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import datetime


load_dotenv()
ROUTER_URL = os.getenv("ROUTER_URL", "http://192.168.29.1")
USERNAME   = os.getenv("USERNAME")
PASSWORD   = os.getenv("PASSWORD")


class JioRouterControls:
    def __init__(self, USERNAME, PASSWORD, ROUTER_URL):
        def create_webdriver():
            options = Options()
            options.add_argument("--headless=new") # don't use --headless args with this router it does not like it and result in error during navigation
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--force-device-scale-factor=1")
            options.add_argument("--start-maximized")
            options.add_argument("--remote-debugging-port=9222")  # Avoid DevToolsActivePort error
            return webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

        self.driver = create_webdriver()
        self.driver.get(ROUTER_URL)
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.ROUTER_URL = ROUTER_URL

    def login(self):
        # Note: have to implement some function to check for forced dialog box that
        # informs user if there is an active session that has not logged out

        # Fill in credentials
        self.driver.find_element(By.NAME, "users.username").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "users.password").send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, "button.loginBtn").click()

        try:
            # Wait for the LAN-IPv4 config tab to appear
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "tf1_network_lanIPv4Config"))
            )

            print("Login successful!")

        except Exception:
            print("Login failed!")

        # Get the current page source after login attempt to debug if needed or checking if logging in is successful manually
        return self.driver.page_source

    def NavigationtoMaintenance(self):
        #Need this because going to tf1_administration_factoryDefault directly results in 401 because of some protection in router.
        try:

            # Click on "ADMINISTRATION" to reveal the submenu
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "mainMenu5"))
            ).click()

            # Click on "Maintenance"
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "tf1_administration_factoryDefault"))
            ).click()

            WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.NAME , "button.reboot.statusPage"))
            )
            print("Navigation to Maintenance page successful!")
            time.sleep(10)
        except Exception as e:
            print(f"Navigation to Maintenance page failed!\n ${e}")
            time.sleep(10)

        return self.driver.page_source

    def RebootRouter(self):
        try:
            # Clicking the reboot button using JS click in the console because usual way through EC.presence_of_element_located not worked
            self.driver.execute_script('document.getElementsByName("button.reboot.statusPage")[0].click();')

            # Wait for alert to appear
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())

            # Switch to alert dialog and accept the alert
            alert = self.driver.switch_to.alert
            print(f"Alert Text: {alert.text}")
            alert.accept()

            print("Reboot confirmed via alert!")

        except Exception as e:
            print(f"Reboot failed: {e}")

    def logout(self):
        # yup this is the fastest way to log out without going through clicking buttons
        try:
            self.driver.execute_script("window.location.href = '?page=index.html'")
            print("Logged out!")
            time.sleep(5)
        except Exception as e:
            print("logout failed!", e)

    def close(self):
        self.driver.quit()



if __name__ == "__main__":

    print(f"\n\nStarted this script on {datetime.datetime.now()}")
    # For now this only reboots the router which is the original idea for why I want to create this
    # because Jio Router Becomes unstable after some hours of working.
    controller = None  # Ensure it's always defined
    try:
        controller = JioRouterControls(USERNAME, PASSWORD, ROUTER_URL)
        LoginPageHtml = controller.login()
        MaintenancePageHtml = controller.NavigationtoMaintenance()
        controller.RebootRouter()

    except Exception as e:
        print(f"Entry Failed! \n {e}")

    finally:
        if controller is not None:
            controller.logout()
            controller.close()


