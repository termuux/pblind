from dyno.extensions.marketplace.activation import Activation
from dyno.extensions.marketplace.dtime import Datetime
from dyno.extensions.marketplace.ip import Ipfetch
from dyno.extensions.marketplace.opchar.ocr_stream import OpticalCharacterStream
from dyno.extensions.marketplace.common import Maintain
from dyno.extensions.marketplace.dobject.dnn.object_detection import ObjectDetector
from dyno.extensions.marketplace.music.youtube.youtube import MusicPlayer
from dyno.extensions.marketplace.news.kathpost.kath_headlines import KathmanduPostHeadlines
from dyno.extensions.marketplace.weather.owm_weather import OpenWeatherMap


control_exts = [
     {
        'func': Activation.agreet,
        'tags': 'start, hi, hello, start, wake up',
        'description': 'Start the assistant service'
    },

    {
        'func': Activation.dassistant,
        'tags': 'bye, shut down, exit, termination, shutdown',
        'description': 'Stop the assistant service '
    }
]
basic_exts = [
    {
        'enable': True,
        'func': Datetime.current_time,
        'tags': 'time, hour, now, here, this',
        'description': 'Show the current time'
    },
    {
        'enable': True,
        'func': Datetime.current_date,
        'tags': 'date',
        'description': 'Show the current date'
    },
    {
        'enable' : True,
        'func' : Ipfetch.fetch_ip,
        'tags' : 'ip, ip address, address, geoip, digital location, digital'

    },
    {
        'enable' : True,
        'func' : Maintain.stop_speech,
        'tags' : 'stop',
        'description' : ' Stop current speech instance'
    },
    {
        'enable' : True,
        'func' : ObjectDetector.detect_objects,
        'tags' : 'detect objects, objects, objects around',
        'description' : 'Detects object'
    },
    {
        'enable': True,
        'func' : OpticalCharacterStream.optical_character_stream,
        'tags' : 'stream text, stream ocr, live ocr stream, live text detector',
        'description' : 'Stream live optical character detection'
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_add,
        'tags' : 'add, aid, ad',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_play,
        'tags' : 'play',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_pause,
        'tags' : 'pause',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_next,
        'tags' : 'next',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_previous,
        'tags' : 'previous',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_resume,
        'tags' : 'resume',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_seek_forward,
        'tags' : 'forward',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_seek_backward,
        'tags' : 'backward',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_repeat_song,
        'tags' : 'repeat current',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_repeat_all,
        'tags' : 'repeat all',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_shuffle,
        'tags' : 'shuffle',
        'description' : ''
    },
    {
        'enable': True,
        'func' : MusicPlayer.rythm_stop,
        'tags' : 'kill',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.national_news,
        'tags' : 'national',
        'description' : ''
    },

    {
        'enable': True,
        'func' : KathmanduPostHeadlines.politics_news,
        'tags' : 'politics',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.valley_news,
        'tags' : 'valley',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.opinion_news,
        'tags' : 'opinion',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.money_news,
        'tags' : 'money',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.sports_news,
        'tags' : 'sports',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.art_and_culture_news,
        'tags' : 'art, culture',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.health_news,
        'tags' : 'health',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.food_news,
        'tags' : 'food',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.travel_news,
        'tags' : 'travel',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.investigations_news,
        'tags' : 'investigation',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.climate_environment_news,
        'tags' : 'climate',
        'description' : ''
    },
    {
        'enable': True,
        'func' : KathmanduPostHeadlines.science_technology_news,
        'tags' : 'science',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.weather,
        'tags' : 'weather',
        'description' : ''
    },

    {
        'enable': True,
        'func' : OpenWeatherMap.temperature,
        'tags' : 'temperature',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.wind_speed,
        'tags' : 'wind speed',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.wind_direction,
        'tags' : 'wind direction',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.humidity,
        'tags' : 'humidity',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.clouds,
        'tags' : 'clouds',
        'description' : ''
    },
    {
        'enable': True,
        'func' : OpenWeatherMap.pressure,
        'tags' : 'pressure',
        'description' : ''
    },
]
exts = control_exts + basic_exts

for ext in exts:
    ext['name'] = ext['func'].__name__

ext_obj = {ext['func'].__name__: ext['func'] for ext in exts}

def ext_to_str(extension):
    for ext in extension:
        ext.update((k, v.__name__) for k, v in ext.items() if k == 'func')

ext_to_str(exts)
