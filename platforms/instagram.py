import requests, pickle

class Instagram:
    def __init__(self):
        self.graphql = "https://www.instagram.com/graphql/query/"
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-full-version-list": '"Chromium";v="136.0.7103.113", "Microsoft Edge";v="136.0.3240.76", "Not.A/Brand";v="99.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"19.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "x-csrftoken": "11111111111",
        }
        
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
                "__req": "a",
                "__hs": "20229.HYP:instagram_web_pkg.2.1...0",
                "dpr": "1",
                "__ccg": "GOOD",
                "__rev": "1023049274",
                "__comet_req": "7",
                "lsd": "AVqQ3As1H7g",
                "jazoest": "2855",
                "__spin_r": "1023049274",
                "__spin_b": "trunk",
                "__spin_t": "1747835843",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
                "variables": '{"shortcode":"item_id","fetch_tagged_user_count":null,"hoisted_comment_id":null,"hoisted_reply_id":null}',
                "server_timestamps": "true",
                "doc_id": "9510064595728286"
            }
            instagram_data['variables'] = instagram_data['variables'].replace('item_id', item_id)
            # print(instagram_data)
            # session = requests.Session()
            # session.cookies.clear()
            response = requests.post(self.graphql, data=instagram_data, headers=self.headers) # , cookies=cookies
            # print(response.text)

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
    data = insta_bot.getData('DHm7knuzl1D', False)
    print(data)

