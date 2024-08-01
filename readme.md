# WEBMEDIA

  

## Overview

**WEBMEDIA** written in python task fetch media files (videos, images, gifs) from supported social media. It uses [Selenium](https://github.com/SeleniumHQ/selenium) for web scraping and in other form it uses predefine method seen from network.


## Features

-  **Fetch Media**: Retrieves both private and public media files.

-  **Cut Data**: shrink and return normal data.

-  **Full Data**: Give full data containing all fields scraped from given platform.
  

## Limitations

-  **Supported Platform**: Tiktok, Instagram, Facebook.

### Apps

-  **Web App**: [WebMedia](https://devfemibadmus.blackstackhub.com/webmedia) limited download(maybe)

-  **Mobile App**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) unlimited download + WhatsApp status saver

  

## Status
|website| status |
|--|--|
| TikTok Videos |✅|
| Instagram Reels |✅|
| Instagram Photos |✅|
| Instagram Posts |✅|
| TikTok Photos |❌|
| Facebook|❌|
| YouTube|❌|


### API


much load? Follow these steps to get yours:

1. Star the original repo [https://devfemibadmus.blackstackhub.com/webmedia](https://devfemibadmus.blackstackhub.com/webmedia)

2. Fork it

3. Clone it

4. Host it on any VPS

Good, now you have yours. Below is a sample:

## API Endpoint

**Method:**  `POST` or `GET`

**URL:**  `https://devfemibadmus.blackstackhub.com/webmedia/api`

**Content-Type:**  `application/json`

  

### Request Body

```json
{

"url": "url",

"cut": true

}
```
#### Notes

- The `data` field should contain the URL as a string.

- The `cut` field is optional indicating whether to perform the cutting operation or not. None cut data have extra fields


### Instagram (Cut Data)

```json

{

    "author": {

        "followers": 10142,

        "image": "https://instagram.flos5-3.fna.fbcdn.net/v/t51.28...",

        "name": "Nupat | Learn tech skills",

        "username": "nupat_technologies",

        "verified": false,

        "videos": 664

    },

    "content": {

        "cover": "https://instagram.flos5-2.fna.fbcdn.net/v/t51.2...",

        "desc": "The motivation to keep going always.\nWe are at it always, steady grinding 💪 💯",

        "id": "3423747737702041332",

        "likes": 12,

        "play": 82,

        "shortcode": "C-DmG16Rwb0",

        "views": 33

    },
 
    "media": [

        {

            "display_url": "https://instagram.flos5-3.fna.fbcdn.net/o1/v/t1...",

            "id": "3423747737702041332",

            "is_video": true,

           "shortcode": "C-DmG16Rwb0"

        }

    ],

    "platform": "instagram"

}

```


### TikTok (Cut Data)

```json

{

    "author": {

        "followers": 38,

        "following": 3,

        "friends": 0,

        "image": "https://p16-sign-va.tiktokcdn.com/tos-maliva-avt...",

        "likes": 216,

        "name": "devfemibadmus",

        "username": "devfemibadmus",

        "verified": false,

        "videos": 7

    },

    "content": {

        "comments": 0,

        "cover": "https://p16-sign-va.tiktokcdn.com/obj/tos-maliva...",

        "desc": "24hrs #nigeriaprogrammer #debian",

        "id": "7390912680883899654",

        "likes": 7,

        "saves": 0,

        "share": 0,

        "views": 478

    },

    "is_video": true,

    "music": {

        "author": "devfemibadmus",

        "cover": "https://p16-sign-va.tiktokcdn.com/tos-maliva-avt..",

        "duration": 68,

        "src": "https://v16-webapp-prime.tiktok.com/video/tos/useast2a/tos-usea..",

        "title": "original sound - devfemibadmus"

    },

    "platform": "tiktok",

    "videos": [

        {

        "hq": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/a...",

            "size": 4528979

            }

        },

        {

        "fhd": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/a...",

            "size": 3692139

            }

        },

        {

        "hd": {

            "address": "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/p...",

            "size": 2663135

            }

        }

    ]

}

```


### Sample Screenshot

| Screenshot | Screenshot |
|-------------------------------------------------------------|-------------------------------------------------------------|
| ![post and video quality](conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max).png?raw=true) | ![author and musicc](conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max)%20(1).png?raw=true) |
