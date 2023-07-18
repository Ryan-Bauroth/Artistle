var currentlyPlaying = false;
var music = new Audio()

function playMusic(){
    if(!currentlyPlaying){
        if(document.getElementById('artist_input').value !== "")
            music = new Audio(document.getElementById("artist_input").value);
        console.log(document.getElementById("artist_input").value)
        music.play();
        currentlyPlaying = true;
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
}