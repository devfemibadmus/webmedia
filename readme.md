
# WEBMEDIA

## Overview

**WEBMEDIA** is a backend Python service designed to fetch media files (videos, images, gifs) from supported given URL. It uses Selenium for web scraping, using predefined XPaths to reliably target elements, even if the target URL's frontend HTML structure changes.

## Features

-   **Fetch Media**: Retrieves both private and public media files.
-   **Spam Detection**: Identifies and prevents user spamming.
-   **Guaranteed Retrieval**: Surely 100% all media gonna get from given supported platforms.

## Limitations

-   **Supported Platform**: Tiktok, Instagram, Facebook. CheckOut [QuickOne version](#quickone).
-   **Performance**: Limited download for web version checkout [MediaSaver](https://github.com/devfemibadmus/mediasaver) for unlimited.

### Apps
-   **Web App**: [WebMedia](https://devfemibadmus.blackstackhub.com/webmedia) limited download
-   **Mobile App**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) unlimited download | one ads

## OnGoing Platforms
| Websites | Status |
|------|------|
| TikTok Videos |✅|
| Instagram Reels |✅|
| Instagram Photos |✅|
| Instagram Posts |✅|
| TikTok Photos |❌|
| Facebook|❌|
| YouTube|❌|



## QuickOne

Just a test script clone [repo](https://devfemibadmus.blackstackhub.com/webmedia/) cd quickOne python app.py. Currently supports Tiktok and Instagram. Intended to be a lightweight tool for studying website networks to identify leaked request paths.



### API ?

No API? Follow these steps to get yours:

1. Star the original repo [https://devfemibadmus.blackstackhub.com/webmedia](https://devfemibadmus.blackstackhub.com/webmedia)
2. Fork it
3. Clone it
4. Host it on any VPS

Good, now you have yours. Below is a sample:

```http
POST https://devfemibadmus.blackstackhub.com/webmedia/api
Content-Type: application/json
{"data": "url"}
```

### Sample Response Tiktok 

<details>
<summary>Image response</summary>

```json
{
  "message": "success",
  "is_image": true,
  "content": {
    "id": "9876543210987654321",
    "desc": "Sample image description",
    "title": "Sample Image Title",
    "views": 50000,
    "likes": 3000,
    "comments": 100,
    "saves": 200,
    "share": 30
  },
  "author": {
    "name": "Sample Author",
    "username": "sampleauthor",
    "verified": true,
    "image": "https://example.com/author_avatar.jpg",
    "location": "Sample Location Name"
  },
  "images": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg"
  ],
  "music": {
    "author": "Sample Musician",
    "title": "Sample Song",
    "cover": "https://example.com/music_cover.jpg",
    "duration": 180,
    "src": "https://example.com/music.mp3"
  }
}
```
</details>

<details>
<summary>Image response</summary>

```json
{
  "message": "success",
  "is_video": true,
  "content": {
    "id": "1234567890123456789",
    "desc": "Sample video description",
    "views": 100000,
    "likes": 5000,
    "comments": 200,
    "saves": 300,
    "share": 50,
    "cover": "https://example.com/video_cover.jpg"
  },
  "author": {
    "name": "Sample Author",
    "username": "sampleauthor",
    "verified": true,
    "image": "https://example.com/author_avatar.jpg",
    "videos": 100,
    "likes": 1000000,
    "friends": 150,
    "followers": 20000,
    "following": 300
  },
  "videos": [
    {
      "quality_0": {
        "size": 500000,
        "address": "https://example.com/video_480p.mp4"
      }
    },
    {
      "quality_1": {
        "size": 1000000,
        "address": "https://example.com/video_720p.mp4"
      }
    },
    {
      "quality_2": {
        "size": 1500000,
        "address": "https://example.com/video_1080p.mp4"
      }
    }
  ],
  "music": {
    "author": "Sample Musician",
    "title": "Sample Song",
    "cover": "https://example.com/music_cover.jpg",
    "duration": 180,
    "src": "https://example.com/music.mp3"
  }
}

```
</details>

### Sample Response Instagram 
<details>
<summary>reels|photo|video response</summary>

```json
{
  "platform": "instagram",
  "content": {
    "id": "1234567890",
    "shortcode": "ABC123",
    "likes": 1500,
    "desc": "This is a sample description of the post.",
    "cover": "https://instagram.com/sample_cover_image.jpg"
  },
  "author": {
    "name": "John Doe",
    "username": "johndoe",
    "verified": true,
    "image": "https://instagram.com/sample_profile_pic.jpg",
    "videos": 100,
    "followers": 5000
  },
  "media": [
    {
      "id": "111222333",
      "shortcode": "ABC123",
      "display_url": "https://instagram.com/sample_image1.jpg",
      "is_video": false
    },
    {
      "id": "444555666",
      "shortcode": "DEF456",
      "display_url": "https://instagram.com/sample_image2.jpg",
      "is_video": false
    },
    {
      "id": "777888999",
      "shortcode": "GHI789",
      "display_url": "https://instagram.com/sample_video.mp4",
      "is_video": true
    }
  ],
  "views": 2000,
  "play": 1800
}
```

</details>

### Sample Screenshot 
| Screenshot | Screenshot |
|-------------------------------------------------------------|-------------------------------------------------------------|
| ![post and video quality](screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max).png?raw=true) | ![author and musicc](screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max)%20(1).png?raw=true) |


