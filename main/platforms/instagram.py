from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Instagram:
    def __init__(self):
        self.edge_options = Options()
        self.edge_options.use_chromium = True
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--mute-audio")
        self.edge_options.add_experimental_option("detach", True)
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Edge(options=self.edge_options)
        self.browser.set_script_timeout(50)
        # self.browser.delete_all_cookies()
        self.browser.get('https://www.instagram.com/accounts/login/')

    def get_slide_media(self, data):
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
    
    def get_instagram_data(self, data):
        try:
            item = data['data']['xdt_shortcode_media']
            if not item:
                print(f'Error: Quick Instagram leaked changed\n{data}')
                return f'Error: Quick Instagram leaked changed.'
            # print("item['shortcode']: ", item['shortcode'])
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
                'media': self.get_slide_media(item),
            }
            if item['is_video']:
                data_info['content'].update({
                    'views': item['video_view_count'],
                    'play': item['video_play_count']
                })
        
            return data_info
        except Exception as e:
            return {'error': True, 'message': f'Error: {e}.'}

    def getData(self, url, item_id, cut):
        instagram_data = {
            'av': '0',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': '3',
            '__hs': '19933.HYP:instagram_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'UNKNOWN',
            '__rev': '1015220271',
            '__comet_req': '7',
            'lsd': 'AVqipa-__e8',
            'jazoest': '2970',
            '__spin_r': '1015220271',
            '__spin_b': 'trunk',
            '__spin_t': '1722271940',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQueryQuery',
            'variables': '{"shortcode":"item_id"}',
            'server_timestamps': 'true',
            'doc_id': '25531498899829322'
        }
        instagramUrl = "https://www.instagram.com/graphql/query"
        instagram_data['variables'] = instagram_data['variables'].replace('item_id', item_id)
        js_script = f"""
            return new Promise(async (resolve, reject) => {{
                try {{
                    const response = await fetch('{instagramUrl}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                      }},
                      body: JSON.stringify({instagram_data})
                    }});
  
                    if (!response.ok) {{
                      throw new Error('Network response was not ok');
                    }}
  
                    const data = await response.json();
                    resolve(data);
        
                  }} catch (e) {{
                    console.error(`Error: Quick Instagram Outdated Error: ${{e}}`);
                    reject(new Error('Error: Quick Instagram Outdated.'));
                  }}
            }});
            """
        data = self.browser.execute_script(js_script)
        data['platform'] = 'instagram'
        if not cut:
            return data
        return self.get_instagram_data(data)

    def end(self):
        self.browser.quit()


