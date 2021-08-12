import json
import asyncio
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from .config import Color


class ProxyGrabber:
    sources = json.load(open(Path().absolute().joinpath('proxy').joinpath('sources.json'), mode='r', encoding='utf-8'))
    # driver = webdriver.Chrome()

    def __init__(self):
        print(Color.FAIL + 'ProxyGrabber initialized' + Color.ENDC)

    def _check_is_available(self, url):
        return requests.get(url)

    def _get_last_page(self, html, page):
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.find(page['block'], id=page['id'], class_=page['class']).find_all(page['inside'])
        return [i.text for i in pages if i.text.isdigit()][-1]

    def start(self):
        print(f'Available {len(self.sources)} sites in base')
        print('Starting...\n')
        for key, value in self.sources.items():
            print(f"GRAB | {value['name']}({key})", end=' ')
            response = self._check_is_available(value['url'])
            if response.status_code == 200:
                print(Color.OKGREEN + '[OK]' + Color.ENDC, end=' ')
                last_page = self._get_last_page(response.content, value['page'])
                print(f"PAGES: {last_page}", end=' ')
            else:
                print('[ERROR]')
