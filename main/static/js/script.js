let collectedData = [];
let message = [];

let intervalData;
let intervalMessage;
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


async function getData() {
    try {

        const response = await fetch('/getData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const allData = await response.json();
        console.log(allData)

        const message = allData.message;
        const newData = allData.mediaurl;

        loadingMessage.textContent = message.substring(0, 21)

        if (!newData.includes("nigga")) {
            const filteredData = newData.filter(newItem =>
                !collectedData.some(collectedItem => JSON.stringify(collectedItem) === JSON.stringify(newItem))
            );
            if (filteredData.length > 0) {
                filteredData.forEach(item => {
                    collectedData.push(item);
                    console.log('New Data collected. Continue interval.');
                    const containerDiv = document.createElement('div');
                    containerDiv.className = 'container post';
                    console.log(newData)

                    if (item.src && item.src.includes('.mp4?X-Goog-Algorithm')) {
                        const video = document.createElement('video');
                        video.className = 'productimg';
                        video.controls = true;
                        // video.autoplay = true;
                        video.loop = true;
                        video.style.width = '100%';
                        video.style.height = 'auto';

                        const source = document.createElement('source');
                        source.src = item.src;
                        source.type = 'video/mp4';
                        source.className = 'productimg';

                        video.appendChild(source);
                        containerDiv.appendChild(video);
                    } else if (item.src && item.src.includes('.png?X-Goog-Algorithm') || item.src && item.src.includes('.jpg?X-Goog-Algorithm') || item.src && item.src.includes('.jpeg?X-Goog-Algorithm')) {
                        const a = document.createElement('a');
                        a.href = item.src;
                        a.download = item.src.split('/').pop();
                        const img = document.createElement('img');
                        img.src = item.src;
                        img.alt = '';
                        img.className = 'productimg';
                        img.style.width = '100%';
                        img.style.height = 'auto';
                        a.appendChild(img);
                        containerDiv.appendChild(a);
                    } else {
                        const p = document.createElement('p');
                        p.textContent = item.message;
                        p.style.color = 'red';
                        containerDiv.appendChild(p);
                    }

                    scrollableContainer.insertBefore(containerDiv, saveId.nextSibling);
                });
            }

        }
        if(message == ""){
            clearInterval(intervalData);
            intervalData = null;
            console.log('Data already collected. Stopping interval.');
        }

    } catch (error) {
        console.error('Error fetching session data:', error);
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

searchButton.addEventListener('click', function (event) {
    event.preventDefault();
    const url = searchInput.value;

    var formData = new FormData();
    formData.append('src', url);

    sections.forEach(section => {
        section.classList.remove('active');
    });
    saveSection.classList.add('active');

    loadingMessage.textContent = "Starting"

    message.push("start")

    fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(response => {
            clearInterval(intervalData);
            intervalData = null;
            console.log(response);
            loading.style.display = "none"
            loadingMessage.textContent = ((response.message).substring(0, 19) + "...")
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

async function checkDone() {
    if (message.includes("start")) {
        loading.style.display = "inline"
        console.log("checkDone include start")
        message = [];

        if (intervalData) {
            clearInterval(intervalData);
        }

        intervalData = setInterval(getData, 5000);
    }
    console.log("checkDone")
}

setInterval(checkDone, 5000);

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

document.body.addEventListener('DOMNodeInserted', e => {
    if (e.target.tagName === 'VIDEO') retryVideo(e.target);
});

if (window.performance) {
    console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
    console.info("This page is reloaded");
} else {
    console.info("This page is not reloaded");
}
