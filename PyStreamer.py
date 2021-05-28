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
import threading
from threading import Thread
root=Tk()
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
query_title = StringVar()
query_title.set("")
found_title = StringVar()
query_thumbnail = ""
display_var = StringVar()
display_var.set("Enter a song name")
queue = []
q_url = []
q_btn_state = False
queue_selected=False
th_timer = ""
in_queue=False
pl_indiv=False
pl_queue=False
play_next=False
end_of_queue=True
is_fin=False
curr_playing=""
curr_search=""



curr_q_index = IntVar()
curr_q_index.set(-1)
queue_length=len(queue)

#Odd numbers are titles, even numbers are urls/ids
top3results=["","","","","",""]



class vlPlayer():
##list of all commands from the terminal for vlc: https://wiki.videolan.org/VLC_command-line_help/
##Also handy for explaining what the above one doesn't: https://www.olivieraubert.net/vlc/python-ctypes/doc/
    def __init__(self):
        # Thread.__init__(self)
        #This makes the audio actually bareable
        self.options = [
            "--aout=waveout",
            "--equalizer-preset=flat",
            "--speex-resampler-quality=10",
            "--src-converter-type=0",
        ]
        self.from_playlist = False
        self.vlc_instance=vlc.Instance(self.options)
        self.player = self.vlc_instance.media_player_new()
        #These also make the audio bareable
        self.eq = vlc.AudioEqualizer()
        self.eq.set_preamp(6)
        self.player.set_equalizer(self.eq)
        self.volume = int(100)


    def play(self, url):
        self.from_playlist-False
        self.player.stop()
        # self.player = self.vlc_instance.media_player_new()
        self.media = self.vlc_instance.media_new(url)
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.player.set_equalizer(self.eq)
        self.player.play()
        self.setVol(self.volume)
    
    def playlist(self, urls):
        self.player=self.vlc_instance.media_player_new()
        playing = set([1,2,3,4])
        for i in urls:
            self.player.set_mrl(i)
            self.player.play()
            play = True
            while play == True:
                time.sleep(1)
                play_state = self.player.get_state()
                if play_state in playing:
                    continue
                else:
                    play=False
        
        # self.from_playlist=True
        # self.player.stop()
        # self.player = self.vlc_instance.media_list_player_new()
        # self.media_list = self.vlc_instance.media_list_new()
        # self.pl_inst = self.player.get_media_player()
        # # self.pl_inst = self.vlc_instance.media_player_new()
        # self.pl_inst.set_equalizer(self.eq)
        # for item in urls:
        #     self.media = self.vlc_instance.media_new(item[1])
        #     self.media.get_mrl()
        #     self.media_list.add_media(self.media)
        # self.player.set_media_list(self.media_list)
        # self.player.set_media_player(self.pl_inst)
        # # self.player.set_equalizer(self.eq)
        # self.player.play()
        # self.setVol(self.volume)

        #  self.media = self.vlc_instance.media_list_new(urls)
        # self.media.get_mrl()
        # self.player=vlc.Instance(self.options).media_list_player_new()
        # self.player.set_media_list(self.media)
        # self.player.set_equalizer(self.eq)
        # self.player.play()
        # self.setVol(self.volume)

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def getCurrTime(self):
        return self.player.get_time() / 1000

    def getLength(self):
        return self.player.get_length() / 1000

    def getFormattedTime(self):
        if (self.getCurrTime() == -.001):
            return "00:00:00"
        return time.strftime('%H:%M:%S', time.gmtime(self.getCurrTime()))

    def getFormattedLength(self):
        if (self.getLength() == -.001):
            return "00:00:00"
        return time.strftime('%H:%M:%S', time.gmtime(self.getLength()))
    
    def setPos(self, time_var):
        self.player.set_time(time_var*1000)
    
    def setVol(self, volume):
        self.volume = volume
        self.player.audio_set_volume(int(volume))
    
    def get_state(self):
        return self.player.get_state()
    
    def get_is_playing(self):
        return self.player.is_playing()
    
    def get_is_finished(self):
        return self.getCurrTime() == self.getLength()


x=vlPlayer()

def play_btn():
    global pl_indiv
    global pl_queue
    global curr_q_index
    if pl_queue==True:
        stop()
        pl_queue = False
    pl_indiv = True
    curr_q_index.set(-1)
    play(query_url.get())

def play_queue_btn():
    global pl_indiv
    global pl_queue
    global play_next
    global curr_q_index
    global queue
    global end_of_queue
    curr_q_index.set(-1)
    print("len(queue): ", len(queue))
    if len(queue) > 0:
        curr_q_index.set(0)
        if pl_indiv==True:
            stop()
            pl_indiv=False
        pl_queue = True
        play_next = True
        end_of_queue = False
        play_queue()

def play(*args):
    ##Helpful link: https://stackoverflow.com/questions/54862611/pafy-and-vlc-audio-only-in-python
    global pl_indiv
    global pl_queue
    global curr_playing
    # if playing.get():
    #     pass
    # else:
    #     if pl_indiv == True:
    #         x.play(query_url.get())
    #         playing.set(True)
    #         res_pause.set("Pause")
    #         play_time()
    #     elif play_queue == True:
    #         x.play(args[0][0])
    #         playing.set(True)
    #         res_pause.set("Pause")
    #         play_time()

    
    
    
    if (len(args) == 0):
        curr_playing=found_title.get()
        x.play(query_url.get())
    else:
        x.play(args[0])
    # x.play(args[0])
    playing.set(True)
    res_pause.set("Pause")
    play_time()
    if pl_queue == True:
        root.after(250, check_finished)

