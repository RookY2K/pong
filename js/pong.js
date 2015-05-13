/**
 * Created by Vince Maiuri on 5/4/2015.
 */

/***************Pong Game JS****************************/
var gameMath = (function () {
    "use strict";
    var fixed, pos, addVector, subtractVector,
        multiplyVectorByScalar, interpolation,
        vectorInterpolation;

    fixed = function (fix, n) {
        n = n || 3;
        return parseFloat(fix.toFixed(n));
    };

    pos = function (v1) {
        return {
            x: v1.x,
            y: v1.y
        };
    };

    addVector = function (v1, v2) {
        return {
            x: fixed(v1.x + v2.x),
            y: fixed(v1.y + v2.y)
        };
    };

    subtractVector = function (v1, v2) {
        return {
            x: fixed(v1.x - v2.x),
            y: fixed(v1.y - v2.y)
        };
    };

    multiplyVectorByScalar = function (v1, scal) {
        return {
            x: fixed(v1.x * scal),
            y: fixed(v1.y * scal)
        };
    };

    interpolation = function (prev, next, alpha) {
        var tAlpha = Number(alpha);
        tAlpha = fixed(Math.max(0, Math.min(1, tAlpha)));

        return fixed(prev + tAlpha * (next - prev));
    };

    vectorInterpolation = function (v1, v2, alpha) {
        return {
            x: interpolation(v1.x, v2.x, alpha),
            y: interpolation(v1.y, v2.y, alpha)
        };
    };

    return {
        "fixed": fixed,
        "pos": pos,
        "addVector": addVector,
        "subtractVector": subtractVector,
        "multiplyVectorByScalar": multiplyVectorByScalar,
        "vectorInterpolation": vectorInterpolation
    };
}());

var gameTimer = (function () {
    "use strict";
    var updateTimer,
        localTime = 0.016,
        timerStartDelta = Date.now(),
        timerEndDelta = Date.now(),
        getLocalTime;

    updateTimer = function () {
        timerStartDelta = Date.now() - timerEndDelta;
        timerEndDelta = Date.now();
        localTime += timerStartDelta / 1000.0;
        setTimeout(updateTimer, 4);
    };

    getLocalTime = function () {
        return localTime;
    };

    return {
        "getLocalTime": getLocalTime,
        "updateTimer": updateTimer
    };
}());

var pongComponents = (function () {
    "use strict";
    var ball, paddle, getPaddle, getBall,
        cvs = document.getElementById("canvas"),
        context = cvs.getContext("2d"),
        width = 800, height = 600, initCanvas;

    initCanvas = function () {
        cvs.width = width;
        cvs.height = height;
    };

    getPaddle = function (side) {
        var retPaddle = Object.create(paddle);

        retPaddle.pos = {
            x: side === "left" ? 10 : (width - retPaddle.width) - 10,
            y: height / 2 - retPaddle.height / 2
        };
        retPaddle.side = side;
        retPaddle.inputs = [];
        retPaddle.curState = {};
        retPaddle.oldState = {};
        retPaddle.oldState.pos = gameMath.pos(retPaddle.pos);
        retPaddle.curState.pos = gameMath.pos(retPaddle.pos);

        return retPaddle;
    };

    getBall = function () {
        return Object.create(ball);
    };

    ball = {
        x: width / 2,
        y: height / 2,
        radius: 5,
        color: "white",
        velX: 5,
        velY: 3,

        draw: function () {
            context.beginPath();
            context.fillStyle = this.color;
            context.arc(this.x,  this.y,  this.radius,  0, Math.PI * 2, false);
            context.fill();
        }
    };

    paddle = {
        width: 5,
        height: 150,
        playerSpeed: 200,
        color: "white",
        limits: {
            minY: 0,
            maxY: height - 150
        },

        draw: function () {
            context.fillStyle = this.color;
            context.fillRect(this.pos.x,  this.pos.y,  this.width, this.height);
        },

        processInputs: function () {
            var xDirection, yDirection, inputsLength, i, j,
                input, inputLength, key, result;

            xDirection = yDirection = 0;
            inputsLength = this.inputs.length;

            if (inputsLength) {
                for (i = 0; i < inputsLength; ++i) {
                    if (this.inputs[i].seq <= this.lastInputSeq) {
                        continue;
                    }

                    input = this.inputs[i].inputs;
                    inputLength = input.length;

                    for (j = 0; j < inputLength; ++j) {
                        key = input[j];
                        switch (key) {
                        case "up":
                            yDirection -= 1;
                            break;
                        case "down":
                            yDirection += 1;
                            break;
                        }
                    }
                }
            }

            result = {
                x: gameMath.fixed(xDirection * (this.playerSpeed * 0.015)),
                y: gameMath.fixed(yDirection * (this.playerSpeed * 0.015))
            };

            if (this.inputs.length) {
                this.lastInputSeq = this.inputs[inputsLength - 1].seq;
                this.inputs.splice(0, inputsLength);
            }

            return result;
        },

        checkCollision: function () {
            if (this.pos.y > this.limits.maxY) {
                this.pos.y = this.limits.maxY;
            }
            if (this.pos.y < this.limits.minY) {
                this.pos.y = this.limits.minY;
            }
        }
    };

    return {
        "getBall": getBall,
        "getPaddle": getPaddle,
        "initCanvas": initCanvas
    };
}());

