import os
import time
import random 
from dyno.extensions.marketplace.music.youtube import player
from dyno.extensions.marketplace.music.youtube import downloader

class Playlist:

    def __init__(self):
        self.queued_playlist=[]
        self.played_playlist=[]
        self.start_time = None
        self.pause_time = None
        self.metadata = None
        self.playback_object = None
        self.current_object = None 
        self.resume_time = None
        self.is_paused = False
        self.is_stopped = False
        self.is_starting = True
        self.play_next_now = False
        self.repeat = 0

    def return_song(self):
        now_playing= self.queued_playlist.pop(0)
        self.played_playlist.append(now_playing)
        return now_playing

    def add_song(self,query):
        self.queued_playlist.append(query +" lyrics")

    def download_song(self,song,download_directory):
        meta=downloader.download_song(song,download_directory)
        return meta
    
    def shuffle_playlist(self):
            random.shuffle(self.queued_playlist)
            print("Enabling shuffle .. ")

    def play_song(self, stream_metadata , download_directory):
        self.play_next_now = False
        self.metadata=stream_metadata
        music_path = os.path.join(download_directory.name, self.metadata['id'])
        self.playback_object = None
        self.playback_object= player.generate_music(music_path)
        print('Now Playing : {0}'.format(self.metadata['title']))


    def resume_song(self):
        if self.is_paused==True:
            player.resume_music(self.current_object)
            self.playback_object = self.current_object
            self.current_object = None
            self.is_paused=False
            time.sleep(5)
        else:
            pass
        print('Streaming : {0}'.format(self.metadata['title']))
    
    def pause_song(self):
        if self.is_paused==True:
            pass
        else:
            self.is_paused=True
            player.pause_music(self.playback_object)
            self.current_object = self.playback_object
            self.playback_object = None

    
    def stop_song(self):
        player.stop_music(self.playback_object)
        self.playback_object = None

    def next_song(self):
        player.stop_music(self.playback_object)

    def shift_last_played_song(self):
        self.queued_playlist=[self.played_playlist.pop()]+self.queued_playlist

    def loop_queue(self):
        self.queued_playlist.extend(self.played_playlist)
        self.played_playlist.clear()
    
    def remove_last_queued_song(self):
        try:
            self.queued_playlist.pop()
        except:
            print("Empty queue")

    def previous_song(self):
        try:
            self.queued_playlist=[self.played_playlist.pop()]+self.queued_playlist
            self.queued_playlist=[self.played_playlist.pop()]+self.queued_playlist
            player.stop_music(self.playback_object)
            self.is_paused=False
        except:
            print('No song before this instance .')

    def repeat_song(self,repeat_mode):
        if repeat_mode == "off":
            self.repeat_mode = 0
        elif mode == "all":
            self.repeat_mode = 1
        elif mode == "song":
            self.repeat_mode = 2
        else:
            print('Repeat mode is invalid')
    
    def seek_song(self,position_value):
        player.set_music_position(self.playback_object, position_value )



    def return_playlist(self):
        all_playlist=self.played_playlist+self.queued_playlist
        return all_playlist
