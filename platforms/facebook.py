import requests, json

class Facebook:
    def __init__(self, user_agent=None):
        self.user_agent = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Dnt': '1',
            'Dpr': '1.3125',
            'Priority': 'u=0, i',
            'Sec-Ch-Prefers-Color-Scheme': 'dark',
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="124.0.6367.156", "Google Chrome";v="124.0.6367.156", "Not-A.Brand";v="99.0.0.0"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Viewport-Width': '1463',
            'User-Agent': self.user_agent
        }

    def getVideo(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
        except requests.RequestException as e:
            return {'error': True, 'message': str(e)}

        try:
            url = resp.url.split('?')[0]
            resp_text = resp.text
            splits = url.split('/')
            video_id = ''
            for ids in splits:
                if ids.isdigit():
                    video_id = ids
        except Exception as e:
            return {'error': True, 'message': str(e)}

        try:
            target_video_audio_id = resp_text.split('"id":"{}"'.format(video_id))[1].split(
                '"dash_prefetch_experimental":[')[1].split(']')[0].strip()
        except IndexError:
            try:
                target_video_audio_id = resp_text.split('"video_id":"{}"'.format(video_id))[1].split(
                    '"dash_prefetch_experimental":[')[1].split(']')[0].strip()
            except Exception as e:
                return {'error': True, 'message': str(e)}

        try:
            list_str = "[{}]".format(target_video_audio_id)
            sources = json.loads(list_str)
        except json.JSONDecodeError as e:
            return {'error': True, 'message': str(e)}

        try:
            video_url = resp_text.split('"representation_id":"{}"'.format(sources[0]))[
                1].split('"base_url":"')[1].split('"')[0].replace('\\', '')
            audio_url = resp_text.split('"representation_id":"{}"'.format(sources[1]))[
                1].split('"base_url":"')[1].split('"')[0].replace('\\', '')
        except Exception as e:
            return {'error': True, 'message': str(e)}

        return {"audio_url": audio_url, "video_url": video_url, "platform": "facebook"}
