/*
 *************************************
 * For any modifications,
 * please contact the nigga (devfemibadmus@gmail.com).
 *************************************
 */


 let isAbout = true;
 let navLink = document.getElementById('nav-privacy');
 
 const saveId = document.getElementById('saveId');
 const loading = document.getElementById('loading');
 const saveSection = document.getElementById('save');
 const links = document.querySelectorAll('.nav-link');
 const sections = document.querySelectorAll('.section');
 const searchInput = document.getElementById('search-input');
 const searchButton = document.getElementById('search-button');
 const loadingMessage = document.getElementById('loading-message');
 const scrollableContainer = document.querySelector('.scrollable-container');
 
 console.log("%cFORGOTTEN?: Show some love star the github repo https://github.com/devfemibadmus/webmedia.", "color: #00faff; font-size: 16px;");
 console.log("%cTHE APP?: Show some love star the APP github repo https://github.com/devfemibadmus/mediasaver get yours on playstore.", "color: #00faff; font-size: 16px;");
 
 
 searchButton.addEventListener('click', function (event) {
     event.preventDefault();
     const url = searchInput.value;
 
     var formData = new FormData();
     formData.append('url', url);
     formData.append('cut', true);
 
     sections.forEach(section => {
         section.classList.remove('active');
     });
     saveSection.classList.add('active');
 
     loadingMessage.textContent = "Starting"
     loadingMessage.style.color = "grey"
     loading.style.display = "inline"
     loading.style.color = "grey"

     if(url.includes("facebook")){
        loadingMessage.textContent = "You need to use the Media Saver app to download facebook videos"
        loadingMessage.style.color = "red"
        loading.style.color = "red"
     }
 
     fetch('/webmedia/api/', {
             method: 'POST',
             body: formData
         })
         .then(response => response.json())
         .then(response => {
            console.log(response)
             loading.style.display = "none"
             loadingMessage.textContent = response.message
             if(response.error){
                 loadingMessage.style.color="red";
             }else if(response.success){
                 loadingMessage.style.color="#00faff";
                 const data = response.data;
                 console.log(data);
                 if(data.platform == 'tiktok'){
                     const tiktokContentManager = new TikTokContentManager(scrollableContainer, saveId);
                     tiktokContentManager.setContent(data.content);
                     tiktokContentManager.setMusic(data.music);
                     tiktokContentManager.setAuthor(data.author);
                     tiktokContentManager.setVideos(data.videos);
                     console.log(data.platform)
                 }else if(data.platform == 'instagram'){
                     const instagramContentManager= new InstagramContentManager(scrollableContainer, saveId)
                     instagramContentManager.setContent(data.content)
                     instagramContentManager.setAuthor(data.author)
                     instagramContentManager.setMedia(data.media)
                     console.log(data.platform)
                 }else if(data.platform == 'facebook'){
                    loadingMessage.textContent = "You need to use the Media Saver app to download facebook videos\n\n"+JSON.stringify(data)
                    loadingMessage.style.color = "red"
                    loading.style.color = "red"
                    console.log(data.platform)
                }
             }
         })
         .catch(error => {
             console.error('Error:', error);
         });
 });
 
 class TikTokContentManager {
     constructor(scrollableContainer, saveId) {
         this.scrollableContainer = scrollableContainer;
         this.saveId = saveId;
     }
 
     formatValue(value) {
         return typeof value === 'number'
             ? (value >= 1e6
                 ? (value / 1e6).toFixed(1) + 'm'
                 : value >= 1e3
                 ? (value / 1e3).toFixed(1) + 'k'
                 : value)
             : value;
     }
 
     setContent(content) {
         const contentDiv = document.createElement('div');
         const contentTitle = document.createElement('p');
         const contentCover = document.createElement('img');
         contentDiv.className = 'container post';
         contentTitle.className = 'title';
         contentCover.className = 'productimg';
 
         contentTitle.innerHTML = "<p class='key'>Post:</p>";
 
         for (const key in content) {
             if (content.hasOwnProperty(key) && key !== "cover" && key !== "id") {
                 const spanKey = document.createElement('span');
                 spanKey.className = 'key';
                 spanKey.textContent = key + ': ';
 
                 const spanValue = document.createElement('span');
                 spanValue.className = key;
                 spanValue.textContent = this.formatValue(content[key]) + ' ';
 
                 contentTitle.appendChild(spanKey);
                 contentTitle.appendChild(spanValue);
             }
         }
         contentCover.src = content.cover;
 
         contentDiv.append(contentCover);
         contentDiv.append(contentTitle);
         this.scrollableContainer.insertBefore(contentDiv, this.saveId.nextSibling);
     }
 
     setAuthor(author) {
         const authorDiv = document.createElement('div');
         const authorTitle = document.createElement('p');
         const authorCover = document.createElement('img');
         authorDiv.className = 'container post';
         authorTitle.className = 'title';
         authorCover.className = 'productimg';
 
         authorTitle.innerHTML = "<p class='key'>Author:</p>";
 
         for (const key in author) {
             if (author.hasOwnProperty(key) && key !== "image" && key !== "id") {
                 const spanKey = document.createElement('span');
                 spanKey.className = 'key';
                 spanKey.textContent = key + ': ';
 
                 const spanValue = document.createElement('span');
                 spanValue.className = key;
                 spanValue.textContent = this.formatValue(author[key]) + ' ';
 
                 authorTitle.appendChild(spanKey);
                 authorTitle.appendChild(spanValue);
             }
         }
         authorCover.src = author.image;
 
         authorDiv.append(authorCover);
         authorDiv.append(authorTitle);
         this.scrollableContainer.insertBefore(authorDiv, this.saveId.nextSibling);
     }
 
     setMusic(music) {
         const musicDiv = document.createElement('div');
         const musicTitle = document.createElement('p');
         const musicCover = document.createElement('img');
         musicDiv.className = 'container post';
         musicCover.className = 'productimg';
         musicTitle.className = 'title';
         musicCover.src = music.cover;
 
         musicTitle.innerHTML = `<p class='key'><span><a href='${music.src}' download='${music.author}.mp3' referrerpolicy='no-referrer'>Download </a></span> Music:</p>`;
 
         for (const key in music) {
             if (music.hasOwnProperty(key) && key !== "src" && key !== "cover") {
                 const spanKey = document.createElement('span');
                 spanKey.className = 'key';
                 spanKey.textContent = key + ': ';
 
                 const spanValue = document.createElement('span');
                 spanValue.className = key;
                 spanValue.textContent = this.formatValue(music[key]) + ' ';
 
                 musicTitle.appendChild(spanKey);
                 musicTitle.appendChild(spanValue);
             }
         }
 
         musicDiv.append(musicCover);
         musicDiv.append(musicTitle);
         this.scrollableContainer.insertBefore(musicDiv, this.saveId.nextSibling);
     }
 
     setVideos(videos) {
         const contentDiv = document.createElement('div');
         const videoTitle = document.createElement('p');
         contentDiv.className = 'container post';
         videoTitle.className = 'title';
         videoTitle.textContent = 'Videos Quality:';
 
         const contentCover = document.createElement('video');
         contentCover.className = 'productimg';
         contentCover.referrerPolicy = 'no-referrer';
         contentCover.crossOrigin = 'anonymous';
         contentCover.controls = true;
 
         const videoQualitySelect = document.createElement('select');
         videoQualitySelect.className = 'select';
 
         videos.forEach(videoData => {
             const videoQuality = Object.keys(videoData)[0];
             const video = videoData[videoQuality];
 
             const option = document.createElement('option');
             option.value = video.address;
             option.textContent = `Quality: ${videoQuality.toUpperCase()}, Size: ${(video.size / 1024 / 1024).toFixed(2)} MB`;
             videoQualitySelect.appendChild(option);
         });
 
         if (videos.length > 0) {
             contentCover.src = 'https://api.cors.lol/?url='+encodeURIComponent(videos[0][Object.keys(videos[0])[0]].address);
         }
 
         videoQualitySelect.addEventListener('change', function() {
             contentCover.src = 'https://api.cors.lol/?url='+encodeURIComponent(this.value);
         });
 
         contentDiv.appendChild(contentCover);
         contentDiv.appendChild(videoTitle);
         contentDiv.appendChild(videoQualitySelect);
 
         this.scrollableContainer.insertBefore(contentDiv, this.saveId.nextSibling);
     }
 }
 
 class InstagramContentManager {
     constructor(scrollableContainer, saveId) {
         this.scrollableContainer = scrollableContainer;
         this.saveId = saveId;
     }
 
     formatValue(value) {
         return typeof value === 'number'
             ? (value >= 1e6
                 ? (value / 1e6).toFixed(1) + 'm'
                 : value >= 1e3
                 ? (value / 1e3).toFixed(1) + 'k'
                 : value)
             : value;
     }
 
     setContent(content) {
         const contentDiv = document.createElement('div');
         const contentTitle = document.createElement('p');
         const contentCover = document.createElement('img');
         contentDiv.className = 'container post';
         contentTitle.className = 'title';
         contentCover.className = 'productimg';
 
         contentTitle.innerHTML = "<p class='key'>Post:</p>";
 
         for (const key in content) {
             if (content.hasOwnProperty(key) && key !== "cover" && key !== "id") {
                 const spanKey = document.createElement('span');
                 spanKey.className = 'key';
                 spanKey.textContent = key + ': ';
 
                 const spanValue = document.createElement('span');
                 spanValue.className = key;
                 spanValue.textContent = this.formatValue(content[key]) + ' ';
 
                 contentTitle.appendChild(spanKey);
                 contentTitle.appendChild(spanValue);
             }
         }
         contentCover.referrerPolicy = 'no-referrer';
         contentCover.crossOrigin = 'anonymous';
         contentCover.src = 'https://corsproxy.io/?' + encodeURIComponent(content.cover);
 
         contentDiv.append(contentCover);
         contentDiv.append(contentTitle);
         this.scrollableContainer.insertBefore(contentDiv, this.saveId.nextSibling);
     }
 
     setAuthor(author) {
         const authorDiv = document.createElement('div');
         const authorTitle = document.createElement('p');
         const authorCover = document.createElement('img');
         authorDiv.className = 'container post';
         authorTitle.className = 'title';
         authorCover.className = 'productimg';
 
         authorTitle.innerHTML = "<p class='key'>Author:</p>";
 
         for (const key in author) {
             if (author.hasOwnProperty(key) && key !== "image" && key !== "id") {
                 const spanKey = document.createElement('span');
                 spanKey.className = 'key';
                 spanKey.textContent = key + ': ';
 
                 const spanValue = document.createElement('span');
                 spanValue.className = key;
                 spanValue.textContent = this.formatValue(author[key]) + ' ';
 
                 authorTitle.appendChild(spanKey);
                 authorTitle.appendChild(spanValue);
             }
         }
 
         authorCover.referrerPolicy = 'no-referrer';
         authorCover.crossOrigin = 'anonymous';
         authorCover.src = 'https://corsproxy.io/?' + encodeURIComponent(author.image);
 
         authorDiv.append(authorCover);
         authorDiv.append(authorTitle);
         this.scrollableContainer.insertBefore(authorDiv, this.saveId.nextSibling);
     }
 
     setMedia(media) {
 
         media.forEach(mediaData => {
             const contentDiv = document.createElement('div');
             const contentTitle = document.createElement('p');
             contentDiv.className = 'container post';
             contentTitle.className = 'title';
             contentTitle.innerHTML = `<p class='key'>${mediaData.id}</p>`;
 
             for (const key in mediaData) {
                 if (mediaData.hasOwnProperty(key) && key !== "display_url" && key !== "id") {
                     const spanKey = document.createElement('span');
                     spanKey.className = 'key';
                     spanKey.textContent = key + ': ';
 
                     const spanValue = document.createElement('span');
                     spanValue.className = key;
                     spanValue.textContent = this.formatValue(mediaData[key]) + ' ';
 
                     contentTitle.appendChild(spanKey);
                     contentTitle.appendChild(spanValue);
                 }
             }
 
             const isVideo = mediaData.is_video;
             const mediaElement = isVideo ? document.createElement('video') : document.createElement('img');
             mediaElement.className = 'productimg';
             mediaElement.referrerPolicy = 'no-referrer';
             mediaElement.crossOrigin = 'anonymous';
 
             if (isVideo) {
                 mediaElement.controls = true;
                 mediaElement.src = 'https://api.cors.lol/?url='+encodeURIComponent(mediaData.display_url)
             }else{
                 mediaElement.src = 'https://corsproxy.io/?' + encodeURIComponent(mediaData.display_url);
             }
 
             contentDiv.appendChild(mediaElement);
             contentDiv.append(contentTitle);
             this.scrollableContainer.insertBefore(contentDiv, saveId.nextSibling);
         });
     }
 
 }
 
 links.forEach(link => {
     link.addEventListener('click', function (event) {
         event.preventDefault();
         const targetId = this.getAttribute('href').substring(1);
         const targetElement = document.getElementById(targetId);
 
         if (targetElement) {
             sections.forEach(container => {
                 container.classList.remove('active');
             });
 
             targetElement.classList.add('active');
         }
     });
 });
 
 document.addEventListener('DOMContentLoaded', function () {
    const currentHash = window.location.hash.substring(1);
    const targetElement = document.getElementById(currentHash);

    if (targetElement) {
        sections.forEach(container => {
            container.classList.remove('active');
        });

        targetElement.classList.add('active');
    }
});

 setInterval(() => {
     navLink.classList.remove('visible');
     navLink.classList.add('hidden');
 
     setTimeout(() => {
         navLink.textContent = isAbout ? 'About' : 'Privacy';
         navLink.classList.remove('hidden');
         navLink.classList.add('visible');
         isAbout = !isAbout;
     }, 500);
 }, 8000);
 
 
 /*
  *************************************
  * For any modifications,
  * please contact the nigga (devfemibadmus@gmail.com).
  *************************************
  */