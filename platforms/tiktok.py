import requests, json
from bs4 import BeautifulSoup

class TikTokv2:
    def __init__(self, url, cut=None):
        print(url)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
        self.url, self.cut = url.replace('/photo', '/video'), cut
        self.error, self.status, self.json_data = None, None, None
        self.data, self.status = self.fetch_and_process()
        try:
            self.item = self.data['itemInfo']['itemStruct']
            self.data['statusMsg'] == "ok"
        except Exception as e:
            self.error, self.status = {'error': True, 'message': 'something went wrong', 'error_message': 'unable to get item from itemStruct'}, 502
    
    def fetch_and_process(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            self.error, self.status = {'error': True, 'message': 'unable to process url', 'error_message': f'Failed to fetch page content: {response.status_code}'}, 502
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        body_content = soup.find('body')
        if body_content is None:
            self.error, self.status = {'error': True, 'message': 'something went wrong', 'error_message': 'No <body> tag found.'}, 502
        script_tag = body_content.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
        if script_tag is None:
            self.error, self.status = {'error': True, 'message': 'something went wrong', 'error_message': 'No <script> tag with ID \'__UNIVERSAL_DATA_FOR_REHYDRATION__\' found.'}, 502
        script_content = script_tag.string.strip()
        try:
            self.json_data = json.loads(script_content)
        except json.JSONDecodeError:
            self.error, self.status = {'error': True, 'message': 'something went wrong', 'error_message': 'The content of the script tag is not valid JSON.'}, 502
        try:
            self.json_data = self.json_data['__DEFAULT_SCOPE__']['webapp.video-detail']
        except KeyError:
            self.error, self.status = {'error': True, 'message': 'something went wrong', 'error_message': 'No \'webapp.video-detail\' found in the JSON data.'}, 502
        return self.json_data, 200
    
    def getData(self):
        if self.error:
            return self.error, self.status
        if not self.cut:
            return self.data, self.status
        item = self.data['itemInfo']['itemStruct']
        if item.get('video').get('bitrateInfo'):
            try:
                item = self.data['itemInfo']['itemStruct']
                video_info = {
                    'platform': 'tiktok',
                    'is_video': True,
                    'content': {
                        'id': item['id'],
                        'desc': item.get('desc', 'N/A'),
                        'views': item['stats'].get('playCount', 0),
                        'likes': item['stats'].get('diggCount', 0),
                        'comments': item['stats'].get('commentCount', 0),
                        'saves': item['stats'].get('collectCount', 0),
                        'share': item['stats'].get('shareCount', 0),
                        'cover': item['video'].get('cover', 'N/A'),
                    },
                    'author': {
                        'name': item['author'].get('nickname', 'N/A'),
                        'username': item['author'].get('uniqueId', 'N/A'),
                        'verified': item['author'].get('verified', False),
                        'image': item['author'].get('avatarMedium', 'N/A'),
                        'bio': item['author'].get('signature', 'N/A')
                    },
                    'videos': [],
                    'music': {
                        'author': item['music'].get('authorName', 'N/A'),
                        'title': item['music'].get('title', 'N/A'),
                        'cover': item['music'].get('coverMedium', 'N/A'),
                        'duration': item['music'].get('duration', 'N/A'),
                        'src': item['music'].get('playUrl', 'N/A'),
                    }
                }
                bitrate_info = item['video'].get('bitrateInfo', [])
                for i, quality_type in enumerate(bitrate_info):
                    key = f'quality_{i}'
                    video_info['videos'].append({
                        key: {
                            'size': quality_type['PlayAddr'].get('DataSize', 'N/A'),
                            'address': quality_type['PlayAddr']['UrlList'][-1] if 'UrlList' in quality_type['PlayAddr'] else 'N/A',
                        }
                    })
                return video_info, 200
            except Exception as e:
                return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500
        else:
            try:
                item = self.data['itemInfo']['itemStruct']
                photo_info = {
                    'platform': 'tiktok',
                    'is_image': True,
                    'content': {
                        'id': item['id'],
                        'desc': item.get('desc', 'N/A'),
                        'title': item['imagePost'].get('title', 'N/A'),
                        'views': item['stats'].get('playCount', 0),
                        'likes': item['stats'].get('diggCount', 0),
                        'comments': item['stats'].get('commentCount', 0),
                        'saves': item['stats'].get('collectCount', 0),
                        'share': item['stats'].get('shareCount', 0),
                    },
                    'author': {
                        'name': item['author'].get('nickname', 'N/A'),
                        'username': item['author'].get('uniqueId', 'N/A'),
                        'verified': item['author'].get('verified', False),
                        'image': item['author'].get('avatarMedium', 'N/A'),
                        'location': item.get('poi', {}).get('address', 'N/A') + ' ' + item.get('poi', {}).get('name', 'N/A'),
                    },
                    'images': [],
                    'music': {
                        'author': item['music'].get('authorName', 'N/A'),
                        'title': item['music'].get('title', 'N/A'),
                        'cover': item['music'].get('coverMedium', 'N/A'),
                        'duration': item['music'].get('duration', 'N/A'),
                        'src': item['music'].get('playUrl', 'N/A'),
                    }
                }
                image_infos = item['imagePost']['images']
                for i, image in enumerate(image_infos):
                    photo_info['images'].append({
                        f'image_{i}': {
                            'original': image.get('imageURL', 'N/A'),
                            'size': image.get('imageHeight', 'N/A'),
                        }
                    })
                return photo_info, 200
            except Exception as e:
                return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500


class TikTokv1:
    def __init__(self, item_id, cut=None):
        self.cut = cut
        self.tiktok_url = (
            "https://www.tiktok.com/api/item/detail/"
            "?WebIdLastTime=1733627509&aid=1988&app_language=en&app_name=tiktok_web"
            "&browser_language=en-US&browser_name=Mozilla&browser_online=true"
            "&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20"
            "AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36%20"
            "Edg%2F131.0.0.0&channel=tiktok_web&clientABVersions=70508271&clientABVersions=72422414"
            "&clientABVersions=72791370&clientABVersions=72879051&clientABVersions=72923695"
            "&clientABVersions=72929405&clientABVersions=73004002&clientABVersions=73004187"
            "&clientABVersions=73004431&clientABVersions=73013519&clientABVersions=73035386"
            "&clientABVersions=73054614&clientABVersions=73055766&clientABVersions=73067877"
            "&clientABVersions=73069408&clientABVersions=73071855&clientABVersions=73078543"
            "&clientABVersions=73084639&clientABVersions=73084703&clientABVersions=73084843"
            "&clientABVersions=73097096&clientABVersions=73104335&clientABVersions=73105884"
            "&clientABVersions=73115494&clientABVersions=73133537&clientABVersions=73147323"
            "&clientABVersions=73149883&clientABVersions=70405643&clientABVersions=71057832"
            "&clientABVersions=71200802&clientABVersions=73004916&cookie_enabled=true"
            "&coverFormat=2&data_collection_enabled=false&device_id=7445873397290829317"
            "&device_platform=web_pc&focus_state=true&from_page=user&history_len=2"
            f"&is_fullscreen=false&is_page_visible=true&itemId={item_id}&language=en"
            "&odinId=7445873068213453829&os=windows&priority_region=&referer="
            "&region=NG&screen_height=1080&screen_width=1920&tz_name=Africa%2FLagos"
            "&user_is_login=false&webcast_language=en&msToken=&X-Bogus=DFSzswSOazJANCKjt/ZQhV6HQhPL"
            "&_signature=_02B4Z6wo00001c.0vKgAAIDArVu.MNnFHWnP9LgAABSq02"
        )
        self.headers = {
            "path": self.tiktok_url.replace('https://www.tiktok.com', ''),
            "authority": "www.tiktok.com",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        self.tiktok_quality_types = ['hq', 'fhd', 'hd', 'standard', 'low']
    
    video_tiktok = (
        "https://www.tiktok.com/api/related/item_list/?WebIdLastTime=1723329164&aid=1988&app_language=en&app_name=tiktok_web"
        "&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20"
        "%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome"
        "%2F127.0.0.0%20Safari%2F537.36%20Edg%2F127.0.0.0&channel=tiktok_web&clientABVersions=70508271%2C72135780%2C72213608"
        "%2C72406134%2C72422414%2C72479967%2C72510488%2C72516803%2C72527747%2C72535241%2C72535252%2C72535588%2C72556483"
        "%2C72563127%2C72587086%2C72607427%2C72620774%2C70405643%2C71057832%2C71200802%2C72445639&cookie_enabled=true&count=16"
        "&coverFormat=2&cursor=0&data_collection_enabled=false&device_id=7401642326072165893&device_platform=web_pc&focus_state=true"
        "&from_page=video&history_len=2&isNonPersonalized=false&is_fullscreen=false&is_page_visible=true&itemID={item_id}"
        "&language=en&odinId=7401642099835978757&os=windows&priority_region=&referer=&region=NG&screen_height=1080&screen_width=1920"
        "&tz_name=America%2FChicago&user_is_login=false&webcast_language=en"
    )

    @staticmethod
    def get_videos(item_id, cut):
        api_url = TikTokv1.video_tiktok.format(item_id=item_id)
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return {'error': True, 'message': str(e)}
        
        try:
            item_list = data.get('itemList', [])
            found_items = [item for item in item_list if item['id'] == item_id]

            if not found_items:
                print(item_list)
                return {'error': True, 'message': 'item not found in data.'}
            
            item = found_items[0]

            if not cut:
                return item
            
            video_info = {
                'platform': 'tiktok',
                'is_video': True,
                'content': {
                    'id': item['id'],
                    'desc': item.get('desc', 'N/A'),
                    'views': item['stats'].get('playCount', 0),
                    'likes': item['stats'].get('diggCount', 0),
                    'comments': item['stats'].get('commentCount', 0),
                    'saves': item['stats'].get('collectCount', 0),
                    'share': item['stats'].get('shareCount', 0),
                    'cover': item['video'].get('cover', 'N/A'),
                },
                'author': {
                    'name': item['author'].get('nickname', 'N/A'),
                    'username': item['author'].get('uniqueId', 'N/A'),
                    'verified': item['author'].get('verified', False),
                    'image': item['author'].get('avatarMedium', 'N/A'),
                    'videos': item['authorStats'].get('videoCount', 0),
                    'likes': item['authorStats'].get('heartCount', 0),
                    'friends': item['authorStats'].get('friendCount', 0),
                    'followers': item['authorStats'].get('followerCount', 0),
                    'following': item['authorStats'].get('followingCount', 0),
                },
                'videos': [],
                'music': {
                    'author': item['music'].get('authorName', 'N/A'),
                    'title': item['music'].get('title', 'N/A'),
                    'cover': item['music'].get('coverMedium', 'N/A'),
                    'duration': item['music'].get('duration', 'N/A'),
                    'src': item['music'].get('playUrl', 'N/A'),
                }
            }
            bitrate_info = item['video'].get('bitrateInfo', [])
            for i, quality_type in enumerate(bitrate_info):
                key = TikTokv1.tiktok_quality_types[i] if i < len(TikTokv1.tiktok_quality_types) else f'quality_{i}'
                video_info['videos'].append({
                    key: {
                        'size': quality_type['PlayAddr'].get('DataSize', 'N/A'),
                        'address': quality_type['PlayAddr']['UrlList'][-1] if 'UrlList' in quality_type['PlayAddr'] else 'N/A',
                    }
                })
            
            return video_info
        except Exception as e:
            return {'error': True, 'message': str(e)}

    def get_images(self):
        try:
            response = requests.get(self.tiktok_url, headers=self.headers)
            response.raise_for_status()
            # print(response.text)
            data = response.json()
        except Exception as e:
            return {'error': True, 'message': str(e)}
        try:
            item = data['itemInfo']['itemStruct']
            if not item:
                return {'error': True, 'message': 'item not found in data'}
            if not self.cut:
                return item
            photo_info = {
                'platform': 'tiktok',
                'is_image': True,
                'content': {
                    'id': item['id'],
                    'desc': item.get('desc', 'N/A'),
                    'title': item['imagePost'].get('title', 'N/A'),
                    'views': item['stats'].get('playCount', 0),
                    'likes': item['stats'].get('diggCount', 0),
                    'comments': item['stats'].get('commentCount', 0),
                    'saves': item['stats'].get('collectCount', 0),
                    'share': item['stats'].get('shareCount', 0),
                },
                'author': {
                    'name': item['author'].get('nickname', 'N/A'),
                    'username': item['author'].get('uniqueId', 'N/A'),
                    'verified': item['author'].get('verified', False),
                    'image': item['author'].get('avatarMedium', 'N/A'),
                    'location': item.get('poi', {}).get('address', 'N/A') + ' ' + item.get('poi', {}).get('name', 'N/A'),
                },
                'images': [],
                'music': {
                    'author': item['music'].get('authorName', 'N/A'),
                    'title': item['music'].get('title', 'N/A'),
                    'cover': item['music'].get('coverMedium', 'N/A'),
                    'duration': item['music'].get('duration', 'N/A'),
                    'src': item['music'].get('playUrl', 'N/A'),
                }
            }
            image_infos = item['imagePost']['images']
            for i, image in enumerate(image_infos):
                photo_info['images'].append({
                    f'image_{i}': {
                        'original': image.get('imageURL', 'N/A'),
                        'size': image.get('imageHeight', 'N/A'),
                    }
                })
            return photo_info
        except Exception as e:
            return {'error': True, 'message': str(e)}


test = TikTokv2('https://www.tiktok.com/@pelyzy035/photo/7401052163021081861', True)
test = test.getData()
print(test)
