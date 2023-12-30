function timeToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

function getMinutesFrom8am() {
    var currentDate = new Date();
    var targetTime = new Date(currentDate);
    targetTime.setHours(8, 0, 0, 0);
    var timeDifference = currentDate - targetTime;
    var minutesPassed = Math.floor(timeDifference / (1000 * 60));
    return minutesPassed
}

// vypocita z casu ve formatu HH:MM pocet minut ktery ubehnul od 8 rano
function calculateMinutesFromStart(startTime, endTime) {
    const timeRangeStart = timeToMinutes("08:00");
    const startMinutes = timeToMinutes(startTime);
    const endMinutes = timeToMinutes(endTime);

    const minutesFromStart = startMinutes - timeRangeStart;
    const minutesFromEnd = endMinutes - timeRangeStart;

    return {
        start: minutesFromStart,
        end: minutesFromEnd
    };
}

function updateTimeVerticalLine() {
    const root = document.querySelector(":root");
    var minutes = getMinutesFrom8am()
    if (minutes < 0 | minutes > 360) {
        root.style.setProperty("--vline-visibility", "hidden");
        return
    }
    root.style.setProperty("--vline-visibility", "visible");
    root.style.setProperty("--vline-left", String(minutes/360*100)+"%");
}

function showContextMenu(event, element) {
    event.stopPropagation();
    var item_id = element.getAttribute('item-id');
    var contextMenu = document.getElementById('cm-'+item_id);
    contextMenu.style.left = event.pageX + 'px';
    contextMenu.style.top = event.pageY + 'px';
    if (contextMenu.style.visibility == 'hidden') {
        hideAllContextMenu();
        contextMenu.style.visibility = 'visible';
        contextMenu.style.width = 'fit-content';
        contextMenu.style.height = 'auto';
    } else {
        contextMenu.style.visibility = 'hidden';
        contextMenu.style.width = '0';
        contextMenu.style.height = '0';
    }
}

function hideAllContextMenu() {
    var cms = document.getElementsByClassName('item-details');
    for (var i=0; i < cms.length; i++) {
        cms[i].style.visibility = 'hidden';
        cms[i].style.width = '0';
        cms[i].style.height = '0';
    }
}

function flashItem(item) {
    for (var t=0; t<8000; t +=300) {
        setTimeout(() => {item.classList.toggle('flashed');}, t);
    }
    setTimeout(() => {item.classList.add('flashed');},600);
    setTimeout(() => {item.classList.remove('flashed');},30000);
}

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let split = el.split('=');
      cookie[split[0].trim()] = split.slice(1).join("=");
    })
    return cookie[name];
}

async function toggleFavorite(uid) {
    console.log(uid);
    const response = await fetch('/favorite/toggle/'+uid, {
        method: 'get'
    });
    const setCookieHeader = response.headers.get('Set-Cookie');
    if (setCookieHeader) {
        document.cookie = setCookieHeader;
    }
    reloadStars();
}

function reloadStars() {
    var stars = document.getElementsByClassName('favorite-star');
    var favoriteCookie = getCookie('favorite').replace('"', '');
    var favoriteItems = favoriteCookie.split(' ');
    for (var i = 0; i < items.length; i++) {
        if (favoriteItems.includes(stars[i].id.split('-')[1])) {
            stars[i].classList.add('in-favorite');
        }
        else {
            stars[i].classList.remove('in-favorite');
        }
    }
}

const mediaQuery = window.matchMedia('(max-width: 330px)');
if (mediaQuery.matches) {
    var items = document.getElementsByClassName('time-item');
    for (var i = 0; i < items.length; i++) {
        items[i].innerHTML = items[i].innerHTML.split(':')[0]
    }
}

var items = document.getElementsByClassName('program-item');
var room_elements = document.getElementsByClassName('room');
var rooms = []
for (var i = 0; i < room_elements.length; i++) {
    var content = room_elements[i].innerHTML;
    rooms.push(content);
}

for (var i = 0; i < items.length; i++) {
    var start_time = items[i].getAttribute('start-time');
    var end_time = items[i].getAttribute('end-time');
    var room = items[i].getAttribute('room');
    var minutesFromStart = calculateMinutesFromStart(start_time, end_time);
    if (minutesFromStart.start == 0) {minutesFromStart.start = 1;}
    items[i].style.gridColumnStart = minutesFromStart.start;
    items[i].style.gridColumnEnd = minutesFromStart.end;
    items[i].style.gridRowStart = rooms.indexOf(room)+2; //+2 je protoze index zacina od 0 a prvni row jsou casy
}

//idk kdyz to dam vsechno do jednoho loopu tak to nefacha protoze se jakoze neupdatuje width a height property hned co zmenim styl
for (var i = 0; i < items.length; i++) {
    if (items[i].offsetHeight - items[i].offsetWidth > 15) {
        items[i].classList += ' vertical';
    }
}

updateTimeVerticalLine()
setInterval(updateTimeVerticalLine, 60*1000)

if (document.URL.indexOf("?") != -1) {
    var item_id = document.URL.split('?')[1];
    var item = document.getElementById(item_id);
    flashItem(item);
}

reloadStars();