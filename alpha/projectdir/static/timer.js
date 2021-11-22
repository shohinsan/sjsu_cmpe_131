function Timer() {
    $(".minutes").html(minutes);
    if (seconds < 10) {
        $(".seconds").html("0" +seconds);
    }
    else {
        $(".seconds").html(seconds);
    }
}

function stop() {
    timerflag=0;
    pauseflag=0;
    minutes=25;
    seconds=0;
    Timer();
    $(".start-stop").html("Start");
    $(".pause-section").hide();
    clearTimeout(t);
}

function start() {
    timerflag=1;
    pauseflag=0;
    update();
    $(".stop-start").html("Stop");
    $(".pause-section").show();
    $(".pause").text("Pause");
    $(".start-stop-section").hide();
}

function pause() {
    pauseflag=1;
    clearTimeout(t);
    $(".start-stop-section").show();
    $(".pause").html("Resume");
}

function resume() {
    pauseflag=0;
    update();
    $(".pause").html("Pause");
    $(".start-stop-section").hide();
}

function update() {
    if (minutes == 0 && seconds == 0) {
        minutes=25;
        seconds=0;
        Timer();
    }
    else if (seconds == 0) {
        minutes-=1;
        seconds=59; 
        Timer();
        t=setTimeout(update, 1000);
    }
    else {
        seconds-=1;
        Timer();
        t=setTimeout(update, 1000);
    }
}