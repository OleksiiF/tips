import string
import itertools

import aiofiles


async def get_or_create(model, data):
    if not await model.objects.filter(**data).exists():
        return await model.objects.create(**data)

    else:
        return await model.objects.get(**data)


def get_alphabet(language: str):
    alphabet = ''
    if language == "en":
        alphabet = list(string.ascii_lowercase)

    elif language == "ru":
        a = ord('а')
        alphabet = [chr(i) for i in range(a, a + 32)] + ['ё']

    else:
        print(f'You provide incorrect language. ===>  {language}')

    return alphabet


def generate_sequence(
        letters: list, number_of_letters: int, last_seq: str
) -> list:
    if number_of_letters == 1:
        sequence = letters

    else:
        multiple_letters = [letters] * number_of_letters
        sequence = [
            ''.join(raw_seq) for raw_seq in itertools.product(*multiple_letters)
        ]

    # Get only new combinations of letters.
    if last_seq and len(last_seq) == number_of_letters:
        sequence = sequence[sequence.index(last_seq) + 1:]

    return sequence


async def logger(file_name, data):
    async with aiofiles.open(file_name, 'a+') as fh:
        await fh.write(data)
