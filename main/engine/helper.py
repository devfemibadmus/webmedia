import re
from datetime import datetime, timedelta

global_messages = []

class GlobalMessagesManager:
    def __init__(self, userId):
        self.userId = userId

    def updateMessage(self, message):
        for user_message in global_messages:
            if self.userId in user_message:
                user_message[self.userId][0]['message'] = message
                return
        global_messages.append({
            self.userId: [
                {'message': message, 'last check_or_update__time': datetime.now().isoformat()},
                {'data': []}
            ]
        })

    def update(self):
        for user_message in global_messages:
            if self.userId in user_message:
                user_message[self.userId][0]['last check_or_update__time'] = datetime.now().isoformat()
                return

    def getMessage(self):
        for user_message in global_messages:
            if self.userId in user_message:
                return user_message[self.userId][0]['message']
        return None

    def setData(self, data):
        for user_message in global_messages:
            if self.userId in user_message:
                user_message[self.userId][1]['data'] = data
                return
        global_messages.append({
            self.userId: [
                {'message': 'loading...', 'last check_or_update__time': datetime.now().isoformat()},
                {'data': data}
            ]
        })

    def getData(self):
        for user_message in global_messages:
            if self.userId in user_message:
                return user_message[self.userId][1]['data']
        return "a nigga once said..."

    def pageUnload(self):
        for user_message in global_messages:
            if self.userId in user_message:
                this_time = datetime.now().isoformat()
                last_time = user_message[self.userId][0]['last check_or_update__time']
                this_time_dt = datetime.fromisoformat(this_time)
                last_time_dt = datetime.fromisoformat(last_time)
                print("last_time", last_time)
                print("this_time", this_time)
                time_difference = (this_time_dt - last_time_dt).total_seconds()
                print("time_difference ", time_difference)
                return time_difference >= 6
        return False


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

