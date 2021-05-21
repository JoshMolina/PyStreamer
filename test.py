import os
import youtube_dl #pip install youtube-dl
import pafy #pip install pafy
import mpv
from bs4 import BeautifulSoup
import re, requests, subprocess, urllib.parse, urllib.request
import vlc #pip install python-vlc
import time
from tkinter import *
root=Tk()
mPlayer = mpv.MPV(ytdl=True, video=False)
root.title("Test MPV Program")
# vlc_instance=vlc.Instance()
# player = vlc_instance.media_player_new()
playing = BooleanVar()
res_pause = StringVar()
res_pause.set("__")

query_url = StringVar()
query_url.set("")
query_title=StringVar()
query_title.set("")
query_thumbnail = ""
display_var = StringVar()
display_var.set("Enter a song name")


def play():
    print("Query URL: " + query_url.get())
    print("hit play()")
    ##VLC Code:
    #  media = vlc_instance.media_new(query_url.get())
    # media.get_mrl()
    # player.set_media(media)
    # player.play()


    mPlayer.play(query_url.get())
    mPlayer.wait_for_playback()
    playing.set(True)
    res_pause.set("Pause")



    play_time()
def resume_pause():
    print("Playing status: "+ str(playing.get()))
    #Ugly code because I haven't gotten around to writing a disable tag for the play/resume/pause/stop buttons
    if playing.get()==True:
        mPlayer._set_property("pause", True)
        print("Hit pause")
        playing.set(False)
        res_pause.set("Resume")
    elif playing.get()==False:
        mPlayer._set_property("pause", False)
        playing.set(True)
        res_pause.set("Pause")
    else:
        pass

def stop():
    # pygame.mixer.music.stop()
    mPlayer.stop()

def play_time():
    #Gets song time
    pass ##VLC code below; not applicable with mpv
    print(mPlayer._get_property(''))
    current_time = mPlayer.get_time() / 1000
    song_length = mPlayer.get_length() / 1000
    format_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
    format_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    status_bar.config(text="Time Elapsed: " + format_time + "     Song Length: " + format_length)
    
    status_bar.after(1000, play_time)

def search(arg):
    if (arg != ""):
        query_title = urllib.parse.urlencode({"search_query":arg})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?"+query_title)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        url = "https://www.youtube.com/watch?v="+"{}".format(search_results[0])
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result=ydl.extract_info(url, download=False)
            query_url.set(result.get("url",None))
            query_title.set(result.get('title',None))

    else:
        print("Empty query")
        query_url.set("")
        update_label("Please input a title for the song you'd like to play")
def update_label(text):
    display_var.set(text)

def add_song():
    pass

e = Entry(root, width=60)
e.pack()
# e.grid(row=1, column=0, columnspan=3)

button = Button(root, text="Enter a Youtube Title", command=lambda: search(e.get()))
button.pack()
# button.grid(row=2, column=0, columnspan=3)

display_label=Label(root, textvariable=display_var, width=60)
display_label.pack()
# display_label.grid(row=4,column=1)

control_frame = Frame(root)
control_frame.pack()

play_button = Button(control_frame, text="Play", command=play, width=15)
play_button.grid(row=0, column=0,padx=35)

res_pause_button = Button(control_frame, textvariable=res_pause, command=resume_pause, width=15)
res_pause_button.grid(row=0, column=1,padx=35)    

stop_button = Button(control_frame, text="Stop", command=stop,width=15)
stop_button.grid(row=0, column=2,padx=35)

##Status Bar Code
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X)
##Status Bar Code

root.mainloop()