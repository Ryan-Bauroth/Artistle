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
const ARTIST_INPUT = document.getElementById("artist-input");
const ARTIST_INPUT_BACKGROUND = document.getElementById("artist-input-background")


// Global Variables
let currentlyPlaying = false;
let allowInput = true;
let currentSongs = [];
let currentSongName = ""
let music = new Audio()

function playMusic(){
    if(!currentlyPlaying){
        music.play();
        currentlyPlaying = true;
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
        allowInput = false;
        ARTIST_INPUT_BACKGROUND.style.filter = "blur(1px)";
        ARTIST_INPUT.disabled = true;
        $.ajax({
            type: "POST",
            url: "/views/store_artist_check",
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain")
            },
            data: {"input": document.getElementById("artist-input").value},
        }).done(function (data) {
            if (data !== "Artist_has_no_url") {
                ARTIST_INPUT_BACKGROUND.style.filter = "blur(1px)";
                ARTIST_INPUT.disabled = true;
                currentSongs = data.replace("[", "").replace("]", "").replace(/"/g, "").split(",");
                currentSongs.shift();
                //TODO add warning if limit
                selectSong();
                allowInput = true;
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
         let x = Math.floor(Math.random()*currentSongs.length)
         music = new Audio(currentSongs[x].split("|#&")[1]);
         currentSongName = currentSongs[x].split("|#&")[0].trim();
         currentSongs.splice(x,1)
         console.log(currentSongName)
        console.log(currentSongs)
    }
    else{
        currentlyPlaying = false;
        music.pause()
        submitArtist();
        //TODO figure out a better way to deal with getting low on songs (this takes load time)
    }
}


ARTIST_INPUT.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        submitArtist();
    }
});

SONG_INPUT.addEventListener("change", (event) => {
    if(makeComparable(currentSongName) === makeComparable(SONG_INPUT.value) && currentlyPlaying){
        //TODO streak
        SONG_INPUT.value = ""
        resetMusic();
        selectSong();
        if(currentSongs.length > 0) {
            playMusic();
            //TODO TEST THIS THIS ISNT WORKING I DONT THINK
        }
    }
});

function makeComparable(string){
    return string.toLowerCase().trim().replace(/'/g,"").replace("?","").replace("!", "").replace(",","").replace(".","").replace(/"/g,"")
}