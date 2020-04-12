# !/usr/bin/env python3
import json
from asyncio import get_event_loop, exceptions
from re import search
from time import time
from json import JSONDecodeError

from httpx import AsyncClient
from httpx._exceptions import ProxyError, NetworkError

from anonimizator import Anonimizator
from utils import get_or_create, get_alphabet, generate_sequence, logger
from options import (
    BASE_URL,
    LETTERS_QUANTITY,
    LANGUAGES,
    REQUEST_HEADERS,
    REQUEST_PARAMS,
    REQUEST_PAYLOAD,
    ERROR_LOG_NAME
)
from models import (
    Good,
    Language,
    Combination,
)


anonimizator = Anonimizator()


async def make_request(seq: str):
    REQUEST_PAYLOAD['q'] = seq
    headers = {'User-Agent': anonimizator.ua.random}
    headers.update(REQUEST_HEADERS)

    error_counter = 0
    while error_counter < 3:
        proxy: str = anonimizator.get_proxy()
        proxies = {
            'http': f"http://{proxy}",
            'https': f"http://{proxy}"
        } if proxy else { }

        try:
            async with AsyncClient(proxies=proxies) as client:
                response = await client.post(
                    f"{BASE_URL}",
                    params=REQUEST_PARAMS,
                    headers=headers,
                    data=REQUEST_PAYLOAD,
                    timeout=5.0
                )
                data: str = response.text

                return data

        except (ProxyError, NetworkError, exceptions.TimeoutError) as e:
            data_to_write = f"Timestamp {int(time())}. "\
                            f"Problem with connection {e}\n"
            await logger(ERROR_LOG_NAME, data_to_write)
            error_counter += 1


async def main():
    combinations: list = await Combination.objects.all()
    last_combo: str = combinations[-1].name if combinations else ''

    for lang_name in LANGUAGES:
        language = await get_or_create(Language, {'name': lang_name})
        alphabet: list = get_alphabet(lang_name)

        for number_of_letters in range(
            len(last_combo) or 1, LETTERS_QUANTITY + 1
        ):
            sequence: list = generate_sequence(
                alphabet, number_of_letters, last_combo
            )
            if last_combo:
                last_combo = ''

            for seq in sequence:
                data_raw: str = await make_request(seq)
                if not data_raw:
                    data_to_write = f"Timestamp {int(time())}. " \
                                    f"Request unsuccessful for combination \"{seq}\""
                    await logger(ERROR_LOG_NAME, data_to_write)
                    continue

                try:
                    data = json.loads(data_raw)
                    if not isinstance(data, dict):
                        data_to_write = f"Timestamp {int(time())}. " \
                                        f"Expect dict, received {data}\n"
                        await logger(ERROR_LOG_NAME,data_to_write)
                        continue

                except JSONDecodeError:
                    data_to_write = f"Timestamp {int(time())}. " \
                                    f"Can't decode. Value - {data_raw}\n"
                    await logger(ERROR_LOG_NAME, data_to_write)

                except Exception as e:
                    data_to_write = f"Timestamp {int(time())}. " \
                                    f"Huston, we have a problem here. " \
                                    f"Value - {data_raw}. Error is {e}\n"
                    await logger(ERROR_LOG_NAME, data_to_write)

                else:
                    combination = await get_or_create(
                        Combination, {'language': language, 'name': seq}
                    )
                    for product_data in data.get('products', []):
                        price_raw = product_data['price'].replace(' ', '')
                        price = search(r'[>]\d+[<]', price_raw)

                        await get_or_create(Good, {
                            'name': product_data['name'],
                            'product_url': product_data['url'],
                            'image_url': product_data['image'],
                            'price': price[0][1:-1] if price else price_raw,
                            'combination': combination
                        })


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
