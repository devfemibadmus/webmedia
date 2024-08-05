# WEBMEDIA

## Overview

**WEBMEDIA**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) backend for saving videos, images, and audio from the web. Currently supports social media platforms only. It performs web scraping and uses predefined methods observed from network traffic.


## Dependencies

- **[Selenium](https://github.com/SeleniumHQ/selenium)**: Primarily used for Instagram (av/s 1.1604s). It's capable of supporting other platforms as well and performs efficiently, but optimization is key.

- **[Requests](https://github.com/psf/requests)**: Used for TikTok and Facebook.

- **[Cors.lol](https://github.com/BradPerbs/cors.lol)**: for video rendering on web 

- **[corsproxy.io](https://github.com/cors-proxy/fix-cors-errors)**: for image rendering on web


## Features

-  **Fetch Media**: Retrieves both private and public media files.

-  **Cut Data**: shrink and return normal data.

-  **Full Data**: Give full data containing all fields scraped from given platform.


### Apps

-  **Web App**: [WebMedia](https://devfemibadmus.blackstackhub.com/webmedia) limited download(maybe)

-  **Mobile App**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) unlimited download + WhatsApp status saver
  

## Status
|website| status |
|--|--|
| TikTok Videos |✅|
| TikTok Photos |❌|
| Facebook Videos |✅|
| Instagram Reels |✅|
| Instagram Photos |✅|
| Instagram Videos |✅|
| YouTube |❌|


### API


1. Check out web version to know how it works https://devfemibadmus.blackstackhub.com/webmedia

1. Star the original repo [https://devfemibadmus.blackstackhub.com/webmedia](https://devfemibadmus.blackstackhub.com/webmedia)

2. Fork it

3. Clone it

4. Host it on any VPS

### When it hit 10 star i will make a youtube video creating from scratch and hosting on vps

### Some Explanation

<details>
<summary>Using Microsoft Edge on Debian VPS</summary>

1. **Familiarize Yourself with Edge WebDriver and Selenium**

   Before proceeding, you might want to check out these issues on GitHub related to Edge WebDriver:
   - [No latest stable release for Linux · Issue #156](https://github.com/MicrosoftEdge/EdgeWebDriver/issues/156)
   - [How to determine the correct Microsoft Edge WebDriver version for a given Edge browser version · Issue #158](https://github.com/MicrosoftEdge/EdgeWebDriver/issues/158#issuecomment-2263769092)

2. **Install Microsoft Edge and Edge WebDriver on Debian**

   - First, add the Microsoft repository to your APT sources list:

     ```bash
     sudo nano /etc/apt/sources.list.d/microsoft-edge.list
     ```

     Add the following line:

     ```bash
     deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main
     ```

     Then, download and add the Microsoft GPG key:

     ```bash
     wget -q https://packages.microsoft.com/keys/microsoft.asc -O microsoft.asc
     sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft.gpg microsoft.asc
     ```

   - Update the APT package list and check for available versions of Microsoft Edge:

     ```bash
     sudo apt update
     apt list -a microsoft-edge-stable
     ```

   - Install the latest matching version of Microsoft Edge:

     ```bash
     sudo apt install microsoft-edge-stable=123.0.2420.53-1
     ```

   - Download the matching version of Edge WebDriver and install it:

     ```bash
     sudo wget https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/123.0.2420.53/edgedriver_linux64.zip
     unzip edgedriver_linux64.zip
     sudo mv msedgedriver /usr/local/bin/
     ```

</details>

<details>
<summary>Login to instagra using selenium</summary>

```python
import time  # Imports the time module, used for adding delays in the script.
import pickle  # Imports the pickle module, used for serializing and deserializing objects.
import os  # Imports the os module, used for interacting with the operating system.
from selenium import webdriver  # Imports the webdriver module from Selenium, used for controlling web browsers.
from selenium.webdriver.common.by import By  # Imports By, which allows selecting elements by various attributes.
from selenium.webdriver.edge.options import Options  # Imports Options, which allows setting Edge browser options.
from selenium.webdriver.edge.service import Service  # Imports Service, which helps manage the Edge WebDriver service.
from selenium.webdriver.support.ui import WebDriverWait  # Imports WebDriverWait, used for waiting for conditions.
from selenium.webdriver.support import expected_conditions as EC  # Imports expected_conditions, which provides conditions to wait for.

class Instagram:
    def __init__(self, username=None, password=None):
        self.username = username  # Stores the username for Instagram login.
        self.password = password  # Stores the password for Instagram login.
        self.edge_options = Options()  # Creates an Options object for configuring Edge WebDriver.
        self.edge_options.use_chromium = True  # Configures the WebDriver to use Chromium-based Edge.
        self.edge_options.add_argument("--headless")  # Runs the browser in headless mode (without GUI).
        self.edge_options.add_argument("--mute-audio")  # Mutes any audio played by the browser.
        self.edge_options.add_argument("--disable-gpu")  # Disables GPU usage to avoid graphical issues.
        service = Service('/usr/local/bin/msedgedriver')  # Specifies the path to the Edge WebDriver executable.
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disables certain logging options.
        self.browser = webdriver.Edge(service=service, options=self.edge_options)  # Creates a new Edge browser instance with the specified options.
        self.browser.set_script_timeout(50)  # Sets the maximum time to wait for scripts to execute.

        self.browser.get('https://www.instagram.com')  # Opens the Instagram login page.
        self.wait_for_page_load()  # Calls a method to wait until the page is fully loaded.
        self.login()  # Calls the login method to log into Instagram.

    def wait_for_page_load(self):
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )  # Waits until the page's JavaScript has finished loading.

    def login(self):
        # Enter username
        username_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )  # Waits for the username input field to appear and selects it.
        username_input.send_keys(self.username)  # Types the username into the input field.

        # Enter password
        password_input = self.browser.find_element(By.NAME, 'password')  # Finds the password input field.
        password_input.send_keys(self.password)  # Types the password into the input field.

        # Click login button
        login_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")  # Finds the login button using XPath.
        login_button.click()  # Clicks the login button.

        # Wait for login to complete (home page or error message)
        self.wait_for_page_load()  # Waits until the next page is fully loaded.
        time.sleep(5)  # Add extra wait for redirection.

        # Check if login was successful
        if "https://www.instagram.com/" in self.browser.current_url:
            print("Login successful")
            print(self.browser.current_url)  # If extra param then account need auth 2FA very simple it can be solve easily hit me
        else:
            print("Login failed")

if __name__ == "__main__":
    username = "username"  # Placeholder for Instagram username.
    password = "passwd"  # Placeholder for Instagram password.

    insta_bot = Instagram(username, password)  # Creates an instance of the Instagram class and logs in with the provided credentials.

```
</details>

<details>
<summary>Saving and using cookies</summary>

```python
def save_cookies(self):
        try:
            print("Saving cookies to file...")
            with open("cookies.pkl", "wb") as f:
                pickle.dump(self.browser.get_cookies(), f)
            print("Cookies successfully saved.")
        except Exception as e:
            print(f"Error saving cookies: {e}")
```
#### Zoom and read log

![post and video quality](conf/image%20copy%205.png?raw=true)
</details>

<details>
<summary>Instagram (Cut Data)</summary>

```json

{

    "author": {

        "followers": 10142,

        "image": "https://instagram.flos5-3.fna.fbcdn.net/v/t51.28...",

        "name": "Nupat | Learn tech skills",

        "username": "nupat_technologies",

        "verified": false,

        "videos": 664

    },

    "content": {

        "cover": "https://instagram.flos5-2.fna.fbcdn.net/v/t51.2...",

        "desc": "The motivation to keep going always.\nWe are at it always, steady grinding 💪 💯",

        "id": "3423747737702041332",

        "likes": 12,

        "play": 82,

        "shortcode": "C-DmG16Rwb0",

        "views": 33

    },
 
    "media": [

        {

            "display_url": "https://instagram.flos5-3.fna.fbcdn.net/o1/v/t1...",

            "id": "3423747737702041332",

            "is_video": true,

           "shortcode": "C-DmG16Rwb0"

        }

    ],

    "platform": "instagram"

}

```
</details>

<details>
<summary>TikTok (Cut Data)</summary>

```json

{

    "author": {

        "followers": 38,

        "following": 3,

        "friends": 0,

        "image": "https://p16-sign-va.tiktokcdn.com/tos-maliva-avt...",

        "likes": 216,

        "name": "devfemibadmus",

        "username": "devfemibadmus",

        "verified": false,

        "videos": 7

    },

    "content": {

        "comments": 0,

        "cover": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva...",

        "desc": "24hrs #nigeriaprogrammer #debian",

        "id": "7390912680883899654",

        "likes": 7,

        "saves": 0,

        "share": 0,

        "views": 478

    },

    "is_video": true,

    "music": {

        "author": "devfemibadmus",

        "cover": "https://p16-sign-va.tiktokcdn.com/tos-maliva-avt..",

        "duration": 68,

        "src": "https://v16-webapp-prime.tiktok.com/video/tos/useast2a/tos-usea..",

        "title": "original sound - devfemibadmus"

    },

    "platform": "tiktok",

    "videos": [

        {

        "hq": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/a...",

            "size": 4528979

            }

        },

        {

        "fhd": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/a...",

            "size": 3692139

            }

        },

        {

        "hd": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/p...",

            "size": 2663135

            }

        }

    ]

}

```
</details>


### Sample Screenshot

![post and video quality](conf/image%20copy%205.png?raw=true)

| Screenshot | Screenshot |
|-------------------------------------------------------------|-------------------------------------------------------------|
| ![post and video quality](conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max).png?raw=true) | ![author and musicc](conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max)%20(1).png?raw=true) |
