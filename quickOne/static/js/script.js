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

    sections.forEach(section => {
        section.classList.remove('active');
    });
    saveSection.classList.add('active');

    loadingMessage.textContent = "Starting"
    loadingMessage.style.color = "grey"
    loading.style.display = "inline"

    fetch('/webmedia/api/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(response => {
            loading.style.display = "none"
            loadingMessage.textContent = response.message
            if(response.error){
                loadingMessage.style.color="red";
            }else if(response.success){
                loadingMessage.style.color="#00faff";
                const data = response.data;
                console.log(data);
                setMusic(data.music);
                setAuthor(data.author);
                setVideos(data.videos);
                setContent(data.content);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

function setContent(content){
    const formatValue = value => typeof value === 'number' ? (value >= 1e6 ? (value / 1e6).toFixed(1) + 'm' : value >= 1e3 ? (value / 1e3).toFixed(1) + 'k' : value) : value;

    const contentDiv = document.createElement('div');
    const contentTitle = document.createElement('p');
    const contentCover = document.createElement('img');
    contentDiv.className = 'container post';
    contentTitle.className = 'title';
    contentCover.className = 'productimg';

    contentTitle.innerHTML = "<p class='key'>Post:</p>";

    for (const key in content) {
        if (content.hasOwnProperty(key)) {
            if (key === "cover") continue;
            if (key === "id") continue;
            const spanKey = document.createElement('span');
            spanKey.className = 'key';
            spanKey.textContent = key + ': ';

            const spanValue = document.createElement('span');
            spanValue.className = key;
            spanValue.textContent = formatValue(content[key]) + ' ';

            contentTitle.appendChild(spanKey);
            contentTitle.appendChild(spanValue);
        }
    }
    contentCover.src = content.cover

    contentDiv.append(contentCover)
    contentDiv.append(contentTitle)
    scrollableContainer.insertBefore(contentDiv, saveId.nextSibling);
}

function setAuthor(author){
    const formatValue = value => typeof value === 'number' ? (value >= 1e6 ? (value / 1e6).toFixed(1) + 'm' : value >= 1e3 ? (value / 1e3).toFixed(1) + 'k' : value) : value;

    const authorDiv = document.createElement('div');
    const authorTitle = document.createElement('p');
    const authorCover = document.createElement('img');
    authorDiv.className = 'container post';
    authorTitle.className = 'title';
    authorCover.className = 'productimg';

    authorTitle.innerHTML = "<p class='key'>Author:</p>";

    for (const key in author) {
        if (author.hasOwnProperty(key)) {
            if (key === "image") continue;
            if (key === "id") continue;
            const spanKey = document.createElement('span');
            spanKey.className = 'key';
            spanKey.textContent = key + ': ';

            const spanValue = document.createElement('span');
            spanValue.className = key;
            spanValue.textContent = formatValue(author[key]) + ' ';

            authorTitle.appendChild(spanKey);
            authorTitle.appendChild(spanValue);
        }
    }
    authorCover.src = author.image

    authorDiv.append(authorCover)
    authorDiv.append(authorTitle)
    scrollableContainer.insertBefore(authorDiv, saveId.nextSibling);
}

function setMusic(music){
    const formatValue = value => typeof value === 'number' ? (value >= 1e6 ? (value / 1e6).toFixed(1) + 'm' : value >= 1e3 ? (value / 1e3).toFixed(1) + 'k' : value) : value;

    const musicDiv = document.createElement('div');
    const musicTitle = document.createElement('p');
    const musicCover = document.createElement('img');
    musicDiv.className = 'container post';
    musicCover.className = 'productimg';
    musicTitle.className = 'title';
    musicCover.src = music.cover;
    

    musicTitle.innerHTML = `<p class='key'><span><a href='${music.src}' download='${music.author}.mp3' referrerpolicy='no-referrer'>Download </a></span> Music:</p>`;

    for (const key in music) {
        if (music.hasOwnProperty(key)) {
            if (key === "src") continue;
            if (key === "cover") continue;
            const spanKey = document.createElement('span');
            spanKey.className = 'key';
            spanKey.textContent = key + ': ';

            const spanValue = document.createElement('span');
            spanValue.className = key;
            spanValue.textContent = formatValue(music[key]) + ' ';

            musicTitle.appendChild(spanKey);
            musicTitle.appendChild(spanValue);
        }
    }

    musicDiv.append(musicCover)
    musicDiv.append(musicTitle)
    scrollableContainer.insertBefore(musicDiv, saveId.nextSibling);
}

function setVideos(videos) {
    const contentDiv = document.createElement('div');
    const videoTitle = document.createElement('p');
    contentDiv.className = 'container post';
    videoTitle.className = 'title';
    videoTitle.textContent = 'Videos Quality:';

    const contentCover = document.createElement('video');
    contentCover.className = 'productimg';
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
        contentCover.src = videos[0][Object.keys(videos[0])[0]].address;
    }

    videoQualitySelect.addEventListener('change', function() {
        contentCover.src = this.value;
    });

    contentDiv.appendChild(contentCover);
    contentDiv.appendChild(videoTitle);
    contentDiv.appendChild(videoQualitySelect);

    scrollableContainer.insertBefore(contentDiv, saveId.nextSibling);
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


function retryVideo(video) {
    let retries = 0;
    video.addEventListener('error', () => {
        if (retries < 3) {
            retries++;
            video.load();
            video.play();
        }
    });
}

/*
 *************************************
 * For any modifications,
 * please contact the nigga (devfemibadmus@gmail.com).
 *************************************
 */
