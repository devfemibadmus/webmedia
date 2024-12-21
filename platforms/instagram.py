import requests

class Instagram:
    def __init__(self):
        self.graphql = "https://www.instagram.com/graphql/query/"
        
    def get_slide_media(self, data):
        media = []
        if "edge_sidecar_to_children" in data and "edges" in data["edge_sidecar_to_children"]:
            for edge in data["edge_sidecar_to_children"]["edges"]:
                node = edge["node"]
                media_item = {
                    "id": node["id"],
                    "shortcode": node["shortcode"],
                    "address": node["display_url"],
                    'cover': node['display_url'],
                    "is_video": 'video_url' in node
                }
                if 'display_resources' in node:
                    media_item.update({
                        'address': node['display_resources'][-1]['src'],
                    })
                if 'video_url' in node:
                    media_item.update({
                        'address': node['video_url'],
                        'play': node['video_play_count'],
                        'views': node['video_view_count'],
                    })
                media.append(media_item)
        if "video_url" in data:
                media.append({
                    "id": data["id"],
                    "shortcode": data["shortcode"],
                    "address": data["video_url"],
                    "is_video": data["is_video"],
                    'cover': data['display_url'],
                })
        return media
    
    def get_instagram_data(self, data):
        try:
            item = data['data']['xdt_shortcode_media']
            if not item:
                return {'error': True, 'message': 'post has been deleted', 'error_message': 'item not found in data'}, 502
            # print("item['shortcode']: ", item['shortcode'])
            desc = item.get('edge_media_to_caption', {}).get('edges', [])
            data_info = {
                'platform':'instagram',
                'content': {
                    'id': item['id'],
                    'shortcode': item['shortcode'],
                    'likes': item['edge_media_preview_like']['count'],
                    'desc': desc[0]['node']['text'] if len(desc)>0 else 'no desc',
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
                'media': self.get_slide_media(item),
            }
            if item['display_resources']:
                data_info['content']['cover'] = item['display_resources'][-1]['src']
            if item['is_video']:
                data_info['content'].update({
                    'views': item['video_view_count'],
                    'play': item['video_play_count']
                })
        
            return data_info, 200
        except Exception as e:
            return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500

    def getData(self, item_id, cut):
        try:
            # with open("cookies.pkl", "rb") as f:
            #     cookies = {cookie["name"]: cookie["value"] for cookie in pickle.load(f)}
            instagram_data = {
                "av": "0",
                "__d": "www",
                "__user": "0",
                "__a": "1",
                "__req": "c",
                "__hs": "20078.HYP:instagram_web_pkg.2.1.0.0.0",
                "dpr": "1",
                "__ccg": "GOOD",
                "__rev": "1019047588",
                "__comet_req": "7",
                "lsd": "AVpJvs7i0Uw",
                "jazoest": "2982",
                "__spin_r": "1019047588",
                "__spin_b": "trunk",
                "__spin_t": "1734758172",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
                "variables": '{"shortcode":"DDfHvqGsUeW","fetch_tagged_user_count":null,"hoisted_comment_id":null,"hoisted_reply_id":null}',
                "server_timestamps": "true",
                "doc_id": "8845758582119845"
            }
            instagram_data['variables'] = instagram_data['variables'].replace('item_id', item_id)
            response = requests.post(self.graphql, json=instagram_data)

            data = response.json()
            # print(data)
            data['platform'] = 'instagram'
            
            if not cut:
                return data, 200
            
            data, status = self.get_instagram_data(data)
            return data, status
            
        except Exception as e:
            return {'error': True, 'message': 'something went wrong', 'error_message': str(e)}, 500

if __name__ == "__main__":
    print("Starting Instagram bot...")
    insta_bot = Instagram()
    data = insta_bot.getData('C8UahW1Nx4y', False)
    print(data)

