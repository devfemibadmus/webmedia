import requests

url = 'https://v16-webapp-prime.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/oIK0jD5IfCFsBADfEQma4Jmtz2RimAyhEECBQP/?a=1988&bti=ODszNWYuMDE6&ch=0&cr=3&dr=0&lr=unwatermarked&cd=0%7C0%7C0%7C&cv=1&br=394&bt=197&cs=0&ds=6&ft=4fUEKMkj8Zmo0eiwG-4jVRTyppWrKsd.&mime_type=video_mp4&qs=5&rc=N2RlODc3PDczPDo4N2VnM0Bpajg4Om05cmpmdDMzNzczM0BiMTIyNV4xXy4xM2EuYF42YSNjLy1hMmRzcGFgLS1kMTZzcw%3D%3D&btag=e00090000&expire=1721689852&l=20240722170904F6395C5699D934330126&ply_type=2&policy=2&signature=cccb1d06d42f0d36dff3909e734afdda&tk=tt_chain_token'
headers = {
    'Referer': 'https://www.tiktok.com/',
}

response = requests.get(url, headers=headers)

# Check the status code and response content
if response.status_code == 200:
    print("Access is OK")
    with open('video.mp4', 'wb') as file:
        file.write(response.content)
elif response.status_code == 403:
    print("Access Denied")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
