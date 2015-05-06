/**
 * Created by Vince Maiuri on 5/4/2015.
 */

/***************Pong Game JS****************************/
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
        sendMessage("/open", {"player": player});
    };

    onMessage = function (message) {
        //TODO finish stub
        return message;
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

        $.post(path,  data,  "json");
    };

    return {
        "open": open,
        "sendMessage": sendMessage
    };
}());

$(document).ready(function () {
    "use strict";
    var userName = window.prompt("User name: ");

    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        url: "/connect",
        method: "GET",
        data: {"userName": userName},
        dataType: "json",
        success: function (data) {
            connector.open(data);
        }
    });
});

