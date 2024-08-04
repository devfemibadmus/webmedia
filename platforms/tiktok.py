import requests, json

class TikTok:
    tiktok_quality_types = ['hq', 'fhd', 'hd', 'standard', 'low']
    video_tiktok = (
        "https://www.tiktok.com/api/related/item_list/?WebIdLastTime=1722322797&aid=1988&app_language=en&app_name=tiktok_web"
        "&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20"
        "%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome"
        "%2F126.0.0.0%20Safari%2F537.36%20Edg%2F126.0.0.0&channel=tiktok_web&clientABVersions=70508271%2C72213608%2C72313476"
        "%2C72406134%2C72422413%2C72430804%2C72444800%2C72454782%2C72479966%2C72502691%2C72508984%2C72527745%2C72587086"
        "%2C70405643%2C71057832%2C71200802%2C72445639&cookie_enabled=true&count=16&coverFormat=2&cursor=0&data_collection_enabled=false"
        "&device_id=7397319992418551302&device_platform=web_pc&focus_state=true&from_page=video&history_len=2&isNonPersonalized=false"
        "&is_fullscreen=false&is_page_visible=true&itemID={item_id}&language=en&odinId=7397319731298616326&os=windows&priority_region="
        "&referer=&region=NG&screen_height=1080&screen_width=1920&tz_name=Africa%2FLagos&user_is_login=false&webcast_language=en"
    )

    image_tiktok = (
        "https://www.tiktok.com/api/related/item_list/?WebIdLastTime=1722076276&aid=1988&app_language=en&app_name=tiktok_web"
        "&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20"
        "%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome"
        "%2F126.0.0.0%20Safari%2F537.36%20Edg%2F126.0.0.0&channel=tiktok_web&clientABVersions=70508271%2C72213608%2C72313476"
        "%2C72406134%2C72408648%2C72430804%2C72444798%2C72454780%2C72478059%2C72479966%2C72502689%2C72508181%2C72508984"
        "%2C72510487%2C72516935%2C72527746%2C70405643%2C71057832%2C71200802%2C72445639&cookie_enabled=true&count=16"
        "&coverFormat=2&cursor=0&data_collection_enabled=false&device_id=7396261186336409094&device_platform=web_pc"
        "&focus_state=true&from_page=video&history_len=3&isNonPersonalized=false&is_fullscreen=false&is_page_visible=true"
        "&itemID={item_id}&language=en&odinId=7396260937399845894&os=windows&priority_region=&referer=&region=NG"
        "&screen_height=1080&screen_width=1920&tz_name=Africa%2FLagos&user_is_login=false&webcast_language=en"
    )

    @staticmethod
    def get_videos(url, item_id, cut):    
        api_url = TikTok.video_tiktok.format(item_id=item_id)
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return f'Error: {e}'
        
        try:
            item_list = data.get('itemList', [])
            found_items = [item for item in item_list if item['id'] == item_id]

            if not found_items:
                print(f'Error: Quick Tiktok leaked changed\n{data}')
                return f'Error: Quick Tiktok leaked changed.'
            
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
                key = TikTok.tiktok_quality_types[i] if i < len(TikTok.tiktok_quality_types) else f'quality_{i}'
                video_info['videos'].append({
                    key: {
                        'size': quality_type['PlayAddr'].get('DataSize', 'N/A'),
                        'address': quality_type['PlayAddr']['UrlList'][-1] if 'UrlList' in quality_type['PlayAddr'] else 'N/A',
                    }
                })
            
            return video_info
        except Exception as e:
            return f'Error: {e}'

    @staticmethod
    def get_images(url, item_id, cut):    
        api_url = TikTok.image_tiktok.format(item_id=item_id)
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return f'Error: {e}'
        
        try:
            with open("tik.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, separators=(',', ': '))
            item = data['itemInfo']['itemStruct']

            if not item:
                print(f'Error: Quick Tiktok leaked changed\n{data}')
                return f'Error: Quick Tiktok leaked changed.'

            if not cut:
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
                    'location': item['poi']['address'] + item['poi']['name'],
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
                        'cover': image.get('cover', 'N/A'),
                        'original': image.get('displayImageURL', 'N/A'),
                        'size': image.get('imageSize', 'N/A'),
                    }
                })
            
            return photo_info
        except Exception as e:
            return f'Error: {e}'


