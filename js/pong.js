/**
 * Created by RookY2K on 5/4/2015.
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
        getLocalTime,
        isTiming = true,
        stopTiming;

    updateTimer = function () {
        timerStartDelta = Date.now() - timerEndDelta;
        timerEndDelta = Date.now();
        localTime += timerStartDelta / 1000.0;
        if (isTiming) {
            setTimeout(updateTimer, 4);
        }
    };

    getLocalTime = function () {
        return localTime;
    };

    stopTiming = function () {
        isTiming = false;
    };

    return {
        "getLocalTime": getLocalTime,
        "updateTimer": updateTimer,
        "stopTiming": stopTiming
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
        var retBall = Object.create(ball);
        retBall.pos = {
            x: width / 2,
            y: height / 2
        };

        return retBall;
    };

    ball = {
        radius: 5,
        color: "white",
        pos: {
            x: width / 2,
            y: height / 2
        },

        draw: function () {
            context.beginPath();
            context.fillStyle = this.color;
            context.arc(this.pos.x,  this.pos.y,  this.radius,  0, Math.PI * 2, false);
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
        initPlayer,
        doPhysics = true,
        stopPhysics;

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
        if (doPhysics) {
            setTimeout(update, (15 - (Date.now() - start)));
        }
    };

    getDelta = function () {
        return delta;
    };

    stopPhysics = function () {
        doPhysics = false;
    };

    return {
        "getDelta": getDelta,
        "update": update,
        "initPlayer": initPlayer,
        "stopPhysics": stopPhysics
    };
}());

var gameUpdate = (function () {
    "use strict";
    var myPlayer, otherPlayer, parseMessage, getMyPlayer, getOtherPlayer,
        gameId = $("#game_id").find("p").text(),
        serverTime, update, up, down, animateId,
        cvs = document.getElementById("canvas"),
        context = cvs.getContext("2d"),
        height = 600, width = 800, inputSeq = 0, netOffset = 100,
        clientTime = 0.01, targetTime = 0.01, bufferSize = 2,
        serverUpdates = [],
        handleKeyBoardInputs, isUp, isDown, handleServerUpdates,
        updateLocalPos, setPlayerName, onGameWin,
        onServerUpdateReceived, processPredictionCorrection, cancelUpdate,
        onStart, onInGame, ball, startBall, canStart = false, isCanStart;

    myPlayer = {};
    otherPlayer = {};
    ball = {};

    handleKeyBoardInputs = function () {
        var input = [],
            data,
            packet;

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
            packet = {
                playerName: myPlayer.playerName,
                input: JSON.stringify(data)
            };
            connector.sendMessage("/game/inputs", packet);
        }
    };

    updateLocalPos = function () {
        myPlayer.paddle.pos = myPlayer.paddle.curState.pos;
        myPlayer.paddle.checkCollision();
    };

    update = function () {
        pongComponents.initCanvas();

        context.fillStyle = "black";
        context.fillRect(0, 0, width, height);

        handleKeyBoardInputs();

        handleServerUpdates();

        otherPlayer.paddle.draw(otherPlayer.side);

        ball.draw();

        updateLocalPos();

        myPlayer.paddle.draw(myPlayer.side);

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
            otherPastPos, i, ballTargetPos, ballPastPos,
            ballLatestPos;

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
            ballTargetPos = target.ball_pos;
            //noinspection JSUnresolvedVariable
            otherPastPos = otherPlayer.side === "left" ? previous.left_pos : previous.right_pos;
            //noinspection JSUnresolvedVariable
            ballPastPos = previous.ball_pos;
            otherLatestPos = gameMath.vectorInterpolation(otherPastPos, otherTargetPos, timePoint);
            ballLatestPos = gameMath.vectorInterpolation(ballPastPos, ballTargetPos, timePoint);
            otherPlayer.paddle.pos = gameMath.vectorInterpolation(otherPlayer.paddle.pos, otherLatestPos, physics.getDelta() * 25);
            ball.pos = gameMath.vectorInterpolation(ball.pos, ballLatestPos, physics.getDelta() * 25);
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
        case "game-win":
            onGameWin(msg);
            break;
        case "cancel-update":
            cancelUpdate();
            break;
        }
    };

    onGameWin = function (msg) {
        gameTimer.stopTiming();
        physics.stopPhysics();
        cancelUpdate();

        window.alert(msg.win + " player won!");
    };

    onInGame = function (msg) {
        myPlayer.side = msg.side;
        otherPlayer.side = msg.side === "left" ? "right" : "left";
        if (myPlayer.side === 'left') {
            canStart = true;
        }
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
        serverUpdates.sort(function (a, b) {return a.server_time - b.server_time; });

        if (serverUpdates.length >= (60 * bufferSize)) {
            serverUpdates.shift();
        }

        processPredictionCorrection();
    };

    onStart = function (msg) {
        myPlayer.paddle = pongComponents.getPaddle(myPlayer.side);
        otherPlayer.paddle = pongComponents.getPaddle(otherPlayer.side);
        ball = pongComponents.getBall();
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

    getMyPlayer = function () {
        return myPlayer;
    };

    getOtherPlayer = function () {
        return otherPlayer;
    };

    startBall = function () {
        connector.sendMessage("/game/startball", {"gameId": gameId});
    };

    isCanStart = function () {
        return canStart;
    };

    return {
        "parseMessage": parseMessage,
        "getMyPlayer": getMyPlayer,
        "getOtherPlayer": getOtherPlayer,
        "up": up,
        "down": down,
        "update": update,
        "setPlayerName": setPlayerName,
        "startBall": startBall,
        "isCanStart": isCanStart
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
        sendMessage("/game/open", data);
    };

    onMessage = function (message) {
        var msg = JSON.parse(message.data);
        gameUpdate.parseMessage(msg);
    };

    onError = function () {
        return null;
    };

    onClose = function () {
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
        url: "/game/connect",
        method: "GET",
        data: {
            "playerName": playerName,
            "gameId": gameId
        },
        dataType: "json",
        success: function (data) {
            gameUpdate.setPlayerName(playerName);
            connector.open(data);
        }
    });

    document.addEventListener('keydown', function (evt) {
        var space = false;
        switch (evt.keyCode) {
        case 32:
            if (!space && gameUpdate.isCanStart()) {
                gameUpdate.startBall();
                space = true;
            }
            break;
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

