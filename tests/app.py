from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/12.0 Mobile/15A372 Safari/604.1")
}

edge_options = Options()
edge_options.add_experimental_option("mobileEmulation", mobile_emulation)
edge_options.add_argument("--auto-open-devtools-for-tabs") 

driver = webdriver.Edge(options=edge_options)

driver.get('https://m.facebook.com/watch/?v=1194662914750077')
time.sleep(3)

try:
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-action-id="32742" and @role="button"]')))
    button.click()
    print('Button clicked')
    time.sleep(2)
except Exception as e:
    print(f'No button found with data-action-id="32742": {e}')

try:
    span_element = driver.find_element(By.XPATH, '//span[@data-action-id="32734" and @role="link"]')
    span_text = span_element.text
    print(f'Text Content of Span: {span_text}')
except Exception as e:
    print(f'Error finding span element: {e}')

def wait_for_video_to_load(driver):
    script = """
    return new Promise((resolve, reject) => {
        const checkVideoLoaded = () => {
            const container = document.querySelector(".inline-video-container");
            if (container) {
                const videoTags = container.getElementsByTagName("video");
                if (videoTags.length > 0) {
                    const video = videoTags[0];
                    if (video.readyState === 4 && video.duration > 0) {  // Check if video is loaded and has a duration
                        resolve("Video loaded");
                    } else {
                        setTimeout(checkVideoLoaded, 1000);  // Check again after 1 second
                    }
                } else {
                    reject("No video tags found");
                }
            } else {
                reject("No inline-video-container found");
            }
        };
        checkVideoLoaded();
    });
    """
    return driver.execute_script(script)

try:
    result = wait_for_video_to_load(driver)
    print(result)
except Exception as e:
    print(f'Error waiting for video to load: {e}')

try:
    script = """
    return new Promise((resolve, reject) => {
        const checkVideoLoaded = () => {
            const container = document.querySelector(".inline-video-container");
            if (container) {
                const videoTags = container.getElementsByTagName("video");
                if (videoTags.length > 0) {
                const video = videoTags[0];  // Assuming there's at least one video tag
                let videoSrc = video.src;
                if (!videoSrc) {
                    const sources = video.getElementsByTagName("source");
                    videoSrc = sources.length > 0 ? Array.from(sources).map(source => source.src) : "No video source found";
                    
                }
                resolve(videoSrc)
                console.log("Video tag is seen");
                return videoSrc;
                } else {
                    reject("No video tags found");
                }
            } else {
                reject("No inline-video-container found");
            }
        };
        checkVideoLoaded();
    });
    """
    video_srcs = driver.execute_script(script)
    print(f'Video src(s): {video_srcs}')
except Exception as e:
    print(f'Error executing JavaScript: {e}')


driver.quit()
