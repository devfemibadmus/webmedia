from platforms.leaked import video_tiktok, image_tiktok
import requests

tiktok_quality_types = ['hq', 'fhd', 'hd', 'standard', 'low']


def get_tiktok_videos(url, item_id):    
    api_url = video_tiktok.format(item_id=item_id)
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Error: Quick Tiktok Outdatd Error: {e}')
        return 'Error: Quick Tiktok Outdatd.'
    
    try:
        item_list = data.get('itemList', [])
        found_items = [item for item in item_list if item['id'] == item_id]

        if not found_items:
            print(f'Error: Quick Tiktok leaked changed\n{data}')
            return f'Error: Quick Tiktok leaked changed.'
        
        item = found_items[0]
        video_info = {
            'platform':'tiktok',
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
            key = tiktok_quality_types[i] if i < len(tiktok_quality_types) else f'quality_{i}'
            video_info['videos'].append({
                key: {
                    'size': quality_type['PlayAddr'].get('DataSize', 'N/A'),
                    'address': quality_type['PlayAddr']['UrlList'][-1] if 'UrlList' in quality_type['PlayAddr'] else 'N/A',
                }
            })
        
        return video_info
    except Exception as e:
        print(f'Error in get_tiktok_videos url: {url}\nError: {e}')
        return f'Error: No items with id {item_id} found.'

def get_tiktok_images(url, item_id):    
    api_url = image_tiktok.format(item_id=item_id)
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Error: Quick Tiktok Outdatd Error: {e}')
        return 'Error: Quick Tiktok Outdatd.'
    
    try:
        item = data['itemInfo']['itemStruct']

        if not item:
            print(f'Error: Quick Tiktok leaked changed\n{data}')
            return f'Error: Quick Tiktok leaked changed.'

        photo_info = {
            'platform':'tiktok',
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
        images = item['imagePost'].get('images', [])
        for image in images:
            photo_info['images'].append(image['imageURL']['urlList'][0])
        
        return photo_info
    except Exception as e:
        print(f'Error in get_tiktok_images url: {url}\nError: {e}')
        return f'Error: No items with id {item_id} found.'
