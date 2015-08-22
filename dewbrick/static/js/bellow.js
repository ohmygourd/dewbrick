$(function() {
    console.log('loaded');
    // fill in later
    var wsUri = "ws://localhost:8888/sockets";
    var output;
    function init() {
    output = document.getElementById("output");
    }

    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };

    function onOpen(evt) {
        doSend("WebSocket rocks");
    }

    function onClose(evt) {
    }

    function onMessage(evt) {
        console.log(evt.data)
    }

    function onError(evt) { writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data); }

    function doSend(message) { websocket.send(message); }

    $('.card_attr').click(function(e) {

        console.log($(this).attr('id'));
        doSend($(this).attr('id'));
    });

});
