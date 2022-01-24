from datetime import datetime
from datetime import date
from dyno.extensions.extension import ParentExtension

hour_mapping = {'0': 'twelve',
                '1': 'one',
                '2': 'two',
                '3': 'three',
                '4': 'four',
                '5': 'five',
                '6': 'six',
                '7': 'seven',
                '8': 'eight',
                '9': 'nine',
                '10': 'ten',
                '11': 'eleven',
                '12': 'twelve',

                }


class Datetime(ParentExtension):

    @classmethod
    def current_time(cls, **kwargs):
        now = datetime.now()
        hour, minute = now.hour, now.minute
        converted_time = cls.time_to_text(hour, minute)
        cls.response('The current time is: {0}'.format(converted_time))

    @classmethod
    def current_date(cls, **kwargs):
        today = date.today()
        cls.response('The current date is: {0}'.format(today))

    @classmethod
    def get_12_hour_period(cls, hour):
        return 'pm' if 12 <= hour < 24 else 'am'

    @classmethod
    def convert_12_hour_format(cls, hour):
        return hour - 12 if 12 < hour <= 24 else hour

    @classmethod
    def create_hour_period(cls, hour):
        hour_12h_format = cls.convert_12_hour_format(hour)
        period = cls.get_12_hour_period(hour)
        return hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'

    @classmethod
    def time_to_text(cls, hour, minute):

        if minute == 0:
            time = cls.create_hour_period(hour) + " o'clock"
        elif minute == 15:
            time = "quarter past " + cls.create_hour_period(hour)
        elif minute == 30:
            time = "half past " + cls.create_hour_period(hour)
        elif minute == 45:
            hour_12h_format = cls.convert_12_hour_format(hour + 1)
            period = cls.get_12_hour_period(hour)
            time = "quarter to " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'
        elif 0 < minute < 30:
            time = str(minute) + " minutes past " + cls.create_hour_period(hour)
        else:
            hour_12h_format = cls.convert_12_hour_format(hour + 1)
            period = cls.get_12_hour_period(hour)
            time = str(60 - minute) + " minutes to " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'

        return time
