#!/usr/bin/env python3

import os
import time
from typing import Callable, Dict

import requests

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import ThreadedCompleter, WordCompleter

API = "https://api.mangadex.org"

commands: Dict[str, Callable] = {}
command_completer = ThreadedCompleter(WordCompleter(
    list(commands.keys()), ignore_case=True, sentence=True
))


def command(function):
    return commands.setdefault(function.__name__, function)


@command
def search(params: str) -> str:
    payload = {'title': params}
    res = requests.get(f'{API}/manga', params=payload)
    status_code = res.status_code
    if status_code == 400:
        return 'Error 400'

    results = res.json()['results']
    result_list = [
        (
            f'Title: {result["data"]["attributes"]["title"]["en"]}, '
            f'ID: {result["data"]["id"]}'
        )
        for result in results
    ]
    return '\n'.join(result_list)


@command
def chapters(params: str) -> str:
    res = requests.get(f'{API}/manga/{params}/feed')
    status_code = res.status_code
    if status_code == 400:
        return 'Error 400'

    results = res.json()['results']
    result_list = [
        (
            f'Chapter {result["data"]["attributes"]["chapter"]}, '
            f'ID: {result["data"]["id"]}'
        )
        for result in results
    ]
    return '\n'.join(result_list)


@command
def get(params: str) -> str:
    if params is None or len(params) == 0:
        return 'Invalid parameter for get'

    res = requests.get(f'{API}/chapter/{params}')
    chapter_hash = res.json()['data']['attributes']['hash']
    chapter_num = res.json()['data']['attributes']['chapter']
    files = res.json()['data']['attributes']['data']

    output_dir = f'Chapter {chapter_num}'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i, file in enumerate(files):
        output_file = os.path.join(output_dir, f'{i + 1}.jpg')

        if not os.path.exists(output_file):
            for attempt in range(6):
                time.sleep(10)
                res = requests.get(f'{API}/at-home/server/{params}')
                base_url = res.json()['baseUrl']
                image_url = f'{base_url}/data/{chapter_hash}/{file}'
                print((
                    f'Downloading {image_url}\n'
                    f'(Attempt {attempt + 1} out of 6)'
                ))

                res = requests.get(image_url)
                if res.status_code == 200:
                    with open(output_file, 'wb') as image_file:
                        image_file.write(res.content)
                    break
                print(f'Got error code {res.status_code}, trying again...')
        else:
            print(f'{output_file} already exists, skipping.')

    return 'Finished.'


def run(text: str) -> str:
    cmd, params = text.split(' ', 1) if ' ' in text else (text, '')
    return commands.get(cmd, lambda x: 'Command not found')(params)


def main():
    session = PromptSession(completer=command_completer)

    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print(run(text))

    print('Bye')


if __name__ == '__main__':
    main()
