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
        topnav_links.style.overflowY = "hidden" // tohle je protoze jinak se v chromu ukazuje scrollbar pri rozbalovani
        animateHeight(0, topnav_links.scrollHeight, topnav_links);
        sleep(320).then(() => {topnav_links.style.height = "auto"; topnav_links.style.overflowY = "";});
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

/** meni vysku elementu od start do target
 * - trva 300ms
 * - na konci nastavi element.height na auto
 * - pouziva se na animovani topnavu
 */
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

/** vyuziva se pri skryvani flash alertu po kliknuti na krizek */
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

/** vytvori HTML element ze stringu - pouziva fce showFlashAlert */
function createElementFromHTML(htmlString) {
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}

function deleteAllFlashAlerts() {
    const elements = document.querySelectorAll(".alert");
    elements.forEach(element => {
        element.remove();
    });
}

/** prida na stranku flash alert s obsahem message a tridou alert-$category */
function showFlashAlert(message, category='', timeout=5000) {
    let eleString = `<div class="alert alert-${category}">
            ${message} <i onclick="setParentDisplayNone(this)" class="fa fa-xmark"></i>
        </div>`
    let ele = createElementFromHTML(eleString)
    let content = document.getElementsByClassName('content')[0]
    content.insertBefore(ele, content.firstChild)
    setTimeout(function() { // tahle monstrozita je tu aby po chvili alert zmizel a aby mizel postupne
        ele.style.opacity = '0'
        setTimeout(function() {
            ele.style.display = 'none'
        }, timeout*1/3)
    }, timeout*2/3)
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
    if (!theme) {
        setTheme('dark')
        setThemeCookie('dark')
    }
    setTheme(theme)
}

function setThemeCookie(theme) {
    const existingThemeCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('theme='));
    if (existingThemeCookie) {
        document.cookie = `theme=${theme};path=/`;
    } else {
        const cookieString = `theme=${theme};path=/`;
        document.cookie = cookieString;
    }
}

/** zmeni theme podle stavu checkboxu - zavola fci setThemeCookie a pak setThemeFromCookie */
function changeTheme() {
    var styleSheet = document.createElement("style")
    styleSheet.innerText = '* {transition: all 1s}' // aby byl prechod mezi themama plynulej
    document.head.appendChild(styleSheet)
    checkboxEle = document.querySelector('.theme-checkbox')
    if (checkboxEle.checked) {
        theme = 'dark'
    }
    else {
        theme = 'light'
    }
    setThemeCookie(theme)
    setThemeFromCookie()
    sleep(500).then(() => {document.head.removeChild(styleSheet)})
}

// posune theme checkbox do spravny polohy podle cookiesky
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

// pokud je obrazovka mensi nez 412px, zmenim napis "Jeden svet na ohradni" na "JSNO"
const logoMediaQuery = window.matchMedia('(max-width: 412px)');
if (logoMediaQuery.matches) {
    let logo = document.querySelector('.logo')
    logo.innerHTML = 'JSNO'
}