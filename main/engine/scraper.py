import time, re
from flask import session
from selenium import webdriver
from engine.validator import Validator
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self):
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(options=self.edge_options)
        self.browser.delete_all_cookies()
        self.browser.set_script_timeout(320)

    def get_video(self, file_folder, video_url):
        source = Validator.validate(video_url)
        print("source: ", source)
        if source == "TikTok":
            return self.scrape_tiktok_video(file_folder, video_url)
        elif source == "Instagram Post":
            return self.scrape_instagram_post(file_folder, video_url)
        elif source == "Facebook Reel":
            return self.scrape_facebook_reel(file_folder, video_url)
        elif source == "Facebook Video":
            return self.scrape_facebook_video(file_folder, video_url)
        else:
            print(f"Unsupported video source: {source}")
            return False

    def scrape_tiktok_video(self, file_folder, tiktok_url):
        video_element_xpaths = [
            '//div[@class="css-8lv75m-DivBasicPlayerWrapper e1yey0rl2"]/div/video'
        ]
        video_id_match = re.search(r'video/(\d+)', tiktok_url)
        video_attribute = 'src'
        video_id = video_id_match.group(1) if video_id_match else None
        response = {"error":False, "message":"response_data['message']"}
        for xpath in video_element_xpaths:
            session.clear()
            try:
                response_data = self.post_video(file_folder=file_folder, video_url=tiktok_url, video_element_xpath=xpath, video_attribute=video_attribute, video_id=video_id)
                if response_data['message'] == "Video uploaded successfully!":
                    response = {"video_url":response_data['video_url'], "success":True, "message": f"{response_data['message']}"}
                else:
                    response = {"error":True, "message": f"{response_data['message']}"}
            except Exception as e:
                response = {"error":True, "message": f"{e}"}
                print(f"XPath: {xpath}. Error: {e}")
                continue
        return response

    def scrape_instagram_post(self, file_folder, instagram_url):
        pass

    def scrape_facebook_reel(self, file_folder, facebook_reel_url):
        pass

    def scrape_facebook_video(self, file_folder, facebook_video_url):
        pass

    def post_video(self, file_folder, video_url, video_element_xpath, video_attribute, video_id):
        self.browser.get(video_url)

        video_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, video_element_xpath))
        )

        video_url = video_element.get_attribute(video_attribute)
        

        js_code = f"""
            return new Promise((resolve, reject) => {{
                var videoElement = document.querySelector('video');
                var videoUrl = videoElement.querySelector('source').src;
                fetch(videoUrl)
                .then(response => response.blob())
                .then(blob => {{
                    var formData = new FormData();
                    formData.append('file', blob, '{video_id}.mp4');
                    formData.append('file_folder', '{file_folder}');
                    return fetch('http://localhost:5000/upload-video', {{
                        method: 'POST',
                        body: formData
                    }});
                }})
                .then(response => response.json())
                .then(data => {{
                    resolve(data);
                }})
                .catch(error => {{
                    reject(error);
                }});
            }});
            """

        self.browser.execute_script(f"window.open('{video_url}', '_blank');")
        time.sleep(5)

        self.browser.switch_to.window(self.browser.window_handles[-1])
        response_data = self.browser.execute_script(js_code)
        print("response_data: ", response_data)

        # response_data:  {'message': 'Video uploaded successfully!', 'success': True, 'video_url': 'https://storage.googleapis.com/mediasaver/07-15-2024/18%3A36%3A47/7390912680883899654.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=931067452340-compute%40developer.gserviceaccount.com%2F20240715%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240715T173742Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=547128b07497f11121d73096a31623b07604aa6cf03d7a43c64fbbfd60535201fc2ca177a59880969163a4ed12f4c167d00f19c591a218400d5ff268978a77019763b13fcbd3450e7f245d5a3a8da4f476c6cfba2beba2182d854f01457ff79ae5de7d1d02ee123d2f33db02ac1a355e9e059001f1a6a9ad8a5163c274fe9d6b3da02fe3182d6991ae7fa8d4655b7b5253b9d4bf4706996cafc2748bc1cbc2aaef65dd604d3994d01f8cffc0145226e350fbf715021720cbd47baa1a3eb1da7f0bc7607139ca3d87a78a23a10dbd99351d59d74d9f7791b7c28921d32a6033ebe00df602cf0a3571f0db80df1cb34f0cf677c5c1d25a03a94ce40fb7ee250c67'} 

        self.browser.quit()
        return response_data
        


"""
# Cum test
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@oorsz/video/7380872550236048645?is_from_webapp=1&sender_device=pc'
    scraper = Scraper()
    scraper.scrape_tiktok_video(tiktok_url)
"""

