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