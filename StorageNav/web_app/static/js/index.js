
function sendRequest(method, params, callback) {
    let session = new XMLHttpRequest();
    session.withCredentials = true;

    session.onerror = function() {
        alert("Connection error")
    }

    params_string = '?'
    for ([name, value] of Object.entries(params)) params_string += `${name}=${encodeURIComponent(value)}&`
    session.open("POST", "/api/v1" + method + params_string, true)
    session.onload = function() {
        if (session.status != 200) {console.log(`status code: ${session.status}`); return}
        if (callback) callback(JSON.parse(session.responseText))}
    session.send()
}

Telegram.WebApp.onEvent('backButtonClicked', function() {
    sendRequest("/logout", {}, none)
})

sendRequest(
    "/login",
    {"hash_string": window.Telegram.WebApp.initDataUnsafe.hash, "data": window.Telegram.WebApp.initData},
    function(resp) {
        console.log(resp)
        document.getElementById("test").style = ""
        document.getElementById("test_1").innerHTML = JSON.stringify(resp)
        document.querySelector(".loading-block").style = "display: none"
        if (resp.status == "ok") {
            sendRequest(
                "/test", {}, function(resp) {
                    document.getElementById("test_2").innerHTML = JSON.stringify(resp)
                }
            )
        }
    }
)
