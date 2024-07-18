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

    def get_media(self, src):
        source = Validator.validate(src)
        print("source: ", source)
        if source == "TikTok":
            return self.scrape_tiktok(src)
        elif source == "Instagram Post":
            return self.scrape_instagram(src)
        elif source == "Facebook Video":
            return self.scrape_facebook_video(src)
        else:
            print(f"Unsupported video source: {source}")
            return False

    def scrape_tiktok(self, tiktok_url):
        # Done
        mediaElement_classNames = ['css-1sb4dwc-DivPlayerContainer']
        usernameElement_xpath = '//span[@data-e2e="browse-username"]'
        media_id = re.search(r'(video|photo)/(\d+)', tiktok_url)
        media_id = media_id.group(2) if media_id else None
        return self.scrap_mediaUrl("TikTok", tiktok_url, usernameElement_xpath, mediaElement_classNames, media_id)

    def scrape_instagram(self, instagram_url):
        mediaElement_classNamess = [
            '//div[@class="css-8lv75m-DivBasicPlayerWrapper e1yey0rl2"]/div/video'
        ]
        usernameElement_xpath = '//a[contains(@class, "_acan") and contains(@class, "_acao") and contains(@class, "_acat") and contains(@class, "_acaw")][1]'
        media_id = instagram_url.split('.com/p/')[1].split('/')[0]
        for xpath in mediaElement_classNamess:
            try:
                return self.scrap_mediaUrl("Instagram", instagram_url, usernameElement_xpath, xpath, media_id, True)
            except Exception as e:
                return {"message": f"{e}", "error": True}
                print(f"XPath: {xpath}. Error: {e}")
                continue
        return {"error":False, "message":"default"}

    def scrape_facebook_reel(self, facebook_reel_url):
        pass

    def scrape_facebook_video(self, facebook_src):
        pass

    def scrap_mediaUrl(self, platform, media_url, usernameElement_xpath, mediaElement_classNames, media_id, new_doc=False):
        try:
            self.browser.get(media_url)
        except Exception as e:
            self.browser.quit()
            return f"Error loading page: {e}"

        try:
            username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
        except Exception as e:
            self.browser.quit()
            return f"Error getting username: {e}"

        file_folder = f"{platform}/{username}"
        uploadedMediaSrcList = {'data':[]}
        videoSrcList = []

        try:
            for className in mediaElement_classNames:
                elements = self.browser.find_elements(By.CLASS_NAME, className)
                for element in elements:
                    video_tags = element.find_elements(By.TAG_NAME, 'video')
                    for video in video_tags:
                        src = video.get_attribute('src') or video.find_element(By.TAG_NAME, 'source').get_attribute('src')
                        if src:
                            videoSrcList.append(src)
        except Exception as e:
            self.browser.quit()
            return f"Error finding media elements: {e}"

        videoScrpt = f"""
            return new Promise((resolve, reject) => {{
                try {{
                    var formData = new FormData();
                    var videoElements = document.querySelectorAll('video');
                    Promise.all(Array.from(videoElements).map((videoElement, index) => {{
                        var videoUrl = videoElement.src || videoElement.querySelector('source').src;
                        return fetch(videoUrl)
                            .then(response => response.blob())
                            .then(blob => {{
                                formData.append(`video_${{index}}`, blob, `{media_id}_${{index}}.mp4`);
                            }})
                            .catch(error => {{
                                throw new Error(`Error fetching video URL: ${{error}}`);
                            }});
                    }}))
                    .then(() => {{
                        formData.append('file_folder', '{file_folder}');
                        fetch('http://localhost:5000/upload-video', {{
                            method: 'POST',
                            body: formData
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            console.log('Response from server(video):', data);
                            resolve(data);
                        }})
                        .catch(error => {{
                            console.error('Error posting video data:', error);
                            reject(error);
                        }});
                    }})
                    .catch(error => {{
                        reject(`Error processing video elements: ${{error}}`);
                    }});
                }} catch (error) {{
                    reject(`Error in videoScrpt: ${{error}}`);
                }}
            }});
        """

        imageScrpt = f"""
            return new Promise((resolve, reject) => {{
                try {{
                    var formData = new FormData();
                    var postBody = {mediaElement_classNames}
                        .map(className => document.querySelector(`.${{className}}`))
                        .find(element => element !== null);

                    if (!postBody) {{
                        throw new Error("Post body not found");
                    }}

                    var imgElements = postBody.querySelectorAll('img');
                    Promise.all(Array.from(imgElements).map((imgElement, index) => {{
                        var imgUrl = imgElement.src || imgElement.querySelector('source').src;
                        console.log("imgUrl: ", imgUrl)
                        return fetch(imgUrl)
                            .then(response => response.blob())
                            .then(blob => {{
                                formData.append(`image_${{index}}`, blob, `{media_id}_${{index}}.jpg`);
                            }})
                            .catch(error => {{
                                throw new Error(`Error fetching image URL: ${{error}}`);
                            }});
                    }}))
                    .then(() => {{
                        formData.append('file_folder', '{file_folder}');
                        fetch('http://localhost:5000/upload-video', {{
                            method: 'POST',
                            body: formData
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            console.log('Response from server:', data);
                            resolve(data);
                        }})
                        .catch(error => {{
                            console.log(formData)
                            console.error('Error posting data:', error);
                            reject(error);
                        }});
                    }})
                    .catch(error => {{
                        reject(`Error processing image elements: ${{error}}`);
                    }});
                }} catch (error) {{
                    reject(`Error in imageScrpt: ${{error}}`);
                }}
            }});
        """

        try:
            try:
                uploadedImages = self.browser.execute_script(imageScrpt)
                print(uploadedImages)
                uploadedMediaSrcList.update(uploadedImages)
            except Exception as e:
                self.browser.quit()
                return f"Error executing image script: {e}"

            for src in videoSrcList:
                self.browser.execute_script(f"window.open('{src}', '_blank');")
                time.sleep(2)
                self.browser.switch_to.window(self.browser.window_handles[-1])
                try:
                    uploadedVideos = self.browser.execute_script(videoScrpt)
                    print(uploadedVideos)
                    for dick in uploadedVideos['data']:
                        uploadedMediaSrcList['data'].append(dick)
                except Exception as e:
                    self.browser.quit()
                    return f"Error executing video script: {e}"
                    
                # self.browser.close()

            try:
                self.browser.quit()
                return uploadedMediaSrcList
            except Exception as e:
                self.browser.quit()
                return f"Error executing media upload script: {e}"
        except Exception as e:
            self.browser.quit()
            return f"General error: {e}"

        # self.browser.execute_script(f"window.open('{media_src}', '_blank');")
        # time.sleep(5)

        # self.browser.switch_to.window(self.browser.window_handles[-1])

        # response_data = self.browser.execute_script(js_upload)
        # print("response_data: ", response_data)

        # return response_data


"""
# Cum test
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@oorsz/video/7380872550236048645?is_from_webapp=1&sender_device=pc'
    scraper = Scraper()
    scraper.scrape_tiktok(tiktok_url)
"""

