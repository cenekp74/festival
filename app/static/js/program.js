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

var items = document.getElementsByClassName('program-item');
for (var i = 0; i < items.length; i++) {
    var start_time = items[i].getAttribute('start-time');
    var end_time = items[i].getAttribute('end-time');
    var minutesFromStart = calculateMinutesFromStart(start_time, end_time);
    if (minutesFromStart.start == 0) {minutesFromStart.start = 1;}
    items[i].style.gridColumnStart = minutesFromStart.start;
    items[i].style.gridColumnEnd = minutesFromStart.end;
}

function updateTimeVerticalLine() {
    const root = document.querySelector(":root");
    var minutes = getMinutesFrom8am()
    if (minutes < 0 | minutes > 360) {
        root.style.setProperty("--vline-visibility", "hidden");
        return
    }
    root.style.setProperty("--vline-visibility", "visible");
    root.style.setProperty("--vline-left", String(100-minutes/100)+"%");
}

const mediaQuery = window.matchMedia('(max-width: 410px)');
if (mediaQuery.matches) {
    var items = document.getElementsByClassName('time-item');
    for (var i = 0; i < items.length; i++) {
        items[i].innerHTML = items[i].innerHTML.split(':')[0]
    }
}

updateTimeVerticalLine()
setInterval(updateTimeVerticalLine, 60*1000)