function timeToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

function getMinutesFrom830am() {
    var currentDate = new Date();
    var targetTime = new Date(currentDate);
    targetTime.setHours(8, 30, 0, 0);
    var timeDifference = currentDate - targetTime;
    var minutesPassed = Math.floor(timeDifference / (1000 * 60));
    return minutesPassed
}

// vypocita z casu ve formatu HH:MM pocet minut ktery ubehnul od 8:30 rano
function calculateMinutesFromStart(startTime, endTime) {
    const timeRangeStart = timeToMinutes("08:30");
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
    var minutes = getMinutesFrom830am()
    if (minutes < 0 | minutes > 390) {
        root.style.setProperty("--vline-visibility", "hidden");
        return
    }
    root.style.setProperty("--vline-visibility", "visible");
    root.style.setProperty("--vline-left", String(minutes/390*100)+"%");
}

function showContextMenu(event, element) {
    event.stopPropagation();
    var item_id = element.getAttribute('item-id');
    var contextMenu = document.getElementById('cm-'+item_id);
    contextMenu.style.top = event.pageY + 'px';

    // tohle je aby se cm zobrazovalo nalevo od kliknuti pokud je moc blizko pravy strane (190px, coz je max-width context menu definovana v program.css)
    let distanceLeft = event.clientX;
    let distanceRight = window.innerWidth - event.clientX;
    if (distanceRight < 190) {
        contextMenu.style.left = ''
        contextMenu.style.borderTopRightRadius = '0'
        contextMenu.style.borderTopLeftRadius = ''
        contextMenu.style.right = distanceRight + 'px'
    } else {
        contextMenu.style.right = ''
        contextMenu.style.borderTopLeftRadius = '0'
        contextMenu.style.borderTopRightRadius = ''
        contextMenu.style.left = distanceLeft + 'px';
    }

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
    const response = await fetch('/favorite/toggle/'+uid, {
        method: 'get'
    });
    const setCookieHeader = response.headers.get('Set-Cookie');
    if (setCookieHeader) {
        document.cookie = setCookieHeader;
    }
    reloadStars();
    showFavoriteAlert(uid)
}

function showFavoriteAlert(uid) { // velice oskliva funkce na zobrazeni alertu kdyz user pridana/odebere z oblibenych
    deleteAllFlashAlerts()
    let itemEle = document.getElementById(uid)
    let itemName = itemEle.querySelector('div').innerText
    let isFavorite = document.getElementById(`star-${uid}`).classList.contains("in-favorite")
    let favoriteAlertHTMLString = `<div class="alert alert-favorite">
    <span></span><a href="#">Vrátit</a><i onclick="setParentDisplayNone(this)" class="fa fa-xmark"></i>
    </div>` // fuj
    let favoriteAlertEle = createElementFromHTML(favoriteAlertHTMLString)
    if (isFavorite) {
        favoriteAlertEle.querySelector('span').innerText = `${itemName} přidán do oblíbených - `
        favoriteAlertEle.classList.add('alert-success')
    } else {
        favoriteAlertEle.querySelector('span').innerText = `${itemName} odebrán z oblíbených - `
        favoriteAlertEle.classList.add('alert-danger')
    }
    favoriteAlertEle.querySelector('a').setAttribute('onclick', `toggleFavorite("${uid}")`)
    setTimeout(function() { // pred pridanim alertu je malej delay, aby to vypadalo lip kdyz kliknu na Vratit
        document.querySelector('.content').insertBefore(favoriteAlertEle, document.querySelector('.program-nav')) // alert pridam pred program-nav (takze za program)
    }, 50)
    setTimeout(function() { // tahle monstrozita je tu aby po chvili alert zmizel a aby mizel postupne
        favoriteAlertEle.style.opacity = '0'
        setTimeout(function() {
            favoriteAlertEle.style.display = 'none'
        }, 2000)
    }, 3500)
}

function reloadStars() {
    if (!(getCookie('favorite'))) {return} // pokud favorite cookie jeste neexistuje, return
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

document.addEventListener('click', () => {
    hideAllContextMenu()
})

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
    items[i].style.gridColumnStart = minutesFromStart.start+1;
    items[i].style.gridColumnEnd = minutesFromStart.end+1;
    items[i].style.gridRowStart = rooms.indexOf(room)+2; //+2 je protoze index zacina od 0 a prvni row jsou casy
}

function checkForSmallProgramItems() { // funkce ktera zkontroluje jestli nejaky program itemy nejsou moc maly, pokud jo tak je zobrazi vertikalne
    let items = document.getElementsByClassName('program-item');
    for (var i = 0; i < items.length; i++) {
        if (items[i].offsetHeight - items[i].offsetWidth > 15) {
            items[i].classList.add('vertical');
        }
        else {
            items[i].classList.remove('vertical')
        }
    }
}
window.addEventListener('resize', checkForSmallProgramItems);
checkForSmallProgramItems()

updateTimeVerticalLine()
setInterval(updateTimeVerticalLine, 60*1000)

if (document.URL.indexOf("?") != -1) {
    var item_id = document.URL.split('?')[1];
    var item = document.getElementById(item_id);
    flashItem(item);
}

reloadStars();

// tohle je tu kvuli tomu, ze grid-template-columns u program-containeru nejde nastavit ve fr, jinak se potom pri zmene velikosti jednoho program itemu (on hover) meni velikost jednoho sloupecku a cely se to posouva (jenom v chromu teda (nemam rad chrom))
function resizeProgramContainer() {
    programContainer = document.getElementsByClassName('program-container')[0]
    colSize = programContainer.offsetWidth / 390
    programContainer.style.gridTemplateColumns = `repeat(390, ${colSize}px)`
}
window.addEventListener('resize', resizeProgramContainer);
resizeProgramContainer()