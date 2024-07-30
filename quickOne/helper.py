import re

tiktok_video_pattern = r'tiktok\.com/.*/video/(\d+)'
tiktok_photo_pattern = r'tiktok\.com/.*/photo/(\d+)'
instagram_pattern = r'(?:https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/)([A-Za-z0-9_-]+)/?'

def tiktok_video_id(url):
    match = re.search(tiktok_video_pattern, url)
    if match:
        return match.group(1)
    return None

def tiktok_photo_id(url):
    match = re.search(tiktok_photo_pattern, url)
    if match:
        return match.group(1)
    return None

def instagram_shortcode(url):
    match = re.match(instagram_pattern, url)
    if match:
        return match.group(1)
    return None

