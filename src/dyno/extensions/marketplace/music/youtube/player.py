import vlc
import time
from threading import Timer



def generate_music(music_path):
    playback_object = vlc.MediaPlayer(music_path)
    playback_object.play()
    print('Music loaded to protocol.')
    return playback_object
    
def pause_music(playback_object):
    playback_object.pause()
    return playback_object

def stop_music(playback_object):
    playback_object.stop()

def resume_music(playback_object):
    playback_object.play()

def set_music_position(playback_object, music_position):
    playback_object.set_position(music_position)

