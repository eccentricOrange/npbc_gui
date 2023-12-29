function dateChangedAction(monthIndex, year) {

    let params = `?month=${monthIndex+1}&year=${year}`;

    window.location.href = params;    
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

function monthYearListener() {
    dateChangedAction(
        document.getElementById("monthInput").selectedIndex,
        document.getElementById("yearInput").value
    );
}

function selectPaper(paperId) {
    let monthIndex = document.getElementById("monthInput").selectedIndex;
    let year = document.getElementById("yearInput").value;

    let params = `?month=${monthIndex+1}&year=${year}&paper=${paperId}`;
    window.location.href = params;
}

    
function init() {
    document.getElementById("nextMonth").addEventListener("click", nextMonthListener);
    document.getElementById("prevMonth").addEventListener("click", previousMonthListener);
    
    document.getElementById("monthInput").addEventListener("change", monthYearListener);
    document.getElementById("yearInput").addEventListener("change", monthYearListener);
}
                
window.onload = init();