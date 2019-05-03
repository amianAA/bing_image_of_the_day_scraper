import hashlib
import os

import requests


def get_md5(file):
    return hashlib.md5(file).hexdigest()


PATH = 'Fotos/Wallpapers/'  # Path inside $HOME folder to store downloaded pictures

AMOUNT = 10  # Amount of pictures

MARKETS = ['ar-XA', 'bg-BG', 'cs-CZ', 'da-DK', 'de-AT', 'de-CH', 'de-DE', 'el-GR', 'en-AU', 'en-CA', 'en-GB', 'en-ID',
           'en-IE', 'en-IN', 'en-MY', 'en-NZ', 'en-PH', 'en-SG', 'en-US', 'en-XA', 'en-ZA', 'es-AR', 'es-CL', 'es-ES',
           'es-MX', 'es-US', 'es-XL', 'et-EE', 'fi-FI', 'fr-BE', 'fr-CA', 'fr-CH', 'fr-FR', 'he-IL', 'hr-HR', 'hu-HU',
           'it-IT', 'ja-JP', 'ko-KR', 'lt-LT', 'lv-LV', 'nb-NO', 'nl-BE', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO',
           'ru-RU', 'sk-SK', 'sl-SL', 'sv-SE', 'th-TH', 'tr-TR', 'uk-UA', 'zh-CN', 'zh-HK', 'zh-TW']

processed_hashes = []
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={}&mkt={}'
home = os.path.expanduser('~')
folder_path = '{}/{}'.format(home, PATH)
existing_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

for file_name in existing_files:
    full_file_path = '{}{}'.format(folder_path, file_name)
    file = open(full_file_path, 'rb')
    md5 = get_md5(file.read())
    if md5 in processed_hashes:
        print('Removed file {}'.format(file_name))
        os.remove(full_file_path)
    else:
        processed_hashes.append(md5)
    file.close()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

for mkt in MARKETS:
    response = requests.get(url.format(AMOUNT, mkt), headers=headers)

    if response.status_code == 200:
        data = response.json()
        for pic in data['images']:
            complete_url = 'https://www.bing.com{}'.format(pic['url'])
            title = pic['copyright'].replace('/', ', ').replace('© ', 'By ').replace(', Getty Images', '')
            file_name = '{} - {}'.format(pic['startdate'], pic['title'] or title)
            image = requests.get(complete_url)

            md5 = get_md5(image.content)
            if md5 not in processed_hashes:
                processed_hashes.append(md5)
                filepath = '{}{}.jpg'.format(folder_path, file_name)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(image.content)

