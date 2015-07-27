var cards = {};
var boardInitialized = false;
var nickname = {name : "default"}
var create_colour = 'blue';

$(document).ready( function(){
    $(".sticky-colour").click(function() {
        create_colour = $(this).attr('colour');
    });

    $("#board-screen-shot").click(function() {
		screenshot('.target_screen');
	});
});


//var socket = io.connect();
var socket = new WebSocket("ws://" + location.host + "/websocket");

function sendAction(a, d) {
    var message = {
        action: a,
        data: d
    };

    socket.send(JSON.stringify(message));
}

socket.onopen = function() {
    var path = location.pathname;
    sendAction('joinRoom', path);
};

socket.onclose = function() {
    blockUI("Server disconnected. Refresh page to try and reconnect...");
};

socket.onmessage = function(data) {
    getMessage(data);
};

function unblockUI() {
    $.unblockUI({fadeOut: 50});
}

function blockUI(message) {
    message = message || 'Waiting...';

    $.blockUI({
        message: message,

        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: 0.5,
            color: '#fff',
            fontSize: '20px'
        },

        fadeOut: 0,
        fadeIn: 10
    });
}

//respond to an action event
function getMessage(m) {
    var message = JSON.parse(m.data);
    var action = message.action;
    var data = message.data;
    console.log('action: ' + action);
    console.log('data  : ');
    console.log(data);

    switch (action) {
        case 'chat':
            $("#chat_div").chatbox("option", "boxManager").addMsg(data.name, data['body']);
            break;

        case 'chatMessages':
            nickname.name = data.name;
            for (var i = 0; i < data.cache.length; i++){
                $("#chat_div").chatbox("option", "boxManager").addMsg(data.cache[i].name, data.cache[i].body);
            }
            break;

        case 'roomAccept':
            sendAction('initializeMe', null);
            break;

        case 'moveCard':
            moveCard($("#" + data.id), data.position);
            break;

        case 'initCards':
            initCards(data);
            break;

        case 'createCard':
            drawNewCard(data.id, data.text, data.x, data.y, data.rot, data.colour, null, data.vote_count);
            break;

        case 'deleteCard':
            $("#" + data.id).fadeOut(500,
                function() {
                    $(this).remove();
                }
            );
            break;

        case 'editCard':
            content =  $("#" + data.id).children('.card-content').children('.content');
            content.text(data.value);
            break;

        case 'voteUp':
            $('#' + data.id + ' .vote-count').html('+' + (parseInt($('#' + data.id + ' .vote-count').html()) + 1));
            break;

        case 'voteDown':
            $('#' + data.id + ' .vote-count').html('+' + (parseInt($('#' + data.id + ' .vote-count').html()) - 1));
            break;

        case 'advice':
        Lobibox.notify('info', {
               msg: data['sent'],
               title: 'ちょっと一言',
               img: "{{ static_url('images/avatar.png') }}",
               position: 'bottom left',
               delay: 5000,
               sound: false
               }
            );
            break;

        case 'countUser':
        	$(".count-user").text('現在の参加人数は'+data+'人です');
            break;

        case 'getMember':
            $('#member_div').html("参加者： "+data);
            break;

        default:
            //unknown message
            alert('unknown action: ' + JSON.stringify(message));
            break;
    }

}

