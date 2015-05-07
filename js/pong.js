/**
 * Created by Vince Maiuri on 5/4/2015.
 */

/***************Pong Game JS****************************/
var gameUpdate = (function () {
    "use strict";
    var myPlayer, otherPlayer, parseMessage, getMyPlayer, getOtherPlayer;

    myPlayer = {};
    otherPlayer = {};

    parseMessage = function (msg) {
        switch (msg.state) {
        case 'in-game':
            myPlayer.side = msg.side;
            myPlayer.numPlayer = msg.player_num;
            break;
        }
    };

    getMyPlayer = function () {
        return myPlayer;
    };

    getOtherPlayer = function () {
        return otherPlayer;
    };

    return {
        'parseMessage': parseMessage,
        'getMyPlayer': getMyPlayer,
        'getOtherPlayer': getOtherPlayer
    };
}());

var connector = (function () {
    "use strict";
    var onOpen, onMessage, onError, onClose, sendMessage,
        open, channel, socket, player;

    open = function (player_input) {
        player = player_input;
        //noinspection JSUnresolvedFunction
        channel = new goog.appengine.Channel(player.token);
        socket = channel.open();
        socket.onopen = onOpen;
        socket.onclose = onClose;
        socket.onerror = onError;
        socket.onmessage = onMessage;
    };

    onOpen = function () {
        //var playerString = JSON.stringify(player);
        var data = {
            "player_info": JSON.stringify(player)
        };
        sendMessage("/open", data);
    };

    onMessage = function (message) {
        gameUpdate.parseMessage(message);
    };

    onError = function () {
        //TODO finish stub
        return null;
    };

    onClose = function () {
        //TODO finish stub
        return null;
    };

    sendMessage = function (path, data) {
        data = data || {};

        $.post(path,  data);
    };

    return {
        "open": open,
        "sendMessage": sendMessage
    };
}());

$(document).ready(function () {
    "use strict";
    var playerName, gameId;
    playerName = $("#display_name").text();
    gameId = $("#game_id").find("p").text();
    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        url: "/connect",
        method: "GET",
        data: {
            "playerName": playerName,
            "gameId": gameId
        },
        dataType: "json",
        success: function (data) {
            connector.open(data);
        }
    });
});

