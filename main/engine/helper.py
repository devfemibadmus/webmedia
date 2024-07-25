import re, urllib.parse, threading
from datetime import datetime, timedelta


global_messages = []

class GlobalMessagesManager:
    def __init__(self, userId):
        self.userId = userId

    def reset(self):
        for user_message in global_messages:
            if self.userId in user_message:
                user_message[self.userId][0].update({
                    'this_time': datetime.now().isoformat(),
                    'last_time': 0,
                    'reload': False,
                    'count': 0
                })
                user_message[self.userId][1].update({'data': [], 'url': []})
                return
        global_messages.append({
            self.userId: [
                {
                    'message': 'starting',
                    'this_time': datetime.now().isoformat(),
                    'last_time': 0,
                    'reload': False,
                    'count': 0
                },
                {'data': [], 'url': []}
            ]
        })

    def updateMessage(self, message):
        for user_message in global_messages:
            if self.userId in user_message:
                user_message[self.userId][0]['message'] = message

    def update(self):
        for user_message in global_messages:
            if self.userId in user_message:

                user_data = user_message[self.userId][0]
                
                this_time = datetime.now()

                if user_data['count'] >= 2:
                    user_data.update({'this_time': this_time.isoformat(), 'last_time': user_data['this_time']})
                elif user_data['count'] == 1:
                    user_data.update({'this_time': this_time.isoformat(), 'last_time': (this_time - timedelta(seconds=5)).isoformat()})
                elif user_data['count'] == 2:
                    pass
                user_data['count'] += 1

                print(user_data)
                return

    def reload(self):
        for user_message in global_messages:
            if self.userId in user_message:
                user_data = user_message[self.userId][0]
                user_data.update({'reload': True})
    
    def pageUnload(self):
        for user_message in global_messages:
            if self.userId in user_message:
                user_data = user_message[self.userId][0]
                if user_data['reload'] == False:
                    return True
                if user_data['reload'] == True and user_data['count'] <= 2:
                    return False
                                
                this_time = datetime.now().isoformat()
                last_time = user_data['this_time']
                this_time_dt = datetime.fromisoformat(this_time)
                last_time_dt = datetime.fromisoformat(last_time)
                
                print("last_time", last_time)
                print("this_time", this_time)
                time_difference = (this_time_dt - last_time_dt).total_seconds()
                print("time_difference ", time_difference)
                
                return time_difference >= 6
        
        return True

    def spamRequest(self):
        for user_message in global_messages:
            if self.userId in user_message:
                user_data = user_message[self.userId][0]
                if user_data['count'] <= 2:
                    return False
                
                this_time = user_data['this_time']
                last_time = user_data['last_time']
                this_time_dt = datetime.fromisoformat(this_time)
                last_time_dt = datetime.fromisoformat(last_time)
                
                print("Spam last_time", last_time)
                print("Spam this_time", this_time)
                time_difference = (this_time_dt - last_time_dt).total_seconds()
                print("Spam time_difference ", time_difference)
                
                return time_difference <= 4
        
        return False

    def getMessage(self):
        for user_message in global_messages:
            if self.userId in user_message:
                return user_message[self.userId][0]['message']
        return None

    def setData(self, data, url):
        for user_message in global_messages:
            if self.userId in user_message:
                if url:
                    user_message[self.userId][1]['url'] = url
                if data:
                    user_message[self.userId][1]['data'] = data
                    return
        self.reset()

    def getUrl(self):
        for user_message in global_messages:
            if self.userId in user_message:
                return user_message[self.userId][1]['url']
        return []

    def getData(self):
        for user_message in global_messages:
            if self.userId in user_message:
                return user_message[self.userId][1]['data']
        return "a nigga once said..."

class Common:
    @staticmethod
    def get_folder(url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        path_components = path.split('/')
        folder = '/'.join(path_components[2:-1])
        return folder

    @staticmethod
    def get_file_name(url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        path_components = path.split('/')
        file_name = path_components[-1]
        return file_name

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

