/***
 * Creates a script element for single-player.html allowing jquery reference in below functions ($ used)
 * @type {HTMLScriptElement}
 */
let script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'https://code.jquery.com/jquery-3.7.0.js';
document.body.appendChild(script);

// Global Variables
let currentlyPlaying = false;
let currentSongs = []
let music = new Audio()

function playMusic(){
    if(!currentlyPlaying){
        music.play();
        currentlyPlaying = true;
        console.log("playing")
        music.addEventListener("ended", function(){
            music.currentTime = 0;
            currentlyPlaying = false;
        });
    }
}

/*
    function editArtist()
    Called upon when the user clicks the edit button under the artist input
    Un-blurs and enables input for the user (allows the user to change their artist)
 */
function editArtist(){
    document.getElementById("artist-input").value = "";
    document.getElementById("artist-input-background").style.filter = "blur(0px)";
    document.getElementById("artist-input").disabled = false;
}

/*
    function submitArtist()
    Called upon when the user submits an artist
    Blurs and disables input (doesn't allow the user to change their artist)
 */
function submitArtist(){
    document.getElementById("artist-input-background").style.filter = "blur(1px)";
    document.getElementById("artist-input").disabled = true;
    $.ajax({
        type: "POST",
        url: "/views/store_artist_check",
        beforeSend: function ( xhr ) {
            xhr.overrideMimeType("text/plain")
        },
        data: {"input": document.getElementById("artist-input").value},
    }).done(function(data){
        if(data !== "Artist_has_no_url"){
            document.getElementById("artist-input-background").style.filter = "blur(1px)";
            document.getElementById("artist-input").disabled = true;
            console.log("current songs")
            console.log(JSON.parse(currentSongs));
            //TODO add warning if limit
            selectSong()
        }
        else{
            editArtist();
            alert("The artist you entered doesn't have preview URLs! Try another artist!");
        }
    })
}
function selectSong(){
    if(currentSongs.length !== 0){
         let x = Math.floor(Math.random()*currentSongs.length)
         music = new Audio(currentSongs[x]);
         console.log(currentSongs[x])
    }
}