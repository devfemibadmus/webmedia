import time, re
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

    def get_video(self, file_folder, src):
        source = Validator.validate(src)
        print("source: ", source)
        if source == "TikTok":
            return self.scrape_tiktok_video(file_folder, src)
        elif source == "Instagram Post":
            return self.scrape_instagram_post(file_folder, src)
        elif source == "Facebook Reel":
            return self.scrape_facebook_reel(file_folder, src)
        elif source == "Facebook Video":
            return self.scrape_facebook_video(file_folder, src)
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
            try:
                response = self.post_video(file_folder=file_folder, src=tiktok_url, video_element_xpath=xpath, video_attribute=video_attribute, video_id=video_id)
            except Exception as e:
                response = {"message": f"{e}", "error": True}
                print(f"XPath: {xpath}. Error: {e}")
                continue
        return response

    def scrape_instagram_post(self, file_folder, instagram_url):
        pass

    def scrape_facebook_reel(self, file_folder, facebook_reel_url):
        pass

    def scrape_facebook_video(self, file_folder, facebook_src):
        pass

    def post_video(self, file_folder, src, video_element_xpath, video_attribute, video_id):
        self.browser.get(src)

        video_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, video_element_xpath))
        )

        src = video_element.get_attribute(video_attribute)
        

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

        self.browser.execute_script(f"window.open('{src}', '_blank');")
        time.sleep(5)

        self.browser.switch_to.window(self.browser.window_handles[-1])
        response_data = self.browser.execute_script(js_code)
        print("response_data: ", response_data)

        # response_data:  we are turning response to list, yes list yeah iknow we still working on tiktok oly and a tiktok video post only have one bu tthink of tiktok image post? it has mutiple images so we iterate through also in instagram photo and story post, also facebook story and photo post i dont know of youtube yet thou............wait do you think we should work on the list now or first do video test for all platform? i.e completing the scrap_{platform} function. Damn still have a long way to go............I didn't see this coming

        self.browser.quit()
        return response_data
        


"""
# Cum test
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@oorsz/video/7380872550236048645?is_from_webapp=1&sender_device=pc'
    scraper = Scraper()
    scraper.scrape_tiktok_video(tiktok_url)
"""

