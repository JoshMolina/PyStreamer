# PyStreamer
Personal Python project with the intent of streaming videos/playlists from Youtube, SoundCloud, and other sites (if I so choose) without having to have designated browser tabs for them.  

# About:  
## Technical Side:  
PyStreamer was created with the Tkinter package with VLC Media Player as the media player of choice. Given that my knowledge about Python and audio playing was very low prior to this project, I decided on working with the tools that have the most documentation. While I know that there are other GUI packages for Python (PyQt5 being one of the ones I tested; see QtStreamer.py in the repository) that can definitely make the interface look cleaner, I decided to take this project as a stepping stone and learn the basic from it rather than throwing myself into the deep end. As for VLC Media Player, this one was a little easier of a choice when put up against the other media players. I tested out MPV, but that required to have a file called mpv-1.dll on the system's PATH when using the python-mpv package. In addition to that, VLC has many more options to tweak and mess around with whereas, from my starting perspective, MPV does not.  
## Personal Side:  
I enjoy listening to music a good bit. I do it whenever I have the time to and, like others, I get annoyed when my music gets interrupted. Interruptions have become especially common on Youtube with it asking if you'd like to keep playing a song/video after a certain amount of time has passed. This is most irritating when I'm fullscreen in a game and have to either let the silence hang until the match is over or quickly tab out and fix it and be at the mercy of the other players. Interruptions aren't the only issue I have, though, as there are a handful of times where I'd find a song on SoundCloud or Youtube and want to add it to the main playlist I'm using at the time only to find out that it's not available on the other platform. By creating this music player, I (hopefully) intend to be able to pull my playlists from all of the services that I have playlists on and centralize them into one place.  


# How To Install:
## Download:
As of right now, I haven't created an exe file for PyStreamer, so the code will need to be pulled/downloaded from this repository. In addition to this, VLC Media Player is required to play audio.
This can be downloaded from their site: https://www.videolan.org/.
## Dependencies:
For PyStreamer to properly work, it requires the following:  
* VLC Media Player (linked above)  
* python-vlc package: pip install python-vlc  
* pafy: pip install pafy  
* bs4 (BeautifulSoup): pip install bs4  
While I didn't work in a virtual environment for this project (although I probably should've), I do recommend installing all of the necessary packages inside of a virtual environment just so that uninstalling doesn't become a hassle.
  
## VLC:  
While I'm not sure how necessary it is to have VLC on your system's PATH, if you encounter an error when it's not on the PATH, I'd recommend putting it there.  

# Services Used:  
As has been stated above, this player uses VLC Media Player, Youtube, and (hopefully) SoundCloud along with others. This project is in no way affiliated with any outside sites or services on a personal or contractual level and was only made out of a desire to sharpen my own craft (coding) as well as make a personal music player that I can enjoy. PyStreamer has not, is not, and will not ever be monetized as it is built on foundations (VLC, Youtube, SoundCloud, packages/libararies, etc) that are not my own. PyStreamer also 'streams' audio by way of VLC's drag and drop feature where you can drag a URL into the media player window and audio/video will be played. PyStreamer works this way so that the songs and videos being played are never downloaded and, as such, staying completely legal. 
