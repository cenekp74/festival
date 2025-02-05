// HODNE FUNKCI JE STEJNEJCH JAKO V PROGRAM.JS - KOMENTARE K NIM JSOU TAM

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

/** vypocita z minut od 1 do 390 cas od 8:30 do 15:00 */
function convertMinutesToTime(minutes) {
    if (minutes == 0) return "08:30"
    let hours = Math.floor(minutes / 60);
    let mins = minutes % 60;
    hours += 8;
    mins += 30;
    if (mins >= 60) {
        mins = mins - 60;
        hours += 1;
    }
    let formattedHours = hours < 10 ? "0" + hours : hours;
    let formattedMins = mins < 10 ? "0" + mins : mins;
    let timeString = formattedHours + ":" + formattedMins;
    return timeString;
}

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let split = el.split('=');
      cookie[split[0].trim()] = split.slice(1).join("=");
    })
    return cookie[name];
}

function showItemDetails(element) {
    var item_id = element.getAttribute('item-id');
    var itemDetails = document.getElementById('details-'+item_id);
    document.querySelectorAll('.interactive-item-details > div').forEach(ele => {
        ele.style.display = 'none'
    })
    itemDetails.style.display = 'block'
    document.querySelectorAll('.program-item').forEach(item => {item.classList.remove('selected')})
    element.classList.add('selected')
}

/** funkce na updatovani vsech inputu casu v item detailech podle attributu jednotlivych itemu v programu */
function updateAllTimeInputs() {
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
        if (item.style.visibility == 'hidden') {return};
        let item_id = item.getAttribute('item-id');
        let itemDetails = document.getElementById('details-'+item_id);
        itemDetails.querySelector('.time-from-input').value = item.getAttribute('start-time')
        itemDetails.querySelector('.time-to-input').value = item.getAttribute('end-time')
    })
}

/** funkce na updatovani polohy v grid u vsech itemu na zaklade jejich start-time a end-time atributu */
function updateAllItemsPosition() {
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
        if (items[i].style.gridColumnEnd > 391) {
            items[i].style.borderRight = '4px solid black'
        } else {items[i].style.borderRight = ''}
        items[i].style.gridRowStart = rooms.indexOf(room)+2; //+2 je protoze index zacina od 0 a prvni row jsou casy
    }
}

/** funkce na updatovani start-time, end-time a room attributu u vsech itemu na zaklade jejich grid stylingu (grid-column a grid-row-start) */
function updatteAllItemTimesAndRooms() {
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
        if (item.style.visibility == 'hidden') {return};
        let column_start = parseInt(item.style.gridColumn.split('/')[0])
        let column_end = parseInt(item.style.gridColumn.split('/')[1])
        item.setAttribute('start-time', convertMinutesToTime(column_start-1))
        item.setAttribute('end-time', convertMinutesToTime(column_end-1))
        let row_start = parseInt(item.style.gridRowStart)
        let room = document.querySelectorAll('.room')[row_start-2].innerHTML
        item.setAttribute('room', room)
    })
}

/** funkce na updatovani mistnosti v item details na zaklade atributu room u itemu */
function updateAllItemDetailsRooms() {
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
        if (item.style.visibility == 'hidden') {return};
        let item_id = item.getAttribute('item-id');
        let itemDetails = document.getElementById('details-'+item_id);
        itemDetails.querySelector('.item-details-room').innerHTML = item.getAttribute('room')
    })
}

