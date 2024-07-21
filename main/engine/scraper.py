import time, re
from flask import session
from engine.helper import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, userId):
        self.userId = userId
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        # self.edge_options.add_argument("--headless")
        # self.edge_options.add_argument("--disable-gpu")
        # self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(options=self.edge_options)
        self.browser.set_script_timeout(320)
        self.browser.delete_all_cookies()
        print("Scraper userId: ", self.userId, " start", datetime.now().strftime("%H:%M:%S"))

    def close(self):
        try:
            if self.browser.session_id:
                self.browser.delete_all_cookies()
                self.browser.quit()
                print("Scraper userId: ", self.userId, " browser Quit : ", datetime.now().strftime("%H:%M:%S"))
            else:
                print("Scraper userId: ", self.userId, " browser already Quit by user : ", datetime.now().strftime("%H:%M:%S"))
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
            update_message(session['userId'], f"loading {media_url}")
            if page_unload(session['userId']):
                self.browser.quit()
                return f"User close or refresh page"
            self.browser.get(media_url)
        except Exception as e:
            print("self.browser.session_id: ", self.browser.session_id)
            print("Scraper userId: ", self.userId, " stop 1 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            update_message(session['userId'], "")
            set_data(session['userId'], [])
            return f"Error loading page: {e}"
        # finally:
            # print("Scraper userId: ", self.userId, " stop: ", datetime.now().strftime("%H:%M:%S"))
            # self.browser.quit()
            # return f"Error loading page. Test"

        try:
            if page_unload(session['userId']):
                self.browser.quit()
                print("User close or refresh page")
                return f"User close or refresh page"
            username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
            update_message(session['userId'], f"username: {username}")
        except Exception as e:
            update_message(session['userId'], f"retrying get username")
            try:
                if page_unload(session['userId']):
                    self.browser.quit()
                    print("User close or refresh page")
                    return f"User close or refresh page"
                print("refreshing: ")
                self.browser.refresh()
                print("refreshed: ")
                if page_unload(session['userId']):
                    self.browser.quit()
                    print("User close or refresh page")
                    return f"User close or refresh page"
                username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, usernameElement_xpath))).text
                update_message(session['userId'], f"username: {username}")
            except Exception as e:
                print("Scraper userId: ", self.userId, " stop 2 : ", datetime.now().strftime("%H:%M:%S"))
                self.browser.quit()
                update_message(session['userId'], "")
                set_data(session['userId'], [])
                return f"Error getting username: {e}"

        file_folder = f"{platform}/{username}"
        uploadedMediaSrcList = []
        mediaSrc = []

        try:
            for className in mediaElement_classNames:
                if page_unload(session['userId']):
                    self.browser.quit()
                    print("User close or refresh page")
                    return f"User close or refresh page"
                elements = self.browser.find_elements(By.CLASS_NAME, className)
                for element in elements:
                    if page_unload(session['userId']):
                       self.browser.quit()
                       print("User close or refresh page")
                       return f"User close or refresh page"
                    try:
                        update_message(session['userId'], f"finding videos...")
                        video_tags = element.find_elements(By.TAG_NAME, 'video')
                        for video in video_tags:
                            src = video.get_attribute('src') or video.find_element(By.TAG_NAME, 'source').get_attribute('src')
                            if src:
                                mediaSrc.append(src)
                    except Exception as e:
                        continue
                    try:
                        update_message(session['userId'], f"finding images...")
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
            update_message(session['userId'], "")
            set_data(session['userId'], [])
            return f"Error finding media elements: {e}"
        finally:
            mediaSrc = list(set(mediaSrc))
            update_message(session['userId'], f"Total media found: {len(mediaSrc)}")
            

        time.sleep(5)

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
                                .catch(error => {{
                                    console.error(`Error fetching URL: ${{src}} - Error: ${{error.message}}`);
                                    throw error;
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
                            // var mediaUrl = mediaElement.src || mediaElement.querySelector('source').src;
                            var mediaUrl = isImagePresent ? mediaElement.src : mediaElement.querySelector('source').src;
                            return fetch(mediaUrl)
                                .then(response => response.blob())
                                .then(blob => {{
                                    formData.append(`${{mediaType}}_{boot}`, blob, `{media_id}_{boot}.${{formats}}`);
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
            update_message(session['userId'], "")
            set_data(session['userId'], [])
            return f"No Media Found!"
        try:
            for boot, puss in enumerate(mediaSrc):
                update_message(session['userId'], f"Scraping {boot+1} of {len(mediaSrc)}")
                self.browser.execute_script(f"window.open('{puss}', '_blank');")
                self.browser.switch_to.window(self.browser.window_handles[-1])
                page_source = self.browser.page_source
                if not '<video' in page_source or not '<img' in page_source:
                    print("refreshing: ", puss)
                    self.browser.refresh()
                    print("refreshed: ", puss)
                time.sleep(3)
                if page_unload(session['userId']):
                    self.browser.quit()
                    print("User close or refresh page")
                    return f"User close or refresh page"
                uploadedMediaDick = WebDriverWait(self.browser, 60).until(lambda driver: driver.execute_script(formScrpt(boot)))
                print("the url: ",puss, " index: ", boot)
                print("uploadedMediaDick: ",uploadedMediaDick)
                uploadedMediaSrcList.append(uploadedMediaDick)
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                set_data(session['userId'], uploadedMediaSrcList)
                update_message(session['userId'], f"scraped {boot+1} of {len(mediaSrc)}")
            update_message(session['userId'], f"Total scrape media {len(uploadedMediaSrcList)} of {len(mediaSrc)}")
            print("Scraper userId: ", self.userId, " finished : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            update_message(session['userId'], "")
            return f"Done!"
        except Exception as e:
            print("Scraper userId: ", self.userId, " stop 5 : ", datetime.now().strftime("%H:%M:%S"))
            self.browser.quit()
            update_message(session['userId'], "")
            set_data(session['userId'], [])
            return f"Error executing media upload script: {e}"


"""
if __name__ == "__main__":
    tiktok_url = 'https://www.tiktok.com/@devfemibadmus/video/7390912680883899654'
    scraper = Scraper()
    scraper.scrapTiktok(tiktok_url)
"""

