/**
 * Created by Vince Maiuri on 5/4/2015.
 */
var connector = function () {
    "use strict";
    var onOpen, onMessage, onError, onClose, sendMessage,
        open, channel, socket, playerName;

    open = function (token, name) {
        playerName = name;
        //noinspection JSUnresolvedFunction
        channel = new goog.appengine.Channel(token);
        socket = channel.open();
        socket.onopen = onOpen;
        socket.onclose = onClose;
        socket.onerror = onError;
        socket.onmessage = onMessage;
    };

    onOpen = function () {
        //TODO finish stub
        return null;
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
    }
};

$(document).ready(function () {
    "use strict";
    var userName = window.prompt("User name: ");

    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        url: "/connect",
        data: {"userName": userName},
        dataType: "json",
        success: function (data) {
            //TODO fill in stub
            return data;
        }
    });
});