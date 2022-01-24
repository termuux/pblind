from pyowm import OWM
from dyno.config import OPEN_WEATHER_MAP_CONFIG
from dyno.extensions.extension import ParentExtension

try:
    open_weather_map = OWM(OPEN_WEATHER_MAP_CONFIG['key'])
    weather_manager = open_weather_map.weather_manager()
    weather_observation = weather_manager.weather_at_id(OPEN_WEATHER_MAP_CONFIG['city_id'])
    weather = weather_observation.weather
except:
    pass

class OpenWeatherMap(ParentExtension):

    @classmethod 
    def weather(cls, **kwargs):
        cls.response('The current weather status is of {0}'.format(weather.detailed_status))

    @classmethod
    def temperature(cls, **kwargs):
        current_temperature = weather.temperature(OPEN_WEATHER_MAP_CONFIG['unit'])
        cls.response('The temperature is {0} degree celsius'.format(current_temperature['temp']))

    @classmethod
    def wind_speed(cls, **kwargs):
        current_speed = weather.wnd['speed']
        cls.response('The wind speed is {0} meter per second'.format(current_speed))
    
    @classmethod
    def wind_direction(cls, **kwargs):
        current_direction = weather.wnd['deg']
        cls.response('The wind direction is {0} degress'.format(current_direction))
    
    @classmethod
    def humidity(cls, **kwargs):
        cls.response('The humidity is present as {0} percentage'.format(weather.humidity))

    @classmethod
    def clouds(cls, **kwargs):
        cls.response('The clouds are covering {0} percentage'.format(weather.clouds))

    @classmethod
    def pressure(cls, **kwargs):
        cls.response('The atmospheric pressure is {0} hecto pascal.'.format(weather.pressure['press']))

