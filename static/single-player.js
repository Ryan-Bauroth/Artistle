/***
 * Creates a script element for single-player.html allowing jquery reference in below functions ($ used)
 * @type {HTMLScriptElement}
 */
let script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'https://code.jquery.com/jquery-3.7.0.js';
document.body.appendChild(script);

// CONSTS
const SONG_INPUT = document.getElementById("song-input");
const SONG_INPUT_BACKGROUND = document.getElementById("song-input-div");
const ARTIST_INPUT = document.getElementById("artist-input");
const ARTIST_INPUT_BACKGROUND = document.getElementById("artist-input-background");
const ARTIST_LOAD_ICON = document.getElementById("artist-loader");
const SONG_INPUT_AUTOCOMPLETE = document.getElementById("autocomplete-song-input");
const COUNTDOWN = document.getElementById("countdown");
const SCORE = document.getElementById("score");

const orgPoint = 1000;
const streakMultiplier = 1.02;


// Global Variables
let currentlyPlaying = false;
let allowInput = true;
let allowPlayMusic = false;
let currentSongs = [];
let backupCurrentSongs = [];
let recentSongs = []
let currentSongName = ""
let music = new Audio()
let countdownTimerInterval;
let time = 0;
let msTimerInterval;
let streak = 0;
let score = 0;
let highScore = 0;

function playMusic(){
    //TODO put input in focus
    if(!currentlyPlaying && allowPlayMusic){
        SONG_INPUT.value = "";
        music.play();
        currentlyPlaying = true;
        countdownTimerInterval = window.setInterval(countdown, 1000);
        msTimerInterval = window.setInterval(calcMSTime, 10);
        music.addEventListener("ended", function(){
            music.currentTime = 0;
            currentlyPlaying = false;
        });
    }
}
function resetMusic(){
    music.pause()
    music.currentTime = 0;
    currentlyPlaying = false;
}

/*
    function editArtist()
    Called upon when the user clicks the edit button under the artist input
    Un-blurs and enables input for the user (allows the user to change their artist)
 */
function editArtist(){
    ARTIST_INPUT.value = "";
    ARTIST_INPUT_BACKGROUND.style.filter = "blur(0px)";
    ARTIST_INPUT.disabled = false;
}

/*
    function submitArtist()
    Called upon when the user submits an artist
    Blurs and disables input (doesn't allow the user to change their artist)
 */
function submitArtist(){
    if(allowInput) {
        allowPlayMusic = false;
        allowInput = false;
        ARTIST_INPUT_BACKGROUND.style.filter = "blur(1px)";
        ARTIST_INPUT.disabled = true;
        SONG_INPUT.disabled = true;
        SONG_INPUT_BACKGROUND.style.filter = "blur(1px)";
        ARTIST_LOAD_ICON.style.opacity = "1";
        $.ajax({
            type: "POST",
            url: "/views/store_artist_check",
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain")
            },
            data: {"input": document.getElementById("artist-input").value},
        }).done(function (data) {
            SONG_INPUT_BACKGROUND.style.filter = "blur(0px)";
            ARTIST_LOAD_ICON.style.opacity = "0";
            SONG_INPUT.disabled = false;
            if (data !== "Artist_has_no_url") {
                allowPlayMusic = true;
                currentSongs = data.replace("[", "").replace("]", "").replace(/"/g, "").split(",");
                currentSongs.shift();
                backupCurrentSongs = currentSongs.slice(0);
                //TODO add warning if limit
                selectSong();
                allowInput = true;
                setAutocomplete();
            } else {
                editArtist();
                alert("The artist you entered doesn't have preview URLs! Try another artist!");
                allowInput = true;
            }
        })
    }
}
function selectSong(){
    if(currentSongs.length > 0){
        let rand = getRandNumber()
        let musicStart = Math.floor(Math.random() * 20)
        music = new Audio(currentSongs[rand].split("|#&")[1] + "#t=" + musicStart.toString() + "," + (musicStart + 10).toString());
        currentSongName = currentSongs[rand].split("|#&")[0].trim();
        recentSongs.push(currentSongs[rand].split("|#&")[0].trim());
        currentSongs.splice(rand,1);
        if(backupCurrentSongs.length > 4 &&  recentSongs.length > 3)
            recentSongs.shift();
        console.log(currentSongName);
    }
    else{
        currentSongs = backupCurrentSongs.slice(0);
        selectSong();
    }
}

function getRandNumber(){
    let rand = 0;
    let hasRun = false
    while(!hasRun && !recentSongs.includes(currentSongs[rand].split("|#&")[0].trim)) {
        hasRun = true;
        rand = Math.floor(Math.random() * currentSongs.length)
    }
    return rand;
}


ARTIST_INPUT.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        submitArtist();
    }
});

SONG_INPUT.addEventListener("change", (event) => {
    if(cleanInput(currentSongName) === cleanInput(SONG_INPUT.value) && currentlyPlaying){
        //TODO streak
        SONG_INPUT.value = ""
        score = calculateScore(time, streak, score);
        SCORE.innerText = Math.round(score).toString();
        console.log(score);
        streak += 1;
        time = 0;
        resetMusic();
        selectSong();
        resetCountdown();
        playMusic();
    }
});

function cleanInput(string){
    return string.toLowerCase().trim().replace(/'/g,"").replace("?","").replace("!", "").replace(",","").replace(".","").replace(/"/g,"")
}
function setAutocomplete(){
    $(SONG_INPUT_AUTOCOMPLETE).empty();
    for(let i = 0; i < backupCurrentSongs.length; i++){
        let option = document.createElement("option");
        option.value = backupCurrentSongs[i].split("|#&")[0].trim()
        SONG_INPUT_AUTOCOMPLETE.appendChild(option);
    }
}

function countdown(){
    if(COUNTDOWN.textContent !== "1")
        COUNTDOWN.textContent = (Number(COUNTDOWN.textContent) - 1).toString();
    else {
        COUNTDOWN.textContent = (Number(COUNTDOWN.textContent) - 1).toString();
        window.clearInterval(countdownTimerInterval)
        window.clearInterval(msTimerInterval)
        time = 0;
        SCORE.innerText = ""
        if(score > highScore){
            highScore = score;
        }
        score = 0;
        streak = 0;
        resetMusic();
        selectSong();
        resetCountdown();
        //todo show correct answer
    }
}
function resetCountdown(){
    if(countdownTimerInterval != null){
        window.clearInterval(countdownTimerInterval)
    }
    COUNTDOWN.textContent = "10";
}

function calculateScore(guessTime, streak, previousScore) {
    let timePenalty = guessTime / 2;
    let point = (orgPoint - timePenalty) * Math.pow(streakMultiplier, streak);
    return point + previousScore;
}

function calcMSTime(){
    time += 1;
}