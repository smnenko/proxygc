import time
import asyncio
from pathlib import Path

import aiohttp
from aiohttp.client_exceptions import (
    ServerDisconnectedError,
    ClientConnectionError,
    ClientHttpProxyError,
    ClientResponseError
)
from asyncio.exceptions import TimeoutError

from .config import Color


class ProxyChecker:

    def __init__(self, file):
        self.file = file
        self.url = input('Enter url to check: ')
        self.folder = Path().absolute().joinpath(self._remove_http_from_url(self.url))
        self.folder.mkdir(parents=True, exist_ok=True)
        self.http = open(self.folder.joinpath('http.txt'), mode='w', encoding='utf-8')
        self.https = open(self.folder.joinpath('https.txt'), mode='w', encoding='utf-8')
        print(Color.FAIL + 'ProxyChecker initialized' + Color.ENDC)

    def _remove_http_from_url(self, url):
        return (
            url
                .replace('http://', '')
                .replace('https://', '')
                .replace('/', '')
        )

    def _convert_proxies(self, proxy_list):
        print('CHECK | Starting to collect proxies', end=' ')
        proxy_list = [*[f'https://{i}' for i in proxy_list], *[f'http://{i}' for i in proxy_list]]
        print(Color.OKGREEN + '[Finished]' + Color.ENDC)
        return proxy_list

    def _get_proxy_type(self, proxy):
        return 'http' if proxy.startswith('http://') else 'https'

    async def _check_url(self, proxy):
        tic = time.perf_counter()
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(self.url, proxy=proxy)
                if response.status == 200:
                    getattr(self, self._get_proxy_type(proxy)).write(f'{proxy}\n')
                    print(
                        f'{proxy.rstrip()} {Color.OKGREEN + response.status + Color.ENDC} {time.perf_counter() - tic} seconds')
        except (
                ServerDisconnectedError,
                ClientConnectionError,
                ClientHttpProxyError,
                ClientResponseError,
                ConnectionResetError,
                TimeoutError,
                ValueError
        ) as ex:
            print(
                f'{proxy.rstrip()} {Color.OKGREEN + "error" + Color.ENDC} {time.perf_counter() - tic} seconds')

    async def check(self):
        proxies = self._convert_proxies(self.file.readlines())
        print('CHECK | Starting to check proxies to ' + Color.OKGREEN + f'{self.url}' + Color.ENDC)
        tasks = [asyncio.create_task(self._check_url(proxy)) for proxy in proxies]
        await asyncio.gather(*tasks)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check())
        loop.close()
