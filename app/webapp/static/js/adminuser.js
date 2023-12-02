function form2Json(form) {
    const formData = new FormData(form)
    const userData = {}
    formData.forEach((value, key) => userData[key] = value)
    return userData
}

function updateUser(userData) {
    fetch("/api/users", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    }).then(res => res.json())
    .then(res => {
        if(res.status == "OK") {
            location.href = "/admin"
        }else {
            alert(res.message)
        }
    })
}

function createUser(userData) {
    fetch("/api/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    }).then(res => res.json())
    .then(res => {
        if(res.status == "OK") {
            alert(res.message);
            location.href = "/admin";
        }else {
            alert(res.message);
        }
    })
}


