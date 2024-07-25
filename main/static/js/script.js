/*
 *************************************
 * WARNING: DO NOT EDIT THIS CODE
 *
 * Unauthorized changes to this code
 * can cause unexpected behavior and
 * errors. For any modifications,
 * please contact the nigga (devfemibadmus@gmail.com).
 *************************************
 */

let collectedData = [];
let startFucking;
let intervalId;

let severResponse;
let isAbout = true;
let navLink = document.getElementById('nav-privacy');

const saveId = document.getElementById('saveId');
const searchId = document.getElementById('home');
const loading = document.getElementById('loading');
const saveSection = document.getElementById('save');
const links = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const loadingMessage = document.getElementById('loading-message');
const scrollableContainer = document.querySelector('.scrollable-container');


async function getData() {
    if (startFucking == "yes"){
        console.log("started Fucking")
        try {
    
            const response = await fetch('/getData', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
    
            const allData = await response.json();
    
            const message = allData.message;
            const newData = allData.mediaurl;

            loadingMessage.textContent = severResponse || message;
        
            if (!newData.includes("nigga")) {
                const filteredData = newData.filter(newItem =>
                    !collectedData.some(collectedItem => JSON.stringify(collectedItem) === JSON.stringify(newItem))
                );
                console.log("allData: ", allData)
                console.log("filteredData: ", filteredData)
                if (filteredData.length > 0) {
                    filteredData.forEach(item => {
                        collectedData.push(item);
                        console.log('New Data collected. Continue interval.');
                        const containerDiv = document.createElement('div');
                        const title = document.createElement('p');
                        containerDiv.className = 'container post';
                        title.className = 'title';
                        title.style.color = 'red';
                        console.log(newData)
                        startCountdown(3, title, containerDiv);
    
                        if (item.src && item.mediaType == "video") {
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
                        } else if (item.src && item.mediaType == "image") {
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
    
                        containerDiv.appendChild(title);
                        scrollableContainer.insertBefore(containerDiv, saveId.nextSibling);
                    });
                }
    
            }
    
        } catch (error) {
            console.error('Error fetching session data:', error);
        }
    } else{
        console.log("stop Fucking")
    }
}

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
    loading.style.display = "inline"

    startFucking = "yes";
    severResponse = null
    console.log("%cNIGGA SAID STOP!", "color: red; font-size: 50px; font-weight: bold;");
    console.log("%cWARNING: Unauthorized changes to this code can cause unexpected behavior and errors. Please contact the developer for any modifications.", "color: white; font-size: 16px;");
    intervalId = setInterval(getData, 5000);

    fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(response => {
            clearInterval(intervalId)
            console.log(response);
            if (response.cancel){
                loadingMessage.textContent = (response.message)
            } else {
                startFucking = "no";
                severResponse = response.message;
                loading.style.display = "none"
                loadingMessage.textContent = (response.message)
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

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


function startCountdown(duration, countdownElement, containerDiv) {
    let totalSeconds = duration * 60;

    function updateCountdown() {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        countdownElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        if (totalSeconds <= 0) {
            clearInterval(countdownInterval);
            countdownElement.textContent = '00:00';
            containerDiv.remove();
            const numberOfChildren = scrollableContainer.children.length;
            if(numberOfChildren == 1){
                sections.forEach(section => {
                    section.classList.remove('active');
                });
                searchId.classList.add('active');
            }
        } else {
            totalSeconds--;
        }
    }

    updateCountdown();
    const countdownInterval = setInterval(updateCountdown, 1000);
}

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


/*
 *************************************
 * WARNING: DO NOT EDIT THIS CODE
 *
 * Unauthorized changes to this code
 * can cause unexpected behavior and
 * errors. For any modifications,
 * please contact the nigga (devfemibadmus@gmail.com).
 *************************************
 */