var physics = (function () {
    "use strict";
    var delta = 0.0001,
        lastDelta = Date.now(),
        player,
        update,
        physicsEngine,
        getDelta,
        initPlayer;

    initPlayer = function (myPlayer) {
        player = myPlayer;
    };

    physicsEngine = function () {
        var vectorResult;
        player.paddle.oldState.pos = gameMath.pos(player.paddle.curState.pos);
        vectorResult = player.paddle.processInputs();
        player.paddle.curState.pos = gameMath.addVector(player.paddle.oldState.pos,  vectorResult);
        player.stateTime = gameTimer.getLocalTime();
    };

    update = function () {
        var start = Date.now();
        delta = (Date.now() - lastDelta) / 1000.0;
        lastDelta = Date.now();
        physicsEngine();
        setTimeout(update,  (15 - (Date.now() - start)));
    };

    getDelta = function () {
        return delta;
    };

    return {
        "getDelta": getDelta,
        "update": update,
        "initPlayer": initPlayer
    };
}());

var gameUpdate = (function () {
    "use strict";
    var myPlayer, otherPlayer, parseMessage, getMyPlayer, getOtherPlayer,
        gameId = $("#game_id").find("p").text(), delta, lastFrameTime,
        serverTime, update, up, down, animateId,
        cvs = document.getElementById("canvas"),
        context = cvs.getContext("2d"),
        height = 600, width = 800, inputSeq = 0, netOffset = 100,
        clientTime = 0.01, targetTime = 0.01, bufferSize = 2,
        serverUpdates = [], fps = 0, fps_avg_count = 0, fps_avg = 0,
        fps_avg_acc = 0,
        handleKeyBoardInputs, isUp, isDown, handleServerUpdates,
        updateLocalPos, refreshFPS, setPlayerName, getFPS,
        onServerUpdateReceived, processPredictionCorrection, cancelUpdate,
        onStart, onInGame;

    myPlayer = {};
    otherPlayer = {};

    handleKeyBoardInputs = function () {
        var input = [],
            data,
            packet = {};

        if (isUp) {
            input.push("up");
        }

        if (isDown) {
            input.push("down");
        }

        if (input.length) {
            inputSeq += 1;

            data = {
                "inputs": input,
                "time": gameMath.fixed(gameTimer.getLocalTime()),
                "seq": inputSeq
            };

            myPlayer.paddle.inputs.push(data);
            data = JSON.stringify(data);
            packet.input = data;
            packet.playerName = myPlayer.playerName;
            connector.sendMessage("/inputs", packet);
        }
    };

    updateLocalPos = function () {
        myPlayer.paddle.pos = myPlayer.paddle.curState.pos;
        myPlayer.paddle.checkCollision();
    };

    refreshFPS = function () {
        fps = 1 / delta;
        fps_avg_acc += fps;
        fps_avg_count++;

        if (fps_avg_count >= 10) {
            fps_avg = fps_avg_acc / 10;
            fps_avg_count = 1;
            fps_avg_acc = fps;
        }
    };

    update = function (curTime) {
        delta = lastFrameTime ? gameMath.fixed((curTime - lastFrameTime) / 1000.0) : 0.016;
        lastFrameTime = curTime;

        pongComponents.initCanvas();

        context.fillStyle = "black";
        context.fillRect(0, 0, width, height);

        handleKeyBoardInputs();

        handleServerUpdates();

        otherPlayer.paddle.draw(otherPlayer.side);

        updateLocalPos();

        myPlayer.paddle.draw(myPlayer.side);

        refreshFPS();

        animateId = window.requestAnimationFrame(update);
    };

    up = function (up) {
        isUp = up;
    };

    down = function (down) {
        isDown = down;
    };

    handleServerUpdates = function () {
        var currentTime, count, target, previous,
            point, nextPoint, difference, maxDifference,
            timePoint, otherTargetPos, otherLatestPos,
            otherPastPos, i;

        if (!serverUpdates.length) {
            return;
        }

        currentTime = clientTime;
        count = serverUpdates.length - 1;
        target = previous = null;

        for (i = 0; i < count; ++i) {
            point = serverUpdates[i];
            nextPoint = serverUpdates[i + 1];

            //noinspection JSUnresolvedVariable
            if (currentTime > point.server_time && currentTime < nextPoint.server_time) {
                target = nextPoint;
                previous = point;
                break;
            }
        }

        if (!target) {
            target = serverUpdates[0];
            previous = serverUpdates[0];
        }

        if (target && previous) {
            //noinspection JSUnresolvedVariable
            targetTime = target.server_time;

            difference = targetTime - currentTime;
            //noinspection JSUnresolvedVariable
            maxDifference = gameMath.fixed(target.server_time - previous.server_time);
            timePoint = gameMath.fixed(difference / maxDifference);

            if (isNaN(timePoint)) {
                timePoint = 0;
            }

            if (timePoint === -Infinity) {
                timePoint = 0;
            }

            if (timePoint === Infinity) {
                timePoint = 0;
            }

            //noinspection JSUnresolvedVariable
            otherTargetPos = otherPlayer.side === "left" ? target.left_pos : target.right_pos;
            //noinspection JSUnresolvedVariable
            otherPastPos = otherPlayer.side === "left" ? previous.left_pos : previous.right_pos;
            otherLatestPos = gameMath.vectorInterpolation(otherPastPos, otherTargetPos, timePoint);
            otherPlayer.paddle.pos = gameMath.vectorInterpolation(otherPlayer.paddle.pos, otherLatestPos, physics.getDelta() * 25);
        }
    };

    setPlayerName = function (name) {
        myPlayer.playerName = name;
    };

    parseMessage = function (msg) {
        switch (msg.state) {
        case "in-game":
            onInGame(msg);
            break;
        case "opponent-notification":
            var time = new Date();
            $("#opponent_list").html("time: " + time + " " + msg.message + "<br />");
            break;
        case "start-game":
            onStart(msg);
            break;
        case "server-update":
            onServerUpdateReceived(msg);
            break;
        case "cancel-update":
            cancelUpdate();
            break;
        }
    };

    onInGame = function (msg) {
        myPlayer.side = msg.side;
        otherPlayer.side = msg.side === "left" ? "right" : "left";
        //noinspection JSUnresolvedVariable
        myPlayer.numPlayer = msg.player_num;
        if (msg.ready === 2) {
            connector.sendMessage("/game/start", {"gameId": gameId});
        }
    };

    onServerUpdateReceived = function (msg) {
        //noinspection JSUnresolvedVariable
        serverTime = msg.server_time;
        clientTime = serverTime - (netOffset / 1000);

        serverUpdates.push(msg);

        if (serverUpdates >= (60 * bufferSize)) {
            serverUpdates.shift();
        }

        processPredictionCorrection();
    };

    onStart = function (msg) {
        myPlayer.paddle = pongComponents.getPaddle(myPlayer.side);
        otherPlayer.paddle = pongComponents.getPaddle(otherPlayer.side);
        gameTimer.updateTimer();
        physics.initPlayer(myPlayer);
        physics.update();
        //noinspection JSUnresolvedVariable
        update(msg.server_time);
    };

    processPredictionCorrection = function () {
        var myServerPos, latestServerData, myLastServerInputSeq, lastInputSeq,
            numToClear, i;

        if (!serverUpdates.length) {
            return;
        }

        latestServerData = serverUpdates[serverUpdates.length - 1];
        //noinspection JSUnresolvedVariable
        myServerPos = myPlayer.side === "left" ? latestServerData.left_pos : latestServerData.right_pos;
        //noinspection JSUnresolvedVariable
        myLastServerInputSeq = myPlayer.side === "left" ? latestServerData.left_seq : latestServerData.right_seq;

        if (myLastServerInputSeq) {
            lastInputSeq = -1;

            for (i = 0; i < myPlayer.paddle.inputs.length; ++i) {
                if (myPlayer.paddle.inputs[i].seq === myLastServerInputSeq) {
                    lastInputSeq = i;
                    break;
                }
            }

            if (lastInputSeq !== -1) {
                numToClear = Math.abs(lastInputSeq - (-1));
                myPlayer.paddle.inputs.splice(0, numToClear);

                myPlayer.paddle.curState.pos = gameMath.pos(myServerPos);
                myPlayer.paddle.lastInputSeq = lastInputSeq;

                physics.update();
                updateLocalPos();
            }
        }
    };

    cancelUpdate = function () {
        window.cancelAnimationFrame(animateId);
    };

    getFPS = function () {
        return fps_avg;
    };

    getMyPlayer = function () {
        return myPlayer;
    };

    getOtherPlayer = function () {
        return otherPlayer;
    };

    return {
        "parseMessage": parseMessage,
        "getMyPlayer": getMyPlayer,
        "getOtherPlayer": getOtherPlayer,
        "up": up,
        "down": down,
        "update": update,
        "setPlayerName": setPlayerName,
        "getFps": getFPS
    };
}());

var connector = (function () {
    "use strict";
    var onOpen, onMessage, onError, onClose, sendMessage,
        open, channel, socket, player;

    open = function (player_input) {
        player = player_input;
        //noinspection JSUnresolvedFunction,JSUnresolvedVariable
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
        var msg = JSON.parse(message.data);
        gameUpdate.parseMessage(msg);
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

    document.addEventListener('keydown', function (evt) {
        switch (evt.keyCode) {
        case 38:
            gameUpdate.up(true);
            break;
        case 40:
            gameUpdate.down(true);
            break;
        }
    }, false);

    document.addEventListener('keyup', function (evt) {
        switch (evt.keyCode) {
        case 38:
            gameUpdate.up(false);
            break;
        case 40:
            gameUpdate.down(false);
            break;
        }
    }, false);
});

