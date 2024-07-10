import requests

def post_to_url(url, data):
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error posting to URL: {e}")

# Example usage
url = "http://127.0.0.1:5000/app/"
data = {
    "url": "value1",
}

post_to_url(url, data)
