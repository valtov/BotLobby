document.addEventListener("DOMContentLoaded", (event) => {
    console.log(window.localStorage.getItem("sso") || '')
    console.log(window.localStorage.getItem("username") || '')    
    console.log(window.localStorage.getItem("platform") || '')
    restoreForm()

    var button = document.getElementById("submitButton");
    button.addEventListener("click", (e) => {
        storeForm()
    });

    // var arr = dropdown.getElementsByTagName("li");
    // console.log(arr)
    // for (var i = 0; i < arr.length; i++) {
    //     console.log(arr[i].children[0].text)
    //     arr[i].children[0].addEventListener("click", function() {
    //         console.log(this);
    //         var button = document.getElementById("dropdown-button");
    //         button.innerText = this.text
    //     });
    // }
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