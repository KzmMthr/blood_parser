import datetime
import json
import re

import requests
from bs4 import BeautifulSoup, element


class Spider():

    def __init__(self):
        self.date_create = datetime.datetime.now().date()
        self.cities = []
        self.regions = []
        self.result = []

    def get_regions_url(self, url) -> list:
        '''Get regions urls'''
        self._page = requests.get(url)
        self._soup = BeautifulSoup(self._page.text, 'lxml')
        self.regions = []
        try:
            regions = self._soup.find('select',
                                      id='search_reg_spk').find_all("option")
            for reg in regions:
                value = reg.get("value")
                if value != '':
                    self.regions.append(
                        f'https://yadonor.ru/donorstvo/gde-sdat/where/'
                        f'{reg.get("value")}/ws0/cgd0/hla0'
                    )
            print(f'Found {len(self.regions)} regions')
            return self.regions
        except Exception as e:
            raise e

    def get_cities_url(self, urls: list) -> list:
        '''Parse cities urls from region urls'''
        self.cities = []
        for url in urls:
            self._page = requests.get(url)
            self._soup = BeautifulSoup(self._page.text, 'lxml')
            try:
                cities = self._soup.find(
                    'div', class_='maps-content__spoler '
                                  'js-maps-spoler-box').find_all("a")
                for city in cities:
                    self.cities.append(
                        f'https://yadonor.ru'
                        f'{city.get("href")}'
                    )
            except Exception as e:
                raise e
        print(f'Found {len(self.cities)} cities')
        return self.cities

    def get_item(self, url):
        '''Get result items'''
        self._page = requests.get(url)
        self._soup = BeautifulSoup(self._page.text, 'lxml')
        self._bloodlines = {}
        self._items = {}
        self._items['url'] = url
        self._items['country'] = 'Россия'
        self._traf_lights_convert = {
            'max': 'no_need',
            'min': 'need',
            'middle': 'need',
            'gray': 'unknown',
            'not': 'no_need'
        }

        try:
            region = re.findall(r'\s(.*)', str(self._soup.find(
                'a', text=re.compile(r'Регион.*')).text)
                                )
            self._items['region'] = region[0]
            city = re.findall(r'\s(.*)', str(self._soup.find(
                'a', text=re.compile(r'Город.*')).text)
                                )
            self._items['city'] = city[0]
            name = self._soup.find('h1',).text
            self._items['name'] = re.findall(r'[А-Я].+', name)[0]
            address = self._soup.find('strong', text=re.compile(r'Адрес.*')).parent
            self._items['address'] = re.findall(r'[а-яА-Я].*', address.text)[0]
        except Exception as e:
            raise e

        try:
            traf_lights = self._soup.find(
                'div', class_='spk-lights')
            for tag_string in traf_lights.children:
                if isinstance(tag_string, element.Tag):
                    group_blood = re.findall(
                        'head">\s(\w{1,2})', str(tag_string)
                    )
                    resus_list = re.findall(
                        r'--(\w{3,6})', str(tag_string)
                    )
                    if len(resus_list) == 2:
                        self._bloodlines[f'{group_blood[0]}_plus'], \
                        self._bloodlines[f'{group_blood[0]}_minus'] = \
                            self._traf_lights_convert[resus_list[0]], \
                            self._traf_lights_convert[resus_list[1]]
                    else:
                        self._bloodlines[f'{group_blood[0]}_plus'], \
                        self._bloodlines[f'{group_blood[0]}_minus'] = \
                            'unknown', 'unknown'
        except Exception as e:
            raise e

        print(f'Found {self._items["city"]} city')
        self._items['bloodlines'] = self._bloodlines
        return self._items

    def display_data(self, urls: list) -> list:
        self.result = []
        for url in urls:
            self.result.append(self.get_item(url))
        return self.result


url = 'https://yadonor.ru/donorstvo/gde-sdat/map-lights/'
obj = Spider()
regions_url = obj.get_regions_url(url)
cities_url = obj.get_cities_url(regions_url)
with open("bloodstations.json", "w", encoding='utf-8') as write_file:
    json.dump(obj.display_data(cities_url), write_file, indent=4)
