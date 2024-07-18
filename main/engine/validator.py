import re

class Validator:
    INSTAGRAM_REGEX = re.compile(r'^https?://(?:www\.)?instagram\.com/p/[\w-]+/?.*$')
    TIKTOK_REGEX = re.compile(r'^https?://(?:www\.)?tiktok\.com/@[\w.-]+/(video|photo)/\d+.*$')
    FACEBOOK_REEL_REGEX = re.compile(r'^https?://(?:www\.)?facebook\.com/share/(r|reel)/[\w-]+/?.*$')
    FACEBOOK_VIDEO_REGEX = re.compile(r'^https?://(?:www\.)?facebook\.com/share/(v|video)/[\w-]+/?.*$')

    @staticmethod
    def is_tiktok(url):
        return bool(Validator.TIKTOK_REGEX.match(url))
    
    @staticmethod
    def is_instagram_post(url):
        return bool(Validator.INSTAGRAM_REGEX.match(url))
    
    @staticmethod
    def is_facebook_video(url):
        return bool(Validator.FACEBOOK_VIDEO_REGEX.match(url))
    
    @staticmethod
    def validate(url):
        if Validator.is_tiktok(url):
            return "TikTok"
        elif Validator.is_instagram_post(url):
            return "Instagram Post"
        elif Validator.is_facebook_video(url):
            return "Facebook Video"
        else:
            return "Unknown"


"""
urls = [
    "https://www.tiktok.com/@devfemibadmus/video/7390912680883899654?is_from_webapp=1&sender_device=pc&web_id=7379337792747193862",
    "https://www.instagram.com/p/C3mr9v5IEr9/",
    "https://www.facebook.com/share/v/qCRH3vKk2FbAEAUP/"
    "https://www.facebook.com/share/r/BLaPVaFoEguzQBio/",
    "https://www.facebook.com/share/reel/BLaPVaFoEguzQBio/",
]

for url in urls:
    platform = Validator.validate(url)
    print(f"{url} is a {platform} URL.")
"""

