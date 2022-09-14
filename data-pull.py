from re import template
import requests, json
from bs4 import BeautifulSoup

''' Session Initialization '''
base_url = f'https://www.wojsko-polskie.pl'
payload = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

''' Settings configuration '''
with open("announcements_archive.json", "r") as json_file:
    json_file = json.load(json_file)

template = json_file["template"]
announcements = json_file["announcements"]
pages = announcements[-1]['page'] if len(announcements) else 0

with requests.Session() as s:
    while True:
        response = s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={pages + 1}', headers=payload)

        if response.status_code != requests.codes.ok:
            break
        else:
            pages += 1

print(pages)

with requests.Session() as s:
    for p in range(pages + 1, 1, -1):
        for link in s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={p}').find('ul', {'class': 'newsgrid-list'}.find_all('a')):
            template['title'] = link['title']
            template['href'] = link['href']
            template['img'] = link.find('img')['src']
            template['content'] = link.find('div', {'class': 'text'}).content
            json_file['announcement'] += template
    
    print(json_file)
    with open("announcements_archive.json", "w") as json_dump:
        json.dump(json_file, json_dump, indent=4)
