# WEBMEDIA

## Overview

**WEBMEDIA**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) backend for saving videos, images, and audio from Intagram, TikTok, Facebok. It performs web scraping and uses predefined methods observed from network traffic

## 🛠️ Dependencies

-  **[Selenium](https://github.com/SeleniumHQ/selenium)**: primarily for Instagram (4s). It's suitable for other platforms, but it's running on [small instance](https://cloud.google.com/blog/products/compute/google-compute-engine-gets-new-e2-vm-machine-types)

-  **[Requests](https://github.com/psf/requests)**: using in TikTok and Facebook

-  **[BeautifulSoup](https://github.com/wention/BeautifulSoup4)**: using in TikTok ad Facebook

-  **[Cors.lol](https://github.com/BradPerbs/cors.lol)**: for video rendering on [web](https://devfemibadmus.blackstackhub.com/webmedia)

-  **[corsproxy.io](https://github.com/cors-proxy/fix-cors-errors)**: for image rendering on [web](https://devfemibadmus.blackstackhub.com/webmedia)

## :star: Features

-  **Fetch Media**: Retrieves both private and public media files

-  **Cut Data**: shrink and return normal data

-  **Full Data**: Give full data containing all fields scraped from given platform

## :rocket: Apps

-  **Web App**: [WebMedia](https://devfemibadmus.blackstackhub.com/webmedia) limited download(maybe)

-  **Mobile App**: [MediaSaver](https://github.com/devfemibadmus/mediasaver) unlimited download + WhatsApp status saver

## :eyes: Checkout This

#### Spam https://devfemibadmus.blackstackhub.com/webmedia/sleep ([❌](https://github.com/devfemibadmus/webmedia/issues/1#issue-2725260727))

#### Main repo https://devfemibadmus.blackstackhub.com/webmedia

#### Web https://devfemibadmus.blackstackhub.com/webmedia

#### App https://play.google.com/store/apps/details?id=com.blackstackhub.mediasaver

## 📖 API Endpoint

-  **Method**: `GET` or `POST`
-  **URL**: `https://devfemibadmus.blackstackhub.com/webmedia/api/`
-  **Parameters**:
-  `cut`: Optional
-  `url`: Required

**Status 200 :white_check_mark:**
```json
{
  "success": true,
  "data": { }
}
```

**Status 400, 404, 500, 502 :x:**
```json
{
  "error": true,
  "message": "...",
  "error_message": "..."
}
```

#### Tiktok https://devfemibadmus.blackstackhub.com/webmedia/api/?cut=-&url=https://www.tiktok.com/@devfemibadmus/video/7390912680883899654

![TikTok](insta%20conf/image%20copy%206.png?raw=true)

#### Instagram https://devfemibadmus.blackstackhub.com/webmedia/api/?cut=-&url=https://www.instagram.com/p/C-TMvc4yQh6/?img_index=3

![Instagram](insta%20conf/image%20copy%207.png?raw=true)

#### Facebook https://devfemibadmus.blackstackhub.com/webmedia/api/?cut=-&url=https://www.facebook.com/share/v/qCRH3vKk2FbAEAUP/

![Facebook](insta%20conf/image%20copy%208.png?raw=true)


### Authentication ([❌](https://github.com/devfemibadmus/webmedia/issues/1#issue-2725260727))

<details>
<summary>Using Microsoft Edge on Debian VPS</summary>

1. **Familiarize Yourself with Edge WebDriver and Selenium**

   Before proceeding, you might want to check out these issues on GitHub related to Edge WebDriver:
   - [No latest stable release for Linux · Issue #156](https://github.com/MicrosoftEdge/EdgeWebDriver/issues/156)
   - [How to determine the correct Microsoft Edge WebDriver version for a given Edge browser version · Issue #158](https://github.com/MicrosoftEdge/EdgeWebDriver/issues/158#issuecomment-2263769092)

2. **Install Microsoft Edge and Edge WebDriver on Debian**

   - First, add the Microsoft repository to your APT sources list:

     ```bash
     sudo nano /etc/apt/sources.list.d/microsoft-edge.list
     ```

     Add the following line:

     ```bash
     deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main
     ```

     Then, download and add the Microsoft GPG key:

     ```bash
     wget -q https://packages.microsoft.com/keys/microsoft.asc -O microsoft.asc
     sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft.gpg microsoft.asc
     ```

   - Update the APT package list and check for available versions of Microsoft Edge:

     ```bash
     sudo apt update
     apt list -a microsoft-edge-stable
     ```

   - Install the latest matching version of Microsoft Edge:

     ```bash
     sudo apt install microsoft-edge-stable=123.0.2420.97-1
     ```

   - Download the matching version of Edge WebDriver and install it:

     ```bash
     sudo wget https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/123.0.2420.97/edgedriver_linux64.zip
     unzip edgedriver_linux64.zip
     sudo mv msedgedriver /usr/local/bin/
     ```

</details>

![login with cokies](insta%20conf/image%20copy%205.png?raw=true)

![login with cokies](insta%20conf/login%20auth.png?raw=true)


| Screenshot | Screenshot |
|-------------------------------------------------------------|-------------------------------------------------------------|
| ![post and video quality](insta%20conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max).png?raw=true) | ![author and musicc](insta%20conf/screenshot/127.0.0.1_5000_(iPhone%2014%20Pro%20Max)%20(1).png?raw=true) |
  

## Status
|website| status |
|--|--|
| TikTok Videos |✅|
| TikTok Photos |❌|
| Facebook Videos |✅|
| Instagram Reels |✅|
| Instagram Photos |✅|
| Instagram Videos |✅|
| YouTube |❌|
