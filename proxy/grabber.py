import json
import asyncio
import re
from pathlib import Path

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
from bs4 import BeautifulSoup
from selenium import webdriver

from .config import Color


class ProxyGrabber:
    sources = json.load(open(Path().absolute().joinpath('proxy').joinpath('sources.json'), mode='r', encoding='utf-8'))
    proxies = set()

    def __init__(self, file):
        self.file = file
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome('chromedriver', chrome_options=self.options)
        print(Color.FAIL + 'ProxyGrabber initialized' + Color.ENDC)

    async def _check_is_available(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                if response and response.status == 200:
                    print(Color.OKGREEN + '[OK]' + Color.ENDC, end=' ')
                    return response
        except ClientConnectionError as ex:
            return None

    async def _get_last_page(self, html, page):
        soup = BeautifulSoup(html, 'lxml')
        pages = None
        if 'class' in page and page.get('class'):
            pages = soup.find(page['block'], class_=page['class']).find_all(page['inside'])
        elif 'id' in page and page.get('id'):
            pages = soup.find(page['block'], id=page['id']).find_all(page['inside'])
        return int([i.text for i in pages if i.text.isdigit()][-1])

    async def _parse_per_page(self, url, content):
        block, proxies, ports = None, None, None
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        if 'class' in content and content.get('class'):
            block = soup.find(class_=content['class'])
        elif 'id' in content and content.get('id'):
            block = soup.find(id=content['id'])

        if block:
            blocks = block.find_all(content['inside'])
            if blocks:
                proxies = re.findall(content['regular_ip'], str(blocks))
                ports = re.findall(content['regular_port'], str(blocks))
                self.proxies.update([f'{i[0]}{i[1]}' for i in zip(proxies, ports)])

    async def _parse_all_pages(self, content, last_page=1):
        proxies_list, tasks = None, []
        for page in range(1, last_page + 1):
            if '{}' in content['url']:
                if 'format' in content:
                    page = self._convert_page_to_numbers(page, content['format'])
                tasks.append(asyncio.create_task(self._parse_per_page(content['url'].format(page), content)))
            else:
                tasks.append(asyncio.create_task(self._parse_per_page(content['url'], content)))
        await asyncio.gather(*tasks)

    def _convert_page_to_numbers(self, page, numbers):
        return f'{page:0={numbers}d}'

    def _write_to_file(self):
        for proxy in self.proxies:
            self.file.write(f'{proxy}\n')

    async def grab(self):
        print(f'Available {len(self.sources)} sites in base')
        print('Starting...\n')
        tasks = []
        for key, value in self.sources.items():
            print(f"GRAB | {value['name']} ({key})", end=' ')
            response = await self._check_is_available(value['url'])
            if response:
                if 'page' in value:
                    last_page = await self._get_last_page(await response.text(), value['page'])
                    print(f"PAGES: {last_page}", end=' ')
                    print(Color.OKGREEN + 'SUCCESS' + Color.ENDC)
                tasks.append(asyncio.create_task(self._parse_all_pages(value['content'], last_page)))
            else:
                print(Color.FAIL + '[ERROR]' + Color.ENDC)
        await asyncio.gather(*tasks)
        self._write_to_file()

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.grab())
        loop.close()
