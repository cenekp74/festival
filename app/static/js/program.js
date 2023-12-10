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

updateTimeVerticalLine()
setInterval(updateTimeVerticalLine, 60*1000)