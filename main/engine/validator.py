import re

class Validator:
    TIKTOK_REGEX = re.compile(r'^https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+$')
    INSTAGRAM_REGEX = re.compile(r'^https?://(?:www\.)?instagram\.com/p/[\w-]+/?$')
    FACEBOOK_REEL_REGEX = re.compile(r'^https?://(?:www\.)?facebook\.com/reel/\d+/\?s=ifu$')
    FACEBOOK_VIDEO_REGEX = re.compile(r'^https?://(?:www\.)?facebook\.com/share/v/[\w-]+/?$')

    @staticmethod
    def is_tiktok(url):
        return bool(Validator.TIKTOK_REGEX.match(url))
    
    @staticmethod
    def is_instagram_post(url):
        return bool(Validator.INSTAGRAM_REGEX.match(url))
    
    @staticmethod
    def is_facebook_reel(url):
        return bool(Validator.FACEBOOK_REEL_REGEX.match(url))
    
    @staticmethod
    def is_facebook_video(url):
        return bool(Validator.FACEBOOK_VIDEO_REGEX.match(url))
    
    @staticmethod
    def validate(url):
        if Validator.is_tiktok(url):
            return "TikTok"
        elif Validator.is_instagram_post(url):
            return "Instagram Post"
        elif Validator.is_facebook_reel(url):
            return "Facebook Reel"
        elif Validator.is_facebook_video(url):
            return "Facebook Video"
        else:
            return "Unknown"

"""
urls = [
    "https://www.tiktok.com/@oorsz/video/7380872550236048645",
    "https://www.instagram.com/p/C7alM-1yRS3/",
    "https://www.facebook.com/reel/530806462711311/?s=ifu",
    "https://www.facebook.com/share/v/qKnPyhfUXr5hCvq6/"
]

for url in urls:
    platform = Validator.validate(url)
    print(f"{url} is a {platform} URL.")
"""

