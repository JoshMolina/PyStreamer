###VIDEO USED: https://www.youtube.com/watch?v=YXPyB4XeYLA ###
###OTHER INFO:
#ffmpeg-python: https://github.com/kkroening/ffmpeg-python#:~:text=bindings%20for%20FFmpeg-,Overview,well%20as%20complex%20signal%20graphs.
##Binding vlc to a Tkinter frame: http://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/tkvlc.py;h=55314cab09948fc2b7c84f14a76c6d1a7cbba127;hb=HEAD
##Helpful video with general concepts: https://www.youtube.com/watch?v=88IJCBKlAPA&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=87
##Impressive way of playing audio; think about switching to Selenium: https://github.com/tanmay606/YoutubeMusicPythonAPI/blob/master/YMusic.py
##Video of above program: https://www.youtube.com/watch?v=GsfLLi_qtYs
##Look up pywin32/win32gui for the media control that shows up in the top left corner of the screen when using media keys





import os
import pafy #pip install pafy
from bs4 import BeautifulSoup
import re, requests, subprocess, urllib.parse, urllib.request
import vlc #pip install python-vlc
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import ImageTk, Image #pip install Pillow
from googleapiclient.discovery import build #pip install google-api-python-client
root=Tk()
process = Variable()
# layer = (ytdl=True, video=False)
root.title("PyStreamer")
# filters = [
#     "--aout=waveout",
#     "--equalizer-preset=flat",
#     "--equalizer-preamp=5"
# ]
# vlc_instance=vlc.Instance(filters)
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

#Odd numbers are titles, even numbers are urls/ids
top3results=["","","","","",""]



class vlPlayer():
##list of all commands from the terminal for vlc: https://wiki.videolan.org/VLC_command-line_help/
##Also handy for explaining what the above one doesn't: https://www.olivieraubert.net/vlc/python-ctypes/doc/
    def __init__(self):
        #This makes the audio actually bareable
        self.options = [
            "--aout=waveout",
            "--equalizer-preset=flat",
            "--speex-resampler-quality=10",
            "--src-converter-type=0",
        ]
        self.vlc_instance=vlc.Instance(self.options)
        self.player = self.vlc_instance.media_player_new()
        #These also make the audio bareable
        self.eq = vlc.AudioEqualizer()
        self.eq.set_preamp(8)
        self.player.set_equalizer(self.eq)
        self.volume = int(100)

    def play(self):
        self.media = self.vlc_instance.media_new(query_url.get())
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.player.set_equalizer(self.eq)
        self.player.play()
        self.setVol(self.volume)

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def getCurrTime(self):
        return self.player.get_time() / 1000

    def getLength(self):
        return self.player.get_length() / 1000

    def getFormattedTime(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.getCurrTime()))

    def getFormattedLength(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.getLength()))
    
    def setPos(self, time_var):
        self.player.set_time(time_var*1000)
    
    def setVol(self, volume):
        self.volume = volume
        self.player.audio_set_volume(int(volume))


x=vlPlayer()

def play():
    print("Query URL: " + query_url.get())
    ##Helpful link: https://stackoverflow.com/questions/54862611/pafy-and-vlc-audio-only-in-python
    print("hit play()")
    
    
    x.play()
    playing.set(True)
    res_pause.set("Pause")
    play_time()
def resume_pause():
    print("Playing status: "+ str(playing.get()))
    if playing.get()==True:
        x.pause()
        print("Hit pause")
        playing.set(False)
        res_pause.set("Resume")
    elif playing.get()==False:
        x.pause()
        playing.set(True)
        res_pause.set("Pause")
    else:
        pass

def stop():
    x.stop()


def change_time(time):
    slide_pos = int(music_slider.get())
    music_slider.set(slide_pos)
    x.setPos(slide_pos)

def change_vol(volume):
    x.setVol(volume_slider.get())

def update_vol():
    v_slide=str(int(volume_slider.get()))
    volume_label.config(text="Volume: " + v_slide)
    volume_label.after(10, update_vol)

def play_time():
    curr_time = x.getCurrTime()
    leng = x.getLength()
    form_time = x.getFormattedTime()
    form_length = x.getFormattedLength()
    curr_time_label.config(text=form_time)
    length_label.config(text=form_length)
    status_bar.config(text="Time Elapsed: " + form_time + "     Song Length: " + form_length)
    music_slider.config(to=leng, value=curr_time)
    # mus_sli_label.config(text=form_time)
    status_bar.after(1000, play_time)

def search(arg):
    if (arg != ""):
        query_title = urllib.parse.urlencode({"search_query":arg})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?"+query_title)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip = requests.get("https://www.youtube.com/watch?v="+"{}".format(search_results[0]))
        clip2 = "https://www.youtu.be/"+"{}".format(search_results[0])
        inspect = BeautifulSoup(clip.content, "html.parser")
        yt_title = inspect.find_all("meta",property="og:title")
        query_url.set(clip2)
        for title in yt_title:
            pass
        query_url.set(pafy.new(clip2).getbestaudio().url)
        update_label(str(title['content']))
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

button = Button(root, text="Enter a Youtube Title", command=lambda: search(e.get()))
button.pack(pady=(0,20))

display_label=Label(root, textvariable=display_var, width=60)
display_label.pack(expand=True, fill=X)

info_frame = Frame(root)
info_frame.pack(pady=(0,10))

music_slider = ttk.Scale(info_frame, from_=0, to=0, orient=HORIZONTAL, value=0, length=360, command=change_time)
music_slider.grid(row=0, column=1)
curr_time_label=Label(info_frame, text="00:00:00")
curr_time_label.grid(row=0,column=0, padx=(20,0))
length_label=Label(info_frame, text="00:00:00")
length_label.grid(row=0,column=2)

volume_slider = ttk.Scale(info_frame, from_=125, to=0, value=100, orient=VERTICAL, command=change_vol)
volume_slider.grid(row=0, column=3, padx=(25, 0))

volume_label = Label(info_frame, text="Volume: " + str(int(volume_slider.get())))
volume_label.grid(row=1, column=3, padx=(35,0))
volume_slider.after(10, update_vol)

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

def popup():
    messagebox.showerror("ERROR!", "You must enter a title and search for it before clicking play!")

root.mainloop()