import time
import pickle
import os
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
        
        self.browser.get('https://www.instagram.com')
        self.wait_for_page_load()
        self.login()

    def wait_for_page_load(self):
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def login(self):
        # Enter username
        username_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_input.send_keys(self.username)

        # Enter password
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys(self.password)

        # Click login button
        login_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Wait for login to complete (home page or error message)
        self.wait_for_page_load()
        time.sleep(5)  # Add extra wait for redirection

        # Check if login was successful
        if "https://www.instagram.com/" in self.browser.current_url:
            print("Login successful")
            print(self.browser.current_url) # If extra param then account need auth 2FA very simple it can be solve easily hit me
        else:
            print("Login failed")

if __name__ == "__main__":
    username = "username"
    password = "passwd"

    insta_bot = Instagram(username, password)
