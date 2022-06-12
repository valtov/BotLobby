document.addEventListener("DOMContentLoaded", (event) => {
    console.log(window.localStorage.getItem("sso") || '')
    console.log(window.localStorage.getItem("username") || '')    
    console.log(window.localStorage.getItem("platform") || '')
    restoreForm()

    var button = document.getElementById("submitButton");
    button.addEventListener("click", (e) => {
        storeForm()
    });

    var url_string = window.location.href;
    var url = new URL(url_string);
    var error = url.searchParams.get("error");
    if (error) {
        alert(error)
    }
});

function storeForm() {
    var sso = document.getElementById("ssoCookieInput")
    var username = document.getElementById("usernameInput")
    var platform = document.getElementById("platformInput")
    window.localStorage.setItem("sso", sso.value)
    window.localStorage.setItem("username", username.value)
    window.localStorage.setItem("platform", platform.value)
    console.log(sso.value)
    console.log(username.value)
    console.log(platform.value)
}

function restoreForm() {
    var sso = document.getElementById("ssoCookieInput")
    var username = document.getElementById("usernameInput")
    var platform = document.getElementById("platformInput")
    sso.value = window.localStorage.getItem("sso") || ''
    username.value = window.localStorage.getItem("username") || ''
    platform.value = window.localStorage.getItem("platform") || ''
}