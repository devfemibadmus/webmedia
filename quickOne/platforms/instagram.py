from platforms.leaked import instagram_data, instagram_url
import requests

def get_slide_media(data):
    media = []
    if "edge_sidecar_to_children" in data and "edges" in data["edge_sidecar_to_children"]:
        for edge in data["edge_sidecar_to_children"]["edges"]:
            node = edge["node"]
            media.append({
                "id": node["id"],
                "shortcode": node["shortcode"],
                "display_url": node["display_url"],
                "is_video": "video_url" in data
            })
    elif "video_url" in data:
            media.append({
                "id": data["id"],
                "shortcode": data["shortcode"],
                "display_url": data["video_url"],
                "is_video": data["is_video"],
            })
    return media

def get_instagram_data(item_id):
    api_data = instagram_data.copy()
    api_data['variables'] = api_data['variables'].replace('item_id',item_id)
    print("item_id: ", item_id)
    
    try:
        response = requests.post(instagram_url, data=api_data)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Error: Quick Instagram Outdatd Error: {e}')
        return 'Error: Quick Instagram Outdatd.'
    
    try:
        item = data['data']['xdt_shortcode_media']
        if not item:
            print(f'Error: Quick Instagram leaked changed\n{data}')
            return f'Error: Quick Instagram leaked changed.'
        print("item['shortcode']: ", item['shortcode'])
        data_info = {
            'platform':'instagram',
            'content': {
                'id': item['id'],
                'shortcode': item['shortcode'],
                'likes': item['edge_media_preview_like']['count'],
                'desc': item['edge_media_to_caption']['edges'][0]['node']['text'],
                'cover': item['thumbnail_src'],
            },
            'author': {
                'name': item['owner'].get('full_name', 'N/A'),
                'username': item['owner'].get('username', 'N/A'),
                'verified': item['owner'].get('is_verified', False),
                'image': item['owner'].get('profile_pic_url', 'N/A'),
                'videos': item['owner']['edge_owner_to_timeline_media'].get('count', 0),
                'followers': item['owner']['edge_followed_by'].get('count', 0),
            },
            'media': get_slide_media(item),
        }
        if item['is_video']:
            data_info['content'].update({
                'views': item['video_view_count'],
                'play': item['video_play_count']
            })
        
        return data_info
    except Exception as e:
        print(f'Error in get_instagram_data url: {item_id}\nError: {e}')
        return f'Error: No items with id {item_id} found.'


