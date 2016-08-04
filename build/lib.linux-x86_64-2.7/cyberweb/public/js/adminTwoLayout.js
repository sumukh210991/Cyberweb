function callURL(url, target) {
    $.get(url, function (data) {
        populateResponse(data,target);
    });
}

function populateResponse(data,target) {
    document.getElementById(target).innerHTML = data;
}