async function saveProgram() {
    if (!confirm('Opravdu chcete uložit program?')) {return}
    toSend = {}
    modifiedItemUids.forEach(uid => {
        item = document.getElementById(uid)
        if (!item) {return}
        time_from = item.getAttribute('start-time')
        time_to = item.getAttribute('end-time')
        room = item.getAttribute('room')
        toSend[uid] = {"time_from":time_from, "time_to":time_to, "room":room}
    })
    resp = await fetch("/api/update_from_json", {
        method: "POST",
        body: JSON.stringify(toSend),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    if (resp.ok) {
        showFlashAlert('Data úspěšně uložena', category='success')
    }
    else {
        alert('Ukládání dat selhalo', category='error')
    }
    modifiedItemUids = []
}

/** funkce na updatovani doby trvani v item details na zaklade hodnot time inputu */
function updateAllItemLengths() {
    itemDetailsEles = document.querySelectorAll('.details')
    itemDetailsEles.forEach(ele => {
        let timeFromInput = ele.querySelector('.time-from-input')
        let timeToInput = ele.querySelector('.time-to-input')
        let lengthEle = ele.querySelector('.item-length')
        let timeFrom = timeFromInput.value
        let timeTo = timeToInput.value
        let differenceMs = getTimeDifferenceInMs(timeFrom, timeTo)
        let timeDifference = msToTimeString(differenceMs)
        lengthEle.innerHTML = timeDifference
    })
}

/** funkce co z casu v ms udela cas ve formatu HH:MM */
function msToTimeString(ms) {
    ms = ms%86400000
    let totalSeconds = Math.floor(ms / 1000);
    let totalMinutes = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;
    let hours = Math.floor(totalMinutes / 60);
    let minutes = totalMinutes % 60;
    let formattedHours = String(hours).padStart(2, '0');
    let formattedMinutes = String(minutes).padStart(2, '0');
    return `${formattedHours}:${formattedMinutes}`;
}

/** funkce co z casu ve formatu HH:MM vypocita milisekundy */
function timeStringToMs(time) {
    const [hours, minutes] = time.split(":").map(Number);
    return (hours * 3600 + minutes * 60) * 1000;
}

function getTimeDifferenceInMs(time1, time2) { // input jsou stringy ve formatu "%H:%M"
    let time1Obj = new Date("01/01/2007 " + time1).getTime()
    let time2Obj = new Date("01/01/2007 " + time2).getTime()
    return time2Obj - time1Obj
}

let timeFromInputs = document.querySelectorAll('.time-from-input')
timeFromInputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid)
        newStartTime = e.target.value

        prevStartTime = programItem.getAttribute('start-time')
        diff = getTimeDifferenceInMs(newStartTime, prevStartTime)
        let timeEnd = programItem.getAttribute('end-time')
        let timeEndMs = timeStringToMs(timeEnd)
        let newEndTime = msToTimeString(timeEndMs - diff)
        
        programItem.setAttribute('end-time', newEndTime)
        programItem.setAttribute('start-time', newStartTime)
        updateAllTimeInputs()
        updateAllItemsPosition()
        modifiedItemUids.push(programItem.id)
    })
})

let timeToInputs = document.querySelectorAll('.time-to-input')
timeToInputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid) 
        programItem.setAttribute('end-time', e.target.value)
        updateAllItemsPosition()
        updateAllItemLengths()
        modifiedItemUids.push(programItem.id)
    })
})

updateAllItemsPosition()
updateAllTimeInputs()
updateAllItemLengths()

let modifiedItemUids = [];

document.addEventListener('DOMContentLoaded', function() {
    var grid = document.querySelector('.program-container');
    var gridWidth = grid.offsetWidth;
    var columnWidth = gridWidth / 390;
    var rowHeight = 69; // vyska jednoho radku v px + 5px
  
    var items = document.querySelectorAll('.program-item');
    items.forEach(function(item) {
        item.addEventListener('mousedown', function(event) {
            row = parseInt(item.style.gridRowStart)-1
            column = parseInt(item.style.gridColumn.split('/')[0])

            var offsetX = event.clientX;
            var offsetY = row*rowHeight

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
    
            function onMouseMove(event) {
                var left = event.clientX - offsetX;
                var top = event.clientY - grid.getBoundingClientRect().top - offsetY;
        
                left = Math.round(left / columnWidth) * columnWidth;
                top = Math.round(top / rowHeight) * rowHeight;
        
                item.style.left = left + 'px';
                item.style.top = top + 'px';
            }
    
            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                if (!(item.style.left && item.style.top)) {return}
                let column_start = parseInt(item.style.gridColumn.split('/')[0])
                let column_end = parseInt(item.style.gridColumn.split('/')[1])

                column_start += Math.round(parseInt(item.style.left)/columnWidth)
                column_end += Math.round(parseInt(item.style.left)/columnWidth)
                if (!(column_start<0 || column_end<1)) {
                    item.style.gridColumn = String(column_start) + '/' + String(column_end)
                }
                item.style.left = 0
                if (item.style.gridColumnEnd > 391) {
                    item.style.borderRight = '4px solid black'
                } else {item.style.borderRight = ''}

                let row_start = parseInt(item.style.gridRowStart)
                row_start += Math.round((parseInt(item.style.top)-30)/rowHeight)
                nRows = document.querySelectorAll('.room').length
                if (!(row_start<2 || row_start>nRows+1)) {
                    item.style.gridRowStart = String(row_start)
                }
                item.style.top = 0
                updatteAllItemTimesAndRooms()
                updateAllTimeInputs()
                updateAllItemDetailsRooms()
                if (!(modifiedItemUids.includes(item.id))) {
                    modifiedItemUids.push(item.id)
                }
            }
        });
    });
});

window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
});