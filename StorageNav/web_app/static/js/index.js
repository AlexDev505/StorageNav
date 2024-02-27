
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

hideLoadingBlock()
showMainBlock()

//sendRequest(
//    "/login",
//    {"hash_string": window.Telegram.WebApp.initDataUnsafe.hash, "data": window.Telegram.WebApp.initData},
//    function(resp) {
//        hideLoadingBlock()
//        if (resp.status == "ok") showMainBlock()
//        else showCloseAppBtnBlock(resp.message + "\ntry again latter...")
//    }
//)

function hideLoadingBlock() {
    document.getElementById("loading-block").style = "display: none"
}
function showMainBlock() {
    document.getElementById("main-block").style = ""
}
function showCloseAppBtnBlock(message) {
    document.getElementById("close-app-btn-block").style = ""
    document.getElementById("close-message").innerHTML = message
}


let map_scale = 1
function scaleUpMap() {
    if (map_scale > 1.9) return
    map_scale += 0.1
    applyScaleMap(1)
}
function scaleLowMap() {
    if (map_scale < 0.6) return
    map_scale -= 0.1
    applyScaleMap(-1)
}
function applyScaleMap(delta) {
    map = document.getElementById("map")
    map_block = document.getElementById("map-block")
    if (map_scale > 1 || (map_scale == 1 & delta == -1)) {
        map.style = `transform: scale(${map_scale});
            top: ${1000 * (map_scale - 1) / 2}px;
            left: ${1000 * (map_scale - 1) / 2}px`
        map_block.scroll({
          top: map_block.scrollTop + 25 * delta,
          left: map_block.scrollLeft + 25 * delta,
        });
    } else {
        map.style = `transform: scale(${map_scale});
            top: ${1000 * Math.abs(map_scale - 1) / 4}px;
            left: ${1000 * Math.abs(map_scale - 1) / 4}px`
        map_block.scroll({
          top: map_block.scrollTop - 75 * delta,
          left: map_block.scrollLeft - 75 * delta,
        });
    }
}


//let handle_move = false
//let last_touches = []
//let last_dist = 0
//let map_scale = 1
//document.getElementById("map").addEventListener('touchstart', function(e) {
//    handle_move = (e.touches.length == 2)
//    if (handle_move) {
//        last_touches = [
//            [e.touches[0].pageX, e.touches[0].pageY],
//            [e.touches[1].pageX, e.touches[1].pageY]
//        ]
//        last_dist = Math.hypot(
//            e.touches[0].pageX - e.touches[1].pageX,
//            e.touches[0].pageY - e.touches[1].pageY
//        )
//        document.getElementById("test").innerHTML = `start`
//    }
//}, false);
//document.getElementById("map").addEventListener('touchend', function(e) {
//    handle_move = (e.touches.length == 2)
//}, false);
//document.getElementById("map").addEventListener('touchmove', function(e) {
//    if (!handle_move) return
//    document.getElementById("test").innerHTML = `move`
//    last_touches = [
//        [e.touches[0].pageX, e.touches[0].pageY],
//        [e.touches[1].pageX, e.touches[1].pageY]
//    ]
//    dist = Math.hypot(
//        e.touches[0].pageX - e.touches[1].pageX,
//        e.touches[0].pageY - e.touches[1].pageY
//    )
//    if (dist < last_dist) {
//        map_scale -= 0.05
//    } else {
//        map_scale += 0.05
//    }
//    last_dist = dist
//}, false);
