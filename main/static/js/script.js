const collectedData = [];

let intervalData;
let intervalMessage;
let isAbout = true;
let navLink = document.getElementById('nav-privacy');

const saveId = document.getElementById('saveId');
const saveSection = document.getElementById('save');
const links = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const loadingMessage = document.getElementById('loading-message');
const scrollableContainer = document.querySelector('.scrollable-container');


async function getData() {
    try {
        // console.log("fetchSessionData")
        const response = await fetch('/getData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        let filteredData;
        const newData = await response.json();
        console.log(newData)

        if(!newData.includes("nigga")){
            const filteredData = newData.filter(newItem => 
                !collectedData.some(collectedItem => JSON.stringify(collectedItem) === JSON.stringify(newItem))
            );
            if(filteredData.length > 0){
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
                
                scrollableContainer.appendChild(containerDiv);
            });} else {
                // clearInterval(intervalData);
                // console.log('Data already collected. Stopping interval.');
            }

        }

    } catch (error) {
        console.error('Error fetching session data:', error);
    }
}


async function getMessage() {
    try {
        const response = await fetch('/getMessage', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            }
        });
        const data = await response.text();
        loadingMessage.textContent  = data;
        console.log("getMessage: ", data)
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

    Array.from(scrollableContainer.children).forEach(child => {
        if (child !== saveId) {
            scrollableContainer.removeChild(child);
        }
    });

    sections.forEach(section => {
        section.classList.remove('active');
    });
    saveSection.classList.add('active');

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(response => {
        console.log(response);
        alert(response);
    })
    .catch(error => {
        console.error('Error:', error);
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


intervalData = setInterval(getData, 5000);
intervalMessage = setInterval(getMessage, 5000);


if (window.performance) {
    console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
    console.info("This page is reloaded");
} else {
    console.info("This page is not reloaded");
}

