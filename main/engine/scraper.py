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

    def get_video(self, src):
        source = Validator.validate(src)
        print("source: ", source)
        if source == "TikTok":
            return self.scrape_tiktok_video(src)
        elif source == "Instagram Post":
            return self.scrape_instagram_post(src)
        elif source == "Facebook Reel":
            return self.scrape_facebook_reel(src)
        elif source == "Facebook Video":
            return self.scrape_facebook_video(src)
        else:
            print(f"Unsupported video source: {source}")
            return False

    def scrape_tiktok_video(self, tiktok_url):
        media_element_xpaths = [
            '//div[@class="css-8lv75m-DivBasicPlayerWrapper e1yey0rl2"]/div/video'
        ]
        # media_element_xpaths images/
        username_element_xpath = '//span[@data-e2e="browse-username" and contains(@class, "css-1c7urt-SpanUniqueId")]'
        media_id_match = re.search(r'video/(\d+)', tiktok_url)
        media_id = media_id_match.group(1) if media_id_match else None
        response = {"error":False, "message":"default"}
        for xpath in media_element_xpaths:
            try:
                response = self.upload_media("TikTok", tiktok_url, username_element_xpath, xpath, media_id)
            except Exception as e:
                response = {"message": f"{e}", "error": True}
                print(f"XPath: {xpath}. Error: {e}")
                continue
        return response

    def scrape_instagram_post(self, instagram_url):
        pass

    def scrape_facebook_reel(self, facebook_reel_url):
        pass

    def scrape_facebook_video(self, facebook_src):
        pass

    def upload_media(self, platform, media_url, username_element_xpath, media_element_xpath, media_id):
        self.browser.get(media_url)

        video_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, media_element_xpath))
        )

        username = self.browser.find_element(By.XPATH, username_element_xpath).text
        media_src = video_element.get_attribute('src')
        file_folder = platform+"/"+username
        
        js_code = f"""
            return new Promise((resolve, reject) => {{
                var formData = new FormData();

                // Function to fetch and append videos to formData
                var fetchVideos = () => {{
                    var videoElements = document.querySelectorAll('video');
                    return Promise.all(Array.from(videoElements).map((videoElement, index) => {{
                        var videoUrl = videoElement.querySelector('source').src;
                        return fetch(videoUrl)
                        .then(response => response.blob())
                        .then(blob => {{
                            formData.append(`file_${{index}}`, blob, `{media_id}_${{index}}.mp4`);
                        }});
                    }}));
                }};

                // Function to fetch and append images to formData
                var fetchImages = () => {{
                    var imgElements = document.querySelectorAll('img');
                    return Promise.all(Array.from(imgElements).map((imgElement, index) => {{
                        var imageUrl = imgElement.src;
                        return fetch(imageUrl)
                        .then(response => response.blob())
                        .then(blob => {{
                            formData.append(`file_${{index}}`, blob, `{media_id}_${{index}}.jpg`);
                        }});
                    }}));
                }};

                // Fetch videos and images, then post formData and log response
                formData.append('file_folder', '{file_folder}');
                Promise.all([fetchVideos(), fetchImages()])
                .then(() => {{
                    return fetch('http://localhost:5000/upload-video', {{
                        method: 'POST',
                        body: formData
                    }});
                }})
                .then(response => response.json()) // assuming the response is JSON
                .then(data => {{
                    console.log('Response from server:', data);
                    resolve(data); // resolve the promise with the response data
                }})
                .catch(error => {{
                    console.error('Error fetching media or posting data:', error);
                    reject(error); // reject the promise with the error
                }});
            }});
        """

        self.browser.execute_script(f"window.open('{media_src}', '_blank');")
        time.sleep(5)

        self.browser.switch_to.window(self.browser.window_handles[-1])
        response_data = self.browser.execute_script(js_code)
        print("response_data: ", response_data)

        self.browser.quit()
        return response_data
        


"""
# Cum test
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@oorsz/video/7380872550236048645?is_from_webapp=1&sender_device=pc'
    scraper = Scraper()
    scraper.scrape_tiktok_video(tiktok_url)
"""

