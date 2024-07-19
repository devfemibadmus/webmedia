import time, re
from datetime import datetime
from selenium import webdriver
from engine.validator import Validator
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, userId):
        self.userId = userId
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(options=self.edge_options)
        self.browser.delete_all_cookies()
        self.browser.set_script_timeout(320)
        print("Scraper userId: ", self.userId, " start", datetime.now().strftime("%H:%M:%S"))

    def close(self):
        try:
            print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            self.browser.delete_all_cookies()
            self.browser.quit()
            return True
        except Exception as e:
            print("Scraper userId: ", self.userId, " unable to stop: ", datetime.now().strftime("%H:%M:%S"))
            return False

    def getMedia(self, src):
        source = Validator.validate(src)
        print("source: ", source)
        if source == "TikTok":
            return self.scrapTiktok(src)
        elif source == "Instagram Post":
            return self.scrapInstagram(src)
        elif source == "Facebook Video":
            return self.scrap_facebook_video(src)
        else:
            print(f"Unsupported video source: {source}")
            return False

    def scrapTiktok(self, tiktok_url):
        mediaElement_classNames = ['css-1sb4dwc-DivPlayerContainer', 'swiper-slide']
        usernameElement_xpath = '//span[@data-e2e="browse-username"]'
        media_id = re.search(r'(video|photo)/(\d+)', tiktok_url)
        media_id = media_id.group(2) if media_id else None
        return self.cloudUrl("TikTok", tiktok_url, usernameElement_xpath, mediaElement_classNames, media_id)

    def scrapInstagram(self, instagram_url):
        mediaElement_classNamess = [
            '//div[@class="css-8lv75m-DivBasicPlayerWrapper e1yey0rl2"]/div/video'
        ]
        usernameElement_xpath = '//a[contains(@class, "_acan") and contains(@class, "_acao") and contains(@class, "_acat") and contains(@class, "_acaw")][1]'
        media_id = instagram_url.split('.com/p/')[1].split('/')[0]
        for xpath in mediaElement_classNamess:
            try:
                return self.cloudUrl("Instagram", instagram_url, usernameElement_xpath, xpath, media_id, True)
            except Exception as e:
                return {"message": f"{e}", "error": True}
                print(f"XPath: {xpath}. Error: {e}")
                continue
        return {"error":False, "message":"default"}

    def scrap_facebook_reel(self, facebook_reel_url):
        pass

    def scrap_facebook_video(self, facebook_src):
        pass

    def cloudUrl(self, platform, media_url, usernameElement_xpath, mediaElement_classNames, media_id, new_doc=False):
        try:
            self.browser.get(media_url)
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            return f"Error loading page. Try Again!"
            # return f"Error loading page: {e}"
        # finally:
            # print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            # self.browser.quit()
            # return f"Error loading page. Test"

        try:
            username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            return f"Error getting username. Try Again!"
            # return f"Error getting username: {e}"

        file_folder = f"{platform}/{username}"
        uploadedMediaSrcList = {}
        mediaSrc = []

        try:
            for className in mediaElement_classNames:
                elements = self.browser.find_elements(By.CLASS_NAME, className)
                for element in elements:
                    try:
                        video_tags = element.find_elements(By.TAG_NAME, 'video')
                        for video in video_tags:
                            src = video.get_attribute('src') or video.find_element(By.TAG_NAME, 'source').get_attribute('src')
                            if src:
                                mediaSrc.append(src)
                    except Exception as e:
                        continue
                    try:
                        image_tags = element.find_elements(By.TAG_NAME, 'img')
                        for image in image_tags:
                            src = image.get_attribute('src')
                            if src:
                                mediaSrc.append(src)
                    except Exception as e:
                        continue
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            return f"Error finding media elements. Try Again!"
            # return f"Error finding media elements: {e}"
        finally:
            mediaSrc = list(set(mediaSrc))

        mediaScript = f"""
            return new Promise((resolve, reject) => {{
                try {{
                    var formData = new FormData();
                    Promise.all(
                        {mediaSrc}.map((src, index) => 
                            fetch(src)
                                .then(response => {{
                                    if (!response.ok) {{
                                        throw new Error(`HTTP error! status: ${{response.status}}`);
                                    }}
                                    var contentType = response.headers.get('Content-Type');
                                    return response.blob().then(blob => ({{ blob, contentType, index }}));
                                }})
                        )
                    )
                    .then(results => {{
                        results.forEach(({{blob, contentType, index}}) => {{
                            if (contentType.startsWith('image/')) {{
                                formData.append(`image_${{index}}`, blob, `{media_id}_${{index}}.jpg`);
                            }} else if (contentType.startsWith('video/')) {{
                                formData.append(`video_${{index}}`, blob, `{media_id}_${{index}}.mp4`);
                            }} else {{
                                throw new Error(`Unsupported content type: ${{contentType}}`);
                            }}
                        }});
                        formData.append('file_folder', '{file_folder}');
                        return fetch('http://localhost:5000/uploadMedia', {{
                            method: 'POST',
                            body: formData
                        }});
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        console.log('Response from server:', data);
                        resolve(data);
                    }})
                    .catch(error => {{
                        console.error('Error posting data:', error);
                        reject(error);
                    }});
                }} catch (error) {{
                    reject(`Error in script: ${{error}}`);
                }}
            }});
        """

        try:
            print(mediaSrc)
            if len(mediaSrc) <= 0:
                print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
                self.browser.quit()
                return f"No Media Found!"
            self.browser.execute_script(f"window.open('{mediaSrc[0]}', '_blank');")
            time.sleep(2)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            try:
                uploadedMediaDick = self.browser.execute_script(mediaScript)
                uploadedMediaSrcList.update(uploadedMediaDick)
                print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
                self.browser.quit()
                return uploadedMediaSrcList
            except Exception as e:
                print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
                self.browser.quit()
                # return f"Error executing media upload script. Try Again!"
                return f"Error executing media upload script: {e}"
                
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            return f"General error. Try Again!"
            # return f"General error: {e}"


"""
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@devfemibadmus/video/7390912680883899654'
    scraper = Scraper()
    scraper.scrapTiktok(tiktok_url)
"""

