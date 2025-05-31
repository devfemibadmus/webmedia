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
 
     loadingMessage.textContent = "Loading"
     loadingMessage.style.color = "grey"
     loading.style.display = "inline"
     loading.style.color = "grey"
 
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
                     tiktokContentManager.setMedia(data);
                     console.log(data.platform)
                 }else if(data.platform == 'instagram'){
                     const instagramContentManager= new InstagramContentManager(scrollableContainer, saveId)
                     instagramContentManager.setContent(data.content)
                     instagramContentManager.setAuthor(data.author)
                     instagramContentManager.setMedia(data.media)
                     console.log(data.platform)
                 }else if(data.platform == 'facebook'){
                    const facebookContentManager= new FacebookContentManager(scrollableContainer, saveId)
                    facebookContentManager.setContent(data.content)
                    facebookContentManager.setAuthor(data.author)
                    facebookContentManager.setMedia(data.media)
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
                //  spanKey.className = 'key';
                //  spanKey.textContent = key + ': ';
                 spanKey.innerHTML = `<a href='${content.cover}' download class='key'>${key}: </a>`;
 
                 const spanValue = document.createElement('span');
                 //spanValue.className = key;
                 spanValue.textContent = content[key] != "" ? this.formatValue(content[key]) + ' ' : "N/A ";
 
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
                 //spanValue.className = key;
                 spanValue.textContent = this.formatValue(music[key]) + ' ';
 
                 musicTitle.appendChild(spanKey);
                 musicTitle.appendChild(spanValue);
             }
         }
 
         musicDiv.append(musicCover);
         musicDiv.append(musicTitle);
         this.scrollableContainer.insertBefore(musicDiv, this.saveId.nextSibling);
     }
 
     setMedia(datas) {
        const media = datas.videos ?? datas.images
 
         media.forEach(mediaData => {
             const contentDiv = document.createElement('div');
             const contentTitle = document.createElement('p');
             contentDiv.className = 'container post';
             contentTitle.className = 'title';
             // contentTitle.innerHTML = `<p class='key'>${mediaData.id}</p>`;
 
             for (const key in mediaData) {
                 if (mediaData.hasOwnProperty(key) && key !== "is_video" && key !== "address" && key !== "cover" && key !== "id") {
                    const spanKey = document.createElement('span');
                    //  spanKey.className = 'key';
                    //  spanKey.textContent = key + ': ';
                     spanKey.innerHTML = `<a href='${mediaData[key]['address']}' download='${mediaData[key]}.${mediaData.is_video?"mp4":"png"}' class='key'>${key}: </a>`;
 
                     const spanValue = document.createElement('span');
                     spanValue.className = key;
                     spanValue.textContent = (Number(mediaData[key]['size']) / 1024 / 1024).toFixed(3) + 'MB';
 
                     contentTitle.appendChild(spanKey);
                     contentTitle.appendChild(spanValue);
 
                     const isVideo = datas.is_video;
                     const mediaElement = isVideo ? document.createElement('video') : document.createElement('img');
                     mediaElement.className = 'productimg';
                     mediaElement.crossOrigin = 'anonymous';
         
                     mediaElement.controls = true;
                     mediaElement.src = 'https://api.cors.lol/?url='+encodeURIComponent(mediaData[key]['address']);
         
                     contentDiv.appendChild(mediaElement);
                     contentDiv.append(contentTitle);
                     this.scrollableContainer.insertBefore(contentDiv, saveId.nextSibling);
                 }
             }
         });
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
         contentCover.src = 'https://api.cors.lol/?url=' + encodeURIComponent(content.cover);
 
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
         authorCover.src = 'https://api.cors.lol/?url=' + encodeURIComponent(author.image);
 
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
             //contentTitle.innerHTML = `<p class='key'>${mediaData.id}</p>`;
 
             for (const key in mediaData) {
                 if (mediaData.hasOwnProperty(key) && key !== "is_video" && key !== "address" && key !== "cover" && key !== "id") {
                    const spanKey = document.createElement('span');
                    spanKey.innerHTML = `<a href='${mediaData.address}' download='${mediaData[key]}.${mediaData.is_video?"mp4":"png"}' class='key'>${key}: </a>`;
                    //  spanKey.className = 'key';
                    //  spanKey.textContent = key + ': ';
 
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
 
             mediaElement.controls = true;
             mediaElement.src = 'https://api.cors.lol/?url='+encodeURIComponent(mediaData.address)
 
             contentDiv.appendChild(mediaElement);
             contentDiv.append(contentTitle);
             this.scrollableContainer.insertBefore(contentDiv, saveId.nextSibling);
         });
     }
 
 }
 
 class FacebookContentManager {
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
 
         //contentTitle.innerHTML = "<p class='key'>Post:</p>";
 
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
         contentCover.src = 'https://api.cors.lol/?url=' + encodeURIComponent(content.cover);
 
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
             if (author.hasOwnProperty(key) && key !== "image") {
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
         authorCover.src = '/static/facebook.png';
 
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
             contentTitle.innerHTML = `<a href='${mediaData.address}' download='${mediaData.id}.${mediaData.is_video?"mp4":"png"}' class='key'>${mediaData.id}</a>`;
 
             for (const key in mediaData) {
                 if (mediaData.hasOwnProperty(key) && key !== "is_video" && key !== "address" && key !== "cover") {
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
                 mediaElement.src = 'https://api.cors.lol/?url='+encodeURIComponent(mediaData.address)
             }else{
                 mediaElement.src = 'https://api.cors.lol/?url=' + encodeURIComponent(mediaData.address);
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
 
document.addEventListener("click", function(e) {
  if (e.target.tagName === "A" && e.target.classList.contains("key")) {
    e.preventDefault();
    loadingMessage.textContent = "Loading";
    loadingMessage.style.color = "red";
    loading.style.display = "inline";
    loading.style.color = "red";
    fetch(e.target.href)
      .then(res => res.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = e.target.getAttribute("download");
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        loadingMessage.textContent = "Downloading";
        loading.style.display = "none";
      })
      .catch(() => {
        loadingMessage.textContent = "Downloading";
        loading.style.display = "none";
      });
  }
});


 
 /*
  *************************************
  * For any modifications,
  * please contact the nigga (devfemibadmus@gmail.com).
  *************************************
  */