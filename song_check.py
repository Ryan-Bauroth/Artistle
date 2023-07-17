
def song_check(guessed_song,actual_song):
    if guessed_song.lower().strip() == actual_song.lower().strip():
        return True
    
    else:
        return False

print(song_check("Akfk lD","akFKl d"))

        
