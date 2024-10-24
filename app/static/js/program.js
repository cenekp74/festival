/** z casu ve formatu HH:MM vypocita kolik to je minut */
function timeToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

/** vrati pocet minut, ktery ubehnul od 8:30 rano */
function getMinutesFrom830am() {
    var currentDate = new Date();
    var targetTime = new Date(currentDate);
    targetTime.setHours(8, 30, 0, 0);
    var timeDifference = currentDate - targetTime;
    var minutesPassed = Math.floor(timeDifference / (1000 * 60));
    return minutesPassed
}

/** vypocita z casu ve formatu HH:MM pocet minut ktery ubehnul od 8:30 rano */
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

/** fce na aktualizovani carecky ukazujici cas podle aktualniho casu */
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

/** ukaze context menu k danymu program itemu */
function showContextMenu(event, element) {
    event.stopPropagation();
    var item_id = element.getAttribute('item-id');
    var contextMenu = document.getElementById('cm-'+item_id);
    contextMenu.style.top = event.pageY + 'px';

    // tohle je aby se cm zobrazovalo nalevo od kliknuti pokud je moc blizko pravy strane (190px, coz je max-width context menu definovana v program.css)
    let distanceLeft = event.clientX;
    let distanceRight = window.innerWidth - event.clientX;
    if (distanceRight < 190 & distanceLeft > distanceRight) { // 210 je max width cm definovana v program.css
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
    contextMenu.style.borderBottomLeftRadius = ''
    contextMenu.style.borderBottomRightRadius = ''

    // a tohle to samy akorat nahoru kdyz je to moc dole
    let distanceTop = event.clientY;
    let distanceBottom = window.innerHeight - event.clientY;
    if (distanceBottom < 200) {
        contextMenu.style.top = ''
        contextMenu.style.bottom = distanceBottom + 'px';
        [contextMenu.style.borderTopLeftRadius, contextMenu.style.borderBottomLeftRadius] = [contextMenu.style.borderBottomLeftRadius, contextMenu.style.borderTopLeftRadius];
        [contextMenu.style.borderTopRightRadius, contextMenu.style.borderBottomRightRadius] = [contextMenu.style.borderBottomRightRadius, contextMenu.style.borderTopRightRadius];
    } else {
        contextMenu.style.bottom = ''
        contextMenu.style.top = distanceTop + 'px';
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

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let split = el.split('=');
      cookie[split[0].trim()] = split.slice(1).join("=");
    })
    return cookie[name];
}

/** prida item s danym uid do oblibenych (posle request na server a podle odpovedi nastavi cookiesku) */
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

/** velice oskliva funkce na zobrazeni alertu kdyz user pridana/odebere z oblibenych, zavisi na tom jestli ma hvezdicka pro dany item class in-favorite */
function showFavoriteAlert(uid) {
    deleteAllFlashAlerts()
    let itemEle = document.getElementById(uid)
    let itemName = itemEle.querySelector('div').innerText
    let isFavorite = document.getElementById(`star-${uid}`).classList.contains("in-favorite")
    let favoriteAlertHTMLString = `<div class="alert alert-favorite">
    <span></span><a href="#">Vrátit</a><i onclick="setParentDisplayNone(this)" class="fa fa-xmark"></i>
    </div>` // fuj
    let favoriteAlertEle = createElementFromHTML(favoriteAlertHTMLString)
    if (isFavorite) {
        favoriteAlertEle.querySelector('span').innerText = `Přídáno do oblíbených: ${itemName} - `
        favoriteAlertEle.classList.add('alert-success')
    } else {
        favoriteAlertEle.querySelector('span').innerText = `Odebráno z oblíbených: ${itemName} - `
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

/** zmeni barvu hvezdicek podle favorite cookiesky */
function reloadStars() {
    var stars = document.querySelectorAll(".favorite-star");
    var program_item_stars = document.querySelectorAll(".program-item-star")

    if (!(getCookie('favorite'))) { // pokud favorite cookie neexistuje nebo je nulova (napr. pokud byl v oblibenych 1 item a odendam ho), tak odendej hvezdicky od vseho a return
        stars.forEach(starEle => {
            starEle.classList.remove('in-favorite');
        })
    
        program_item_stars.forEach(starEle => {
            starEle.classList.remove('in-favorite');
        })
    }
    var favoriteCookie = getCookie('favorite').replace('"', '');
    var favoriteItems = favoriteCookie.split(' ');
    stars.forEach(starEle => {
        if (favoriteItems.includes(starEle.id.split('-')[1])) {
            starEle.classList.add('in-favorite');
        }
        else {
            starEle.classList.remove('in-favorite');
        }
    })

    program_item_stars.forEach(starEle => {
        if (favoriteItems.includes(starEle.id.split('-')[1])) {
            starEle.classList.add('in-favorite');
        }
        else {
            starEle.classList.remove('in-favorite');
        }
    })
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
/** funkce ktera zkontroluje jestli nejaky program itemy nejsou moc maly, pokud jo tak je zobrazi vertikalne (prida class .vertical) */
function checkForSmallProgramItems() {
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

document.querySelectorAll(".item-details").forEach(ele => {
    ele.addEventListener("click", (e => {e.stopPropagation()})) // aby kdyz kliknu na cm (napr. pridam do oblibenych) tak okynko nezmizelo
})
    
updateTimeVerticalLine()
setInterval(updateTimeVerticalLine, 60*1000)

if (document.URL.indexOf("?") != -1) {
    var item_id = document.URL.split('?')[1];
    var item = document.getElementById(item_id);
    item.classList.add('flashed')
}

reloadStars();

/** tahle fce se pousti na zacatku a po kazdy zmene velikosti okna kvuli tomu, 
 * ze grid-template-columns u program-containeru nejde nastavit ve fr, 
 * jinak se potom pri zmene velikosti jednoho program itemu (on hover) meni velikost jednoho sloupecku a cely se to posouva 
 * (jenom v chromu teda (nemam rad chrom)) */
function resizeProgramContainer() {
    programContainer = document.getElementsByClassName('program-container')[0]
    colSize = programContainer.offsetWidth / 390
    programContainer.style.gridTemplateColumns = `repeat(390, ${colSize}px)`
}
window.addEventListener('resize', resizeProgramContainer);
resizeProgramContainer()

window.addEventListener('scroll', hideAllContextMenu)