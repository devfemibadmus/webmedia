import time, pickle, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Instagram:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_argument("--disable-gpu")
        service = Service('/usr/local/bin/msedgedriver')
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(service=service, options=self.edge_options)
        self.browser.set_script_timeout(50)

        print("Opening Instagram homepage...")
        self.browser.get('https://www.instagram.com')
        self.wait_for_page_load()

        if not self.login_with_cookies():
            self.login()

    def wait_for_page_load(self):
        try:
            print("Waiting for the page to load...")
            WebDriverWait(self.browser, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("Page fully loaded.")
        except Exception as e:
            print(f"Error during page load: {e}")

    def login(self):
        try:
            print("Attempting login with username and password...")
            # Enter username
            print("Locating username input field...")
            username_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            print(f"Entering username: {self.username}")
            username_input.send_keys(self.username)

            # Enter password
            print("Locating password input field...")
            password_input = self.browser.find_element(By.NAME, 'password')
            print(f"Entering password: {self.password}")
            password_input.send_keys(self.password)

            # Click login button
            print("Locating and clicking login button...")
            login_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for login to complete (home page or error message)
            print("Waiting for login to complete...")
            self.wait_for_page_load()
            time.sleep(5)  # Add extra wait for redirection

            # Check if login was successful
            if "https://www.instagram.com/" in self.browser.current_url:
                print(self.browser.current_url)
                print("Login successful!")
                self.save_cookies()
            else:
                print("Login failed. Please check your credentials.")
        except Exception as e:
            print(f"Error during login: {e}")

    def save_cookies(self):
        try:
            print("Saving cookies to file...")
            with open("cookies.pkl", "wb") as f:
                pickle.dump(self.browser.get_cookies(), f)
            print("Cookies successfully saved.")
        except Exception as e:
            print(f"Error saving cookies: {e}")

    def login_with_cookies(self):
        try:
            print("Attempting to login using saved cookies...")
            if os.path.exists("cookies.pkl"):
                print("Loading cookies from file...")
                with open("cookies.pkl", "rb") as f:
                    cookies = pickle.load(f)
                for cookie in cookies:
                    print(f"Adding cookie: {cookie['name']}")
                    self.browser.add_cookie(cookie)
                print("All cookies added. Navigating to Instagram homepage...")
                self.browser.get('https://www.instagram.com')
                self.wait_for_page_load()
                time.sleep(5)  # Add extra wait for redirection

                if "https://www.instagram.com/" in self.browser.current_url:
                    print(self.browser.current_url)
                    print("Login with cookies successful!")
                    self.save_cookies()  # Update cookies even if login is successful with cookies
                    return True
                else:
                    print("Cookies didn't work, reverting to username and password login.")
                    return False
            else:
                print("No cookies file found.")
                return False
        except Exception as e:
            print(f"Error during login with cookies: {e}")
            return False

if __name__ == "__main__":
    username = "username"
    password = "passwd"

    print("Starting Instagram bot...")
    insta_bot = Instagram(username, password)