def play_queue():
    global pl_queue
    global play_next
    global end_of_queue
    global curr_playing

    if play_next == True:
        if curr_q_index.get() < len(queue):
            play_next = False
            curr_playing = str(queue[curr_q_index.get()][0])
            play(queue[curr_q_index.get()][1])
            curr_q_index.set(curr_q_index.get() + 1)
        else: 
            print("End of queue")
            pl_queue=False
    else:
        pass

    # if len(queue) != 0 and curr_q_index.get() < len(queue):
        

    # if len(queue) != 0 and curr_q_index.get() < len(queue):
    #     # x.playlist(queue)
    #     if curr_q_index.get() == -1:
    #         curr_q_index.set(curr_q_index.get() + 1)
    #     print("hit")
    #     play(queue[curr_q_index.get()][1])
    #     playing = set([1,2,3,4])
    #     time.sleep(1)
    #     check_finished()
    #     play_queue()
        # while True:
        #     state = x.get_state()
        #     if state not in playing:
        #         break
        #     continue
        # if len(queue) > curr_q_index.get():
        #     curr_q_index.set(curr_q_index.get() + 1)
        #     play_queue()
        # for item in queue:
        #     print("Title: " + item[0])
        #     play(item[1])
        #     time.sleep(1)
        #     check_finished()


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
    curr_time_label.config(text=x.getFormattedTime())

def change_vol(volume):
    x.setVol(volume_slider.get())
    v_slide=str(int(volume_slider.get()))
    volume_label.config(text="Volume: " + v_slide)

def play_time():
    global pl_queue
    global curr_playing

    curr_time = x.getCurrTime()
    leng = x.getLength()
    form_time = x.getFormattedTime()
    form_length = x.getFormattedLength()
    fin = x.get_is_finished()
    if curr_time != leng:
        playing.set(True)
    else:
        playing.set(False)
    curr_time_label.config(text=form_time)
    length_label.config(text=form_length)
    status_bar.config(text="Song Playing: " + curr_playing + "     Time Elapsed: " + form_time + "     Song Length: " + form_length)
    music_slider.config(to=leng, value=curr_time)
    status_bar.after(1000, play_time)
    if pl_queue == True:
        root.after(250, check_finished)

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
        found_title.set(str(title['content']))
        update_label(found_title.get())
        add_q_btn.config(state='normal')
    else:
        print("Empty query")
        query_url.set("")
        update_label("Please input a title for the song you'd like to play")
        add_q_btn.config(state='disabled')
def update_label(text):
    display_var.set("Found:\t" + text)

def add_song():
    queue.append([found_title.get(), query_url.get()])
    q_url.append(query_url.get())
    queue_listbox.insert(END, found_title.get())

# def play_queue():
#     in_queue=True
#     th_timer = threading.Timer(.5, p_q)
#     th_timer.start()

def is_done():
    if x.get_is_playing() == True:
        if music_slider.get() == x.getLength():
            pass

def check_finished():
    global play_next
    global pl_queue
    print ("hit outside")
    is_fin = x.get_is_finished()
    print("is_fin: ", is_fin, " pl_queue: ", pl_queue, "playing.get(): ", playing.get())
    if x.get_is_playing()==False and pl_queue == True:
        x.stop()
        play_next = True
        time.sleep(1)
        print("hit inside")
        play_queue()

def on_closing():
    if in_queue==True:
        th_timer.stop()
    root.destroy()

e = Entry(root, width=60)
e.pack()

search_frame = Frame(root)
search_frame.pack()

search_btn = Button(search_frame, text="Enter a Youtube Title", command=lambda: search(e.get()))
search_btn.grid(row=0,column=0,pady=(0,10))
add_q_btn = Button(search_frame, text="Add song to queue", state='disabled', command=add_song)
add_q_btn.grid(row=0,column=1,pady=(0,10))


display_label=Label(root, textvariable=display_var, width=60)
display_label.pack(expand=True, fill=X)

info_frame = Frame(root)
info_frame.pack(pady=(0,10))

queue_listbox=Listbox(info_frame)
queue_listbox.grid(row=0, column=0, padx=(10,0))

queue_play=Button(info_frame, text="Play Queue", command=play_queue_btn)
queue_play.grid(row=1,column=0, padx=(10,0))

curr_time_label=Label(info_frame, text="00:00:00")
curr_time_label.grid(row=0,column=1, padx=(20,0))

music_slider = ttk.Scale(info_frame, from_=0, to=1, orient=HORIZONTAL, value=0, length=360, command=change_time)
music_slider.grid(row=0, column=2)
# music_slider.after(1000, command=is_done)

length_label=Label(info_frame, text="00:00:00")
length_label.grid(row=0,column=3,padx=(0,65))

volume_slider = ttk.Scale(info_frame, from_=125, to=0, value=100, orient=VERTICAL, command=change_vol)
volume_slider.grid(row=0, column=3, padx=(25, 0))

volume_label = Label(info_frame, text="Volume: " + str(int(volume_slider.get())))
volume_label.grid(row=1, column=3, padx=(35,0))

control_frame = Frame(root)
control_frame.pack()

play_button = Button(control_frame, text="Play", command=play_btn, width=15)
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

# add_q_btn.after(500, check_finished)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()