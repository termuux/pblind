import requests
from bs4 import BeautifulSoup
from dyno.extensions.extension import ParentExtension

KPOST_NATIONAL_URL = 'https://kathmandupost.com/national'
KPOST_POLITICS_URL = 'https://kathmandupost.com/politics'
KPOST_VALLEY_URL = 'https://kathmandupost.com/valley'
KPOST_OPINION_URL = 'https://kathmandupost.com/opinion'
KPOST_MONEY_URL = 'https://kathmandupost.com/money'
KPOST_SPORTS_URL = 'https://kathmandupost.com/sports'
KPOST_ART_CULTURE_URL = 'https://kathmandupost.com/art-culture'
KPOST_HEALTH_URL = 'https://kathmandupost.com/health'
KPOST_FOOD_URL = 'https://kathmandupost.com/food'
KPOST_TRAVEL_URL = 'https://kathmandupost.com/travel'
KPOST_INVESTIGATIONS_URL = 'https://kathmandupost.com/investigations'
KPOST_CLIMATE_ENVIRONMENT_URL = 'https://kathmandupost.com/climate-environment'
KPOST_SCIENCE_TECHNOLOGY_URL = 'https://kathmandupost.com/science-technology'

def parse_kathmandu_news(site_url):
    site_response = requests.get(site_url).text
    soup = BeautifulSoup(site_response, 'html.parser')
    head_lines = soup.find_all('h3')
    head_lines_paragraph = ''
    for head_line in head_lines:
        head_lines_paragraph += head_line.get_text() + '. '
    return head_lines_paragraph

class KathmanduPostHeadlines(ParentExtension):

    @classmethod
    def national_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_NATIONAL_URL))
    
    @classmethod
    def politics_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_POLITICS_URL))
    
    @classmethod
    def valley_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_VALLEY_URL))
    
    @classmethod
    def opinion_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_OPINION_URL))
    
    @classmethod
    def money_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_MONEY_URL))
    
    @classmethod
    def sports_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_SPORTS_URL))
    
    @classmethod
    def art_and_culture_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_ART_CULTURE_URL))
    
    @classmethod
    def health_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_HEALTH_URL))
    
    @classmethod
    def food_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_FOOD_URL))
    
    @classmethod
    def travel_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_TRAVEL_URL))

    @classmethod
    def investigations_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_INVESTIGATIONS_URL))

    @classmethod
    def climate_environment_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_CLIMATE_ENVIRONMENT_URL))

    @classmethod
    def science_technology_news(cls, **kwargs):
        cls.response(parse_kathmandu_news(KPOST_SCIENCE_TECHNOLOGY_URL))


