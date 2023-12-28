function dateChangedAction(monthIndex, year) {

    let params = `?month=${monthIndex+1}&year=${year}`;
    let url = `${params}`;

    window.location.href = url;    
}

function previousMonthListener() {
    let monthIndex = document.getElementById("monthInput").selectedIndex;
    console.log(monthIndex);
    let year = document.getElementById("yearInput").value;

    if (monthIndex == 0) {
        monthIndex = 11;
        year--;
    } else {
        monthIndex--;
    }

    document.getElementById("monthInput").selectedIndex = monthIndex;
    document.getElementById("yearInput").value = year;

    dateChangedAction(monthIndex, year);
}

function nextMonthListener() {
    let monthIndex = document.getElementById("monthInput").selectedIndex;
    let year = document.getElementById("yearInput").value;

    if (monthIndex == 11) {
        monthIndex = 0;
        year++;
    } else {
        monthIndex++;
    }

    document.getElementById("monthInput").selectedIndex = monthIndex;
    document.getElementById("yearInput").value = year;

    dateChangedAction(monthIndex, year);
}
    
function init() {
    document.getElementById("nextMonth").addEventListener("click", nextMonthListener);
    document.getElementById("prevMonth").addEventListener("click", previousMonthListener);
    
}
                
window.onload = init();