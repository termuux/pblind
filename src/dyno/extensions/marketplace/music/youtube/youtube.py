import re
import time
import threading
from dyno.extensions.marketplace.music.youtube import downloader 
from dyno.extensions.marketplace.music.youtube.playlistmanager import Playlist
from dyno.extensions.extension import ParentExtension

music_playlist = Playlist()
song_available = threading.Event()


download_directory=downloader.make_download_directory()

def start_music():
    music_playlist.is_starting= False
    song= music_playlist.return_song()
    try:
        metadata = music_playlist.download_song(song,download_directory)
    except Exception as exception:
        print('Downloading song error with message {0}'.format(exception))
    else:
        music_playlist.play_song(metadata, download_directory)
    


def play_music():
    while not music_playlist.is_stopped:
        
        if  music_playlist.is_paused==True:
            time.sleep(2)

        elif music_playlist.repeat==2:
            music_playlist.shift_last_playedsong()
            start_music()

        elif music_playlist.queued_playlist :
            start_music()
            time.sleep(10)

        else:
            if music_playlist.repeat==1:
                music_playlist.loop_queue()

            else:
                song_available.clear()
                song_available.wait()

        try:
            if music_playlist.playback_object.is_playing() == 1:
                while True:
                    time.sleep(2)
                    if music_playlist.play_next_now == True:
                        music_playlist.stop_song()
                        start_music()
                        break
                    if music_playlist.playback_object.is_playing() == 0:
                        break
            else:
                time.sleep(10)            
        except Exception as e:
            pass
        

def get_regex_text(cls, stream, ext):
    tags = cls.extract_tags(stream, ext['tags'])
    for tag in tags:
        regex_text = re.search(tag + ' (.*)', stream)
    return regex_text

    
        

class MusicPlayer(ParentExtension):
    @classmethod 
    def rythm_add(cls, stream, ext):
        regex_text = get_regex_text(cls, stream, ext)
        try:
                if regex_text:
                    song_name = regex_text.group(1)
                    if   music_playlist.is_starting:
                        play_thread = threading.Thread(target=play_music, daemon=True)
                        play_thread.start()
                    music_playlist.add_song(song_name)
                song_available.set()
            
        except Exception as exception:
                cls.console('Error : {0}'.format(exception))
                cls.response("Please provide a song name.")

    @classmethod
    def rythm_play(cls,stream, ext):
        regex_text = get_regex_text(cls, stream, ext) 
        try:
              if music_playlist.is_paused == True:
                 music_playlist.resume_song()
                 return
              if regex_text:
                    song_name = regex_text.group(1)
                    if  music_playlist.is_starting:
                        play_thread = threading.Thread(target=play_music, daemon=True)
                        play_thread.start()
                    music_playlist.add_song(song_name)
                    music_playlist.play_next_now = True
              song_available.set()
            
        except Exception as exception:
                cls.console('Error : {0}'.format(exception))
                cls.response("Please provide a song name.")


    @classmethod
    def rythm_shuffle(cls, **kwargs):
        if music_playlist.queued_playlist:
            music_playlist.shuffle_playlist()
            cls.response('Shuffle enabled.')
        else:
            cls.response('Playlist is empty.')

    @classmethod
    def rythm_resume(cls, **kwargs):
        music_playlist.resume_song()
        cls.response('Music resumed.')

    @classmethod
    def rythm_seek_forward(cls, **kwargs):
        current_position = music_playlist.playback_object.get_position()
        music_playlist.seek_song(current_position + 0.1)
        cls.console('Music forwarded by ten percent')

    @classmethod
    def rythm_seek_backward(cls, **kwargs):
        current_position = music_playlist.playback_object.get_position()
        if current_position > 0.1:
            music_playlist.seek_song(current_position - 0.1)
            cls.console('Music lagged by ten percent')
        else :
            cls.console('Seek music only after ten percent of it is complete.')


    @classmethod
    def rythm_pause(cls, **kwargs):
        music_playlist.pause_song()
        cls.response('Music paused.')
    
    @classmethod
    def rythm_next(cls, **kwargs):
        music_playlist.next_song()
        cls.response('Switching to next song')

    @classmethod
    def rythm_previous(cls, **kwargs):
        music_playlist.previous_song()
        cls.response('Switching to previous song')

    @classmethod
    def rythm_repeat_all(cls, **kwargs):
        music_playlist.repeat_song(2)
        cls.response('Repeating all songs')

    @classmethod
    def rythm_repeat_song(cls, **kwargs):
        music_playlist.repeat_song(1)
        cls.response('Repeating current song')

    
    @classmethod
    def rythm_stop(cls, **kwargs):
        global music_playlist
        music_playlist.is_stopped = True
        music_playlist.stop_song()
        cls.response('Stopping music player')
        downloader.remove_download_directory(download_directory)
        music_playlist = Playlist()



