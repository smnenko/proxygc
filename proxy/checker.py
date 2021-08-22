import time
import asyncio
from pathlib import Path

import aiohttp
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientHttpProxyError, ClientResponseError
import aiosocks
from aiosocks.connector import ProxyConnector, ProxyClientRequest

from .config import Color


class ProxyChecker:
    output = open(Path().absolute().joinpath('proxy.txt'), mode='r', encoding='utf-8')

    def __init__(self, file):
        self.file = file
        self.url = input('Enter url to check: ')
        self.folder = Path().absolute().joinpath(self._remove_http_from_url(self.url))
        self.folder.mkdir(parents=True, exist_ok=True)
        self.http = open(self.folder.joinpath('http.txt'), mode='w', encoding='utf-8')
        self.socks4 = open(self.folder.joinpath('socks4.txt'), mode='w', encoding='utf-8')
        self.socks5 = open(self.folder.joinpath('socks5.txt'), mode='w', encoding='utf-8')
        print(Color.FAIL + 'ProxyChecker initialized' + Color.ENDC)

    def _remove_http_from_url(self, url):
        return (
            url
            .replace('http://', '')
            .replace('https://', '')
            .replace('socks4://', '')
            .replace('socks5://', '')
            .replace('/', '')
        )

    def _proxies_list_to_dict(self, proxy_list):
        print('CHECK | Starting to collect proxies', end=' ')
        proxies_dict = {}
        for i in proxy_list:
            proxies_dict[i] = {
                'http': {
                    'http': f'http://{i}',
                    'https': f'https://{i}',
                },
                'socks4': {
                    'http': f'socks4://{i}',
                    'https': f'socks4://{i}',
                },
                'socks5': {
                    'http': f'socks5://{i}',
                    'https': f'socks5://{i}',
                }
            }
        print(Color.OKGREEN + '[Finished]' + Color.ENDC)
        return proxies_dict

    def _get_proxy_type(self, proxy):
        if proxy.startswith('http'):
            return ProxyType.HTTP
        if proxy.startswith('https'):
            return ProxyType.HTTPS
        if proxy.startswith('socks4'):
            return ProxyType.SOCKS4
        return ProxyType.SOCKS5

    async def _check_url(self, name, proxy, proxy_type):
        tic = time.perf_counter()
        connector = ProxyConnector()
        async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
            try:
                response = await session.get(self.url, proxy=proxy)
                if response.status_code == 200:
                    getattr(self, proxy_type).write(f'{name}\n')
                    print(f'{name.rstrip()} {Color.OKGREEN + response.status + Color.ENDC} {time.perf_counter() - tic} seconds')
            except aiohttp.ClientProxyConnectionError:
                print(f'{name.rstrip()} {Color.FAIL + "error" + Color.ENDC} {time.perf_counter() - tic} seconds')
            except aiohttp.ClientConnectorError:
                print(f'{name.rstrip()} {Color.FAIL + "error" + Color.ENDC} {time.perf_counter() - tic} seconds')
            except aiosocks.SocksError:
                print(f'{name.rstrip()} {Color.FAIL + "error" + Color.ENDC} {time.perf_counter() - tic} seconds')

    async def check(self):
        tasks = []
        proxies = self._proxies_list_to_dict(self.file.readlines())
        proxy_types = ['http', 'socks4', 'socks5']
        print('CHECK | Starting to check proxies to ' + Color.OKGREEN + f'{self.url}' + Color.ENDC)
        for name, proxy in proxies.items():
            for proxy_type in proxy_types:
                for type_, proxy_value in proxy[proxy_type].items():
                    tasks.append(asyncio.create_task(self._check_url(name, proxy_value, proxy_type)))
        await asyncio.gather(*tasks)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check())
        loop.close()
