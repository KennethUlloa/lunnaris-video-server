async function allMedia() {
    let resp = await fetch('api/media');
    return resp.json()
}

async function searchMedia(search, type = "movie") {
    let resp = await fetch(`api/media?search=${search}&type=${type}`);
    return resp.json()
}


function loadPosters(data) {
    data.forEach(element => {
        $("#content-pane").append(poster(element));
        //document.querySelector("#content-pane").innerHTML += poster(element);
    }); 
}

allMedia().then(data => loadPosters(data));

$('#close-button').click(function () {
    hideTopLayer();
});

window.onload = () => {
    //$("#user-name").text(sessionStorage.getItem("LN-USERNAME"));
    $("#search-bar").submit(function(e) {
        e.preventDefault();
        const values = new FormData(e.target)
        searchMedia(values.get("search")).then(data => {
            $("#content-pane").empty();
            if (data.length == 0) {
                alert("No se encontró")
            }else{
                loadPosters(data);
            }
            
        })
    })
    $("#login-btn").click(function() {
        fetch("/api/auth/logout",{method: 'post'})
        .then(response => response.json())
        .then(res => {
            if(res.status == "ok") {
                location.href = "/";
            }
        })
        ;
    });
}