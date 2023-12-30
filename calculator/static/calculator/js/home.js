function dateChangedAction(monthIndex, year) {

    let params = `?month=${monthIndex+1}&year=${year}`;

    window.location.href = params;    
}

function monthYearListener() {
    dateChangedAction(
        document.getElementById("monthInput").selectedIndex,
        document.getElementById("yearInput").value
    );
}

function registerUndelivered(day) {
    const statusElement = document.getElementById("registerStatus");
    const CSRFToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const cell = document.getElementById(day);
    const url = cell.classList.contains("undelivered") ? "/unregister-undelivered-date/" : "/register-undelivered-date/";


    requestData = {
        method: "POST",
        body: JSON.stringify({
            day: day,
            month: currentMonth,
            year: currentYear,
            paper: currentPaperID
        }),
        headers: {
            "X-CSRFToken": CSRFToken,
        },
        timeout: 5000,
    };

    fetch(url, requestData)
    .then(response => {
        console.log(response);
        if (!response.ok) {
            throw new Error("Network response was not OK");
        }
        return response;
    })
    .then(data => {
        statusElement.innerHTML = `Successfully updated date ${day}`;
        statusElement.classList.add("success");
        setTimeout(() => {
            statusElement.innerHTML = "";
        }, 2000);
        updateCalculatedCosts();
        cell.classList.toggle("undelivered");
    })
    .catch(error => {
        console.log(error);
        statusElement.innerHTML = "Error updating date";
        statusElement.classList.add("error");
        setTimeout(() => {
            statusElement.innerHTML = "";
        }, 5000);
    });
}

function copyToClipboard() {
    const url = `/get-calculated-string/?month=${currentMonth}&year=${currentYear}`;
    const statusElement = document.getElementById("copySaveStatus");

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not OK");
        }
        return response.text();
    })
    .then(data => {
        navigator.clipboard.writeText(data);
        statusElement.innerHTML = "Copied to clipboard";
        statusElement.classList.add("success");
        setTimeout(() => {
            statusElement.innerHTML = "";
        }, 2000);
    })
    
}

function getUpdatedCalculatedCosts() {
    const url = `/get-calculated-costs/?month=${currentMonth}&year=${currentYear}`;

    return fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not OK");
        }
        return response.json();
    })
}

function updateCalculatedCosts() {
    
    getUpdatedCalculatedCosts().then(data => {
        console.log(data);
        for (let paper in data["costs"]) {
            document.getElementById(`${paper}calculatedCost`).innerHTML = data["costs"][paper];
        }
        document.getElementById("calculatedTotalCost").innerHTML = data["total_cost"];
    })
    .catch(error => {
        console.log(error);
    });
}

    
function init() {
    document.getElementById("monthInput").addEventListener("change", monthYearListener);
    document.getElementById("yearInput").addEventListener("change", monthYearListener);
}
                
window.onload = init();