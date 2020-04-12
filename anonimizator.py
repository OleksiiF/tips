import json
from random import choice
from asyncio import get_event_loop

import aiofiles
from httpx import AsyncClient
from httpx._exceptions import NetworkError
from fake_useragent import UserAgent

from options import (
    PROXIES_FILENAME,
    PROXY_SOURCE,
    PROXIES_QUANTITY,
    USE_PROXY
)


class Anonimizator:
    _PROXY_URL = f"{PROXY_SOURCE}?type=http&limit={PROXIES_QUANTITY}"

    def __init__(self):
        self.ua = UserAgent()
        self.proxies = []

        if USE_PROXY:
            try:
                with open(PROXIES_FILENAME, 'r') as fh:
                    self.proxies = json.loads(fh.read())

            except FileNotFoundError:
                loop = get_event_loop()
                loop.run_until_complete(self.__get_new_proxies())

    async def __get_new_proxies(self):
        error_counter = 0
        while error_counter < 3:
            try:
                async with AsyncClient() as client:
                    response = await client.get(self._PROXY_URL)
                    data_raw = response.text

                data: dict = json.loads(data_raw)
                for element in data['data']:
                    self.proxies.append(element['ipPort'])

                if len(self.proxies) >= PROXIES_QUANTITY:
                    break

            except (json.decoder.JSONDecodeError, NetworkError):
                error_counter += 1

        if self.proxies:
            async with aiofiles.open(PROXIES_FILENAME, 'w') as fh:
                await fh.write(json.dumps(self.proxies))

    def get_proxy(self) -> str:
        return choice(self.proxies) if self.proxies else ''
