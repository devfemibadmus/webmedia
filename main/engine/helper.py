import re
import threading
from datetime import datetime, timedelta

global_messages = []

class GlobalMessagesManager:
    lock = threading.Lock()
    def __init__(self, userId):
        self.userId = userId

    def updateMessage(self, message):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    user_message[self.userId][0]['message'] = message
                    return
            global_messages.append({
                self.userId: [
                    {'message': message, 'this_time': 0, 'last_time': 0},
                    {'data': []}
                ]
            })

    def update(self):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    now = datetime.now()
                    last_time = user_message[self.userId][0]['this_time']
                    if user_message[self.userId][0]['last_time'] == 0 or user_message[self.userId][0]['this_time'] == 0:
                        last_time = (now - timedelta(seconds=6)).isoformat()
                        this_time = now.isoformat()
                    user_message[self.userId][0].update({'this_time': datetime.now().isoformat(), 'last_time': last_time})
                    print(global_messages)
                    return

    def getMessage(self):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    return user_message[self.userId][0]['message']
            return None

    def setData(self, data):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    user_message[self.userId][1]['data'] = data
                    return
            global_messages.append({
                self.userId: [
                    {'message': 'loading...', 'this_time': 0, 'last_time': 0},
                    {'data': data}
                ]
            })

    def getData(self):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    return user_message[self.userId][1]['data']
            return "a nigga once said..."

    def pageUnload(self):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    this_time = datetime.now().isoformat()
                    last_time = user_message[self.userId][0]['this_time']
                    this_time_dt = datetime.fromisoformat(this_time)
                    last_time_dt = datetime.fromisoformat(last_time)
                    print("last_time", last_time)
                    print("this_time", this_time)
                    time_difference = (this_time_dt - last_time_dt).total_seconds()
                    print("time_difference ", time_difference)
                    return time_difference >= 6
            return True

    def spamRequest(self):
        with self.lock:
            for user_message in global_messages:
                if self.userId in user_message:
                    this_time = user_message[self.userId][0]['this_time']
                    last_time = user_message[self.userId][0]['last_time']
                    this_time_dt = datetime.fromisoformat(this_time)
                    last_time_dt = datetime.fromisoformat(last_time)
                    print("Spam last_time", last_time)
                    print("Spam this_time", this_time)
                    time_difference = (this_time_dt - last_time_dt).total_seconds()
                    print("Spam time_difference ", time_difference)
                    return time_difference <= 4
            return False

class Validator:
    TIKTOK_REGEX = re.compile(r'^https://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+.*$')
    INSTAGRAM_REGEX = re.compile(r'^https://(?:www\.)?instagram\.com/(p|reel)/[\w-]+/?.*$')
    FACEBOOK_REGEX = re.compile(r'^https://(?:www\.)?facebook\.com/(?:watch|share/(?:r|v)|reel)/.*$')


    @staticmethod
    def is_tiktok(url):
        return bool(Validator.TIKTOK_REGEX.match(url))
    
    @staticmethod
    def is_instagram(url):
        return bool(Validator.INSTAGRAM_REGEX.match(url))
    
    @staticmethod
    def is_facebook(url):
        return bool(Validator.FACEBOOK_REGEX.match(url))
    
    @staticmethod
    def validate(url):
        if Validator.is_tiktok(url):
            return "TikTok"
        elif Validator.is_instagram(url):
            return "Instagram"
        elif Validator.is_facebook(url):
            return "Facebook"
        else:
            return "Unknown"

