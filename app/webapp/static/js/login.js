let form = $("#form");
form.on('submit', function(e) {
    e.preventDefault();
    //console.log(form.attr('action'));
    fetch(form.attr('action'),{
        method: form.attr('method'),
        body: new URLSearchParams(new FormData(form[0]))
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status == "ok") {
            console.log("OK")
            sessionStorage.setItem("LN-USERNAME", data.user);
            location.href = "/";
        }else if (data.status == "error") {
            alert(data.reason);
        }
        
    });
});