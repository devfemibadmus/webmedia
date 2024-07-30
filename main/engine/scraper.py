import time, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from engine.helper import GlobalMessagesManager, Validator
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, userId):
        self.userId = userId
        self.edge_options = Options()
        self.globalMessage = GlobalMessagesManager(userId)
        self.edge_options.use_chromium = True
        # self.edge_options.add_argument("--headless")
        # self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(options=self.edge_options)
        self.browser.set_script_timeout(320)
        self.browser.delete_all_cookies()
        print("Scraper userId: ", self.userId, " start", datetime.now().strftime("%H:%M:%S"))

    def getMedia(self, src):
        source = Validator.validate(src)
        print("src: ", src)
        print("source: ", source)
        if source == "TikTok":
            return self.scrapTiktok(src)
        elif source == "Instagram Post":
            return self.scrapInstagram(src)
        elif source == "Facebook Video":
            return self.scrap_facebook_video(src)
        else:
            print(f"Unsupported video source: {source}")
            return "Error: Unsupported video source"

    def scrapTiktok(self, url):
        mediaElement_classNames = ['css-1sb4dwc-DivPlayerContainer', 'swiper-slide']
        usernameElement_xpath = '//span[@data-e2e="browse-username"]'
        media_id = re.search(r'(video|photo)/(\d+)', url)
        media_id = media_id.group(2) if media_id else None
        return self.cloudUrl("TikTok", url, usernameElement_xpath, mediaElement_classNames, media_id)

    def scrapInstagram(self, url):
        mediaElement_classNames = ['css-1sb4dwc-DivPlayerContainer', 'swiper-slide']
        usernameElement_xpath = "//div[text()[normalize-space()='More posts from']]/following-sibling::a"
        media_id = re.search(r'/p/([^/]+)/', url)
        media_id = media_id.group(2) if media_id else None
        return self.cloudUrl("Instagram", url, usernameElement_xpath, mediaElement_classNames, media_id)

    def scrap_facebook_reel(self, facebook_reel_url):
        pass

    def scrapFacebook(self, facebook_src):
        mediaElement_classNames = ['inline-video-container']
        usernameElement_xpath = "//div[text()[normalize-space()='More posts from']]/following-sibling::a"
        media_id = re.search(r'/p/([^/]+)/', url)
        media_id = media_id.group(2) if media_id else None
        return self.cloudUrl("Instagram", url, usernameElement_xpath, mediaElement_classNames, media_id)

    def cloudUrl(self, platform, media_url, usernameElement_xpath, mediaElement_classNames, media_id, new_doc=False):
        try:
            print("Have reach here")
            self.globalMessage.updateMessage(f"loading {media_url}")
            if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                self.browser.quit()
                return f"page unload or spam"
            self.browser.get(media_url)
        except Exception as e:
            print("self.browser.session_id: ", self.browser.session_id)
            print("Scraper userId: ", self.userId, " stop 1 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            self.globalMessage.updateMessage("slow internet detected")
            self.globalMessage.setData([], [])
            return f"Error loading page: {e}"
        # finally:
            # print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            # self.browser.quit()
            # return f"Error loading page. Test"

        try:
            if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                self.browser.quit()
                print("page unload or spam")
                return f"page unload or spam"
            username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
            self.globalMessage.updateMessage(f"username: {username}")
        except Exception as e:
            self.globalMessage.updateMessage(f"retrying get username")
            try:
                if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                    self.browser.quit()
                    print("page unload or spam")
                    return f"page unload or spam"
                print("refreshing: ")
                self.browser.refresh()
                print("refreshed: ")
                if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                    self.browser.quit()
                    print("page unload or spam")
                    return f"page unload or spam"
                username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
                self.globalMessage.updateMessage(f"username: {username}")
            except Exception as e:
                print("Scraper userId: ", self.userId, " stop 2 : ", datetime.now().strftime("%H:%M:%S"))
                self.browser.quit()
                self.globalMessage.updateMessage("")
                self.globalMessage.setData([], [])
                return f"Error getting username: {e}"

        file_folder = f"{platform}/{username}"
        uploadedMediaSrcList = []
        mediaSrc = []
        cloudUrl = []

        try:
            for className in mediaElement_classNames:
                if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                    self.browser.quit()
                    print("page unload or spam")
                    return f"page unload or spam"
                self.globalMessage.updateMessage(f"finding media")
                elements = self.browser.find_elements(By.CLASS_NAME, className)
                for element in elements:
                    if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                       self.browser.quit()
                       print("page unload or spam")
                       return f"page unload or spam"
                    try:
                        self.globalMessage.updateMessage(f"finding videos")
                        video_tags = element.find_elements(By.TAG_NAME, 'video')
                        for video in video_tags:
                            src = video.get_attribute('src') or video.find_element(By.TAG_NAME, 'source').get_attribute('src')
                            if src:
                                mediaSrc.append(src)
                    except Exception as e:
                        continue
                    try:
                        self.globalMessage.updateMessage(f"finding images")
                        image_tags = element.find_elements(By.TAG_NAME, 'img')
                        for image in image_tags:
                            src = image.get_attribute('src')
                            if src:
                                mediaSrc.append(src)
                    except Exception as e:
                        continue
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop 3 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            self.globalMessage.updateMessage("")
            self.globalMessage.setData([], [])
            return f"Error finding media elements: {e}"
        finally:
            mediaSrc = list(set(mediaSrc))
            self.globalMessage.updateMessage(f"Total media found {len(mediaSrc)}")

        # time.sleep(2)

        def formScrpt(boot):
            return f"""
            return new Promise((resolve, reject) => {{
                try {{
                    var formData = new FormData();
                    const isImage = document.querySelectorAll('img');
                    const isVideo = document.querySelectorAll('video');
                    
                    const isImagePresent = isImage.length > 0;
                    const formats = isImagePresent ? 'jpg' : 'mp4';
                    const mediaType = isImagePresent ? 'image' : 'video';
                    const mediaElements = isImagePresent ? isImage : isVideo;

                    Promise.all(Array.from(mediaElements).map((mediaElement, index) => {{
                        if (mediaElements.length >= 1){{
                            var mediaUrl = isImagePresent ? mediaElement.src : mediaElement.querySelector('source').src;
                            return fetch(mediaUrl)
                                .then(response => response.blob())
                                .then(blob => {{
                                    formData.append(`${{mediaType}}_{boot}`, blob, `{media_id}_{boot}.${{formats}}`);
                                    formData.append('mediaType', `${{mediaType}}`);
                                }})
                                .catch(error => {{
                                    throw new Error(`Error fetching media URL: ${{error}}`);
                                }});
                        }} else {{
                            console.log(`No media elements found in URL ${{window.location.href}}`);
                            console.log(`No media elements found in URL ${{window.location.href}}`);
                            resolve(JSON.stringify({{"data": []}}))
                        }}
                    }}))
                    .then(() => {{
                        formData.append('file_folder', '{file_folder}');
                        fetch('http://localhost:5000/uploadMedia', {{
                            method: 'POST',
                            body: formData
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            console.log('Response from server(media):', data);
                            resolve(data);
                        }})
                        .catch(error => {{
                            console.error('Error posting media data:', error);
                            reject(error);
                        }});
                    }})
                    .catch(error => {{
                        reject(`Error processing media elements: ${{error}}`);
                    }});
                }} catch (error) {{
                    reject(`Error in mediaScrpt: ${{error}}`);
                }}
            }});
            """

        print("mediaSrc: ", mediaSrc)

        if len(mediaSrc) <= 0:
            print("Scraper userId: ", self.userId, " stop 4 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            self.globalMessage.updateMessage("No Media Found!")
            self.globalMessage.setData([], [])
            return f"No Media Found!"
        try:
            for boot, puss in enumerate(mediaSrc):
                self.globalMessage.updateMessage(f"Scraping {boot+1} of {len(mediaSrc)}")
                self.browser.execute_script(f"window.open('{puss}', '_blank');")
                self.browser.switch_to.window(self.browser.window_handles[-1])
                page_source = self.browser.page_source
                if not '<video' in page_source or not '<img' in page_source:
                    print("refreshing: ", puss)
                    self.browser.refresh()
                    print("refreshed: ", puss)
                # time.sleep(3)
                if self.globalMessage.pageUnload() or self.globalMessage.spamRequest():
                    self.browser.quit()
                    print("page unload or spam")
                    return f"page unload or spam"
                uploadedMediaDick = WebDriverWait(self.browser, 60).until(lambda driver: driver.execute_script(formScrpt(boot)))
                print("the url: ",puss, " index: ", boot)
                print("uploadedMediaDick: ",uploadedMediaDick)
                uploadedMediaSrcList.append(uploadedMediaDick)
                if uploadedMediaDick['src']:
                    cloudUrl.append(uploadedMediaDick['src'])
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.globalMessage.setData(uploadedMediaSrcList, cloudUrl)
                self.globalMessage.updateMessage(f"scraped {boot+1} of {len(mediaSrc)}")
            self.globalMessage.updateMessage(f"Done scraping {len(uploadedMediaSrcList)} media in {media_url}")
            print("Scraper userId: ", self.userId, " finished : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            return f"Scraping completed successfully!"
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop 5 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            self.globalMessage.updateMessage("")
            self.globalMessage.setData([], [])
            return f"Error executing media upload script: {e}"