function drawNewCard(id, text, x, y, rot, colour, sticker, vote_count, animationspeed) {

    var template = '<div id={id} class="card {colour}" style="width:250px;position:absolute;">' +
                       '<div class="card-content white-text">' +
                          '<p class="content black-text">{text}</p>' +
                       '</div>' +
                       '<div class="card-action">' +
                           '<a href="#" class="thumb-up"><i class="material-icons">thumb_up</i></a>' +
                           '<a href="#" class="delete-card">DEL</a>' +
                       '</div>' +
                   '</div>';
    var h = '';
    template = template.replace('{id}', id);
    template = template.replace('{colour}', colour);
    template = template.replace('{text}', text);
    h = template;

    var card = $(h);
    card.appendTo('.boundary');

    card.draggable({
        snap: false,
        snapTolerance: 5,
        containment: '.boundary',
        scroll: false,
        stack: ".card",
		handle: "div.card-content",
    });

    //After a drag:
    card.bind("dragstop", function(event, ui) {

        var data = {
            id: this.id,
            position: ui.position,
            oldposition: ui.originalPosition,
        };

        sendAction('moveCard', data);
    });


    var speed = Math.floor(Math.random() * 1000);
    if (typeof(animationspeed) != 'undefined') speed = animationspeed;

    var startPosition = $(".boundary").position();

    card.css('top', startPosition.top - card.height() * 0.5);
    card.css('left', startPosition.left - card.width() * 0.5);

    card.animate({
        left: x + "px",
        top: y + "px"
    }, speed);

   var zindex;

    card.hover(
        function() {
            $(this).addClass('hover');
            $(this).children('.card-icon').fadeIn(10);
            zindex = $(this).css('z-index');
            $(this).css('z-index', 10000);

        },
        function() {
            $(this).removeClass('hover');
            $(this).children('.card-icon').fadeOut(150);
            $(this).css('z-index', zindex);
        }
    );

    card.children('.card-icon').hover(
        function() {
            $(this).addClass('card-icon-hover');
        },
        function() {
            $(this).removeClass('card-icon-hover');
        }
    );

    card.children('.card-action').children('.delete-card').click(
        function() {
            $("#" + id).remove();
            sendAction('deleteCard', {
                'id': id
            });
        }
    );

    card.children('.card-action').children('.thumb-up').click(
        function() {
            console.log(parseInt($('#' + id + ' .vote-count').html()));
            sendAction('voteUp', {
                'id': id
            });
        }
    );

    card.children('.card-content').children('.content').editable(function(value, settings) {
        onCardChange(id, value);
        return ("");
        //return (value);
    }, {
        type: 'textarea',
        submit: 'OK',
        style: 'inherit',
        cssclass: 'card-edit-form',
        placeholder: 'Double Click to Edit.',
        onblur: 'submit',
        event: 'dblclick', //event: 'mouseover'
    });

}

// Chat get new message
function newMessage(msg, name) {
    var data = {body: msg, name: name}
    sendAction('chat', data);
}

function onCardChange(id, text) {
    sendAction('editCard', {
        id: id,
        value: text
    });
}

function moveCard(card, position) {
    card.animate({
        left: position.left + "px",
        top: position.top + "px"
    }, 500);
}


//----------------------------------
// cards
//----------------------------------
function createCard(id, text, x, y, rot, colour, vote_count) {
    var action = "createCard";
    var data = {
        id: id,
        text: text,
        x: x,
        y: y,
        rot: rot,
        colour: colour,
        vote_count: vote_count
    };

    sendAction(action, data);
}

function initCards(cardArray) {
    //first delete any cards that exist
    $('.card').remove();

    cards = cardArray;

    for (var i in cardArray) {
        card = cardArray[i];

        drawNewCard(
            card.id,
            card.text,
            card.x,
            card.y,
            card.rot,
            card.colour,
            card.sticker,
            card.vote_count,
            0
        );
    }

    boardInitialized = true;
    unblockUI();
}


function kakunin() {
    var uniqueID = Math.round(Math.random() * 99999999); //is this big enough to assure uniqueness?

    createCard('card' + uniqueID,
               $('#idea-input').val(), // text
               58, 100,//$('div.board-outline').height(), // hack - not a great way to get the new card coordinates, but most consistant ATM
               0, // rotation,
               create_colour,
               0); //vote count
};



$(function() {

    if (boardInitialized === false)
        blockUI('<img src="images/ajax-loader.gif" width=43 height=11/>');

});


function screenshot( selector) {
    var element = $(selector)[0];
    html2canvas(element, { onrendered: function(canvas) {
        date = new Date(jQuery.now()).toLocaleString();
        if (canvas.msToBlob) { //for IE
            var blob = canvas.msToBlob();
            window.navigator.msSaveBlob(blob, "Brain_Hacker" + date + ".png");
        } else {
        	var imgData = canvas.toDataURL();
	        var a = document.createElement('a');
	        a.href = imgData;
	        a.download = "Brain_Hacker" + date + ".png";
	        document.body.appendChild(a);
	        a.click();
	        a.remove();
        }
    }});
}