from datetime import datetime, timedelta
import re

global_messages = []

def update_message(user_id, message):
    # Check if user_id exists in global_messages
    for user_message in global_messages:
        if user_id in user_message:
            # Update the message and time
            user_message[user_id][0]['message'] = message
            return
    # If user_id doesn't exist, add new entry
    global_messages.append({
        user_id: [
            {'message': message, 'last check_or_update__time': datetime.now().isoformat()},
            {'data': []}
        ]
    })

def update_date(user_id):
    for user_message in global_messages:
        if user_id in user_message:
            user_message[user_id][0]['last check_or_update__time'] = datetime.now().isoformat()
            return

def get_message(user_id):
    # Find and return message for the given user_id
    for user_message in global_messages:
        if user_id in user_message:
            return user_message[user_id][0]['message']
    return None

def get_check_or_update_time(user_id):
    # Find and return check_or_update__time for the given user_id
    for user_message in global_messages:
        if user_id in user_message:
            return user_message[user_id][0]['last check_or_update__time']
    return None

def set_data(user_id, data):
    # Set the data for the given user_id
    for user_message in global_messages:
        if user_id in user_message:
            user_message[user_id][1]['data'] = data
            return
    # If user_id doesn't exist, add new entry with empty data
    global_messages.append({
        user_id: [
            {'message': 'loading...', 'last check_or_update__time': datetime.now().isoformat()},
            {'data': data}
        ]
    })

def get_data(user_id):
    # Find and return data for the given user_id
    for user_message in global_messages:
        if user_id in user_message:
            return user_message[user_id][1]['data']
    return "a nigga once said..."


def page_unload(user_id):
    for user_message in global_messages:
        if user_id in user_message:

            this_time = datetime.now().isoformat()
            last_time = user_message[user_id][0]['last check_or_update__time']
            
            # Convert ISO format strings to datetime objects
            this_time_dt = datetime.fromisoformat(this_time)
            last_time_dt = datetime.fromisoformat(last_time)
        
            print("last_time", last_time)
            print("this_time", this_time)
        
            # Calculate the time difference in seconds
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

