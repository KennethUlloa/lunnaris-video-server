function requestData(callback) {
    fetch('api/media')
    .then(response => response.json())
    .then(data => callback(data));
}

function loadPosters(data) {
    data.forEach(element => {
        $("#content-pane").append(poster(element));
        //document.querySelector("#content-pane").innerHTML += poster(element);
    }); 
}

requestData(loadPosters);

$('#close-button').click(function () {
    hideTopLayer();
});