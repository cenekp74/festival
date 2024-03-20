var disableanim = false
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function topnav_drop() {
    var topnav = document.getElementById("topnav");
    var topnav_links = document.getElementById("topnav-links");
    var icon = document.getElementById("icon");
    icon.className = "fa fa-xmark"
    if (topnav.className === "topnav") {
        topnav.className += " responsive";
        disableanim = false;
        animateHeight(0, topnav_links.scrollHeight, topnav_links);
        sleep(320).then(() => {topnav_links.style.height = "auto";});
    } else {
        var icon = document.getElementById("icon");
        icon.className = "fa fa-bars"
        disableanim = true
        topnav_links.style.height = "auto";
        topnav.className = "topnav";
        sleep(320).then(() => {disableanim=false;});
    }
}
function hide_topnav() {
    var topnav = document.getElementById("topnav");
    var topnav_links = document.getElementById("topnav-links");
    var icon = document.getElementById("icon");
    icon.className = "fa fa-bars"
    disableanim = true
    topnav_links.style.height = "auto";
    topnav.className = "topnav";
    sleep(320).then(() => {disableanim=false;});
}
function animateHeight(start, target, element) {
    var duration = 300;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = timestamp - startTime;
        var percentage = Math.min(progress / duration, 1);

        element.style.height = start + (target - start) * percentage + 'px';

        if (progress < duration) {
            if (disableanim) {
                element.style.height = "auto";
                return;
            }
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

function setParentDisplayNone(element) {
    element.parentNode.style.display = 'none';
}

function stopEventPropagation(event) {
    event.stopPropagation()
}

function toggleProgramDropdown() {
    element = document.getElementsByClassName('program-dropdown-content')[0];
    element.classList.toggle('dropped');
}

function hideProgramDropdown() {
    element = document.getElementsByClassName('program-dropdown-content')[0];
    element.classList.remove('dropped');
}

function createElementFromHTML(htmlString) {
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}

function showFlashAlert(message, category='') {
    let eleString = `<div class="alert alert-${category}">
            ${message} <i onclick="setParentDisplayNone(this)" class="fa fa-xmark"></i>
        </div>`
    let ele = createElementFromHTML(eleString)
    let content = document.getElementsByClassName('content')[0]
    content.insertBefore(ele, content.firstChild)
}

document.addEventListener('click', () => {
    hide_topnav()
    hideProgramDropdown()
})

document.addEventListener('scroll', () => {
    hide_topnav()
})

const logoMediaQuery = window.matchMedia('(max-width: 380px)');
if (logoMediaQuery.matches) {
    let logo = document.querySelector('.logo')
    logo.innerHTML = 'JSNO'
}