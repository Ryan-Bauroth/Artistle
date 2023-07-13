var currentlyPlaying = false;
var music = new Audio()

function playMusic(){
    if(!currentlyPlaying){
        music = new Audio(document.getElementById("hidden").textContent);
        music.play();
        currentlyPlaying = true;
        music.addEventListener("ended", function(){
            music.currentTime = 0;
            currentlyPlaying = false;
        });
    }
}