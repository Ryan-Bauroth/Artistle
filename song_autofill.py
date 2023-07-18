def song_autofill(song_list,user_input):
    
    names_list = []
    final_list = []
    
    for i in range(len(song_list)):
        names_list.append(song_list[i].split("-")[0])

    for i in range(len(names_list)):
        if names_list[i].lower().strip().__contains__(user_input.lower()) == True:
            final_list.append(names_list[i])