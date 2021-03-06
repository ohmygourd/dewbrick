$(function() {
    console.log('loaded');
    // fill in later
    var wsUri = "ws://"+window.location.host+"/sockets";
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
        if (card.image) {
            var img = $('#monster-image');
            img.attr('src', card.image);
            img.attr('alt', card.name);
        }
        if (card.screenshot) {
            $('#screenshot').css('background-image', 'url('+card.screenshot+')');
        }
	$('#description').html(card.description);
        for (key in card.attributes) {
            if (card.turn){
                $( "#jumboTurn").html("Your turn");
                $( "#" + card.attributes[key].name ).html('<a href="#">' + card.attributes[key].name + ':' + card.attributes[key].value + "</a>");

            } else {
                $( "#jumboTurn").html("Their turn");
                $( "#" + card.attributes[key].name ).html(card.attributes[key].name + ':' + card.attributes[key].value) ;
            }
            $('#site-name').html(card.site);
            $('#card-name').html(card.name);
        }
        if (card.win !== undefined) {
            if (card.win) {
                $('#winner-msg').show();
                $('#loser-msg').hide();
		setTimeout(function() {$('#winner-msg').fadeOut(600);}, 1500);
            } else {
                $('#loser-msg').show();
                $('#winner-msg').hide();
		setTimeout(function() {$('#loser-msg').fadeOut(600);}, 1500);
            }
            $('#my-score').html(card.my_score);
            $('#opponent-score').html(card.opponent_score);
        }
        if (card.winner !== undefined) {
            if (card.winner) {
                $('#match-win').show();
            } else {
                $('#match-lose').show();
            }
            $('#score-label').html('Final scores:');
        }

        console.log(evt.data);
    }

    function onError(evt) { writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data); }

    function doSend(message) { websocket.send(message); }

    $('.card_attr').click(function(e) {
        e.preventDefault();

        console.log($(this).attr('id'));
        doSend($(this).attr('id'));
    });

});
