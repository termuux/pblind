from dyno.extensions.extension import ParentExtension
import requests


class Ipfetch(ParentExtension):

    @classmethod
    def fetch_ip(cls, **kwargs):
        url = 'https://ident.me'
        response = requests.get(url)
        cls.console('Printing ip address')
        cls.response('The ip address is {0}'.format(response.text))


