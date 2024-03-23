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

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let split = el.split('=');
      cookie[split[0].trim()] = split.slice(1).join("=");
    })
    return cookie[name];
}

const setTheme = theme => document.documentElement.className = theme;

function setThemeFromCookie() {
    theme = getCookie('theme')
    console.log(theme)
    if (!theme) {
        setTheme('dark')
        setThemeCookie('dark')
    }
    setTheme(theme)
}

function setThemeCookie(theme) {
    const existingThemeCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('theme='));
    if (existingThemeCookie) {
        console.log('setThemeCookie', theme)
        document.cookie = `theme=${theme};path=/`;
        console.log(document.cookie)
    } else {
        const cookieString = `theme=${theme};path=/`;
        document.cookie = cookieString;
    }
}

function changeTheme() {
    checkboxEle = document.querySelector('.theme-checkbox')
    if (checkboxEle.checked) {
        theme = 'dark'
    }
    else {
        theme = 'light'
    }
    setThemeCookie(theme)
    setThemeFromCookie()
}

if (document.querySelector('.theme-checkbox')) {
    if (getCookie('theme') == 'light') {
        document.querySelector('.theme-checkbox').checked = false;
    } else {
        document.querySelector('.theme-checkbox').checked = true;
    }
}

setThemeFromCookie()

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