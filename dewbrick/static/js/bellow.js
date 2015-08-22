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
        //doSend("WebSocket rocks");
    }

    function onClose(evt) {
    }

    function onMessage(evt) {
        card = JSON.parse(evt.data);
        for (key in card.attributes) {
            if (card.turn){
                // <a href="#">agility: 1</a>
                $( "#jumboTurn").html("Your turn");
                $( "#" + card.attributes[key].name ).html('<a href="#">' + card.attributes[key].name + ':' + card.attributes[key].value + "</a>");
            } else {
                $( "#jumboTurn").html("Their turn");
                $( "#" + card.attributes[key].name ).html(card.attributes[key].name + ':' + card.attributes[key].value) ;
            }
        }

        console.log(evt.data)
    }

    function onError(evt) { writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data); }

    function doSend(message) { websocket.send(message); }

    $('.card_attr').click(function(e) {

        console.log($(this).attr('id'));
        doSend($(this).attr('id'));
    });

});
