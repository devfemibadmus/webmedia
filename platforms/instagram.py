import time, pickle, os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve().parent.parent

class Instagram:
    def __init__(self):
        self.username = "username"
        self.password = "password"
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_argument("--disable-gpu")
        service = Service(os.path.join(BASE_DIR, 'msedgedriver'))
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(service=service, options=self.edge_options)
        self.browser.set_script_timeout(50)

        self.graphql = "https://www.instagram.com/graphql/query/"

        print("Opening Instagram homepage...")
        self.browser.get('https://www.instagram.com')
        self.wait_for_page_load()

        if not self.login_with_cookies():
            self.login()

    def close(self):
        self.browser.quit()

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
            with open(os.path.join(BASE_DIR, "cookies.pkl"), "wb") as f:
                pickle.dump(self.browser.get_cookies(), f)
            print("Cookies successfully saved.")
        except Exception as e:
            print(f"Error saving cookies: {e}")

    def login_with_cookies(self):
        try:
            print("Attempting to login using saved cookies...")
            if os.path.exists(os.path.join(BASE_DIR, "cookies.pkl")):
                print("Loading cookies from file...")
                with open(os.path.join(BASE_DIR, "cookies.pkl"), "rb") as f:
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


    def get_slide_media(self, data):
        media = []
        if "edge_sidecar_to_children" in data and "edges" in data["edge_sidecar_to_children"]:
            for edge in data["edge_sidecar_to_children"]["edges"]:
                node = edge["node"]
                media_item = {
                    "id": node["id"],
                    "shortcode": node["shortcode"],
                    "address": node["display_url"],
                    'cover': node['display_url'],
                    "is_video": 'video_url' in node
                }
                if 'display_resources' in node:
                    media_item.update({
                        'address': node['display_resources'][-1]['src'],
                    })
                if 'video_url' in node:
                    media_item.update({
                        'address': node['video_url'],
                        'play': node['video_play_count'],
                        'views': node['video_view_count'],
                    })
                media.append(media_item)
        if "video_url" in data:
                media.append({
                    "id": data["id"],
                    "shortcode": data["shortcode"],
                    "address": data["video_url"],
                    "is_video": data["is_video"],
                    'cover': data['display_url'],
                })
        return media
    
    def get_instagram_data(self, data):
        try:
            item = data['data']['xdt_shortcode_media']
            if not item:
                return {'error': True, 'message': 'something went wrong', 'error_message': 'item not found in data'}, 502
            # print("item['shortcode']: ", item['shortcode'])
            data_info = {
                'platform':'instagram',
                'content': {
                    'id': item['id'],
                    'shortcode': item['shortcode'],
                    'likes': item['edge_media_preview_like']['count'],
                    'desc': item['edge_media_to_caption']['edges'][0]['node']['text'],
                    'cover': item['thumbnail_src'],
                },
                'author': {
                    'name': item['owner'].get('full_name', 'N/A'),
                    'username': item['owner'].get('username', 'N/A'),
                    'verified': item['owner'].get('is_verified', False),
                    'image': item['owner'].get('profile_pic_url', 'N/A'),
                    'videos': item['owner']['edge_owner_to_timeline_media'].get('count', 0),
                    'followers': item['owner']['edge_followed_by'].get('count', 0),
                },
                'media': self.get_slide_media(item),
            }
            if item['display_resources']:
                data_info['content']['cover'] = item['display_resources'][-1]['src']
            if item['is_video']:
                data_info['content'].update({
                    'views': item['video_view_count'],
                    'play': item['video_play_count']
                })
        
            return data_info, 200
        except Exception as e:
            return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500

    def getData(self, item_id, cut):
        instagram_data = {
            'av': '0',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': '3',
            '__hs': '19933.HYP:instagram_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'UNKNOWN',
            '__rev': '1015220271',
            '__comet_req': '7',
            'lsd': 'AVqipa-__e8',
            'jazoest': '2970',
            '__spin_r': '1015220271',
            '__spin_b': 'trunk',
            '__spin_t': '1722271940',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQueryQuery',
            'variables': '{"shortcode":"item_id"}',
            'server_timestamps': 'true',
            'doc_id': '25531498899829322'
        }
        instagramUrl = "https://www.instagram.com/graphql/query"
        instagram_data['variables'] = instagram_data['variables'].replace('item_id', item_id)
        js_script = f"""
            return new Promise(async (resolve, reject) => {{
                try {{
                    const response = await fetch('{instagramUrl}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                      }},
                      body: JSON.stringify({instagram_data})
                    }});
  
                    const data = await response.json();
                    resolve(data);
        
                  }} catch (e) {{
                    console.error(e.message);
                    reject(new Error(e.message));
                  }}
            }});
            """
        try:
            data = self.browser.execute_script(js_script)
            data['platform'] = 'instagram'
            if not cut:
                return data, 200
            data, status = self.get_instagram_data(data)
            return data, status
        except Exception as e:
            return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500


if __name__ == "__main__":
    print("Starting Instagram bot...")
    insta_bot = Instagram()
    data = insta_bot.getData('C8UahW1Nx4y', True)
    print(data)

