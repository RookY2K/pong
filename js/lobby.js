/**
 * Created by Vince Maiuri on 5/5/2015.
 */

$(document).ready(function () {
    "use strict";
    var getLobbyStatus, enterGame, stopPolling = false;

    enterGame = function (that, playerName) {
        var id = $(that).find(".game_button").prop("id");
        $.ajax({
            url: "/",
            success: function (json) {
                if (json.open) {
                    $(location).attr("href",
                        "/pong?playerName=" + playerName +
                        "&gameId=" + id
                        );
                } else {
                    window.alert("Sorry, that game is full!");
                    stopPolling = false;
                    getLobbyStatus();
                }
            },
            data: {
                "gameId": id,
                "playerName": playerName
            },
            dataType: "json",
            method: "POST"
        });
    };

    $("a.lobby_link").click(function (evt) {
        var playerName = $("#display_name").text();
        stopPolling = true;
        evt.preventDefault();
        enterGame(this, playerName);
    });

    getLobbyStatus = function () {
        $.ajax({
            url: "/lobby-update",
            success: function (html) {
                $(".game_button").each(function () {
                    var id, gameLobby, button;
                    button = $(this);
                    id = button.prop("id");
                    gameLobby = $("#" + id, html);
                    button.html(gameLobby);
                });
            },
            dataType: "html",
            method: "GET"
        });
        if (!stopPolling) {
            setTimeout(getLobbyStatus, 1000);
        }
    };

    getLobbyStatus();

});
