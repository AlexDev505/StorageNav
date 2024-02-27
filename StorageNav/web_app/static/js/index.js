
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
    applyScaleMap(0.1)
}
function scaleLowMap() {
    if (map_scale < 0.6) return
    applyScaleMap(-0.1)
}
function applyScaleMap(delta) {
    if (map_scale + delta > 2 || map_scale + delta < 0.5) return
    map_scale += delta
    delta_sign = delta / Math.abs(delta)

    map = document.getElementById("map")
    map_block = document.getElementById("map-block")
    if (map_scale > 1 || (map_scale == 1 & delta < 0)) {
        map.style = `transform: scale(${map_scale});
            top: ${1000 * (map_scale - 1) / 2}px;
            left: ${1000 * (map_scale - 1) / 2}px`
        map_block.scroll({
          top: map_block.scrollTop + (1000 * delta / 4),
          left: map_block.scrollLeft + (1000 * delta / 4),
        });
    } else {
        map.style = `transform: scale(${map_scale});
            top: ${1000 * Math.abs(map_scale - 1) / 4}px;
            left: ${1000 * Math.abs(map_scale - 1) / 4}px`
        map_block.scroll({
          top: map_block.scrollTop - (1000 * delta / 4 * 3),
          left: map_block.scrollLeft - (1000 * delta / 4 * 3),
        });
    }
}


let handle_move = false
let last_dist = 0
document.getElementById("map").addEventListener('touchstart', function(e) {
    handle_move = (e.touches.length == 2)
    if (handle_move) {
        last_dist = Math.hypot(
            e.touches[0].pageX - e.touches[1].pageX,
            e.touches[0].pageY - e.touches[1].pageY
        )
        document.getElementById("map-block").style = "overflow: hidden;"
    }
}, false);
document.getElementById("map").addEventListener('touchend', function(e) {
    handle_move = false
    document.getElementById("map-block").style = ""
}, false);
document.getElementById("map").addEventListener('touchmove', function(e) {
    if (!handle_move) return
    dist = Math.hypot(
        e.touches[0].pageX - e.touches[1].pageX,
        e.touches[0].pageY - e.touches[1].pageY
    )
    if (dist < last_dist) {
        applyScaleMap(-0.01)
    } else {
        applyScaleMap(0.01)
    }
    last_dist = dist
}, false);
