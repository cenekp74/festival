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
}

function updateAllTimeInputs() { /* funkce na updatovani vsech inputu casu v item detailech podle properties jednotlivych itemu v programu */
    let programItems = document.querySelectorAll('.program-item')
    programItems.forEach(item => {
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
        if (minutesFromStart.start == 0) {minutesFromStart.start = 1;}
        items[i].style.gridColumnStart = minutesFromStart.start;
        items[i].style.gridColumnEnd = minutesFromStart.end;
        items[i].style.gridRowStart = rooms.indexOf(room)+2; //+2 je protoze index zacina od 0 a prvni row jsou casy
    }
}

let time_from_inputs = document.querySelectorAll('.time-from-input')
time_from_inputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid) 
        programItem.setAttribute('start-time', e.target.value)
        updateAllItemsPosition()
    })
})

let time_to_inputs = document.querySelectorAll('.time-to-input')
time_to_inputs.forEach(inputEle => {
    inputEle.addEventListener('input', (e) => {
        uid = e.target.closest('.details').id.split('-')[1]
        let programItem = document.getElementById(uid) 
        programItem.setAttribute('end-time', e.target.value)
        updateAllItemsPosition()
    })
})

updateAllItemsPosition()
updateAllTimeInputs()