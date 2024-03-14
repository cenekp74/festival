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

// vypocita z minut od 1 do 360 cas od 8:00 do 14:00
function convertMinutesToTime(minutes) {
    if (minutes == 0) return "08:00"
    if (minutes < 1 || minutes > 360) {
        return;
    }
    let hours = Math.floor(minutes / 60);
    let mins = minutes % 60;
    hours += 8;
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

function updateAllTimeInputs() { /* funkce na updatovani vsech inputu casu v item detailech podle properties jednotlivych itemu v programu */
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
        if (item.style.visibility == 'hidden') {return};
        let item_id = item.getAttribute('item-id');
        let itemDetails = document.getElementById('details-'+item_id);
        itemDetails.querySelector('.time-from-input').value = item.getAttribute('start-time')
        itemDetails.querySelector('.time-to-input').value = item.getAttribute('end-time')
    })
}

function updateAllItemsPosition() { /* funkce na updatovani polohy v grid u vsech itemu na zaklade jejich start-time a end-time atributu */
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
}

function updatteAllItemTimesAndRooms() { // funkce na updatovani start-time, end-time a room attributu u vsech itemu na zaklade jejich grid stylingu (grid-column a grid-row-start)
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

function updateAllItemDetailsRooms() { // funkce na updatovani mistnosti v item details na zaklade atributu room u itemu
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
        if (item.style.visibility == 'hidden') {return};
        let item_id = item.getAttribute('item-id');
        let itemDetails = document.getElementById('details-'+item_id);
        itemDetails.querySelector('.item-details-room').innerHTML = item.getAttribute('room')
    })
}

let timeFromInputs = document.querySelectorAll('.time-from-input')
timeFromInputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid) 
        programItem.setAttribute('start-time', e.target.value)
        updateAllItemsPosition()
    })
})

let timeToInputs = document.querySelectorAll('.time-to-input')
timeToInputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid) 
        programItem.setAttribute('end-time', e.target.value)
        updateAllItemsPosition()
    })
})

updateAllItemsPosition()
updateAllTimeInputs()

document.addEventListener('DOMContentLoaded', function() {
    var grid = document.querySelector('.program-container');
    var gridWidth = grid.offsetWidth;
    var columnWidth = gridWidth / 360;
    var rowHeight = 53;
  
    var items = document.querySelectorAll('.program-item');
    items.forEach(function(item) {
        item.addEventListener('mousedown', function(event) {
            row = parseInt(item.style.gridRowStart)-1
            column = parseInt(item.style.gridColumn.split('/')[0])

            var offsetX = event.clientX;
            var offsetY = row*53 /* 30 je vyska radku s casem + gap */

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
                if (!(column_start<0 || column_end<1 || column_end > 361)) {
                    item.style.gridColumn = String(column_start) + '/' + String(column_end)
                }
                item.style.left = 0

                let row_start = parseInt(item.style.gridRowStart)
                row_start += Math.round((parseInt(item.style.top)-30)/53+1)
                nRows = document.querySelectorAll('.room').length
                if (!(row_start<0 || row_start>nRows+1)) {
                    item.style.gridRowStart = String(row_start)
                }
                item.style.top = 0
                updatteAllItemTimesAndRooms()
                updateAllTimeInputs()
                updateAllItemDetailsRooms()
            }
        });
    });
});